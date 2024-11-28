import rospy
import plan_arm_traj_bezier_demo 
import simStepControl 

# from plan_arm_traj_bezier_demo import Pre_to_catch_bag, call_change_arm_ctrl_mode_service
# from simStepControl import publish_multiple_steps

from humanoid_plan_arm_trajectory.srv import planArmTrajectoryBezierCurve, planArmTrajectoryBezierCurveRequest, planArmTrajectoryBezierCurveResponse
from humanoid_plan_arm_trajectory.msg import jointBezierTrajectory, bezierCurveCubicPoint
from kuavo_msgs.msg import robotHandPosition
from kuavo_msgs.srv import catch_bag_ik_Control, catch_bag_ik_ControlRequest, catch_bag_ik_ControlResponse
from kuavo_msgs.msg import robotHeadMotionData
from kuavo_msgs.srv import AprtagRequest, AprtagRequestRequest

import time
from visualization_msgs.msg import Marker
from sensor_msgs.msg import JointState
from motion_capture_ik.msg import twoArmHandPose, armHandPose
from geometry_msgs.msg import PoseStamped, Quaternion
from ocs2_msgs.msg import mpc_observation
import numpy as np
import matplotlib.pyplot as plt
import math

IK_SUCCESS_FALG = False  # 全局ik成功的标志位

current_arm_joint_state = []

# 灵巧手的发布器
control_robot_hand_position_pub = rospy.Publisher(
    "/control_robot_hand_position", robotHandPosition, queue_size=10
)

# 定义服务
START_FLAG = 0
FINISH_FLAG = 0
called_once = False

def publish_hand_position(left_position, right_position):
    global control_robot_hand_position_pub
    # 确保位置数据是6维的
    if len(left_position) != 6 or len(right_position) != 6:
        rospy.logerr("左手和右手的位置数据必须为6维。")
        return
    # 创建消息实例
    msg = robotHandPosition()
    msg.header.stamp = rospy.Time.now()
    msg.left_hand_position = left_position
    msg.right_hand_position = right_position
    
    # 发布消息
    control_robot_hand_position_pub.publish(msg)

