#!/usr/bin/env python3
"""
箱子抓取示例 - 支持速度控制和AprilTag识别

用法:
  仿真模式: python3 grasp_box_example.py --sim
  实物模式: python3 grasp_box_example.py
  速度控制模式: python3 grasp_box_example.py --velocity-control

安全须知:
  实物机器人需要用到末端力控制, sim_mode=False
  仿真机器人不需要力控制, sim_mode=True (使用 --sim 参数)
  
注意:
  手臂控制模式已固定为 ArmOnly（身体保持不动，只有手臂运动）
"""
import os
# 禁用日志服务器连接，加快启动速度
os.environ['KUAVO_DISABLE_LOGGER_SERVER'] = '1'

import time
import math
import argparse
import numpy as np
import rospy
import tf2_ros
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from kuavo_humanoid_sdk import KuavoSDK, KuavoRobot, KuavoRobotState, KuavoRobotTools, KuavoRobotVision
from kuavo_humanoid_sdk.common.logger import SDKLogger
from kuavo_humanoid_sdk.interfaces.data_types import KuavoPose, AprilTagData, PoseQuaternion
from kuavo_humanoid_sdk.kuavo_strategy.grasp_box.grasp_box_strategy import KuavoGraspBox, BoxInfo
from kuavo_humanoid_sdk.common.logger import SDKLogger
from scipy.spatial.transform import Rotation as R

# ============== 距离配置 ==============
GRASP_DISTANCE = 0.28    # 抓取时与AprilTag的距离(米)
PLACE_DISTANCE = 0.53    # 放置时与AprilTag的距离(米)

# ============== 中间位置配置 ==============
# 放置位置的AprilTag在后方，需要先走到中间位置再转向识别
MID_POSITION = (-0.5, 0.0)  # 中间位置坐标 (odom坐标系)

# ============== 预设手臂关节位置 (角度制) ==============
# 每个手臂7个关节: [shoulder_pitch, shoulder_roll, shoulder_yaw, elbow, wrist_yaw, wrist_pitch, wrist_roll]
# 左臂(7) + 右臂(7) = 14个关节
ARM_POSES = {
    # 安全收起姿态
    "side": [
        20, 90.8, 0.0, -30, 0.0, 0.0, 0.0,    # 左臂
        20, -90.8, 0.0, -30, -0.0, 0.0, 0.0   # 右臂
    ],
    "safe": [
        7.6, 68.8, 0.0, -90.8, 77.1, 0.0, 0.0,    # 左臂
        7.6, -68.8, 0.0, -90.8, -77.1, 0.0, 0.0   # 右臂
    ],
    # 手臂抬高准备姿态（避免撞到桌子）
    "prepare_high": [
        -35.4, 14.5, -27.7, -51.0, 15.3, 0.0, 0.0,   # 左臂 - 抬高
        -35.4, -14.5, 27.7, -51.0, -15.3, 0.0, 0.0   # 右臂 - 抬高
    ],
    "prepare_high": [
        7.6, 68.8, -25.0, -90.8, 77.1, 0.0, 0.0,    # 左臂
        7.6, -68.8, 25.0, -90.8, -77.1, 0.0, 0.0   # 右臂
    ],
}

# 预设点执行顺序（列表格式保证顺序）
# 可以根据需要添加/删除/调整顺序
ARM_POSE_SEQUENCE = [
    ("side", ARM_POSES["side"]),
    ("safe", ARM_POSES["safe"]),
    # ("prepare_high", ARM_POSES["prepare_high"]),  # 取消注释以启用
]


def normalize_angle(angle):
    """归一化角度到[-pi, pi]"""
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle


def get_robot_pose_from_tf():
    """通过TF获取机器人当前位姿"""
    try:
        tf_buffer = tf2_ros.Buffer()
        tf_listener = tf2_ros.TransformListener(tf_buffer)
        time.sleep(0.3)
        
        transform = tf_buffer.lookup_transform('odom', 'base_link', rospy.Time(0), rospy.Duration(1.0))
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
        SDKLogger.warn(f"获取机器人位姿失败: {e}")
        return None, None, None


