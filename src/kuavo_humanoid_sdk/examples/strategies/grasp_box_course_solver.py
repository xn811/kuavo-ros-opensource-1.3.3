#!/usr/bin/env python3
"""
箱子抓取课程解决方案 - 使用预设关节轨迹
不使用manipulation_mpc，直接用关节位置控制

用法:
  仿真模式: python3 grasp_box_course_solver.py --sim
  实物模式: python3 grasp_box_course_solver.py
  速度控制转向(低配电脑): python3 grasp_box_course_solver.py --velocity-turn
"""
import time
import math
import argparse
import numpy as np
import rospy
import tf2_ros
from tf.transformations import euler_from_quaternion
from kuavo_humanoid_sdk import KuavoRobot, KuavoRobotState, KuavoRobotTools, KuavoRobotVision
from kuavo_humanoid_sdk.interfaces.data_types import KuavoPose, AprilTagData, PoseQuaternion
from kuavo_humanoid_sdk.kuavo_strategy.grasp_box.grasp_box_strategy import KuavoGraspBox, BoxInfo

# 导入link attacher服务
try:
    from gazebo_ros_link_attacher.srv import Attach, AttachRequest
    HAS_ATTACH_SERVICE = True
except ImportError:
    HAS_ATTACH_SERVICE = False
    print("警告: gazebo_ros_link_attacher 未安装，将不使用物理抓取")

# 全局配置
USE_VELOCITY_TURN = False  # 是否使用速度控制转向

# 距离配置
GRASP_DISTANCE = 0.35   # 抓取时与AprilTag的距离(米)
PLACE_DISTANCE = 0.75   # 放置时与AprilTag的距离(米)，比抓取远一点

# ============== 预设手臂关节位置 (角度制) ==============
# 每个手臂7个关节: [shoulder_pitch, shoulder_roll, shoulder_yaw, elbow, wrist_yaw, wrist_pitch, wrist_roll]
# 左臂(7) + 右臂(7) = 14个关节

ARM_POSES = {
    # 安全收起姿态
    "safe": [
        7.6, 68.8, 0.0, -90.8, 77.1, 0.0, 0.0,    # 左臂
        7.6, -68.8, 0.0, -90.8, -77.1, 0.0, 0.0   # 右臂
    ],
    # 准备抓取姿态 (手臂向前伸展，准备抱箱子)
    "pre_grasp": [
        -33.0, 4.7, 9.4, -40.0, 12.0, 0.0, 0.0,   # 左臂
        -33.0, -4.7, 9.4, -40.0, -12.0, 0.0, 0.0   # 右臂
    ],
    # 抓取姿态 (手臂合拢抱住箱子)
    "grasp": [
        -30.2, -2, -30.0, -40.0, 12.0, 0.0, 0.0,   # 左臂
        -30.2, 2, 30.0, -40.0, -12.0, 0.0, 0.0   # 右臂
    ],
    # 抬起搬运姿态 (抱着箱子抬高)
    "carry": [
        -30.0, 25.0, 0.0, -90.0, 0.0, 0.0, 0.0,   # 左臂
        -30.0, -25.0, 0.0, -90.0, 0.0, 0.0, 0.0   # 右臂
    ],
    # 放下姿态 (准备放下箱子)
    "place": [
        -15.0, 30.0, 0.0, -75.0, 0.0, 0.0, 0.0,   # 左臂
        -15.0, -30.0, 0.0, -75.0, 0.0, 0.0, 0.0   # 右臂
    ],
    # 松开姿态 (放开箱子)
    "release": [
        -15.0, 50.0, 0.0, -60.0, 0.0, 0.0, 0.0,   # 左臂
        -15.0, -50.0, 0.0, -60.0, 0.0, 0.0, 0.0   # 右臂
    ],
}

def deg_to_rad(positions_deg):
    """角度转弧度"""
    return [np.radians(deg) for deg in positions_deg]