class GraspObject:
    def __init__(self):
        """
            监听/humanoid_mpc_observation 观测值获取手臂的结果
    value: [-0.00034107835381291807, 0.0005232919938862324, -0.0011112227803096175, 5.352366861188784e-05, -0.00012360882828943431, 3.8690734527335735e-07, 
            0.005742086097598076, -0.0005736173479817808, 0.8397912979125977, 0.0, 0.04594825953245163, -0.005243686959147453, 
            
            -0.0114652831107378, -0.0081667834892869, -0.4010554254055023, 0.7490444183349609, -0.39383670687675476, 0.01675693690776825, 
            0.024423126131296158, 0.009306231513619423, -0.39746934175491333, 0.7413363456726074, -0.38966259360313416, -0.019895771518349648, 

            0.129044771194458, -0.004668411333113909, 0.038888972252607346, -0.34535521268844604, -0.00862877443432808, -0.006027891766279936, -0.003882358781993389, 
            0.12587447464466095, 0.00179283507168293, -0.01976587437093258, -0.3355172574520111, 0.00375999859534204, -0.007768881972879171, 0.004849466495215893]

        """
        self.grasp_info = Marker()
        self.robot_arm_traj = JointState()
        
        self.grasp_info.pose.position.x = 100.0  # 设置初始位置 x
        self.grasp_info.pose.position.y = 100.0  # 设置初始位置 y
        self.grasp_info.pose.position.z = 100.0  # 设置初始位置 z

        self.grasp_info.pose.orientation.x = 0.0
        self.grasp_info.pose.orientation.y = 0.0
        self.grasp_info.pose.orientation.z = 0.0
        self.grasp_info.pose.orientation.w = 1.0

        # 头部控制发送器
        self.head_pub = rospy.Publisher("/robot_head_motion_data", robotHeadMotionData, queue_size=10)

        # 姿态订阅器
        self.grasp_sub = rospy.Subscriber("grasp_visualization_marker", Marker, self.grasp_callback)
        
        # 监听轨迹判断是否ik成功
        self.now_pub_traj_sub = rospy.Subscriber('/robot_ik_arm_traj', JointState, self.robot_traj_callback)
        
        # 发布ik命令
        self.ik_pub = rospy.Publisher('/ik/two_arm_hand_pose_cmd', twoArmHandPose, queue_size=10)

        # 观测手臂状态
        self.mpc_obs_sub = rospy.Subscriber('/humanoid_mpc_observation', mpc_observation, self.mpc_obs_callback)

        # 创建Publisher用于发布 最终 ik的 Marker
        self.marker_pub = rospy.Publisher("final_visualization_marker", Marker, queue_size=10)
        self.model_path = "/home/lab/kuavo-ros-control/src/humanoid-control/biped_s40"
        
        # 创建全局服务指南
        self.bag_service = rospy.Service('/start_put_bag_to_tag_area', catch_bag_ik_Control, self.handle_start_put_bag_to_tag_area)

        # 创建手臂控制joint_pub
        self.joint_state_pub = rospy.Publisher('/kuavo_arm_traj', JointState, queue_size=10)

    def pubHeadMotionData(self, yaw, pitch):
        """
            头部电机发布器
        """
        msg = robotHeadMotionData()
        msg.joint_data.append(yaw)
        msg.joint_data.append(pitch)
        time.sleep(2)
        self.head_pub.publish(msg)
        rospy.loginfo(" ------ 发送头部控制指令 --------- ")

    def aprtag_client(self, command, tag_id=2, interval_x=0.5, y=0, yaw=0, is_x=False, is_y=False, angle_move=False, is_aprtag=False):
        rospy.wait_for_service('aprtag_service')
        try:
            aprtag_req = rospy.ServiceProxy('aprtag_service', AprtagRequest)
            resp = aprtag_req(command, tag_id, interval_x, y, yaw, is_x, is_y, angle_move, is_aprtag)
            return resp.status, resp.success
        except rospy.ServiceException as e:
            rospy.logerr(f"Service call failed: {e}")
            return None

    def handle_start_put_bag_to_tag_area(self, req):
        global START_FLAG
        global FINISH_FLAG

        # 如果请求的 start_flag 为 True，设置 START_FLAG
        if req.start_flag:
            START_FLAG = 1
            rospy.loginfo("START_FLAG 设置为 1")
            # 返回 FINISH_FLAG 的值
            return catch_bag_ik_ControlResponse(FINISH_FLAG)
        else:
            START_FLAG = 0
            called_once = False
            # 纯check
            return catch_bag_ik_ControlResponse(FINISH_FLAG)
    
    def mpc_obs_callback(self, msg):
        global current_arm_joint_state
        current_arm_joint_state = msg.state.value[24:] # 获取弧度制的关节状态
        current_arm_joint_state = [round(math.degrees(pos), 2) for pos in current_arm_joint_state] #  # 将关节状态从弧度制转换为角度制并保留两位小数
        # current_arm_joint_state.extend([0] * 14) # 在关节状态列表的末尾添加14个零
        # print( " current_arm_joint_state : ", current_arm_joint_state)

    def publish_joint_state(self, positions):
        """ 发布JointState到 /kuavo_arm_traj 话题 """
        joint_state_msg = JointState()

        # 关节名称
        joint_state_msg.name = [
            "zarm_l1_link", "zarm_l2_link", "zarm_l3_link", "zarm_l4_link", "zarm_l5_link", "zarm_l6_link", "zarm_l7_link",
            "zarm_r1_link", "zarm_r2_link", "zarm_r3_link", "zarm_r4_link", "zarm_r5_link", "zarm_r6_link", "zarm_r7_link"
        ]
        
        # 14维度的关节位置
        if len(positions) == 14:
            joint_state_msg.position = positions
        else:
            rospy.logerr("Position list must be of length 14.")
            return

        # 发布JointState消息
        joint_state_msg.header.stamp = rospy.Time.now()
        self.joint_state_pub.publish(joint_state_msg)
        rospy.loginfo("发布了JointState到/kuavo_arm_traj")

    def grasp_callback(self, msg):
        """ 回调 """
        self.grasp_info = msg
        # rospy.loginfo("Grasp info updated with the latest marker data.")
    
    def robot_traj_callback(self, msg):
        """ 回调 """
        global IK_SUCCESS_FALG
        self.robot_arm_traj = msg
        IK_SUCCESS_FALG = True
        print( " Successfully - 成功ik 数据 : ", msg)
        print( " Successfully - grasp_info 数据 : ", self.grasp_info)

    def construct_marker(self, arm_pose_p, arm_pose_q, r, g, b, side):
        """
            处理Marker信息
        """
        if len(arm_pose_q) != 4 or len(arm_pose_p) != 3:
            rospy.logerr("Invalid arm pose, cannot construct marker")
            return None

        marker = Marker()
        marker.header.frame_id = "torso"
        marker.type = Marker.MESH_RESOURCE
        marker.action = Marker.ADD

        if side == "Left":
            marker.mesh_resource = (
                "file://" + self.model_path + "/meshes/l_hand_roll.STL"
            )
        elif side == "Right":
            marker.mesh_resource = (
                "file://" + self.model_path + "/meshes/r_hand_roll.STL"
            )
        elif side == "Torso":
            marker.mesh_resource = (
                "file://" + self.model_path + "/meshes/base_link.STL"
            )

        marker.scale.x = 1.0
        marker.scale.y = 1.0
        marker.scale.z = 1.0
        marker.color.a = 0.3
        marker.color.r = r
        marker.color.g = g
        marker.color.b = b
        marker.header.stamp = rospy.Time.now()
        marker.pose.position.x = arm_pose_p[0]
        marker.pose.position.y = arm_pose_p[1]
        marker.pose.position.z = arm_pose_p[2]
        marker.pose.orientation = Quaternion(*arm_pose_q)

        return marker

    def send_ik_command(self):
        """ 发送ik指令 """
        global IK_SUCCESS_FALG
        # 初始化 ik 命令信息
        ik_msg = twoArmHandPose()

        target_position_x = self.grasp_info.pose.position.x
        target_position_y = self.grasp_info.pose.position.y
        target_position_z = self.grasp_info.pose.position.z

        target_orientation_x = self.grasp_info.pose.orientation.x
        target_orientation_y = self.grasp_info.pose.orientation.y
        target_orientation_z = self.grasp_info.pose.orientation.z
        target_orientation_w = self.grasp_info.pose.orientation.w

        final_grasp_position = [target_position_x, target_position_y, target_position_z]
        final_combined_quat = [target_orientation_x, target_orientation_y, target_orientation_z, target_orientation_w]

        if not IK_SUCCESS_FALG:
            # 发送ik指令 left_pose right_pose
            ik_msg.right_pose.pos_xyz = final_grasp_position
            ik_msg.right_pose.quat_xyzw = final_combined_quat
            ik_msg.right_pose.elbow_pos_xyz = [0.0, 0.0, 0.0]
            ik_msg.right_pose.joint_angles = [0.0] * 7

            ik_msg.left_pose.pos_xyz = [0.0, 0.0, 0.0]
            ik_msg.left_pose.quat_xyzw = [0.0, 0.0, 0.0, 1.0]
            ik_msg.left_pose.elbow_pos_xyz = [0.0, 0.0, 0.0]
            ik_msg.left_pose.joint_angles = [0.0] * 7

            rospy.loginfo("基于最佳抓取姿态发布 IK 命令")
            self.ik_pub.publish(ik_msg)
            print(" ik_msg : ", ik_msg)

            # 构建并发布 Marker，显示 IK 目标姿态
            marker = self.construct_marker(final_grasp_position, final_combined_quat, 0.0, 1.0, 0.0, "Right")  # 使用绿色标记左臂
            if marker:
                self.marker_pub.publish(marker)  # 发布 marker
                rospy.loginfo("已发布 Marker 显示 IK 目标姿态")