def velocity_walk_to_target(robot, target_x, target_y, target_yaw,
                            linear_speed=0.3, angular_speed=0.3,
                            pos_tolerance=0.2, yaw_tolerance=0.1,
                            walk_timeout=180.0):
    """
    使用速度控制行走到目标位置（基于odom坐标系的闭环控制）
    
    三阶段策略：
    1. 先转向目标方向
    2. 直线行走到目标位置（边走边微调）
    3. 最后调整到目标朝向
    
    Args:
        walk_timeout: 阶段2行走的超时时间(秒)，默认15秒
    """
    SDKLogger.info(f"[速度控制行走] 目标: ({target_x:.2f}, {target_y:.2f}), yaw={math.degrees(target_yaw):.1f}°")
    
    # 初始化速度发布器
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.sleep(0.3)  # 等待发布器初始化
    
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
    
    def publish_vel(vx, vy, vz):
        """发布速度命令到 /cmd_vel 话题"""
        cmd_vel_msg = Twist()
        cmd_vel_msg.linear.x = vx
        cmd_vel_msg.linear.y = vy
        cmd_vel_msg.angular.z = vz
        cmd_vel_pub.publish(cmd_vel_msg)
    
    # ========== 阶段1：转向目标方向 ==========
    SDKLogger.info("  阶段1: 转向目标方向...")
    max_turn_time = 180.0
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
            SDKLogger.debug(f"    [转向] 当前yaw={math.degrees(current_yaw):.1f}°, 目标={math.degrees(target_dir):.1f}°, 差={math.degrees(angle_diff):.1f}°")
            last_print_time = elapsed
        
        if abs(angle_diff) < yaw_tolerance:
            SDKLogger.info(f"    ✓ 转向完成 (误差={math.degrees(angle_diff):.1f}°)")
            break
        
        # 改进：平滑的速度规划，避免在阈值附近抖动
        if abs(angle_diff) > 0.35:  # 大角度
            turn_speed = angular_speed
        elif abs(angle_diff) > 0.2:  # 中等角度，线性插值
            turn_speed = angular_speed * 0.5 + (abs(angle_diff) - 0.2) / (0.35 - 0.2) * angular_speed * 0.5
        else:  # 小角度
            turn_speed = angular_speed * 0.5
        
        turn_speed = turn_speed if angle_diff > 0 else -turn_speed
        
        publish_vel(0.0, 0.0, turn_speed)
        time.sleep(0.1)
    else:
        SDKLogger.warn("    ⚠️ 转向超时")
    
    # 改进：保持微小前进速度，避免触发 stance
    SDKLogger.debug("    保持微小速度，准备进入下一阶段...")
    for _ in range(10):  # 持续1秒
        publish_vel(0.05, 0.0, 0.0)  # 0.05 m/s，避免触发 stance
        time.sleep(0.1)
    
    # ========== 阶段2：直线行走到目标位置 ==========
    SDKLogger.info("  阶段2: 行走到目标位置...")
    max_walk_time = walk_timeout
    start_time = time.time()
    last_print_time = 0
    
    while time.time() - start_time < max_walk_time:
        current_x, current_y, current_yaw = get_robot_pose()
        if current_x is None:
            time.sleep(0.1)
            continue
        
        # 计算距离
        dx = target_x - current_x
        dy = target_y - current_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # 计算目标方向和角度差
        target_dir = math.atan2(dy, dx)
        angle_diff = normalize_angle(target_dir - current_yaw)
        
        # 改进：平滑的速度规划，避免突变
        if distance > 0.5:
            vx = linear_speed
        elif distance > 0.35:
            # 线性插值：0.35m→0.7*linear_speed, 0.5m→linear_speed
            vx = linear_speed * 0.7 + (distance - 0.35) / (0.5 - 0.35) * linear_speed * 0.3
        else:
            vx = linear_speed * 0.7
        
        # 改进：角速度死区，避免小角度频繁调整
        if abs(angle_diff) < 0.05:  # 约3°的死区
            vz = 0.0
        elif abs(angle_diff) < 0.15:  # 小角度平滑调整
            vz = 0.1 if angle_diff > 0 else -0.1
        else:  # 大角度快速调整
            vz = 0.15 if angle_diff > 0 else -0.15
        
        # 每0.5秒打印一次详细状态
        elapsed = time.time() - start_time
        if elapsed - last_print_time > 0.5:
            SDKLogger.debug(f"    [行走] pos=({current_x:.2f}, {current_y:.2f}), dist={distance:.2f}m, angle_diff={math.degrees(angle_diff):.1f}°, vx={vx:.2f}, vz={vz:.2f}")
            last_print_time = elapsed
        
        if distance < pos_tolerance:
            SDKLogger.info(f"    ✓ 到达位置 (距离={distance:.2f}m)")
            break
        
        publish_vel(vx, 0.0, vz)
        time.sleep(0.1)
    else:
        SDKLogger.warn("    ⚠️ 行走超时")
    
    # 改进：保持微小前进速度，避免触发 stance
    SDKLogger.debug("    保持微小速度，准备进入下一阶段...")
    for _ in range(10):  # 持续1秒
        publish_vel(0.05, 0.0, 0.0)  # 0.05 m/s，避免触发 stance
        time.sleep(0.1)
    
    # ========== 阶段3：调整最终朝向 ==========
    SDKLogger.info("  阶段3: 调整最终朝向...")
    max_turn_time = 60.0
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
            SDKLogger.debug(f"    [朝向] 当前yaw={math.degrees(current_yaw):.1f}°, 目标={math.degrees(target_yaw):.1f}°, 差={math.degrees(angle_diff):.1f}°")
            last_print_time = elapsed
        
        if abs(angle_diff) < yaw_tolerance:
            SDKLogger.info(f"    ✓ 朝向调整完成 (误差={math.degrees(angle_diff):.1f}°)")
            # 改进：逐渐减速到停止，避免突然触发 stance
            SDKLogger.debug("    逐渐减速停止...")
            for i in range(10):
                speed = 0.05 * (10 - i) / 10  # 从 0.05 逐渐降到 0
                publish_vel(speed, 0.0, 0.0)
                time.sleep(0.1)
            publish_vel(0.0, 0.0, 0.0)
            time.sleep(0.5)
            SDKLogger.info(f"  ✅ 到达目标位置")
            return True
        
        # 改进：平滑的速度规划，避免在阈值附近抖动
        if abs(angle_diff) > 0.35:  # 大角度
            turn_speed = angular_speed
        elif abs(angle_diff) > 0.2:  # 中等角度，线性插值
            turn_speed = angular_speed * 0.5 + (abs(angle_diff) - 0.2) / (0.35 - 0.2) * angular_speed * 0.5
        else:  # 小角度
            turn_speed = angular_speed * 0.5
        
        turn_speed = turn_speed if angle_diff > 0 else -turn_speed
        
        publish_vel(0.0, 0.0, turn_speed)
        time.sleep(0.1)
    
    # 超时情况也要逐渐减速
    SDKLogger.warn("    ⚠️ 朝向调整超时，逐渐减速停止...")
    for i in range(10):
        speed = 0.05 * (10 - i) / 10
        publish_vel(speed, 0.0, 0.0)
        time.sleep(0.1)
    publish_vel(0.0, 0.0, 0.0)
    return False