def attach_box(robot_link="zarm_l7_link", box_model="block", box_link="base_link"):
    """将箱子附着到机器人手上"""
    if not HAS_ATTACH_SERVICE:
        print("⚠️ attach服务不可用")
        return True
    try:
        service_name = '/link_attacher_node/attach'
        rospy.wait_for_service(service_name, timeout=2.0)
        attach_srv = rospy.ServiceProxy(service_name, Attach)
        req = AttachRequest()
        req.model_name_1 = "biped_s42"
        req.link_name_1 = robot_link
        req.model_name_2 = box_model
        req.link_name_2 = box_link
        resp = attach_srv(req)
        if resp.ok:
            print(f"✅ 附着成功: {robot_link} <-> {box_model}/{box_link}")
        else:
            print(f"⚠️ 附着失败")
        return resp.ok
    except Exception as e:
        print(f"⚠️ attach服务调用失败: {e}")
        return False

def detach_box(robot_link="zarm_l7_link", box_model="block", box_link="base_link"):
    """将箱子从机器人手上分离"""
    if not HAS_ATTACH_SERVICE:
        print("⚠️ detach服务不可用")
        return True
    try:
        service_name = '/link_attacher_node/detach'
        rospy.wait_for_service(service_name, timeout=2.0)
        detach_srv = rospy.ServiceProxy(service_name, Attach)
        req = AttachRequest()
        req.model_name_1 = "biped_s42"
        req.link_name_1 = robot_link
        req.model_name_2 = box_model
        req.link_name_2 = box_link
        resp = detach_srv(req)
        if resp.ok:
            print(f"✅ 分离成功: {robot_link} <-> {box_model}/{box_link}")
        else:
            print(f"⚠️ 分离失败")
        return resp.ok
    except Exception as e:
        print(f"⚠️ detach服务调用失败: {e}")
        return False

def wait_for_confirm(step_name):
    """等待用户确认继续"""
    while True:
        user_input = input(f"\n>>> {step_name} - 输入 'y' 继续, 'q' 退出: ").strip().lower()
        if user_input == 'y':
            return True
        elif user_input == 'q':
            print("用户取消操作")
            return False
        else:
            print("请输入 'y' 或 'q'")

def move_arm_to_pose(robot, pose_name, duration=2.0):
    """移动手臂到预设姿态"""
    if pose_name not in ARM_POSES:
        print(f"❌ 未知姿态: {pose_name}")
        return False
    
    positions_rad = deg_to_rad(ARM_POSES[pose_name])
    print(f"  移动到 [{pose_name}] 姿态...")
    robot.control_arm_joint_positions(positions_rad)
    time.sleep(duration)
    print(f"  ✅ 已到达 [{pose_name}] 姿态")
    return True

def adjust_grasp_pose(robot):
    """交互式调整抓取姿态"""
    current_pose = ARM_POSES["grasp"].copy()
    
    while True:
        print(f"\n当前抓取姿态 (角度):")
        print(f"  左臂: {current_pose[:7]}")
        print(f"  右臂: {current_pose[7:]}")
        
        user_input = input("\n输入新的14个关节角度(逗号分隔), 'y'确认并抓取, 'q'退出: ").strip()
        
        if user_input.lower() == 'y':
            print("✅ 确认抓取姿态")
            return True
        elif user_input.lower() == 'q':
            print("❌ 取消抓取")
            return False
        else:
            try:
                # 解析输入的角度
                new_angles = [float(x.strip()) for x in user_input.split(',')]
                if len(new_angles) != 14:
                    print(f"⚠️ 需要14个角度值，你输入了{len(new_angles)}个")
                    continue
                
                # 更新姿态
                current_pose = new_angles
                ARM_POSES["grasp"] = current_pose
                
                # 执行新姿态
                positions_rad = deg_to_rad(current_pose)
                print("  移动到新的抓取姿态...")
                robot.control_arm_joint_positions(positions_rad)
                time.sleep(2.0)
                print("  ✅ 已到达新姿态")
                
            except ValueError as e:
                print(f"⚠️ 输入格式错误: {e}")
                print("  示例: -33.2, 2.5, -15.0, -40.0, 12.0, 0.0, 0.0, -33.2, 2.5, -15.0, -40.0, -12.0, 0.0, 0.0")