## ----------------- 外部函数 ---------------------- ## 
def bezier_curve(P0, P1, P2, P3, t):
    return (1 - t)**3 * np.array(P0) + \
           3 * (1 - t)**2 * t * np.array(P1) + \
           3 * (1 - t) * t**2 * np.array(P2) + \
           t**3 * np.array(P3)

def generate_plan_arm_trajectory_service(start_positions, target_positions, start_time, end_time, grasp, alpha=0.3, offset=1.0):
    # 返回值
    flag = False

    # 初始化一个存储所有关节贝塞尔曲线的列表
    all_bezier_points = []

    # 对每个关节遍历并生成贝塞尔曲线
    for i in range(14):  # 假设有14个关节
        # 构造单关节p0和p3
        P0 = [start_time, start_positions[i]]
        P3 = [end_time, target_positions[i]]
        # print(f"PO (Joint {i}) : {P0} | P3 : {P3}")

        direction = np.array([P3[0] - P0[0], P3[1] - P0[1]])
        # print(f"Direction (Joint {i}) : {direction}")

        perpendicular = np.array([-direction[1], direction[0]])
        perpendicular = perpendicular / np.linalg.norm(perpendicular)  # 归一化

        # 生成控制点 P1 和 P2，加入垂直方向的偏移
        P1 = P0 + alpha * direction + offset * perpendicular
        P2 = P3 - alpha * direction + offset * perpendicular
        # print(f"P1 (Joint {i}): [{P1[0]:.6f}, {P1[1]:.6f}], P2: [{P2[0]:.6f}, {P2[1]:.6f}]")

        # 生成 t 的取值
        t_values = np.linspace(0, 1, 100)

        # 计算贝塞尔曲线的点
        bezier_points = np.array([bezier_curve(P0, P1, P2, P3, t) for t in t_values])
        np.set_printoptions(suppress=True, precision=6, formatter={'float_kind': '{:f}'.format})
        # print(f"bezier_points (Joint {i}): {bezier_points}")
        # print(f"bezier_points length (Joint {i}): {len(bezier_points)}")

        # 将当前关节的贝塞尔曲线添加到总列表中
        all_bezier_points.append(bezier_points)

    # 转换为 NumPy 数组，方便操作
    all_bezier_points = np.array(all_bezier_points)

    # 打印和返回所有关节的贝塞尔曲线
    # print(f"All Bezier Points Shape: {all_bezier_points.shape}")

    # 遍历时间步长并发布关节状态
    plan_arm_traj_bezier_demo.call_change_arm_ctrl_mode_service(2)
    for t_index in range(len(t_values)):
        # 初始化要发布的关节位置列表
        current_joint_positions = []

        # 提取所有关节在当前时刻的贝塞尔曲线位置
        for i in range(14):
            joint_position_at_t = all_bezier_points[i][t_index][1]  # 获取每个关节的当前时刻的位置
            current_joint_positions.append(joint_position_at_t)

        # 发布当前时刻的所有关节位置
        # print(f"current_joint_positions : {current_joint_positions}")
        time.sleep(0.02)
        grasp.publish_joint_state(current_joint_positions)
    
    flag = True
    return flag