def calculate_approach_pose_from_apriltag(tag_pose, target_distance):
    """
    根据AprilTag位姿计算接近位置
    """
    p_wa = np.array([tag_pose.position.x, tag_pose.position.y, tag_pose.position.z])
    quat_wa = np.array([tag_pose.orientation.x, tag_pose.orientation.y,
                        tag_pose.orientation.z, tag_pose.orientation.w])
    R_wa = R.from_quat(quat_wa).as_matrix()
    
    # 计算目标位置：沿AprilTag法线方向后退
    p_at = np.array([0, 0, target_distance], np.float32)
    p_at_w = R_wa @ p_at
    p_wt = p_wa + p_at_w
    
    # 计算目标朝向：面向AprilTag
    target_yaw = math.atan2(p_at_w[1], p_at_w[0])
    target_yaw += math.pi  # 转180度，面向AprilTag
    target_yaw = normalize_angle(target_yaw)
    
    return p_wt[0], p_wt[1], target_yaw


def velocity_backward(robot, distance=0.5, linear_speed=0.2, tolerance=0.05):
    """
    基于odom闭环控制后退指定距离
    """
    SDKLogger.info(f"  [闭环后退] 目标距离: {distance:.2f}m")
    
    # 初始化速度发布器
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.sleep(0.3)  # 等待发布器初始化
    
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
            return x, y
        except Exception as e:
            return None, None
    
    def publish_vel(vx, vy, vz):
        """发布速度命令到 /cmd_vel 话题"""
        cmd_vel_msg = Twist()
        cmd_vel_msg.linear.x = vx
        cmd_vel_msg.linear.y = vy
        cmd_vel_msg.angular.z = vz
        cmd_vel_pub.publish(cmd_vel_msg)
    
    # 获取起始位置
    start_x, start_y = get_robot_pose()
    if start_x is None:
        SDKLogger.warn("  ⚠️ 无法获取起始位置")
        return False
    
    SDKLogger.debug(f"    起始位置: ({start_x:.2f}, {start_y:.2f})")
    
    max_time = 30.0
    start_time = time.time()
    last_print_time = 0
    
    while time.time() - start_time < max_time:
        current_x, current_y = get_robot_pose()
        if current_x is None:
            time.sleep(0.1)
            continue
        
        # 计算已后退距离
        dx = current_x - start_x
        dy = current_y - start_y
        moved_distance = math.sqrt(dx*dx + dy*dy)
        
        # 每2秒打印一次状态
        elapsed = time.time() - start_time
        if elapsed - last_print_time > 2.0:
            SDKLogger.debug(f"    [后退] 已移动: {moved_distance:.2f}m, 目标: {distance:.2f}m")
            last_print_time = elapsed
        
        # 检查是否到达目标距离
        if moved_distance >= distance - tolerance:
            publish_vel(0.0, 0.0, 0.0)
            time.sleep(0.3)
            SDKLogger.info(f"    ✓ 后退完成 (实际距离={moved_distance:.2f}m)")
            return True
        
        # 后退（负速度）
        publish_vel(-linear_speed, 0.0, 0.0)
        time.sleep(0.02)
    
    # 超时停止
    publish_vel(0.0, 0.0, 0.0)
    SDKLogger.warn("    ⚠️ 后退超时")
    return False


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='箱子抓取示例')
    parser.add_argument('--sim', action='store_true', help='仿真模式')
    parser.add_argument('--velocity-control', action='store_true', help='使用速度控制模式')
    parser.add_argument('--wait-for-bottle', action='store_true', help='等待抓水瓶任务完成信号后再开始')
    args = parser.parse_args()
    
    use_velocity_control = args.velocity_control
    sim_mode = args.sim
    
    mode_str = "速度控制" if use_velocity_control else "单步控制"
    
    SDKLogger.info(f"运行模式: {'仿真' if sim_mode else '实物'}, 行走方式: {mode_str}")
    SDKLogger.info(f"手臂模式: ArmOnly（身体保持不动）")
    
    # 初始化SDK
    SDKLogger.info("正在初始化 SDK...")
    init_start = time.time()
    if not KuavoSDK().Init():
        SDKLogger.error("Init KuavoSDK failed, exit!")
        exit(1)
    SDKLogger.info(f"✅ SDK 初始化完成 (耗时: {time.time()-init_start:.2f}秒)")
    
    SDKLogger.info("正在初始化机器人组件...")
    components_start = time.time()
    # 初始化机器人及相关组件
    robot = KuavoRobot()
    robot_state = KuavoRobotState()
    robot_tools = KuavoRobotTools()
    robot_vision = KuavoRobotVision()
    SDKLogger.info(f"✅ 机器人组件初始化完成 (耗时: {time.time()-components_start:.2f}秒)")
    
    # 初始化箱子抓取策略
    SDKLogger.info("正在初始化抓取策略...")
    strategy_start = time.time()
    grasp_strategy = KuavoGraspBox(robot, robot_state, robot_tools, robot_vision)
    SDKLogger.info(f"✅ 抓取策略初始化完成 (耗时: {time.time()-strategy_start:.2f}秒)")
    
    # ============== 箱子配置 ==============
    # 箱子尺寸 (宽, 长, 高) 单位：米
    box_size = (0.3, 0.4, 0.22)
    box_mass = 1.5  # 箱子质量，单位：千克
    
    # 创建AprilTag数据对象 - 箱子上的标签
    target_april_tag = AprilTagData(
        id=[1],  # AprilTag ID
        size=[0.1],  # AprilTag 标签尺寸
        pose=[PoseQuaternion(
            position=(1.0, 0.0, 0.8),  # 基于odom坐标系下的大致位置
            orientation=(0.0, 0.0, 0.0, 1.0)  # 四元数方向
        )]
    )
    
    # 创建放置位置的AprilTag数据对象
    placement_april_tag = AprilTagData(
        id=[2],  # 放置位置的AprilTag ID
        size=[0.1],  # AprilTag 标签尺寸
        pose=[PoseQuaternion(
            position=(-1.0, 0.0, 0.8),  # 放置位置的大致坐标
            orientation=(0.0, 0.0, 1.0, 0.0)    # 四元数方向 - 旋转180度
        )]
    )
    
    # 备用：固定放置位置，当无法识别AprilTag时使用
    placement_pose = KuavoPose(
        position=(0.5, 0.0, 0.8),  # 目标放置位置坐标（机器人正前方0.5m）
        orientation=(0.0, 0.0, 0.0, 1.0)  # 目标放置方向（四元数）yaw=0°
    )
    
    time.sleep(1)
    
    # ============== 等待抓水瓶任务完成信号 ==============
    # 如果设置了 --wait-for-bottle 参数，则等待抓水瓶任务完成的信号
    if hasattr(args, 'wait_for_bottle') and args.wait_for_bottle:
        SDKLogger.info("=" * 60)
        SDKLogger.info("⏳ 等待抓水瓶任务完成信号...")
        SDKLogger.info("提示: 抓水瓶程序完成后会发布 /bottle_task_done 话题")
        SDKLogger.info("=" * 60)
        
        try:
            from std_msgs.msg import Bool
            # 等待抓水瓶任务完成信号（最多等待300秒=5分钟）
            msg = rospy.wait_for_message('/bottle_task_done', Bool, timeout=300.0)
            if msg.data:
                SDKLogger.info("✅ 收到抓水瓶任务完成信号，开始搬箱子任务")
            else:
                SDKLogger.warn("⚠️ 收到抓水瓶任务失败信号，但仍继续搬箱子任务")
        except rospy.ROSException:
            SDKLogger.warn("⚠️ 等待抓水瓶任务信号超时，继续执行搬箱子任务")
        except Exception as e:
            SDKLogger.error(f"❌ 等待信号时发生错误: {e}")
            return
    
    # 执行完整抓取策略
    try:
        SDKLogger.info("========== 开始执行箱子抓取策略 ==========")
        
        # !!! Important: 关闭 basePitch 限制, 否则无法进行大幅度的前后倾动作
        SDKLogger.info("⚠️ 重要提示: 关闭 basePitch 限制...")
        grasp_strategy.robot.enable_base_pitch_limit(False)
        # 检查 pitch limit 状态
        for i in range(3):
            if not robot_state.pitch_limit_enabled():
                SDKLogger.info("✅ 已关闭 basePitch 限制")
                break
            else:
                if i < 2:
                    SDKLogger.info(f"⚠️ 第{i+1}次检查 basePitch 限制状态...")
                time.sleep(0.5)
        else:
            SDKLogger.warn("⚠️ 关闭 basePitch 限制失败，继续执行...")
        
        # 步骤1：使用头部寻找目标
        SDKLogger.info("1. 寻找目标箱子...")
        grasp_strategy.robot.disable_head_tracking()
        SDKLogger.info("✅ 已关闭头部追踪")
        
        find_success = grasp_strategy.head_find_target(
            target_april_tag, 
            max_search_time=15.0,
            search_pattern="rotate_body" if not use_velocity_control else "rotate_head"
        )
        
        if not find_success:
            SDKLogger.error("❌ 寻找目标失败，无法继续执行")
            return
        
        SDKLogger.info("✅ 已找到目标箱子")
        time.sleep(1)  # 等待识别稳定
        
        # 从AprilTag获取箱子位置信息
        target_id = target_april_tag.id[0]
        box_tag_data = robot_vision.get_data_by_id_from_odom(target_id)
        if not box_tag_data:
            SDKLogger.error(f"❌ 未识别到 AprilTag ID 为 {target_id} 的目标箱子")
            return
        
        SDKLogger.debug(f"box_tag_data: {box_tag_data}")
        
        # 从AprilTag动态创建BoxInfo
        box_info = BoxInfo.from_apriltag(
            box_tag_data,
            xyz_offset=(box_size[0]/2 + 0.03, 0.0, -0.06),  # tag粘贴在箱子正面，偏移到箱子中心
            size=box_size,
            mass=box_mass
        )
        SDKLogger.info(f"box_info: {box_info}")
        
        # 步骤2：走路接近目标
        SDKLogger.info("2. 走路接近目标...")
        
        if use_velocity_control:
            # 速度控制模式：获取AprilTag位置，用速度控制接近
            target_data = robot_vision.get_data_by_id_from_odom(target_id)
            
            if target_data and 'poses' in target_data and len(target_data['poses']) > 0:
                tag_pose = target_data['poses'][0]
                target_x, target_y, target_yaw = calculate_approach_pose_from_apriltag(
                    tag_pose, GRASP_DISTANCE
                )
                
                SDKLogger.info(f"  AprilTag位置: ({tag_pose.position.x:.2f}, {tag_pose.position.y:.2f})")
                SDKLogger.info(f"  接近位置: ({target_x:.2f}, {target_y:.2f})")
                SDKLogger.info(f"  目标朝向: {math.degrees(target_yaw):.1f}°")
                
                approach_success = velocity_walk_to_target(
                    robot, target_x, target_y, target_yaw,
                    linear_speed=0.3,
                    angular_speed=0.3,
                    pos_tolerance=0.2
                )
            else:
                SDKLogger.warn("⚠️ 无法获取目标位置，使用策略模块")
                approach_success = grasp_strategy.walk_approach_target(
                    target_id,
                    target_distance=GRASP_DISTANCE,
                    approach_speed=0.2
                )
        else:
            # 单步控制模式
            approach_success = grasp_strategy.walk_approach_target(
                target_id,
                target_distance=GRASP_DISTANCE,
                approach_speed=0.2
            )
        
        if not approach_success:
            SDKLogger.error("❌ 接近目标失败，无法继续执行")
            return
            
        SDKLogger.info("✅ 已成功接近目标")
        time.sleep(1)
        
        # 步骤3：手臂移动到抓取位置
        SDKLogger.info("3. 手臂移动到抓取位置...")
        
        # 使用 ARM_POSE_SEQUENCE 列表，按顺序执行预设点
        move_success = grasp_strategy.arm_move_to_target(
            box_info,
            preset_poses=ARM_POSE_SEQUENCE
        )
        
        if not move_success:
            SDKLogger.error("❌ 手臂移动失败，无法继续执行")
            return
            
        SDKLogger.info("✅ 手臂已到达抓取位置")
        time.sleep(1.0)
        
        # 步骤4：提起箱子
        SDKLogger.info("4. 提起箱子...")
        transport_up_success = grasp_strategy.arm_transport_target_up(
            box_info,
            sim_mode=sim_mode
        )
        
        if not transport_up_success:
            SDKLogger.error("❌ 提起箱子失败")
            return
        time.sleep(1.0)
            
        SDKLogger.info("✅ 成功提起箱子")
        time.sleep(1.0)

        # 步骤5：关闭头部追踪
        SDKLogger.info("5. 关闭头部追踪...")
        grasp_strategy.robot.disable_head_tracking()
        SDKLogger.info("✅ 已关闭头部追踪")
        time.sleep(1.0)

        # 步骤6：寻找放置位置的AprilTag并移动
        SDKLogger.info("6. 寻找放置位置并移动...")
        
        # 先走到中间位置
        SDKLogger.info(f"  先走到中间位置 ({MID_POSITION[0]}, {MID_POSITION[1]})...")
        
        if use_velocity_control:
            mid_success = velocity_walk_to_target(
                robot,
                MID_POSITION[0], MID_POSITION[1], math.pi,
                linear_speed=0.15,  # 搬箱子时的速度
                angular_speed=0.2,
                pos_tolerance=0.2,  # 搬箱子时精度要求不高，避免边界震荡
                walk_timeout=15.0  # 中间位置超时时间短一些
            )
        else:
            mid_pose = KuavoPose(
                position=(MID_POSITION[0], MID_POSITION[1], 0.9),
                orientation=(0.0, 0.0, 1.0, 0.0)
            )
            mid_success = grasp_strategy.walk_to_pose(
                mid_pose,
                target_distance=0.1,
                approach_speed=0.2,
            )
        
        if not mid_success:
            SDKLogger.warn("  ⚠️ 走到中间位置失败，尝试使用固定坐标")
        else:
            SDKLogger.info("  ✅ 已到达中间位置，开始寻找放置位置的AprilTag...")
        
        # 到达中间位置后再识别放置位置的AprilTag
        find_placement_success = False
        saved_placement_tag_data = None  # 保存AprilTag数据供步骤7使用
        if mid_success:
            find_placement_success = grasp_strategy.head_find_target(
                placement_april_tag,
                max_search_time=15.0,
                search_pattern="rotate_body" if not use_velocity_control else "rotate_head",
            )
        
        if find_placement_success:
            SDKLogger.info("  ✅ 找到放置位置的AprilTag")
            
            # 等待视觉系统稳定，确保位置数据更新
            SDKLogger.info("  等待视觉数据稳定...")
            time.sleep(2.0)  # 增加到2秒
            
            if use_velocity_control:
                placement_tag_id = placement_april_tag.id[0]
                
                # 多次尝试获取数据
                placement_data = None
                for attempt in range(3):
                    placement_data = robot_vision.get_data_by_id_from_odom(placement_tag_id)
                    SDKLogger.debug(f"  尝试{attempt+1}: placement_data = {placement_data}")
                    
                    if placement_data and 'poses' in placement_data and len(placement_data['poses']) > 0:
                        saved_placement_tag_data = placement_data  # 保存数据
                        break
                    time.sleep(0.5)
                
                if placement_data and 'poses' in placement_data and len(placement_data['poses']) > 0:
                    tag_pose = placement_data['poses'][0]
                    target_x, target_y, target_yaw = calculate_approach_pose_from_apriltag(
                        tag_pose, PLACE_DISTANCE
                    )
                    
                    SDKLogger.info(f"  放置AprilTag位置: ({tag_pose.position.x:.2f}, {tag_pose.position.y:.2f})")
                    SDKLogger.info(f"  接近位置: ({target_x:.2f}, {target_y:.2f})")
                    
                    move_success = velocity_walk_to_target(
                        robot, target_x, target_y, target_yaw,
                        linear_speed=0.15,  # 搬箱子时的速度
                        angular_speed=0.2,
                        pos_tolerance=0.3
                    )
                else:
                    SDKLogger.warn("  ⚠️ 无法获取放置位置，使用固定坐标")
                    qx, qy, qz, qw = placement_pose.orientation
                    target_yaw = math.atan2(2 * (qw * qz + qx * qy), 1 - 2 * (qy**2 + qz**2))
                    move_success = velocity_walk_to_target(
                        robot,
                        placement_pose.position[0],
                        placement_pose.position[1],
                        target_yaw,
                        linear_speed=0.15,  # 搬箱子时的速度
                        angular_speed=0.2,
                        pos_tolerance=0.3
                    )
            else:
                move_success = grasp_strategy.walk_approach_target(
                    placement_april_tag.id[0],
                    target_distance=PLACE_DISTANCE,
                    approach_speed=0.2
                )
        else:
            SDKLogger.warn("  ⚠️ 未找到放置位置的AprilTag，使用固定坐标")
            
            if use_velocity_control:
                qx, qy, qz, qw = placement_pose.orientation
                target_yaw = math.atan2(2 * (qw * qz + qx * qy), 1 - 2 * (qy**2 + qz**2))
                
                move_success = velocity_walk_to_target(
                    robot,
                    placement_pose.position[0],
                    placement_pose.position[1],
                    target_yaw,
                    linear_speed=0.15,  # 搬箱子时降低速度
                    angular_speed=0.2,
                    pos_tolerance=0.3
                )
            else:
                move_success = grasp_strategy.walk_to_pose(
                    placement_pose,
                    target_distance=PLACE_DISTANCE,
                    approach_speed=0.2,
                )
        
        if not move_success:
            SDKLogger.error("❌ 移动到放置位置失败")
            return
        SDKLogger.info("✅ 已到达放置位置")
        time.sleep(1.0)

        # 步骤7：放下箱子
        SDKLogger.info("7. 放下箱子...")
        
        # 放置位置使用机器人当前位置前方的相对位置
        # 获取机器人当前位姿
        current_x, current_y, current_yaw = get_robot_pose_from_tf()
        if current_x is not None:
            # 计算机器人前方0.4m处的放置位置
            place_distance = 0.4
            place_x = current_x + place_distance * math.cos(current_yaw)
            place_y = current_y + place_distance * math.sin(current_yaw)
            place_z = 0.8  # 放置高度
            
            # 创建放置位置的BoxInfo
            placement_box_info = BoxInfo(
                pose=KuavoPose(
                    position=(place_x, place_y, place_z),
                    orientation=(0.0, 0.0, math.sin(current_yaw/2), math.cos(current_yaw/2))
                ),
                size=box_size,
                mass=box_mass
            )
            SDKLogger.info(f"  放置位置: ({place_x:.2f}, {place_y:.2f}, {place_z:.2f})")
        else:
            SDKLogger.warn("⚠️ 无法获取机器人位姿，使用固定坐标")
            placement_box_info = BoxInfo(
                pose=placement_pose,
                size=box_size,
                mass=box_mass
            )
        
        transport_down_success = grasp_strategy.arm_transport_target_down(
            placement_box_info
        )
        
        if not transport_down_success:
            SDKLogger.error("❌ 放下箱子失败")
            return
            
        SDKLogger.info("✅ 成功放下箱子")
        time.sleep(1.0)
        
        SDKLogger.info("========== 箱子抓取任务完成 ==========")
        
    except Exception as e:
        SDKLogger.error(f"执行过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        SDKLogger.info("将机器人恢复到安全姿态...")


if __name__ == "__main__":
    main()