def get_current_yaw():
    """通过TF获取当前机器人yaw角度"""
    try:
        tf_buffer = tf2_ros.Buffer()
        tf_listener = tf2_ros.TransformListener(tf_buffer)
        time.sleep(0.2)
        
        transform = tf_buffer.lookup_transform('odom', 'base_link', rospy.Time(0), rospy.Duration(1.0))
        quat = [
            transform.transform.rotation.x,
            transform.transform.rotation.y,
            transform.transform.rotation.z,
            transform.transform.rotation.w
        ]
        _, _, yaw = euler_from_quaternion(quat)
        return yaw
    except Exception as e:
        print(f"⚠️ 获取yaw角度失败: {e}")
        return None

def velocity_turn_to_target(robot, robot_state, target_yaw, angular_speed=0.3, tolerance=0.1):
    """
    使用速度控制转向到目标角度
    
    Args:
        robot: 机器人对象
        robot_state: 机器人状态对象
        target_yaw: 目标yaw角度(弧度)
        angular_speed: 转向角速度(rad/s)，默认0.3
        tolerance: 角度容差(弧度)，默认0.1(约5.7度)
    """
    print(f"  [速度控制转向] 目标角度: {math.degrees(target_yaw):.1f}°")
    
    max_time = 30.0  # 最大转向时间
    start_time = time.time()
    
    while time.time() - start_time < max_time:
        current_yaw = get_current_yaw()
        if current_yaw is None:
            time.sleep(0.1)
            continue
        
        # 计算角度差，归一化到[-pi, pi]
        yaw_error = target_yaw - current_yaw
        while yaw_error > math.pi:
            yaw_error -= 2 * math.pi
        while yaw_error < -math.pi:
            yaw_error += 2 * math.pi
        
        print(f"    当前: {math.degrees(current_yaw):.1f}°, 误差: {math.degrees(yaw_error):.1f}°")
        
        # 检查是否到达目标
        if abs(yaw_error) < tolerance:
            # 停止转向
            robot.walk(0.0, 0.0, 0.0)
            time.sleep(0.5)
            print(f"  ✅ 转向完成")
            return True
        
        # 计算转向速度（带方向）
        turn_speed = angular_speed if yaw_error > 0 else -angular_speed
        # 接近目标时减速
        if abs(yaw_error) < 0.3:  # 约17度
            turn_speed = turn_speed * 0.5
        
        robot.walk(0.0, 0.0, turn_speed)
        time.sleep(0.1)
    
    # 超时，停止转向
    robot.walk(0.0, 0.0, 0.0)
    print(f"  ⚠️ 转向超时")
    return False