def init_state_To_target(target_state, grasp):
    """
        发布机器人手臂轨迹
        @param target_state: 目标关节正解
        @param grasp: 实例对象
        TODO: 添加Bezier插值
    """
    # # 记录目标状态
    # rospy.loginfo("target_state : %s", target_state)

    # if len(target_state.position) == 14:
    #     rospy.loginfo("目标状态 JointState: %s", target_state.position)
        
    #     # 调用 publish_joint_state 发布关节状态
    #     grasp.publish_joint_state(target_state.position)
    # else:
    #     rospy.logerr("position 数据长度不为 14。")
    
    global current_arm_joint_state

    # 14维度手臂数据构造
    start_positions = current_arm_joint_state
    target_positions = target_state.position
    print(f" start_positions : {start_positions}  ")
    print(f" target_positions : {target_positions} ")

    # 设置开始和结束的时间
    start_time = rospy.Time.now().to_sec()
    end_time = start_time + 2.0  # 假设轨迹时长为2秒

    # 生成贝塞尔曲线服务 | 同时发布出去
    success = generate_plan_arm_trajectory_service(start_positions, target_positions, start_time, end_time, grasp, alpha=0.3, offset=1.0)
    
    if success:
        rospy.loginfo("成功生成 | 发布贝塞尔轨迹！")
    else:
        rospy.logerr("贝塞尔轨迹发布失败。")


