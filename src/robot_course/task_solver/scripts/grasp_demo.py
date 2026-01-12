#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抓取放置演示程序
机器人导航到抓取区 -> 抓取物体 -> 导航到放置区 -> 放置物体

通过ROS服务调用grasp_controller实现抓取/放置

位置判断方式：
1. odom - 通过odom话题判断机器人位置
2. gazebo - 通过Gazebo真实值判断位置
3. apriltag - 通过AprilTag二维码定位物品位置

机器人控制：cmd_vel
"""

import rospy
import math
import time
import json
import argparse
import numpy as np
from enum import Enum

from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry
from std_msgs.msg import String

# 抓取服务
from task_solver.srv import GraspObject, GraspObjectRequest
from task_solver.srv import PlaceObject, PlaceObjectRequest
from task_solver.srv import ResetArm, ResetArmRequest

# AprilTag检测
try:
    from apriltag_ros.msg import AprilTagDetectionArray
    from scipy.spatial.transform import Rotation as R
    HAS_APRILTAG = True
except ImportError:
    HAS_APRILTAG = False
    rospy.logwarn("apriltag_ros 未安装，AprilTag定位不可用")

# TF2用于坐标变换
import tf2_ros
import tf2_geometry_msgs

# Gazebo服务
try:
    from gazebo_msgs.srv import GetModelState, GetModelStateRequest
    HAS_GAZEBO = True
except ImportError:
    HAS_GAZEBO = False


class TaskState(Enum):
    """任务状态"""
    IDLE = 0
    NAV_TO_GRASP = 1      # 导航到抓取区
    GRASPING = 2          # 抓取中
    NAV_TO_PLACE = 3      # 导航到放置区
    PLACING = 4           # 放置中
    DONE = 5              # 完成


class GraspServiceClient:
    """抓取服务客户端 - 通过ROS服务调用grasp_controller"""
    
    def __init__(self):
        self.grasp_srv_name = '/grasp_controller/grasp'
        self.place_srv_name = '/grasp_controller/place'
        self.reset_arm_srv_name = '/grasp_controller/reset_arm'
        
        # 等待服务可用
        rospy.loginfo("等待抓取服务...")
        rospy.wait_for_service(self.grasp_srv_name, timeout=30.0)
        rospy.wait_for_service(self.place_srv_name, timeout=30.0)
        rospy.wait_for_service(self.reset_arm_srv_name, timeout=30.0)
        rospy.loginfo("抓取服务已连接")
        
        self.grasp_srv = rospy.ServiceProxy(self.grasp_srv_name, GraspObject)
        self.place_srv = rospy.ServiceProxy(self.place_srv_name, PlaceObject)
        self.reset_arm_srv = rospy.ServiceProxy(self.reset_arm_srv_name, ResetArm)
        
        # 当前状态
        self.grasped_hand = None
    
    def grasp(self, target_class, track_id=-1, grasp_only=True, hand="right"):
        """
        调用抓取服务
        :param target_class: 目标类别 'cup'/'plate'/'scissors'
        :param track_id: 指定track_id (-1表示自动选择最近的)
        :param grasp_only: True只抓取不释放, False抓取后释放
        :param hand: 指定使用的手 "left"/"right"/"auto"，默认"right"
        :return: (success, track_id, hand)
        """
        try:
            req = GraspObjectRequest()
            req.target_class = target_class
            req.track_id = track_id
            req.grasp_only = grasp_only
            req.hand = hand
            
            rospy.loginfo(f"[GraspClient] 调用抓取服务: {target_class}, hand={hand}")
            resp = self.grasp_srv(req)
            
            if resp.success:
                self.grasped_hand = resp.grasped_hand
                rospy.loginfo(f"[GraspClient] 抓取成功: {resp.message}")
            else:
                rospy.logwarn(f"[GraspClient] 抓取失败: {resp.message}")
            
            return resp.success, resp.grasped_track_id, resp.grasped_hand
        
        except rospy.ServiceException as e:
            rospy.logerr(f"[GraspClient] 服务调用失败: {e}")
            return False, -1, ""
    
    def place(self, hand="", reset_arm=True):
        """
        调用放置服务
        :param hand: 使用的手 "left"/"right"，空字符串表示自动
        :param reset_arm: 是否复位手臂，False时只释放物体不复位
        :return: success
        """
        try:
            req = PlaceObjectRequest()
            req.hand = hand if hand else (self.grasped_hand or "")
            req.reset_arm = reset_arm
            
            rospy.loginfo(f"[GraspClient] 调用放置服务: hand={req.hand}, reset_arm={reset_arm}")
            resp = self.place_srv(req)
            
            if resp.success:
                if reset_arm:
                    self.grasped_hand = None
                rospy.loginfo(f"[GraspClient] 放置成功: {resp.message}")
            else:
                rospy.logwarn(f"[GraspClient] 放置失败: {resp.message}")
            
            return resp.success
        
        except rospy.ServiceException as e:
            rospy.logerr(f"[GraspClient] 服务调用失败: {e}")
            return False
    
    def reset_arm(self, hand=""):
        """
        调用手臂复位服务 (放置后后退再调用)
        :param hand: 使用的手 "left"/"right"
        :return: success
        """
        try:
            req = ResetArmRequest()
            req.hand = hand if hand else (self.grasped_hand or "")
            
            rospy.loginfo(f"[GraspClient] 调用手臂复位服务: hand={req.hand}")
            resp = self.reset_arm_srv(req)
            
            if resp.success:
                self.grasped_hand = None
                rospy.loginfo(f"[GraspClient] 手臂复位成功: {resp.message}")
            else:
                rospy.logwarn(f"[GraspClient] 手臂复位失败: {resp.message}")
            
            return resp.success
        
        except rospy.ServiceException as e:
            rospy.logerr(f"[GraspClient] 服务调用失败: {e}")
            return False


class PositionTracker:
    """位置追踪器 - 支持多种位置判断方式"""
    
    def __init__(self, mode='odom', robot_model='biped_s42'):
        """
        :param mode: 'odom', 'gazebo'
        :param robot_model: Gazebo中机器人模型名称
        """
        self.mode = mode
        self.robot_model = robot_model
        
        # 当前位置
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0
        
        if mode == 'odom':
            self.odom_sub = rospy.Subscriber('/odom', Odometry, self._odom_callback, queue_size=1)
        elif mode == 'gazebo':
            if HAS_GAZEBO:
                rospy.wait_for_service('/gazebo/get_model_state')
                self.get_model_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
            else:
                rospy.logerr("Gazebo服务不可用")
        
        rospy.loginfo(f"[PositionTracker] 模式: {mode}")
    
    def _odom_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        # 从四元数计算yaw
        q = msg.pose.pose.orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        self.current_yaw = math.atan2(siny_cosp, cosy_cosp)
    
    def get_position(self):
        """获取当前位置 (x, y, yaw)"""
        if self.mode == 'gazebo' and HAS_GAZEBO:
            try:
                req = GetModelStateRequest()
                req.model_name = self.robot_model
                req.relative_entity_name = 'world'
                resp = self.get_model_state(req)
                if resp.success:
                    self.current_x = resp.pose.position.x
                    self.current_y = resp.pose.position.y
                    q = resp.pose.orientation
                    siny_cosp = 2 * (q.w * q.z + q.x * q.y)
                    cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
                    self.current_yaw = math.atan2(siny_cosp, cosy_cosp)
            except Exception as e:
                rospy.logwarn(f"获取Gazebo位置失败: {e}")
        
        return self.current_x, self.current_y, self.current_yaw
    
    def distance_to(self, target_x, target_y):
        """计算到目标点的距离"""
        x, y, _ = self.get_position()
        return math.sqrt((target_x - x)**2 + (target_y - y)**2)
    
    def is_at_position(self, target_x, target_y, tolerance=0.1):
        """判断是否到达目标位置"""
        return self.distance_to(target_x, target_y) < tolerance


class RobotController:
    """机器人运动控制器"""
    
    def __init__(self):
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rospy.sleep(0.5)
    
    def move(self, linear_x, linear_y, angular_z):
        """发送速度指令 (支持全向移动)"""
        twist = Twist()
        twist.linear.x = linear_x
        twist.linear.y = linear_y
        twist.angular.z = angular_z
        self.cmd_vel_pub.publish(twist)
    
    def stop(self):
        """停止"""
        self.move(0, 0, 0)
    
    def move_backward(self, distance, speed=0.1, tracker=None, tolerance=0.05):
        """
        后退指定距离（闭环控制，基于已走距离）
        :param distance: 后退距离(m)
        :param speed: 后退速度(m/s)
        :param tracker: 位置追踪器，用于闭环控制
        :param tolerance: 到达容差(m)
        """
        rospy.loginfo(f"后退 {distance}m...")
        
        if tracker is None:
            # 无tracker时使用开环控制（时间控制）
            duration = distance / speed
            start_time = time.time()
            rate = rospy.Rate(10)
            
            while not rospy.is_shutdown() and (time.time() - start_time < duration):
                self.move(-speed, 0, 0)
                rate.sleep()
            
            self.stop()
            rospy.loginfo("后退完成 (开环)")
            return True
        
        # 闭环控制：基于已走距离判断
        start_x, start_y, _ = tracker.get_position()
        
        rospy.loginfo(f"  起点: ({start_x:.2f}, {start_y:.2f}), 目标距离: {distance}m")
        
        rate = rospy.Rate(50)
        last_print_time = 0
        start_time = time.time()
        
        while not rospy.is_shutdown():
            x, y, _ = tracker.get_position()
            
            # 计算已走距离（从起点到当前位置）
            traveled = math.sqrt((x - start_x)**2 + (y - start_y)**2)
            remaining = distance - traveled
            
            # 每2秒打印一次状态
            elapsed = time.time() - start_time
            if elapsed - last_print_time > 2.0:
                rospy.loginfo(f"    [后退] 当前({x:.2f}, {y:.2f}), 已走={traveled:.2f}m, 剩余={remaining:.2f}m")
                last_print_time = elapsed
            
            if remaining < tolerance:
                self.stop()
                rospy.loginfo(f"  ✓ 后退完成 (已走={traveled:.2f}m)")
                return True
            
            # 速度规划：接近目标时减速
            actual_speed = speed if remaining > 0.3 else speed * 0.7
            
            self.move(-actual_speed, 0, 0)
            rate.sleep()
        
        self.stop()
        return False
    
    def move_lateral(self, tracker, target_x, target_y, speed=0.1, tolerance=0.1):
        """
        左右平移到目标点 (保持朝向不变)
        :return: True if reached
        """
        rate = rospy.Rate(10)
        
        while not rospy.is_shutdown():
            x, y, yaw = tracker.get_position()
            
            # 计算到目标的距离
            dx = target_x - x
            dy = target_y - y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < tolerance:
                self.stop()
                rospy.loginfo(f"到达目标 ({target_x:.2f}, {target_y:.2f})")
                return True
            
            # 将世界坐标系的位移转换到机器人坐标系
            # 机器人坐标系: x前, y左
            cos_yaw = math.cos(yaw)
            sin_yaw = math.sin(yaw)
            
            # 机器人坐标系下的目标位移
            local_x = dx * cos_yaw + dy * sin_yaw   # 前后方向
            local_y = -dx * sin_yaw + dy * cos_yaw  # 左右方向
            
            # 归一化速度，接近目标时减速
            local_dist = math.sqrt(local_x**2 + local_y**2)
            actual_speed = min(speed, local_dist * 0.5)  # 接近时减速
            actual_speed = max(actual_speed, 0.03)  # 最小速度
            
            if local_dist > 0:
                vx = actual_speed * local_x / local_dist
                vy = actual_speed * local_y / local_dist
            else:
                vx, vy = 0, 0
            
            self.move(vx, vy, 0)
            rate.sleep()
        
        return False
    
    def move_to(self, tracker, target_x, target_y, linear_speed=0.15, angular_speed=0.3, 
                tolerance=0.1, yaw_tolerance=0.1, target_yaw=None):
        """
        三阶段移动到目标点（参考grasp_box_course_solver）
        1. 先转向目标方向
        2. 直线行走到目标位置（边走边微调）
        3. 最后调整到目标朝向
        
        :param tracker: 位置追踪器
        :param target_x, target_y: 目标位置(odom坐标系)
        :param linear_speed: 线速度(m/s)
        :param angular_speed: 角速度(rad/s)
        :param tolerance: 位置容差(米)
        :param yaw_tolerance: 角度容差(弧度)
        :param target_yaw: 最终朝向(弧度)，None表示面向目标方向
        :return: True if reached
        """
        rospy.loginfo(f"[移动] 目标: ({target_x:.2f}, {target_y:.2f})")
        
        def normalize_angle(angle):
            """归一化角度到[-pi, pi]"""
            while angle > math.pi:
                angle -= 2 * math.pi
            while angle < -math.pi:
                angle += 2 * math.pi
            return angle
        
        rate = rospy.Rate(50)  # 50Hz控制频率
        
        # ========== 阶段1：转向目标方向 ==========
        rospy.loginfo("  阶段1: 转向目标方向...")
        max_turn_time = 60.0
        start_time = time.time()
        last_print_time = 0
        
        while not rospy.is_shutdown() and (time.time() - start_time < max_turn_time):
            x, y, yaw = tracker.get_position()
            
            # 计算目标方向
            dx = target_x - x
            dy = target_y - y
            target_dir = math.atan2(dy, dx)
            
            # 计算角度差
            angle_diff = normalize_angle(target_dir - yaw)
            
            # 每2秒打印一次状态
            elapsed = time.time() - start_time
            if elapsed - last_print_time > 2.0:
                rospy.loginfo(f"    [转向] 当前yaw={math.degrees(yaw):.1f}°, 目标={math.degrees(target_dir):.1f}°, 差={math.degrees(angle_diff):.1f}°")
                last_print_time = elapsed
            
            if abs(angle_diff) < yaw_tolerance:
                self.stop()
                rospy.loginfo(f"    ✓ 转向完成 (误差={math.degrees(angle_diff):.1f}°)")
                break
            
            # 速度规划
            turn_speed = angular_speed if abs(angle_diff) > 0.25 else angular_speed * 0.5
            turn_speed = turn_speed if angle_diff > 0 else -turn_speed
            
            self.move(0, 0, turn_speed)
            rate.sleep()
        else:
            self.stop()
            rospy.logwarn("    ⚠️ 转向超时")
        
        time.sleep(0.3)
        
        # ========== 阶段2：直线行走到目标位置 ==========
        rospy.loginfo("  阶段2: 行走到目标位置...")
        start_time = time.time()
        last_print_time = 0
        
        while not rospy.is_shutdown():
            x, y, yaw = tracker.get_position()
            
            # 计算距离
            dx = target_x - x
            dy = target_y - y
            distance = math.sqrt(dx**2 + dy**2)
            
            # 每2秒打印一次状态
            elapsed = time.time() - start_time
            if elapsed - last_print_time > 2.0:
                rospy.loginfo(f"    [行走] 当前({x:.2f}, {y:.2f}), 距离={distance:.2f}m")
                last_print_time = elapsed
            
            if distance < tolerance:
                self.stop()
                rospy.loginfo(f"    ✓ 到达位置 (距离={distance:.2f}m)")
                break
            
            # 计算目标方向和角度差
            target_dir = math.atan2(dy, dx)
            angle_diff = normalize_angle(target_dir - yaw)
            
            # 速度规划
            vx = linear_speed if distance > 0.3 else linear_speed * 0.7
            
            # 边走边微调方向
            vz = 0.1 * angle_diff  # 比例控制
            vz = max(-angular_speed * 0.3, min(angular_speed * 0.3, vz))  # 限幅
            
            self.move(vx, 0, vz)
            rate.sleep()
        
        time.sleep(0.3)
        
        # ========== 阶段3：调整最终朝向 ==========
        # 如果指定了target_yaw，则调整到该朝向；否则保持面向目标方向
        if target_yaw is not None:
            final_yaw = target_yaw
        else:
            # 默认面向目标方向（已经在行走时保持了）
            x, y, yaw = tracker.get_position()
            dx = target_x - x
            dy = target_y - y
            final_yaw = math.atan2(dy, dx)
        
        rospy.loginfo(f"  阶段3: 调整最终朝向 ({math.degrees(final_yaw):.1f}°)...")
        max_turn_time = 60.0
        start_time = time.time()
        last_print_time = 0
        
        while not rospy.is_shutdown() and (time.time() - start_time < max_turn_time):
            x, y, yaw = tracker.get_position()
            
            # 计算角度差
            angle_diff = normalize_angle(final_yaw - yaw)
            
            # 每2秒打印一次状态
            elapsed = time.time() - start_time
            if elapsed - last_print_time > 2.0:
                rospy.loginfo(f"    [朝向] 当前yaw={math.degrees(yaw):.1f}°, 目标={math.degrees(final_yaw):.1f}°, 差={math.degrees(angle_diff):.1f}°")
                last_print_time = elapsed
            
            if abs(angle_diff) < yaw_tolerance:
                self.stop()
                rospy.loginfo(f"    ✓ 朝向调整完成 (误差={math.degrees(angle_diff):.1f}°)")
                time.sleep(0.5)
                rospy.loginfo(f"  ✅ 到达目标位置")
                return True
            
            # 速度规划
            turn_speed = angular_speed if abs(angle_diff) > 0.25 else angular_speed * 0.5
            turn_speed = turn_speed if angle_diff > 0 else -turn_speed
            
            self.move(0, 0, turn_speed)
            rate.sleep()
        
        self.stop()
        rospy.logwarn("    ⚠️ 朝向调整超时")
        return False
        return False


class GraspDemo:
    """抓取放置演示主程序"""
    
    def __init__(self, position_mode='odom', robot_model='biped_s42'):
        rospy.init_node('grasp_demo', anonymous=True)
        
        # 初始化组件
        self.tracker = PositionTracker(mode=position_mode, robot_model=robot_model)
        self.robot = RobotController()
        self.grasp_client = GraspServiceClient()
        
        # 任务状态
        self.state = TaskState.IDLE
        
        # 位置配置 (可通过参数修改)
        self.grasp_position = rospy.get_param('~grasp_position', [1.0, 0.0])
        self.place_position = rospy.get_param('~place_position', [0.0, 1.0])
        self.position_tolerance = rospy.get_param('~position_tolerance', 0.1)
        self.move_speed = rospy.get_param('~move_speed', 0.1)
        
        # 3D检测结果 (odom坐标系)
        self.detections_3d_odom = []
        self.detection_sub = rospy.Subscriber(
            '/yolo/detections_3d_odom', String,
            self._detection_callback, queue_size=1
        )
        
        # AprilTag检测结果 (odom坐标系，和SDK一致)
        # SDK使用 /robot_tag_info_odom 话题，已经是odom坐标系下的数据
        self.apriltag_detections_odom = None
        if HAS_APRILTAG:
            self.apriltag_sub = rospy.Subscriber(
                '/robot_tag_info_odom', AprilTagDetectionArray,
                self._apriltag_callback, queue_size=1
            )
        
        rospy.loginfo(f"[GraspDemo] 抓取位置: {self.grasp_position}")
        rospy.loginfo(f"[GraspDemo] 放置位置: {self.place_position}")
        rospy.loginfo(f"[GraspDemo] 精度: {self.position_tolerance}m, 速度: {self.move_speed}m/s")
    
    def _detection_callback(self, msg):
        """接收3D检测结果 (odom坐标系)"""
        try:
            self.detections_3d_odom = json.loads(msg.data)
        except json.JSONDecodeError:
            pass
    
    def _apriltag_callback(self, msg):
        """接收AprilTag检测结果 (odom坐标系)"""
        self.apriltag_detections_odom = msg
    
    def get_apriltag_position_odom(self, tag_id, timeout=10.0):
        """
        获取指定AprilTag在odom坐标系下的位置和姿态
        直接从 /robot_tag_info_odom 话题获取，和SDK一致
        
        :param tag_id: AprilTag的ID
        :param timeout: 超时时间
        :return: (position, quaternion) 或 None
                 position: np.array([x, y, z])
                 quaternion: np.array([qx, qy, qz, qw])
        """
        if not HAS_APRILTAG:
            rospy.logerr("[GraspDemo] AprilTag功能不可用")
            return None
        
        rospy.loginfo(f"[GraspDemo] 等待检测 AprilTag ID:{tag_id}...")
        rate = rospy.Rate(10)
        end_time = rospy.Time.now() + rospy.Duration(timeout)
        
        while not rospy.is_shutdown() and rospy.Time.now() < end_time:
            if self.apriltag_detections_odom is None:
                rate.sleep()
                continue
            
            for detection in self.apriltag_detections_odom.detections:
                if detection.id[0] == tag_id:
                    # 直接使用odom坐标系下的位姿（不需要TF变换）
                    pose = detection.pose.pose.pose
                    
                    # 位置
                    position = np.array([
                        pose.position.x,
                        pose.position.y,
                        pose.position.z
                    ])
                    
                    # 四元数 [qx, qy, qz, qw]
                    quaternion = np.array([
                        pose.orientation.x,
                        pose.orientation.y,
                        pose.orientation.z,
                        pose.orientation.w
                    ])
                    
                    rospy.loginfo(f"[GraspDemo] 找到 AprilTag ID:{tag_id} @ odom({position[0]:.2f}, {position[1]:.2f}, {position[2]:.2f})")
                    return (position, quaternion)
            
            rate.sleep()
        
        rospy.logwarn(f"[GraspDemo] 未检测到 AprilTag ID:{tag_id}")
        return None
    
    def move_to_apriltag_object_with_saved_tag(self, tag_position, tag_quaternion,
                                                lateral_offset=0.0, forward_offset=0.0,
                                                approach_distance=0.5, use_lateral=False):
        """
        使用已保存的AprilTag位置移动到物品前方
        
        :param tag_position: AprilTag位置 np.array([x, y, z])
        :param tag_quaternion: AprilTag四元数 np.array([qx, qy, qz, qw])
        :param lateral_offset: 物品相对AprilTag的横向偏移（正=机器人右边，负=机器人左边）
        :param forward_offset: 物品相对AprilTag的前向偏移
        :param approach_distance: 停在物品前方的距离
        :param use_lateral: 是否使用左右平移
        :return: True if success
        """
        # 使用scipy计算旋转矩阵
        R_wa = R.from_quat(tag_quaternion).as_matrix()
        
        # 计算机器人面向AprilTag时的方向
        z_axis = R_wa[:, 2]  # AprilTag的Z轴（指向机器人）
        
        # 机器人面向AprilTag的方向（在水平面上）
        forward_dir = np.array([-z_axis[0], -z_axis[1]])
        forward_norm = np.linalg.norm(forward_dir)
        if forward_norm < 0.01:
            rospy.logwarn("[GraspDemo] 无法确定方向")
            return False
        forward_dir = forward_dir / forward_norm
        
        # 机器人的"右"方向（顺时针旋转90度）
        right_dir = np.array([forward_dir[1], -forward_dir[0]])
        
        # 计算物品位置
        object_x = tag_position[0] + lateral_offset * right_dir[0] - forward_offset * forward_dir[0]
        object_y = tag_position[1] + lateral_offset * right_dir[1] - forward_offset * forward_dir[1]
        
        # 计算机器人目标位置：在物品前方approach_distance处
        target_x = object_x - approach_distance * forward_dir[0]
        target_y = object_y - approach_distance * forward_dir[1]
        
        # 计算目标朝向：面向物品
        target_yaw = math.atan2(forward_dir[1], forward_dir[0])
        
        rospy.loginfo(f"[GraspDemo] AprilTag位置: ({tag_position[0]:.2f}, {tag_position[1]:.2f})")
        rospy.loginfo(f"[GraspDemo] 偏移: lateral={lateral_offset:.2f}m(右为正), forward={forward_offset:.2f}m")
        rospy.loginfo(f"[GraspDemo] 物品位置(odom): ({object_x:.2f}, {object_y:.2f})")
        rospy.loginfo(f"[GraspDemo] 接近位置(odom): ({target_x:.2f}, {target_y:.2f})")
        rospy.loginfo(f"[GraspDemo] 目标朝向: {math.degrees(target_yaw):.1f}°")
        
        if use_lateral:
            return self.robot.move_lateral(self.tracker, target_x, target_y,
                                           speed=self.move_speed,
                                           tolerance=self.position_tolerance)
        else:
            return self.robot.move_to(self.tracker, target_x, target_y,
                                      linear_speed=self.move_speed,
                                      tolerance=self.position_tolerance,
                                      target_yaw=target_yaw)
    
    def move_to_apriltag_box_with_saved_tag(self, tag_position, tag_quaternion,
                                            lateral_offset=0.0, approach_distance=0.5, 
                                            use_lateral=False):
        """
        使用已保存的AprilTag位置移动到箱子前方（用于放置）
        
        :param tag_position: AprilTag位置 np.array([x, y, z])
        :param tag_quaternion: AprilTag四元数 np.array([qx, qy, qz, qw])
        :param lateral_offset: 放置点相对AprilTag的横向偏移（正=机器人右边，负=机器人左边）
        :param approach_distance: 停在箱子前方的距离
        :param use_lateral: 是否使用左右平移
        :return: True if success
        """
        # 使用scipy计算旋转矩阵
        R_wa = R.from_quat(tag_quaternion).as_matrix()
        
        # 计算机器人面向AprilTag时的方向
        z_axis = R_wa[:, 2]
        forward_dir = np.array([-z_axis[0], -z_axis[1]])
        forward_norm = np.linalg.norm(forward_dir)
        if forward_norm < 0.01:
            rospy.logwarn("[GraspDemo] 无法确定方向")
            return False
        forward_dir = forward_dir / forward_norm
        
        # 机器人的"右"方向
        right_dir = np.array([forward_dir[1], -forward_dir[0]])
        
        # 计算放置点位置（AprilTag位置 + 横向偏移）
        place_x = tag_position[0] + lateral_offset * right_dir[0]
        place_y = tag_position[1] + lateral_offset * right_dir[1]
        
        # 计算机器人目标位置：在放置点前方approach_distance处
        target_x = place_x - approach_distance * forward_dir[0]
        target_y = place_y - approach_distance * forward_dir[1]
        
        # 计算目标朝向：面向放置点
        target_yaw = math.atan2(forward_dir[1], forward_dir[0])
        
        rospy.loginfo(f"[GraspDemo] 箱子AprilTag位置(odom): ({tag_position[0]:.2f}, {tag_position[1]:.2f})")
        rospy.loginfo(f"[GraspDemo] 放置点偏移: lateral={lateral_offset:.2f}m(右为正)")
        rospy.loginfo(f"[GraspDemo] 放置点位置: ({place_x:.2f}, {place_y:.2f})")
        rospy.loginfo(f"[GraspDemo] 接近位置(odom): ({target_x:.2f}, {target_y:.2f})")
        rospy.loginfo(f"[GraspDemo] 目标朝向: {math.degrees(target_yaw):.1f}°")
        
        if use_lateral:
            return self.robot.move_lateral(self.tracker, target_x, target_y,
                                           speed=self.move_speed,
                                           tolerance=self.position_tolerance)
        else:
            return self.robot.move_to(self.tracker, target_x, target_y,
                                      linear_speed=self.move_speed,
                                      tolerance=self.position_tolerance,
                                      target_yaw=target_yaw)
    
    def get_object_position_odom(self, target_class, track_id=-1, timeout=10.0):
        """
        获取目标物体在odom坐标系下的位置
        :param target_class: 目标类别
        :param track_id: 指定track_id，-1表示选最近的
        :param timeout: 等待检测超时时间
        :return: (x, y, z) 或 None
        """
        rospy.loginfo(f"[GraspDemo] 等待检测 {target_class}...")
        rate = rospy.Rate(10)
        end_time = rospy.Time.now() + rospy.Duration(timeout)
        
        while not rospy.is_shutdown() and rospy.Time.now() < end_time:
            candidates = [obj for obj in self.detections_3d_odom
                          if obj['class_name'] == target_class]
            
            if candidates:
                if track_id >= 0:
                    for obj in candidates:
                        if obj.get('track_id') == track_id:
                            pos = obj['position']
                            rospy.loginfo(f"[GraspDemo] 找到 {target_class} ID:{track_id} @ ({pos['x']:.2f}, {pos['y']:.2f}, {pos['z']:.2f})")
                            return (pos['x'], pos['y'], pos['z'])
                else:
                    # 选最近的
                    nearest = min(candidates, key=lambda x: x['distance'])
                    pos = nearest['position']
                    tid = nearest.get('track_id', -1)
                    rospy.loginfo(f"[GraspDemo] 找到最近的 {target_class} ID:{tid} @ ({pos['x']:.2f}, {pos['y']:.2f}, {pos['z']:.2f})")
                    return (pos['x'], pos['y'], pos['z'])
            
            rate.sleep()
        
        rospy.logwarn(f"[GraspDemo] 未检测到 {target_class}")
        return None
    
    def move_to_object(self, target_class, offset_distance=0.5, use_lateral=False, track_id=-1):
        """
        移动到目标物体前方（基于odom坐标）
        参考grasp_box_course_solver的接近逻辑：
        - 计算从当前位置到物体的方向
        - 在物体前方offset_distance处停下
        - 最终朝向面向物体
        
        :param target_class: 目标类别
        :param offset_distance: 距离物体的距离（正值，单位米）
        :param use_lateral: 是否使用左右平移
        :param track_id: 指定track_id，-1表示选最近的
        :return: True if success
        """
        pos = self.get_object_position_odom(target_class, track_id)
        if pos is None:
            return False
        
        object_x, object_y, object_z = pos
        
        # 获取当前机器人位置
        robot_x, robot_y, robot_yaw = self.tracker.get_position()
        
        # 计算从机器人到物体的方向向量
        dx = object_x - robot_x
        dy = object_y - robot_y
        distance_to_object = math.sqrt(dx**2 + dy**2)
        
        if distance_to_object < 0.01:
            rospy.logwarn("[GraspDemo] 已经在物体位置")
            return True
        
        # 单位方向向量（从机器人指向物体）
        dir_x = dx / distance_to_object
        dir_y = dy / distance_to_object
        
        # 目标位置 = 物体位置 - 偏移距离 * 方向向量（在物体前方）
        target_x = object_x - offset_distance * dir_x
        target_y = object_y - offset_distance * dir_y
        
        # 目标朝向 = 面向物体
        target_yaw = math.atan2(dy, dx)
        
        rospy.loginfo(f"[GraspDemo] 物体位置(odom): ({object_x:.2f}, {object_y:.2f})")
        rospy.loginfo(f"[GraspDemo] 机器人位置: ({robot_x:.2f}, {robot_y:.2f})")
        rospy.loginfo(f"[GraspDemo] 移动目标: ({target_x:.2f}, {target_y:.2f}), 朝向: {math.degrees(target_yaw):.1f}°")
        
        if use_lateral:
            return self.robot.move_lateral(self.tracker, target_x, target_y,
                                           speed=self.move_speed,
                                           tolerance=self.position_tolerance)
        else:
            return self.robot.move_to(self.tracker, target_x, target_y,
                                      linear_speed=self.move_speed,
                                      tolerance=self.position_tolerance,
                                      target_yaw=target_yaw)
    
    def run_task(self, target_class='cup', use_lateral=False, use_detection=False, grasp_offset=0.5, hand="right",
                 use_apriltag=False, tag_id=0, lateral_offset=0.0, forward_offset=0.0, 
                 place_offset=0.5, place_lateral_offset=0.0, backward_distance=0.5):
        """
        执行完整的抓取放置任务
        :param target_class: 要抓取的物体类别
        :param use_lateral: 是否使用左右平移 (True) 或转向前进 (False)
        :param use_detection: 是否使用YOLO检测结果确定抓取位置 (True) 或使用固定坐标 (False)
        :param grasp_offset: 使用检测时，距离物体的偏移量 (m)
        :param hand: 指定使用的手 "left"/"right"/"auto"，默认"right"
        :param use_apriltag: 是否使用AprilTag定位物品
        :param tag_id: AprilTag的ID
        :param lateral_offset: 物品相对AprilTag的横向偏移（正=右，负=左）
        :param forward_offset: 物品相对AprilTag的前向偏移
        :param place_offset: 放置时距离箱子的距离 (m)
        :param place_lateral_offset: 放置点相对AprilTag的横向偏移（正=右，负=左）
        :param backward_distance: 放置后后退距离 (m)
        """
        rospy.loginfo(f"========== 开始任务: 抓取 {target_class} ==========")
        rospy.loginfo(f"移动方式: {'左右平移' if use_lateral else '转向前进'}")
        if use_apriltag:
            rospy.loginfo(f"定位方式: AprilTag (ID:{tag_id}, 横向偏移:{lateral_offset}m, 前向偏移:{forward_offset}m)")
            rospy.loginfo(f"放置点: 距离={place_offset}m, 横向偏移={place_lateral_offset}m")
        elif use_detection:
            rospy.loginfo(f"定位方式: YOLO检测")
        else:
            rospy.loginfo(f"定位方式: 固定坐标")
        rospy.loginfo(f"使用手: {hand}")
        
        # 保存AprilTag位置，用于放置阶段
        saved_tag_position = None
        saved_tag_quaternion = None
        
        # 阶段1: 导航到抓取区
        self.state = TaskState.NAV_TO_GRASP
        
        if use_apriltag:
            rospy.loginfo(f"[1/6] 导航到 {target_class} 位置 (基于AprilTag ID:{tag_id})")
            # 先获取并保存AprilTag位置
            result = self.get_apriltag_position_odom(tag_id)
            if result is None:
                rospy.logerr("未检测到AprilTag")
                return False
            saved_tag_position, saved_tag_quaternion = result
            rospy.loginfo(f"[GraspDemo] 保存AprilTag位置: ({saved_tag_position[0]:.2f}, {saved_tag_position[1]:.2f})")
            
            # 移动到物品位置
            success = self.move_to_apriltag_object_with_saved_tag(
                saved_tag_position, saved_tag_quaternion,
                lateral_offset, forward_offset,
                approach_distance=grasp_offset, use_lateral=use_lateral)
        elif use_detection:
            rospy.loginfo(f"[1/6] 导航到 {target_class} 位置 (基于检测)")
            success = self.move_to_object(target_class, offset_distance=grasp_offset, use_lateral=use_lateral)
        else:
            rospy.loginfo(f"[1/6] 导航到抓取区 {self.grasp_position}")
            if use_lateral:
                success = self.robot.move_lateral(self.tracker,
                                                  self.grasp_position[0],
                                                  self.grasp_position[1],
                                                  speed=self.move_speed,
                                                  tolerance=self.position_tolerance)
            else:
                success = self.robot.move_to(self.tracker, 
                                             self.grasp_position[0], 
                                             self.grasp_position[1],
                                             linear_speed=self.move_speed,
                                             tolerance=self.position_tolerance)
        
        if not success:
            rospy.logerr("导航到抓取区失败")
            return False
        
        time.sleep(1.0)
        
        # 阶段2: 抓取 (只抓取不释放)
        self.state = TaskState.GRASPING
        rospy.loginfo(f"[2/6] 抓取 {target_class}")
        
        success, track_id, hand = self.grasp_client.grasp(target_class, grasp_only=True, hand=hand)
        if not success:
            rospy.logerr(f"抓取 {target_class} 失败")
            return False
        
        time.sleep(1.0)
        
        # 阶段3: 导航到放置区
        self.state = TaskState.NAV_TO_PLACE
        
        if use_apriltag:
            # 使用保存的AprilTag位置移动到箱子前方放置（不重新检测）
            rospy.loginfo(f"[3/6] 导航到箱子位置 (使用保存的AprilTag位置)")
            success = self.move_to_apriltag_box_with_saved_tag(
                saved_tag_position, saved_tag_quaternion,
                lateral_offset=place_lateral_offset,
                approach_distance=place_offset, use_lateral=use_lateral)
        else:
            rospy.loginfo(f"[3/6] 导航到放置区 {self.place_position}")
            if use_lateral:
                success = self.robot.move_lateral(self.tracker,
                                                  self.place_position[0],
                                                  self.place_position[1],
                                                  speed=self.move_speed,
                                                  tolerance=self.position_tolerance)
            else:
                success = self.robot.move_to(self.tracker,
                                             self.place_position[0],
                                             self.place_position[1],
                                             linear_speed=self.move_speed,
                                             tolerance=self.position_tolerance)
        
        if not success:
            rospy.logerr("导航到放置区失败")
            return False
        
        time.sleep(1.0)
        
        # 阶段4: 放置 (只释放物体，不复位手臂)
        self.state = TaskState.PLACING
        rospy.loginfo("[4/6] 放置物体 (不复位手臂)")
        
        success = self.grasp_client.place(hand, reset_arm=False)
        if not success:
            rospy.logerr("放置失败")
            return False
        
        # 阶段5: 后退，防止手臂复位时打倒桌子（闭环控制）
        rospy.loginfo(f"[5/6] 后退离开桌子 ({backward_distance}m)")
        self.robot.move_backward(backward_distance, speed=0.1, tracker=self.tracker)
        
        # 阶段6: 复位手臂
        rospy.loginfo("[6/6] 复位手臂")
        success = self.grasp_client.reset_arm(hand)
        if not success:
            rospy.logwarn("手臂复位失败")
        
        self.state = TaskState.DONE
        rospy.loginfo("========== 任务完成 ==========")
        return True
    
    def run_manual(self, target_class='cup', hand="right"):
        """
        手动模式 - 等待到达位置后执行抓取/放置
        适用于外部控制机器人移动的场景
        """
        rospy.loginfo(f"========== 手动模式: 等待抓取 {target_class} ==========")
        rate = rospy.Rate(10)
        
        # 等待到达抓取区
        self.state = TaskState.NAV_TO_GRASP
        rospy.loginfo(f"等待到达抓取区 {self.grasp_position}...")
        
        while not rospy.is_shutdown():
            if self.tracker.is_at_position(self.grasp_position[0], 
                                           self.grasp_position[1],
                                           self.position_tolerance):
                break
            rate.sleep()
        
        rospy.loginfo("到达抓取区，开始抓取")
        self.state = TaskState.GRASPING
        success, _, hand = self.grasp_client.grasp(target_class, grasp_only=True, hand=hand)
        
        if not success:
            rospy.logerr("抓取失败")
            return False
        
        # 等待到达放置区
        self.state = TaskState.NAV_TO_PLACE
        rospy.loginfo(f"等待到达放置区 {self.place_position}...")
        
        while not rospy.is_shutdown():
            if self.tracker.is_at_position(self.place_position[0],
                                           self.place_position[1],
                                           self.position_tolerance):
                break
            rate.sleep()
        
        rospy.loginfo("到达放置区，开始放置")
        self.state = TaskState.PLACING
        success = self.grasp_client.place(hand, reset_arm=False)
        
        if not success:
            rospy.logerr("放置失败")
            return False
        
        # 后退1m，防止手臂复位时打倒桌子（闭环控制）
        rospy.loginfo("后退离开桌子")
        self.robot.move_backward(1.0, speed=0.1, tracker=self.tracker)
        
        # 复位手臂
        rospy.loginfo("复位手臂")
        self.grasp_client.reset_arm(hand)
        
        self.state = TaskState.DONE
        rospy.loginfo("========== 任务完成 ==========")
        return True
    
    def grasp_at_current(self, target_class='cup', hand="right"):
        """在当前位置抓取"""
        rospy.loginfo(f"在当前位置抓取 {target_class}")
        success, track_id, hand = self.grasp_client.grasp(target_class, grasp_only=True, hand=hand)
        return success, hand
    
    def place_at_current(self, hand=""):
        """在当前位置放置"""
        rospy.loginfo("在当前位置放置")
        success = self.grasp_client.place(hand, reset_arm=False)
        
        if success:
            # 后退1m，防止手臂复位时打倒桌子（闭环控制）
            rospy.loginfo("后退离开桌子")
            self.robot.move_backward(1.0, speed=0.1, tracker=self.tracker)
            
            # 复位手臂
            rospy.loginfo("复位手臂")
            self.grasp_client.reset_arm(hand)
        
        return success


def main():
    parser = argparse.ArgumentParser(description="抓取放置演示")
    parser.add_argument("--mode", type=str, default="auto",
                        choices=["auto", "manual", "grasp", "place"],
                        help="运行模式: auto(自动导航), manual(等待外部控制), grasp(只抓取), place(只放置)")
    parser.add_argument("--position_mode", type=str, default="gazebo",
                        choices=["odom", "gazebo"],
                        help="位置判断方式 (默认gazebo，使用--use_detection或--use_apriltag时自动切换为odom)")
    parser.add_argument("--target", type=str, default="cup",
                        help="抓取目标: cup/plate/scissors")
    parser.add_argument("--grasp_x", type=float, default=-0.28,
                        help="抓取位置X")
    parser.add_argument("--grasp_y", type=float, default=-4.4,
                        help="抓取位置Y")
    parser.add_argument("--place_x", type=float, default=0.88,
                        help="放置位置X")
    parser.add_argument("--place_y", type=float, default=-4.35,
                        help="放置位置Y")
    parser.add_argument("--robot_model", type=str, default="biped_s42",
                        help="Gazebo机器人模型名称")
    parser.add_argument("--grasp_hand", type=str, default="right",
                        choices=["left", "right", "auto"],
                        help="抓取时使用的手 (left/right/auto，默认right)")
    parser.add_argument("--place_hand", type=str, default="",
                        help="放置时使用的手 (left/right，空表示使用抓取的手)")
    parser.add_argument("--lateral", action="store_true",
                        help="使用左右平移移动 (默认转向前进)")
    parser.add_argument("--speed", type=float, default=0.1,
                        help="移动速度 (m/s)")
    parser.add_argument("--tolerance", type=float, default=0.1,
                        help="到达位置精度 (m)")
    parser.add_argument("--use_detection", action="store_true",
                        help="使用3D检测结果确定抓取位置 (默认使用固定坐标)")
    parser.add_argument("--grasp_offset", type=float, default=0.15,
                        help="使用检测时，距离物体的距离 (m，正值)")
    # AprilTag相关参数
    parser.add_argument("--use_apriltag", action="store_true",
                        help="使用AprilTag定位物品位置")
    parser.add_argument("--tag_id", type=int, default=0,
                        help="AprilTag的ID (默认0)")
    parser.add_argument("--lateral_offset", type=float, default=0.75,
                        help="物品相对AprilTag的横向偏移 (正=右边，负=左边，单位m)")
    parser.add_argument("--forward_offset", type=float, default=0.0,
                        help="物品相对AprilTag的前向偏移 (正=前方，负=后方，单位m)")
    parser.add_argument("--place_offset", type=float, default=0.32,
                        help="放置时距离箱子的距离 (m，正值)")
    parser.add_argument("--place_lateral_offset", type=float, default=-0.50,
                        help="放置点相对AprilTag的横向偏移 (正=右边，负=左边，单位m)")
    parser.add_argument("--backward_distance", type=float, default=0.5,
                        help="放置后后退距离 (m，默认0.5)")
    args = parser.parse_args()
    
    # 使用检测或AprilTag时自动切换为odom模式
    position_mode = args.position_mode
    if (args.use_detection or args.use_apriltag) and position_mode == "gazebo":
        position_mode = "odom"
        rospy.loginfo("使用检测/AprilTag模式，自动切换为odom坐标系")
    
    try:
        demo = GraspDemo(
            position_mode=position_mode,
            robot_model=args.robot_model
        )
        
        # 设置位置
        demo.grasp_position = [args.grasp_x, args.grasp_y]
        demo.place_position = [args.place_x, args.place_y]
        demo.position_tolerance = args.tolerance
        demo.move_speed = args.speed
        
        if args.mode == "auto":
            demo.run_task(args.target, use_lateral=args.lateral, 
                          use_detection=args.use_detection, grasp_offset=args.grasp_offset,
                          hand=args.grasp_hand,
                          use_apriltag=args.use_apriltag, tag_id=args.tag_id,
                          lateral_offset=args.lateral_offset, forward_offset=args.forward_offset,
                          place_offset=args.place_offset, place_lateral_offset=args.place_lateral_offset,
                          backward_distance=args.backward_distance)
        elif args.mode == "manual":
            demo.run_manual(args.target, hand=args.grasp_hand)
        elif args.mode == "grasp":
            demo.grasp_at_current(args.target, hand=args.grasp_hand)
        elif args.mode == "place":
            demo.place_at_current(args.place_hand)
    
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        rospy.loginfo("用户中断")


if __name__ == '__main__':
    main()
