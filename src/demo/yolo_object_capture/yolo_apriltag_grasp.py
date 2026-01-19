#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实物抓取程序 - 基于AprilTag定位 + YOLOv8检测

流程：
1. 识别AprilTag获取位置和姿态
2. 根据偏移量计算物品位置
3. 低头检测YOLOv8目标
4. IK求解并执行抓取
5. 移动到放置点放置

用法:
  python3 yolo_apriltag_grasp.py --offset_start True
  python3 yolo_apriltag_grasp.py --offset_start True --lateral_offset 0.75 --place_lateral_offset -0.5
"""

import rospy
import math
import time
import yaml
import os
import numpy as np
from collections import defaultdict

# ROS消息
from vision_msgs.msg import Detection2DArray
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from kuavo_msgs.msg import armTargetPoses, robotHandPosition, robotHeadMotionData
from kuavo_msgs.msg import twoArmHandPoseCmd, ikSolveParam
from kuavo_msgs.srv import changeArmCtrlMode, changeArmCtrlModeRequest
from kuavo_msgs.srv import twoArmHandPoseCmdSrv

# AprilTag检测
try:
    from apriltag_ros.msg import AprilTagDetectionArray
    from scipy.spatial.transform import Rotation as R
    HAS_APRILTAG = True
except ImportError:
    HAS_APRILTAG = False
    print("警告: apriltag_ros 未安装，AprilTag定位不可用")


# ==================== IK参数配置 ====================
use_custom_ik_param = True
joint_angles_as_q0 = True
ik_solve_param = ikSolveParam()
ik_solve_param.major_optimality_tol = 1e-3
ik_solve_param.major_feasibility_tol = 1e-3
ik_solve_param.minor_feasibility_tol = 1e-3
ik_solve_param.major_iterations_limit = 500
ik_solve_param.oritation_constraint_tol = 1e-3
ik_solve_param.pos_constraint_tol = 1e-3
ik_solve_param.pos_cost_weight = 0.0

# 手部开合控制
CLOSE_HAND = [80, 100, 80, 75, 75, 75]
OPEN_HAND = [0, 100, 0, 0, 0, 0]
ZERO_HAND = [0, 0, 0, 0, 0, 0]


# ==================== 工具函数 ====================
def set_head_target(yaw, pitch):
    """设置头部目标位置"""
    pub = rospy.Publisher('/robot_head_motion_data', robotHeadMotionData, queue_size=10)
    rospy.sleep(0.5)
    msg = robotHeadMotionData()
    msg.joint_data = [yaw, pitch]
    pub.publish(msg)
    rospy.loginfo(f"头部目标: yaw={yaw}, pitch={pitch}")


def get_robot_version():
    """获取机器人版本"""
    try:
        version = rospy.get_param('robot_version')
        valid_series = [42, 45, 49, 52]
        series = version % 100000
        if series not in valid_series:
            rospy.logerr(f"无效版本号: {version}")
            return None
        rospy.loginfo(f"机器人版本: {version}")
        return version
    except:
        rospy.logerr("获取版本号失败")
        return None


def call_ik_srv(eef_pose_msg):
    """调用IK逆解服务"""
    rospy.wait_for_service('/ik/two_arm_hand_pose_cmd_srv')
    try:
        srv = rospy.ServiceProxy('/ik/two_arm_hand_pose_cmd_srv', twoArmHandPoseCmdSrv)
        return srv(eef_pose_msg)
    except rospy.ServiceException as e:
        rospy.logerr(f"IK服务调用失败: {e}")
        return None


def set_arm_control_mode(mode):
    """设置手臂控制模式 (1=自动摆手, 2=外部控制)"""
    try:
        srv = rospy.ServiceProxy("/arm_traj_change_mode", changeArmCtrlMode)
        req = changeArmCtrlModeRequest()
        req.control_mode = mode
        resp = srv(req)
        if resp.result:
            rospy.loginfo(f"手臂模式切换为 {mode}")
        else:
            rospy.logwarn(f"手臂模式切换失败: {resp.message}")
    except Exception as e:
        rospy.logerr(f"手臂模式切换异常: {e}")


class Quaternion:
    def __init__(self):
        self.w = self.x = self.y = self.z = 0


def euler_to_quaternion(yaw, pitch, roll=0):
    """欧拉角转四元数"""
    cy, sy = np.cos(yaw), np.sin(yaw)
    cp, sp = np.cos(pitch), np.sin(pitch)
    
    R_mat = np.array([
        [cy * cp, -sy, cy * sp],
        [sy * cp, cy, sy * sp],
        [-sp, 0, cp]
    ])
    
    trace = np.trace(R_mat)
    q = Quaternion()
    
    if trace > 0:
        q.w = math.sqrt(trace + 1.0) / 2
        q.x = (R_mat[2, 1] - R_mat[1, 2]) / (4 * q.w)
        q.y = (R_mat[0, 2] - R_mat[2, 0]) / (4 * q.w)
        q.z = (R_mat[1, 0] - R_mat[0, 1]) / (4 * q.w)
    else:
        i = np.argmax([R_mat[0, 0], R_mat[1, 1], R_mat[2, 2]])
        j, k = (i + 1) % 3, (i + 2) % 3
        t = np.zeros(4)
        t[i] = math.sqrt(R_mat[i, i] - R_mat[j, j] - R_mat[k, k] + 1) / 2
        t[j] = (R_mat[i, j] + R_mat[j, i]) / (4 * t[i])
        t[k] = (R_mat[i, k] + R_mat[k, i]) / (4 * t[i])
        t[3] = (R_mat[k, j] - R_mat[j, k]) / (4 * t[i])
        q.x, q.y, q.z, q.w = t
    
    norm = math.sqrt(q.w**2 + q.x**2 + q.y**2 + q.z**2)
    if norm > 0:
        q.w, q.x, q.y, q.z = q.w/norm, q.x/norm, q.y/norm, q.z/norm
    return q


# ==================== 主类 ====================
class AprilTagGraspDemo:
    def __init__(self):
        rospy.init_node('apriltag_grasp_demo', anonymous=True)
        
        # AprilTag检测
        self.apriltag_detections = None
        if HAS_APRILTAG:
            self.apriltag_sub = rospy.Subscriber(
                '/robot_tag_info_odom', AprilTagDetectionArray,
                self._apriltag_callback, queue_size=1
            )
        
        # YOLOv8检测
        self.yolo_positions = {}
        self.yolo_sub = rospy.Subscriber(
            '/robot_yolov8_info', Detection2DArray,
            self._yolo_callback, queue_size=1
        )
        
        # Odom位置
        self.current_x = self.current_y = self.current_yaw = 0.0
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self._odom_callback, queue_size=1)
        
        # 控制发布者
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.hand_pub = rospy.Publisher('/control_robot_hand_position', robotHandPosition, queue_size=10)
        self.arm_pub = rospy.Publisher('kuavo_arm_target_poses', armTargetPoses, queue_size=10)
        
        # 关键：等待Publisher注册完成（与yolo_object_capture.py一致）
        rospy.sleep(0.5)
        
        # 创建手部消息对象（复用，与yolo_object_capture.py一致）
        self.hand_msg = robotHandPosition()
        self.hand_msg.left_hand_position = ZERO_HAND
        self.hand_msg.right_hand_position = ZERO_HAND
        
        # 等待订阅者连接
        rate = rospy.Rate(10)
        while self.arm_pub.get_num_connections() == 0 and not rospy.is_shutdown():
            rospy.loginfo("等待 kuavo_arm_target_poses 订阅者连接...")
            rate.sleep()
        while self.hand_pub.get_num_connections() == 0 and not rospy.is_shutdown():
            rospy.loginfo("等待 control_robot_hand_position 订阅者连接...")
            rate.sleep()
        
        # 再等待一下确保连接稳定
        rospy.sleep(0.3)
        
        rospy.loginfo("AprilTagGraspDemo 初始化完成")
    
    def _apriltag_callback(self, msg):
        self.apriltag_detections = msg
    
    def _yolo_callback(self, msg):
        self.yolo_positions.clear()
        for det in msg.detections:
            if det.results:
                result = det.results[0]
                pos = result.pose.pose.position
                self.yolo_positions[result.id] = (pos.x, pos.y, pos.z)
    
    def _odom_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        self.current_yaw = math.atan2(2*(q.w*q.z + q.x*q.y), 1 - 2*(q.y**2 + q.z**2))
    
    def get_apriltag_position(self, tag_id, timeout=10.0):
        """获取AprilTag位置和姿态"""
        if not HAS_APRILTAG:
            return None
        
        rospy.loginfo(f"等待检测 AprilTag ID:{tag_id}...")
        rate = rospy.Rate(10)
        end_time = rospy.Time.now() + rospy.Duration(timeout)
        
        while not rospy.is_shutdown() and rospy.Time.now() < end_time:
            if self.apriltag_detections:
                for det in self.apriltag_detections.detections:
                    if det.id[0] == tag_id:
                        pose = det.pose.pose.pose
                        position = np.array([pose.position.x, pose.position.y, pose.position.z])
                        quaternion = np.array([
                            pose.orientation.x, pose.orientation.y,
                            pose.orientation.z, pose.orientation.w
                        ])
                        rospy.loginfo(f"找到 AprilTag ID:{tag_id} @ ({position[0]:.2f}, {position[1]:.2f})")
                        return position, quaternion
            rate.sleep()
        
        rospy.logwarn(f"未检测到 AprilTag ID:{tag_id}")
        return None
    
    def calculate_target_position(self, tag_position, tag_quaternion, lateral_offset, forward_offset=0):
        """根据AprilTag计算目标位置"""
        R_mat = R.from_quat(tag_quaternion).as_matrix()
        z_axis = R_mat[:, 2]
        
        # 机器人面向AprilTag的方向
        forward_dir = np.array([-z_axis[0], -z_axis[1]])
        forward_norm = np.linalg.norm(forward_dir)
        if forward_norm < 0.01:
            return None, None
        forward_dir = forward_dir / forward_norm
        
        # 右方向
        right_dir = np.array([forward_dir[1], -forward_dir[0]])
        
        # 目标位置
        target_x = tag_position[0] + lateral_offset * right_dir[0] - forward_offset * forward_dir[0]
        target_y = tag_position[1] + lateral_offset * right_dir[1] - forward_offset * forward_dir[1]
        target_yaw = math.atan2(forward_dir[1], forward_dir[0])
        
        return (target_x, target_y), target_yaw
    
    def move_to(self, target_x, target_y, target_yaw=None, tolerance=0.1, yaw_tolerance=0.1):
        """三阶段移动到目标点"""
        rospy.loginfo(f"移动到 ({target_x:.2f}, {target_y:.2f})")
        
        def normalize_angle(a):
            while a > math.pi: a -= 2*math.pi
            while a < -math.pi: a += 2*math.pi
            return a
        
        rate = rospy.Rate(50)
        
        # 阶段1: 转向
        rospy.loginfo("  阶段1: 转向...")
        for _ in range(3000):  # 最多60秒
            dx, dy = target_x - self.current_x, target_y - self.current_y
            target_dir = math.atan2(dy, dx)
            angle_diff = normalize_angle(target_dir - self.current_yaw)
            
            if abs(angle_diff) < yaw_tolerance:
                self._stop()
                break
            
            vz = 0.3 if abs(angle_diff) > 0.25 else 0.15
            vz = vz if angle_diff > 0 else -vz
            self._move(0, 0, vz)
            rate.sleep()
        
        time.sleep(0.3)
        
        # 阶段2: 行走
        rospy.loginfo("  阶段2: 行走...")
        for _ in range(6000):
            dx, dy = target_x - self.current_x, target_y - self.current_y
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist < tolerance:
                self._stop()
                break
            
            target_dir = math.atan2(dy, dx)
            angle_diff = normalize_angle(target_dir - self.current_yaw)
            
            vx = 0.15 if dist > 0.3 else 0.1
            vz = 0.1 * angle_diff
            vz = max(-0.1, min(0.1, vz))
            self._move(vx, 0, vz)
            rate.sleep()
        
        time.sleep(0.3)
        
        # 阶段3: 调整朝向
        if target_yaw is not None:
            rospy.loginfo(f"  阶段3: 调整朝向 ({math.degrees(target_yaw):.1f}°)...")
            for _ in range(3000):
                angle_diff = normalize_angle(target_yaw - self.current_yaw)
                if abs(angle_diff) < yaw_tolerance:
                    self._stop()
                    break
                vz = 0.3 if abs(angle_diff) > 0.25 else 0.15
                vz = vz if angle_diff > 0 else -vz
                self._move(0, 0, vz)
                rate.sleep()
        
        self._stop()
        rospy.loginfo("  ✅ 到达目标")
        return True
    
    def move_backward(self, distance, speed=0.1):
        """后退指定距离"""
        rospy.loginfo(f"后退 {distance}m...")
        start_x, start_y = self.current_x, self.current_y
        rate = rospy.Rate(50)
        
        while not rospy.is_shutdown():
            traveled = math.sqrt((self.current_x - start_x)**2 + (self.current_y - start_y)**2)
            if traveled >= distance - 0.05:
                break
            self._move(-speed, 0, 0)
            rate.sleep()
        
        self._stop()
        rospy.loginfo(f"  ✅ 后退完成")
    
    def move_lateral(self, distance, speed=0.1):
        """
        横向平移指定距离（带闭环检测）
        :param distance: 平移距离，正值=向右，负值=向左
        :param speed: 平移速度
        """
        direction = "右" if distance > 0 else "左"
        rospy.loginfo(f"横向平移 {abs(distance):.2f}m (向{direction})...")
        start_x, start_y = self.current_x, self.current_y
        target_distance = abs(distance)
        rate = rospy.Rate(50)
        
        # 计算横向速度方向（正值向右，负值向左）
        # ROS中 linear.y 正值为左，负值为右，所以取反
        vy = -speed if distance > 0 else speed
        
        while not rospy.is_shutdown():
            traveled = math.sqrt((self.current_x - start_x)**2 + (self.current_y - start_y)**2)
            if traveled >= target_distance - 0.05:
                break
            self._move(0, vy, 0)
            rate.sleep()
        
        self._stop()
        rospy.loginfo(f"  ✅ 横向平移完成")
    
    def _move(self, vx, vy, vz):
        twist = Twist()
        twist.linear.x, twist.linear.y, twist.angular.z = vx, vy, vz
        self.cmd_vel_pub.publish(twist)
    
    def _stop(self):
        self._move(0, 0, 0)
    
    def publish_arm_poses(self, times, values):
        """发布手臂目标姿态"""
        msg = armTargetPoses()
        msg.times = times
        msg.values = values
        self.arm_pub.publish(msg)
    
    def set_hand(self, left=None, right=None):
        """设置手部姿态，未指定的手保持当前状态（与yolo_object_capture.py一致）"""
        # 只修改指定的手，另一只手保持之前的值
        if left is not None:
            self.hand_msg.left_hand_position = left
        if right is not None:
            self.hand_msg.right_hand_position = right
        self.hand_pub.publish(self.hand_msg)
        rospy.loginfo(f"手部控制: 左={self.hand_msg.left_hand_position}, 右={self.hand_msg.right_hand_position}")

    def grasp_object(self, target_id=39, hand="auto",
                    offset_z=-0.013, temp_x_l=-0.016, temp_y_l=0.038,
                    temp_x_r=0.055, temp_y_r=-0.038, offset_angle=1.0):
        """
        执行抓取动作
        :param target_id: YOLOv8目标ID (39=瓶子, 41=杯子)
        :param hand: 使用的手 "left"/"right"/"auto"
        :param offset_z: Z轴偏移量
        :param temp_x_l: 左手X轴偏移
        :param temp_y_l: 左手Y轴偏移
        :param temp_x_r: 右手X轴偏移
        :param temp_y_r: 右手Y轴偏移
        :param offset_angle: Z轴角度偏移量缩放倍率
        """
        # 获取机器人版本
        robot_version = get_robot_version()
        if robot_version is None:
            return False
        
        # 机器人初始位置
        if robot_version == 52:
            robot_zero = (-0.012, -0.255 + 0.03, -0.315)
        elif robot_version == 45:
            robot_zero = (-0.0173, -0.2927, -0.2837)
        elif robot_version == 49:
            # 49系列机器人参数（与45系列相同，根据实际调整）
            robot_zero = (-0.0173, -0.2927, -0.2837)
        else:
            rospy.logerr("不支持的机器人版本")
            return False
        
        # 低头检测
        set_head_target(0, 30)
        time.sleep(1.5)
        
        # 等待YOLOv8检测
        rospy.loginfo(f"等待检测目标 ID:{target_id}...")
        rate = rospy.Rate(10)
        target_pos = None
        for _ in range(100):  # 最多10秒
            if target_id in self.yolo_positions:
                target_pos = self.yolo_positions[target_id]
                rospy.loginfo(f"检测到目标: ({target_pos[0]:.3f}, {target_pos[1]:.3f}, {target_pos[2]:.3f})")
                break
            rate.sleep()
        
        if target_pos is None:
            rospy.logerr("未检测到目标")
            set_head_target(0, 0)
            return False
        
        obj_x, obj_y, obj_z = target_pos
        
        # 判断左右手
        if hand == "auto":
            use_left = obj_y > 0
        else:
            use_left = (hand == "left")
        
        rospy.loginfo(f"使用{'左' if use_left else '右'}手抓取")
        
        # 设置手臂外部控制模式
        set_arm_control_mode(2)
        
        # 计算抓取位置
        if use_left:
            set_x = obj_x + temp_x_l
            set_y = obj_y + temp_y_l
        else:
            set_x = obj_x + temp_x_r
            set_y = obj_y - temp_y_r
        set_z = obj_z + offset_z
        
        rospy.loginfo(f"抓取位置: ({set_x:.3f}, {set_y:.3f}, {set_z:.3f})")
        
        # 构建IK请求
        eef_pose_msg = twoArmHandPoseCmd()
        eef_pose_msg.ik_param = ik_solve_param
        eef_pose_msg.use_custom_ik_param = use_custom_ik_param
        eef_pose_msg.joint_angles_as_q0 = joint_angles_as_q0
        # 设置初始关节角度作为IK求解的初始猜测（第4个关节弯曲-90度）
        eef_pose_msg.hand_poses.left_pose.joint_angles = np.array([0.0, 0.0, 0.0, -1.57079633, 0.0, 0.0, 0.0])
        eef_pose_msg.hand_poses.right_pose.joint_angles = np.array([0.0, 0.0, 0.0, -1.57079633, 0.0, 0.0, 0.0])
        
        if use_left:
            # 左手抓取
            eef_pose_msg.hand_poses.left_pose.pos_xyz = np.array([set_x, set_y, set_z])
            relative_angle = math.atan((robot_zero[1] - set_y) / (set_x - robot_zero[0]))
            quat = euler_to_quaternion(relative_angle * offset_angle, -1.57, 0)
            eef_pose_msg.hand_poses.left_pose.quat_xyzw = [quat.x, quat.y, quat.z, quat.w]
            eef_pose_msg.hand_poses.left_pose.elbow_pos_xyz = np.zeros(3)
            # 右手初始位置
            eef_pose_msg.hand_poses.right_pose.pos_xyz = np.array([robot_zero[0], robot_zero[1], robot_zero[2] + 0.05])
            eef_pose_msg.hand_poses.right_pose.quat_xyzw = [0, 0, 0, 1]
            eef_pose_msg.hand_poses.right_pose.elbow_pos_xyz = np.zeros(3)
        else:
            # 右手抓取
            eef_pose_msg.hand_poses.right_pose.pos_xyz = np.array([set_x, set_y, set_z])
            relative_angle = math.atan((set_y - robot_zero[1]) / (set_x - robot_zero[0]))
            quat = euler_to_quaternion(relative_angle * offset_angle, -1.57, 0)
            eef_pose_msg.hand_poses.right_pose.quat_xyzw = [quat.x, quat.y, quat.z, quat.w]
            eef_pose_msg.hand_poses.right_pose.elbow_pos_xyz = np.zeros(3)
            # 左手初始位置
            eef_pose_msg.hand_poses.left_pose.pos_xyz = np.array([robot_zero[0], -robot_zero[1], robot_zero[2] + 0.05])
            eef_pose_msg.hand_poses.left_pose.quat_xyzw = [0, 0, 0, 1]
            eef_pose_msg.hand_poses.left_pose.elbow_pos_xyz = np.zeros(3)
        
        # 调用IK
        res = call_ik_srv(eef_pose_msg)
        if res is None or not res.success:
            rospy.logerr("IK求解失败")
            set_head_target(0, 0)
            set_arm_control_mode(1)
            return False
        
        rospy.loginfo(f"IK求解成功, 耗时: {res.time_cost:.2f}ms")
        
        # 获取IK结果的关节角度
        if use_left:
            target_joints = list(res.hand_poses.left_pose.joint_angles)
        else:
            target_joints = list(res.hand_poses.right_pose.joint_angles)
        
        # 执行抓取动作序列 (与yolo_object_capture.py一致的提肘方式)
        # ========== 阶段1: 初始位置 + 双手归零 ==========
        self.set_hand(ZERO_HAND, ZERO_HAND)
        self.publish_arm_poses([1.5], [20, 0, 0, -30, 0, 0, 0, 20, 0, 0, -30, 0, 0, 0])
        rospy.loginfo("回到初始位置")
        time.sleep(0.5)
        
        # ========== 阶段2: 准备姿态（提肘，与yolo_object_capture.py一致） ==========
        if use_left:
            # 左手提肘: [40, 20, 0, -120, 0, 0, -20] 手腕有-20度旋转
            self.publish_arm_poses([2.5], [40, 20, 0, -120, 0, 0, -20, 20, 0, 0, -30, 0, 0, 0])
            time.sleep(2)
            self.set_hand(left=OPEN_HAND)
        else:
            # 右手提肘: [40, -20, 0, -120, 0, 0, -20]
            self.publish_arm_poses([2.5], [20, 0, 0, -30, 0, 0, 0, 40, -20, 0, -120, 0, 0, -20])
            time.sleep(2)
            self.set_hand(right=OPEN_HAND)
        time.sleep(1.5)  # 等待手部张开完成
        
        # ========== 阶段3: 最终抓取位置（使用IK结果，另一只手保持初始） ==========
        # 另一只手使用弧度值 [0.35, 0, 0, -0.52, 0, 0, 0] 约等于 [20, 0, 0, -30, 0, 0, 0]
        if use_left:
            joint_end_angles = list(target_joints) + [0.35, 0, 0, -0.52, 0, 0, 0]
        else:
            joint_end_angles = [0.35, 0, 0, -0.52, 0, 0, 0] + list(target_joints)
        
        target_deg = [math.degrees(rad) for rad in joint_end_angles]
        self.publish_arm_poses([2.5], target_deg)
        rospy.loginfo("到达抓取位置")
        time.sleep(5)
        
        # ========== 阶段4: 握紧 ==========
        if use_left:
            self.set_hand(left=CLOSE_HAND)
        else:
            self.set_hand(right=CLOSE_HAND)
        time.sleep(1)
        
        # ========== 阶段5: 抬起（递水位置，避免打到桌子） ==========
        if use_left:
            self.publish_arm_poses([2], [-60, 0, 0, -30, 0, 0, 0, 20, 0, 0, -30, 0, 0, 0])
        else:
            self.publish_arm_poses([2], [20, 0, 0, -30, 0, 0, 0, -60, 0, 0, -30, 0, 0, 0])
        time.sleep(3)
        
        # ========== 阶段6: 抬起到搬运位置（侧抬+弯肘） ==========
        if use_left:
            self.publish_arm_poses([3], [20, 90, 0, -110, 0, 0, 0, 20, 0, 0, -30, 0, 0, 0])
        else:
            self.publish_arm_poses([3], [20, 0, 0, -30, 0, 0, 0, 20, -90, 0, -110, 0, 0, 0])
        time.sleep(3)
        
        # 抬头
        set_head_target(0, 0)
        
        rospy.loginfo("✅ 抓取完成")
        return "left" if use_left else "right"
    
    def place_object(self, hand):
        """放置物体（与grasp_controller一致）"""
        rospy.loginfo(f"放置物体 (使用{hand}手)")
        use_left = (hand == "left")
        
        # 直接在搬运位置释放
        if use_left:
            self.set_hand(left=OPEN_HAND)
        else:
            self.set_hand(right=OPEN_HAND)
        time.sleep(1)
        
        rospy.loginfo("✅ 放置完成")
    
    def reset_arm(self, hand):
        """复位手臂（与grasp_controller一致）"""
        rospy.loginfo("复位手臂...")
        use_left = (hand == "left")
        
        # ========== 阶段1: 收肘中间位置 ==========
        if use_left:
            self.publish_arm_poses([3], [6, 50, 0, -90, 0, 0, 0, 20, 0, 0, -30, 0, 0, 0])
            time.sleep(3)
            self.publish_arm_poses([3], [6, 50, 0, -20, 0, 0, 0, 20, 0, 0, -30, 0, 0, 0])
            time.sleep(3)
        else:
            self.publish_arm_poses([3], [20, 0, 0, -30, 0, 0, 0, 6, -50, 0, -90, 0, 0, 0])
            time.sleep(3)
            self.publish_arm_poses([3], [20, 0, 0, -30, 0, 0, 0, 6, -50, 0, -20, 0, 0, 0])
            time.sleep(3)
        
        # ========== 阶段2: 双手归零 ==========
        self.set_hand(ZERO_HAND, ZERO_HAND)
        
        # ========== 阶段3: 侧抬，防止撞倒桌子 ==========
        if use_left:
            self.publish_arm_poses([3], [20, 90, 0, -110, 0, 0, 0, 20, 0, 0, -30, 0, 0, 0])
            time.sleep(3)
            self.publish_arm_poses([3], [20, 90, 0, -30, 0, 0, 0, 20, 0, 0, -30, 0, 0, 0])
        else:
            # 右手直接侧抬到-30度（无需-110中间步骤）
            self.publish_arm_poses([3], [20, 0, 0, -30, 0, 0, 0, 20, -90, 0, -30, 0, 0, 0])
        time.sleep(3)
        
        # ========== 阶段4: 回到初始位置 ==========
        self.publish_arm_poses([3], [20, 0, 0, -30, 0, 0, 0, 20, 0, 0, -30, 0, 0, 0])
        time.sleep(3)
        
        # 恢复自动摆手
        set_arm_control_mode(1)
        rospy.loginfo("✅ 手臂复位完成")
    
    def run_task(self, tag_id=0, lateral_offset=0.75, grasp_offset=0.15,
                 place_lateral_offset=-0.5, place_offset=0.32, backward_distance=0.5,
                 target_id=39, hand="auto",
                 offset_z=-0.013, temp_x_l=-0.016, temp_y_l=0.038,
                 temp_x_r=0.055, temp_y_r=-0.038, offset_angle=1.0):
        """
        执行完整的抓取放置任务
        
        :param tag_id: AprilTag ID
        :param lateral_offset: 物品横向偏移 (正=机器人右边，负=机器人左边)
        :param grasp_offset: 抓取距离
        :param place_lateral_offset: 放置点横向偏移 (正=机器人右边，负=机器人左边)
        :param place_offset: 放置距离
        :param backward_distance: 后退距离
        :param target_id: YOLOv8目标ID
        :param hand: 使用的手
        :param offset_z: 抓取Z轴偏移
        :param temp_x_l: 左手X轴偏移
        :param temp_y_l: 左手Y轴偏移
        :param temp_x_r: 右手X轴偏移
        :param temp_y_r: 右手Y轴偏移
        :param offset_angle: Z轴角度偏移量缩放倍率
        """
        rospy.loginfo("=" * 50)
        rospy.loginfo("开始抓取放置任务")
        rospy.loginfo("=" * 50)
        
        # 1. 检测AprilTag
        result = self.get_apriltag_position(tag_id)
        if result is None:
            rospy.logerr("未检测到AprilTag")
            return False
        tag_position, tag_quaternion = result
        
        # 2. 计算抓取位置并移动
        target_pos, target_yaw = self.calculate_target_position(
            tag_position, tag_quaternion, lateral_offset)
        if target_pos is None:
            return False
        
        rospy.loginfo(f"[1/6] 移动到抓取位置 ({target_pos[0]:.2f}, {target_pos[1]:.2f})")
        # 停在物品前方grasp_offset处
        approach_x = target_pos[0] - grasp_offset * math.cos(target_yaw)
        approach_y = target_pos[1] - grasp_offset * math.sin(target_yaw)
        self.move_to(approach_x, approach_y, target_yaw)
        
        # 3. 抓取
        rospy.loginfo("[2/6] 执行抓取")
        grasped_hand = self.grasp_object(
            target_id=target_id, hand=hand,
            offset_z=offset_z, temp_x_l=temp_x_l, temp_y_l=temp_y_l,
            temp_x_r=temp_x_r, temp_y_r=temp_y_r, offset_angle=offset_angle
        )
        if not grasped_hand:
            return False
        
        # 4. 横向平移到放置位置
        # 计算横向平移距离：从抓取位置到放置位置的横向差
        lateral_move = place_lateral_offset - lateral_offset
        rospy.loginfo(f"[3/6] 横向平移到放置位置 ({lateral_move:.2f}m)")
        self.move_lateral(lateral_move)
        
        # 5. 放置
        rospy.loginfo("[4/6] 放置物体")
        self.place_object(grasped_hand)
        
        # 6. 放置后后退
        rospy.loginfo(f"[5/6] 放置后后退 {backward_distance}m")
        self.move_backward(backward_distance)
        
        # 7. 复位
        rospy.loginfo("[6/6] 复位手臂")
        self.reset_arm(grasped_hand)
        
        rospy.loginfo("=" * 50)
        rospy.loginfo("✅ 任务完成")
        rospy.loginfo("=" * 50)
        return True


def load_config():
    """加载YAML配置文件（从脚本同级的config目录）"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config', 'yolo_apriltag_grasp_config.yaml')
    
    if not os.path.exists(config_path):
        print(f"警告: 配置文件不存在: {config_path}")
        return {}
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f) or {}
    
    print(f"已加载配置文件: {config_path}")
    return config