def catch_bag_demo(grasp):
    """
    # # reset_zero
    # plan_arm_traj_bezier_demo.call_change_arm_ctrl_mode_service(2)
    # time.sleep(2)
    # grasp.publish_joint_state([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    #                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    # time.sleep(2)

    # 左手pre姿态
    grasp.publish_joint_state([-10.0, 10.0, 0.0, -70.0, -90.0, 0.0, 0.0, 
                                 0.0,  0.0, 0.0,   0.0,   0.0, 0.0, 0.0])
    """
    global FINISH_FLAG
    
    """
        Tag识别and放置位置
        1 拿到ik的位置
    """
    zero_hand = [0, 0, 0, 0, 0, 0]
    full_hand = [100, 100, 100, 100, 100, 100]  # 右手位置数据

    # 降低头部
    grasp.pubHeadMotionData(0, 25) # yaw保持不变.pitch降低高度

    # pre姿态
    plan_arm_traj_bezier_demo.call_change_arm_ctrl_mode_service(2)
    time.sleep(2)
    grasp.publish_joint_state([ 0.0,  0.0, 0.0,   0.0,   0.0, 0.0, 0.0,
                              -25.0, -10.0, 0.0, -70.0, 90.0, 0.0, 0.0,])

    time.sleep(3)
    publish_hand_position(zero_hand, full_hand)

    # 走到位置 | tag定位走到位置
    command = 'run'  # 或 'check'
    tag_id = 2
    interval_x = 0.3 # 注意是间隔
    y = 0.0
    yaw = 0.0
    is_x = True
    is_y = True
    angle_move = False
    is_aprtag = True
    status, success = grasp.aprtag_client(command, tag_id, interval_x, y, yaw, is_x, is_y, angle_move, is_aprtag)

    time.sleep(1)

    command = 'check' 
    status = "Busy"
    while status == "Busy":
        status, success = grasp.aprtag_client(command)
        time.sleep(1)
    
    # # 等待 
    # input( " ----- 位置已经到达 ------ Enter按下键 继续IK解 ----------- ")

    # # 发送 IK 指令，直到 IK_SUCCESS_FALG 为 True
    # plan_arm_traj_bezier_demo.call_change_arm_ctrl_mode_service(2)
    # rospy.loginfo("开始发送 IK 指令...")
    # rate = rospy.Rate(10)  # 设置循环频率为10Hz
    # while not IK_SUCCESS_FALG:
    #     grasp.send_ik_command()
    #     rate.sleep()  # 等待 100ms 继续下一次循环
    
    # rospy.loginfo("IK 成功，继续执行接下来的操作。")

    """
    """
    # 拿到ik的数据: grasp.robot_arm_traj 目标帧 | 然后将当前机器人的动作帧 和 目标帧 生成贝塞尔曲线
    # grasp.robot_arm_traj.position = [ 0.0,  0.0,  0.0,   0.0,  0.0, 0.0, 0.0,
    #                                 -30.0, -3.0, 31.0, -48.0, 70.0, 0.0, -12.0]

    grasp.robot_arm_traj.position = [ 0.0,  0.0,  0.0,   0.0,  0.0, 0.0, 0.0,
                                    -15.0, -10.0, 0.0, -55.0, 90.0, 0.0, 0.0]

    rospy.loginfo("开始进行贝塞尔曲线轨迹发布 IK 指令...")
    init_state_To_target(grasp.robot_arm_traj, grasp)
    publish_hand_position(zero_hand, zero_hand)
    time.sleep(1) # 灵巧手执行时间

    # 放完之后，抬高一点
    plan_arm_traj_bezier_demo.call_change_arm_ctrl_mode_service(2)
    # grasp.publish_joint_state([ 0.0,  0.0,  0.0,   0.0,  0.0, 0.0,  0.0,
    #                           -30.0, -3.0, 31.0, -48.0, 70.0, 10.0, -30.0])

    grasp.publish_joint_state([ 0.0,  0.0,  0.0,   0.0,  0.0, 0.0,  0.0,
                              -15.0, -10.0, 0.0, -55.0, 70.0, 0.0, -20.0])

    time.sleep(1) # 等待抬高
    """
        End 结束
    """
    # 退出来(以tag出来)
    command = 'run'  # 或 'check'
    interval_x = -0.5
    is_x = True
    is_y = False
    angle_move = False
    is_aprtag = False

    tag_id = 2
    y = 0.0
    yaw = 0.0

    status, success = grasp.aprtag_client(command, tag_id, interval_x, y, yaw, is_x, is_y, angle_move, is_aprtag)
    time.sleep(1)
    command = 'check' 
    status = "Busy"
    while status == "Busy":
        status, success = grasp.aprtag_client(command)
        time.sleep(1)

    # 放手位置 
    plan_arm_traj_bezier_demo.call_change_arm_ctrl_mode_service(2)
    grasp.publish_joint_state([ 0.0,  0.0, 0.0,  0.0,  0.0, 0.0, 0.0,
                                0.0,  0.0, 0.0,  0.0,  0.0, 0.0, 0.0,])
    # publish_hand_position(zero_hand, zero_hand)
    grasp.pubHeadMotionData(0, 0) # 头部回正
    time.sleep(1) 
    FINISH_FLAG = True
    rospy.loginfo(" ... 完成任务 ...")

    # 重置位置
    plan_arm_traj_bezier_demo.call_change_arm_ctrl_mode_service(1)

def main(): 
    rospy.init_node('catch_bag_demo_node')
    grasp = GraspObject() 
    global called_once
    global START_FLAG
    
    # 创建标志变量，确保 catch_bag_demo 只调用一次
    rospy.loginfo(" ...  IK 放置demo开始，等待Service的调用 ...")

    while not rospy.is_shutdown():
        if (START_FLAG == 1) and (not called_once):
            rospy.loginfo(" ...  开始执行 catch_bag_demo 函数 ...")
            catch_bag_demo(grasp)  # 调用 ik 函数
            called_once = True     # 设置标志，防止重复调用
            
    # 结束
    rospy.loginfo(" ... catch_bag_demo_node 结束 ...")
    
if __name__ == '__main__':
    main()
    