def velocity_walk_to_target(robot, robot_state, target_x, target_y, target_yaw, 
                            linear_speed=0.12, angular_speed=0.15, 
                            pos_tolerance=0.2, yaw_tolerance=0.1):
    """
    使用速度控制行走到目标位置（基于odom坐标系的闭环控制）
    
    三阶段策略：
    1. 先转向目标方向
    2. 直线行走到目标位置（边走边微调）
    3. 最后调整到目标朝向
    
    Args:
        robot: 机器人对象
        robot_state: 机器人状态对象
        target_x, target_y: 目标位置(odom坐标系)
        target_yaw: 目标朝向(弧度)
        linear_speed: 线速度(m/s)
        angular_speed: 角速度(rad/s)
        pos_tolerance: 位置容差(米)
        yaw_tolerance: 角度容差(弧度)
    """
    print(f"  [速度控制行走] 目标: ({target_x:.2f}, {target_y:.2f}), yaw={math.degrees(target_yaw):.1f}°")
    
    # 初始化TF
    tf_buffer = tf2_ros.Buffer()
    tf_listener = tf2_ros.TransformListener(tf_buffer)
    time.sleep(0.3)
    
    def get_robot_pose():
        """获取机器人当前位姿"""
        try:
            transform = tf_buffer.lookup_transform('odom', 'base_link', rospy.Time(0), rospy.Duration(0.5))
            x = transform.transform.translation.x
            y = transform.transform.translation.y
            quat = [
                transform.transform.rotation.x,
                transform.transform.rotation.y,
                transform.transform.rotation.z,
                transform.transform.rotation.w
            ]
            _, _, yaw = euler_from_quaternion(quat)
            return x, y, yaw
        except Exception as e:
            return None, None, None
    
    def normalize_angle(angle):
        """归一化角度到[-pi, pi]"""
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle
    
    def publish_vel(vx, vy, vz):
        """发布速度命令"""
        robot.walk(vx, vy, vz)
    
    # ========== 阶段1：转向目标方向 ==========
    print("  阶段1: 转向目标方向...")
    max_turn_time = 120.0  # 增加超时时间，仿真中转向较慢
    start_time = time.time()
    last_print_time = 0
    
    while time.time() - start_time < max_turn_time:
        current_x, current_y, current_yaw = get_robot_pose()
        if current_x is None:
            time.sleep(0.1)
            continue
        
        # 计算目标方向
        dx = target_x - current_x
        dy = target_y - current_y
        target_dir = math.atan2(dy, dx)
        
        # 计算角度差
        angle_diff = normalize_angle(target_dir - current_yaw)
        
        # 每2秒打印一次状态
        elapsed = time.time() - start_time
        if elapsed - last_print_time > 2.0:
            print(f"    [转向] 当前yaw={math.degrees(current_yaw):.1f}°, 目标={math.degrees(target_dir):.1f}°, 差={math.degrees(angle_diff):.1f}°")
            last_print_time = elapsed
        
        if abs(angle_diff) < yaw_tolerance:
            publish_vel(0.0, 0.0, 0.0)
            print(f"    ✓ 转向完成 (误差={math.degrees(angle_diff):.1f}°)")
            break
        
        # 速度规划（限制在 SDK 允许范围内 [-0.4, 0.4]）
        turn_speed = 0.4 if abs(angle_diff) > 0.25 else 0.15
        turn_speed = turn_speed if angle_diff > 0 else -turn_speed
        
        publish_vel(0.0, 0.0, turn_speed)
        time.sleep(0.02)
    else:
        publish_vel(0.0, 0.0, 0.0)
        print("    ⚠️ 转向超时")
    
    time.sleep(0.3)
    
    # ========== 阶段2：直线行走到目标位置 ==========
    print("  阶段2: 行走到目标位置...")
    max_walk_time = 90.0
    start_time = time.time()
    
    while time.time() - start_time < max_walk_time:
        current_x, current_y, current_yaw = get_robot_pose()
        if current_x is None:
            time.sleep(0.1)
            continue
        
        # 计算距离
        dx = target_x - current_x
        dy = target_y - current_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < pos_tolerance:
            publish_vel(0.0, 0.0, 0.0)
            print(f"    ✓ 到达位置 (距离={distance:.2f}m)")
            break
        
        # 计算目标方向和角度差
        target_dir = math.atan2(dy, dx)
        angle_diff = normalize_angle(target_dir - current_yaw)
        
        # 速度规划（限制在 SDK 允许范围内 [-0.4, 0.4]）
        vx = 0.4 if distance > 0.3 else 0.3
        
        # 边走边微调方向
        vz = 0.08 if angle_diff > 0 else -0.08
        
        publish_vel(vx, 0.0, vz)
        time.sleep(0.02)
    else:
        publish_vel(0.0, 0.0, 0.0)
        print("    ⚠️ 行走超时")
    
    time.sleep(0.3)
    
    # ========== 阶段3：调整最终朝向 ==========
    print("  阶段3: 调整最终朝向...")
    max_turn_time = 120.0  # 增加超时时间，仿真中转向较慢
    start_time = time.time()
    last_print_time = 0
    
    while time.time() - start_time < max_turn_time:
        current_x, current_y, current_yaw = get_robot_pose()
        if current_x is None:
            time.sleep(0.1)
            continue
        
        # 计算角度差
        angle_diff = normalize_angle(target_yaw - current_yaw)
        
        # 每2秒打印一次状态
        elapsed = time.time() - start_time
        if elapsed - last_print_time > 2.0:
            print(f"    [朝向] 当前yaw={math.degrees(current_yaw):.1f}°, 目标={math.degrees(target_yaw):.1f}°, 差={math.degrees(angle_diff):.1f}°")
            last_print_time = elapsed
        
        if abs(angle_diff) < yaw_tolerance:
            publish_vel(0.0, 0.0, 0.0)
            print(f"    ✓ 朝向调整完成 (误差={math.degrees(angle_diff):.1f}°)")
            time.sleep(0.5)
            print(f"  ✅ 到达目标位置")
            return True
        
        # 速度规划（限制在 SDK 允许范围内 [-0.4, 0.4]）
        turn_speed = 0.4 if abs(angle_diff) > 0.25 else 0.15
        turn_speed = turn_speed if angle_diff > 0 else -turn_speed
        
        publish_vel(0.0, 0.0, turn_speed)
        time.sleep(0.02)
    
    publish_vel(0.0, 0.0, 0.0)
    print("    ⚠️ 朝向调整超时")
    return False