def main():
    # 加载YAML配置
    config = load_config()
    
    # 导航参数
    tag_id = config.get('tag_id', 0)
    lateral_offset = config.get('lateral_offset', 0.75)
    grasp_offset = config.get('grasp_offset', 0.15)
    place_lateral_offset = config.get('place_lateral_offset', -0.5)
    place_offset = config.get('place_offset', 0.32)
    backward_distance = config.get('backward_distance', 0.5)
    target_id = config.get('target_id', 39)
    hand = config.get('hand', 'auto')
    
    # 抓取手部偏移量
    offset_z = config.get('offset_z', -0.013)
    temp_x_l = config.get('temp_x_l', -0.016)
    temp_y_l = config.get('temp_y_l', 0.038)
    temp_x_r = config.get('temp_x_r', 0.055)
    temp_y_r = config.get('temp_y_r', -0.038)
    offset_angle = config.get('offset_angle', 1.0)
    
    # 打印最终配置
    print("=" * 50)
    print("运行配置:")
    print(f"  tag_id: {tag_id}")
    print(f"  target_id: {target_id}")
    print(f"  hand: {hand}")
    print(f"  lateral_offset: {lateral_offset}")
    print(f"  grasp_offset: {grasp_offset}")
    print(f"  place_lateral_offset: {place_lateral_offset}")
    print(f"  place_offset: {place_offset}")
    print(f"  backward_distance: {backward_distance}")
    print("抓取偏移量:")
    print(f"  offset_z: {offset_z}")
    print(f"  temp_x_l: {temp_x_l}, temp_y_l: {temp_y_l}")
    print(f"  temp_x_r: {temp_x_r}, temp_y_r: {temp_y_r}")
    print(f"  offset_angle: {offset_angle}")
    print("=" * 50)
    
    try:
        demo = AprilTagGraspDemo()
        demo.run_task(
            tag_id=tag_id,
            lateral_offset=lateral_offset,
            grasp_offset=grasp_offset,
            place_lateral_offset=place_lateral_offset,
            place_offset=place_offset,
            backward_distance=backward_distance,
            target_id=target_id,
            hand=hand,
            offset_z=offset_z,
            temp_x_l=temp_x_l,
            temp_y_l=temp_y_l,
            temp_x_r=temp_x_r,
            temp_y_r=temp_y_r,
            offset_angle=offset_angle
        )
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        rospy.loginfo("用户中断")


if __name__ == '__main__':
    main()