def main():
    global USE_VELOCITY_TURN
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='箱子抓取课程解决方案')
    parser.add_argument('--sim', action='store_true', help='仿真模式 (默认max_yaw_step=90)')
    parser.add_argument('--max-yaw-step', type=float, default=None, help='自定义单步最大转向角度(度)')
    parser.add_argument('--velocity-turn', action='store_true', help='使用速度控制转向(适用于低配电脑)')
    args = parser.parse_args()
    
    # 设置转向模式
    USE_VELOCITY_TURN = args.velocity_turn
    
    # 确定max_yaw_step
    if args.max_yaw_step is not None:
        max_yaw_step = args.max_yaw_step
    else:
        max_yaw_step = 90 if args.sim else 15
    
    mode_str = "速度控制" if USE_VELOCITY_TURN else "步态规划"
    print(f"运行模式: {'仿真' if args.sim else '实物'}, 转向方式: {mode_str}, max_yaw_step={max_yaw_step}°")
    
    # 设置ROS参数
    rospy.set_param('/kuavo_sdk/max_yaw_step', max_yaw_step)
    rospy.set_param('/kuavo_sdk/use_velocity_turn', USE_VELOCITY_TURN)
    
    print("初始化机器人...")
    robot = KuavoRobot()
    robot_state = KuavoRobotState()
    robot_tools = KuavoRobotTools()
    robot_vision = KuavoRobotVision()
    
    grasp_strategy = KuavoGraspBox(robot, robot_state, robot_tools, robot_vision)
    
    # AprilTag目标 - 箱子上的标签
    target_april_tag = AprilTagData(
        id=[0],
        size=[0.088],
        pose=[PoseQuaternion(
            position=(1.5, 0.0, 0.9),
            orientation=(0.0, 0.0, 0.0, 1.0)
        )]
    )
    
    # 放置位置的 AprilTag - 货架上的标签
    placement_april_tag = AprilTagData(
        id=[2],                                 # 放置位置的 AprilTag ID
        size=[0.088],                           # AprilTag 标签尺寸
        pose=[PoseQuaternion(
            position=(-4.0, 0.0, 1.2),          # 基于odom坐标系下的大致位置
            orientation=(0.0, 0.0, 1.0, 0.0)    # 四元数方向 - 旋转180度
        )]
    )
    
    # 备用：固定放置位置 (yaw=180°)，当无法识别AprilTag时使用
    placement_pose = KuavoPose(
        position=(-4.80, 0.0, 0.9),
        orientation=(0.0, 0.0, 1.0, 0.0)
    )
    
    time.sleep(1)
    
    try:
        print("========== 开始执行箱子抓取策略 ==========")
        
        # 步骤1：寻找目标
        print("\n1. 寻找目标箱子...")
        robot.disable_head_tracking()
        
        if USE_VELOCITY_TURN:
            # 速度控制模式：使用头部搜索，不旋转身体
            find_success = grasp_strategy.head_find_target(
                target_april_tag, 
                max_search_time=15.0,
                search_pattern="rotate_head"  # 只用头部搜索，不旋转身体
            )
        else:
            # 步态规划模式：可以旋转身体
            find_success = grasp_strategy.head_find_target(
                target_april_tag, 
                max_search_time=15.0,
                search_pattern="rotate_body"
            )
        
        if not find_success:
            print("❌ 寻找目标失败")
            return
        print("✅ 已找到目标箱子")
        time.sleep(1)

        # 步骤2：走路接近目标
        print("\n2. 走路接近目标...")
        
        if USE_VELOCITY_TURN:
            # 速度控制模式：获取AprilTag位置，用速度控制接近
            # 从视觉获取目标位置
            target_id = target_april_tag.id[0]
            target_data = robot_vision.get_data_by_id_from_odom(target_id)
            
            if target_data and 'poses' in target_data and len(target_data['poses']) > 0:
                tag_pose = target_data['poses'][0]
                
                # 使用与原有方法一致的计算逻辑：
                # 沿着AprilTag的Z轴方向（法线方向）后退target_distance米
                from scipy.spatial.transform import Rotation as R
                
                p_wa = np.array([tag_pose.position.x, tag_pose.position.y, tag_pose.position.z])
                quat_wa = np.array([tag_pose.orientation.x, tag_pose.orientation.y, 
                                   tag_pose.orientation.z, tag_pose.orientation.w])
                R_wa = R.from_quat(quat_wa).as_matrix()
                
                # 计算目标位置：沿AprilTag法线方向后退
                target_distance = GRASP_DISTANCE  # 抓取时与AprilTag的距离(米)
                p_at = np.array([0, 0, target_distance], np.float32)  # AprilTag坐标系下的偏移
                p_at_w = R_wa @ p_at  # 转换到世界坐标系
                p_wt = p_wa + p_at_w  # 最终目标位置
                
                # 计算目标朝向：面向AprilTag
                target_yaw = math.atan2(p_at_w[1], p_at_w[0])
                target_yaw += math.pi  # 转180度，面向AprilTag
                while target_yaw > math.pi:
                    target_yaw -= 2 * math.pi
                while target_yaw < -math.pi:
                    target_yaw += 2 * math.pi
                
                print(f"  AprilTag位置: ({p_wa[0]:.2f}, {p_wa[1]:.2f})")
                print(f"  接近位置: ({p_wt[0]:.2f}, {p_wt[1]:.2f})")
                print(f"  目标朝向: {math.degrees(target_yaw):.1f}°")
                
                approach_success = velocity_walk_to_target(
                    robot, robot_state,
                    p_wt[0], p_wt[1], target_yaw,
                    linear_speed=0.15,
                    angular_speed=0.3,
                    pos_tolerance=0.2
                )
            else:
                print("⚠️ 无法获取目标位置，使用策略模块")
                approach_success = grasp_strategy.walk_approach_target(
                    target_april_tag,
                    target_distance=GRASP_DISTANCE,
                    approach_speed=0.2
                )
        else:
            # 步态规划模式
            approach_success = grasp_strategy.walk_approach_target(
                target_april_tag,
                target_distance=GRASP_DISTANCE,
                approach_speed=0.2
            )
        
        if not approach_success:
            print("❌ 接近目标失败")
            return
        print("✅ 已成功接近目标")
        
        # if not wait_for_confirm("步骤3: 切换stance并移动手臂"):
        #     return

        # 步骤3：切换到stance，准备抓取
        print("\n3. 切换到stance状态...")
        robot.stance()
        if not robot_state.wait_for_stance(timeout=10.0):
            print("⚠️ 等待站稳超时")
            return
        print("✅ 机器人已站稳")
        
        # 移动到安全姿态
        move_arm_to_pose(robot, "safe", duration=2.0)
        
        # if not wait_for_confirm("步骤4: 手臂准备抓取"):
        #     return

        # 步骤4：手臂准备抓取
        print("\n4. 手臂准备抓取...")
        move_arm_to_pose(robot, "pre_grasp", duration=2.0)
        
        # if not wait_for_confirm("步骤5: 抓取箱子"):
        #     return

        # 步骤5：抓取
        print("\n5. 抓取箱子...")
        move_arm_to_pose(robot, "grasp", duration=2.0)
        time.sleep(2.0)  # 等待手臂到位
        # 交互式调整抓取姿态 (调试时启用)
        # if not adjust_grasp_pose(robot):
        #     return
        
        # 调用attach服务 (双手附着)
        print("🤖 执行物理抓取...")
        attach_box("zarm_l7_link", "block", "base_link")
        attach_box("zarm_r7_link", "block", "base_link")

        
        # if not wait_for_confirm("步骤6: 抬起箱子"):
        #     return

        # 步骤6：抬起搬运
        print("\n6. 抬起箱子...")
        move_arm_to_pose(robot, "carry", duration=2.0)
        print("✅ 成功抬起箱子")
        
        # if not wait_for_confirm("步骤7: 走到放置位置"):
        #     return

        # 步骤7：走到放置位置
        print("\n7. 走到放置位置...")
        robot.disable_head_tracking()
        
        # 是否启用放置位置的 AprilTag 识别（设为 False 则直接用固定坐标）
        USE_PLACEMENT_APRILTAG = True
        
        # 中间位置：先走到这里再识别放置位置的 AprilTag
        mid_position = (-2.0, 0.0)  # 中间位置坐标
        
        find_placement_success = False
        if USE_PLACEMENT_APRILTAG:
            # 先走到中间位置
            print(f"  先走到中间位置 ({mid_position[0]}, {mid_position[1]})...")
            
            if USE_VELOCITY_TURN:
                mid_success = velocity_walk_to_target(
                    robot, robot_state,
                    mid_position[0], mid_position[1], math.pi,  # 面向放置位置方向
                    linear_speed=0.15,
                    angular_speed=0.3,
                    pos_tolerance=0.3
                )
            else:
                mid_pose = KuavoPose(
                    position=(mid_position[0], mid_position[1], 0.9),
                    orientation=(0.0, 0.0, 1.0, 0.0)  # yaw=180°
                )
                mid_box_info = BoxInfo(
                    pose=mid_pose,
                    size=(0.3, 0.2, 0.15),
                    mass=0.5
                )
                mid_success = grasp_strategy.walk_to_pose(
                    mid_box_info,
                    target_distance=0.1,
                    approach_speed=0.2,
                )
            
            if mid_success:
                print("  ✅ 已到达中间位置，开始寻找放置位置的 AprilTag...")
                # 到达中间位置后再识别
                find_placement_success = grasp_strategy.head_find_target(
                    placement_april_tag,
                    max_search_time=15.0,
                    search_pattern="rotate_body" if not USE_VELOCITY_TURN else "rotate_head",
                    pitch_angles_deg=[-15, 0],  # 放置位置可能在较高处
                    yaw_angles_deg=[0, -20, 20, -40, 40]
                )
            else:
                print("  ⚠️ 走到中间位置失败")
        
        if find_placement_success:
            print("  ✅ 找到放置位置的 AprilTag")
            
            if USE_VELOCITY_TURN:
                # 速度控制模式：获取AprilTag位置，用速度控制接近
                placement_tag_id = placement_april_tag.id[0]
                placement_data = robot_vision.get_data_by_id_from_odom(placement_tag_id)
                
                if placement_data and 'poses' in placement_data and len(placement_data['poses']) > 0:
                    tag_pose = placement_data['poses'][0]
                    
                    # 计算接近位置
                    from scipy.spatial.transform import Rotation as R
                    
                    p_wa = np.array([tag_pose.position.x, tag_pose.position.y, tag_pose.position.z])
                    quat_wa = np.array([tag_pose.orientation.x, tag_pose.orientation.y, 
                                       tag_pose.orientation.z, tag_pose.orientation.w])
                    R_wa = R.from_quat(quat_wa).as_matrix()
                    
                    # 计算目标位置：沿AprilTag法线方向后退
                    target_distance = PLACE_DISTANCE  # 放置时与AprilTag的距离(米)
                    p_at = np.array([0, 0, target_distance], np.float32)
                    p_at_w = R_wa @ p_at
                    p_wt = p_wa + p_at_w
                    
                    # 计算目标朝向：面向AprilTag
                    target_yaw = math.atan2(p_at_w[1], p_at_w[0])
                    target_yaw += math.pi
                    while target_yaw > math.pi:
                        target_yaw -= 2 * math.pi
                    while target_yaw < -math.pi:
                        target_yaw += 2 * math.pi
                    
                    print(f"  放置AprilTag位置: ({p_wa[0]:.2f}, {p_wa[1]:.2f})")
                    print(f"  接近位置: ({p_wt[0]:.2f}, {p_wt[1]:.2f})")
                    
                    move_success = velocity_walk_to_target(
                        robot, robot_state,
                        p_wt[0], p_wt[1], target_yaw,
                        linear_speed=0.15,
                        angular_speed=0.3,
                        pos_tolerance=0.4
                    )
                else:
                    print("  ⚠️ 无法获取放置位置，使用固定坐标")
                    move_success = velocity_walk_to_target(
                        robot, robot_state,
                        placement_pose.position[0], placement_pose.position[1], math.pi,
                        linear_speed=0.15,
                        angular_speed=0.3,
                        pos_tolerance=0.4
                    )
            else:
                # 步态规划模式：使用 walk_approach_target
                move_success = grasp_strategy.walk_approach_target(
                    placement_april_tag,
                    target_distance=PLACE_DISTANCE,
                    approach_speed=0.2
                )
        else:
            # 未找到AprilTag，使用固定坐标
            print("  ⚠️ 未找到放置位置的 AprilTag，使用固定坐标")
            
            if USE_VELOCITY_TURN:
                target_x = placement_pose.position[0]
                target_y = placement_pose.position[1]
                target_yaw = math.pi  # 180度
                
                move_success = velocity_walk_to_target(
                    robot, robot_state,
                    target_x, target_y, target_yaw,
                    linear_speed=0.15,
                    angular_speed=0.3,
                    pos_tolerance=0.4
                )
            else:
                placement_box_info = BoxInfo(
                    pose=placement_pose,
                    size=(0.3, 0.2, 0.15),
                    mass=0.5
                )
                move_success = grasp_strategy.walk_to_pose(
                    placement_box_info,
                    target_distance=PLACE_DISTANCE,
                    approach_speed=0.2,
                )
        
        if not move_success:
            print("❌ 移动到放置位置失败")
            return
        
        # 到达后切换stance
        robot.stance()
        robot_state.wait_for_stance(timeout=10.0)
        print("✅ 已到达放置位置")
        
        # if not wait_for_confirm("步骤8: 放下箱子"):
        #     return

        # 步骤8：放下箱子
        print("\n8. 放下箱子...")
        move_arm_to_pose(robot, "place", duration=2.0)
        
        # 松开
        move_arm_to_pose(robot, "release", duration=2.0)
        
        # 调用detach服务 (双手分离)
        print("🤖 执行物理释放...")
        detach_box("zarm_l7_link", "block", "base_link")
        detach_box("zarm_r7_link", "block", "base_link")
        
        # 收回手臂
        move_arm_to_pose(robot, "safe", duration=2.0)
        
        print("\n========== 箱子抓取任务完成 ==========")
        
    except Exception as e:
        print(f"执行过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("将机器人恢复到安全姿态...")
        try:
            robot.stance()
            robot_state.wait_for_stance(timeout=5.0)
        except:
            pass

if __name__ == "__main__":
    main()
