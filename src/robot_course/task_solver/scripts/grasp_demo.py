#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抓取放置演示程序
机器人导航到抓取区 -> 抓取物体 -> 导航到放置区 -> 放置物体

通过ROS服务调用grasp_controller实现抓取/放置

位置判断方式：
1. odom - 通过odom话题判断机器人位置
2. aruco - 通过二维码检测判断位置
3. gazebo - 通过Gazebo真实值判断位置

机器人控制：cmd_vel
"""

import rospy
import math
import time
import argparse
from enum import Enum

from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry

# 抓取服务
from task_solver.srv import GraspObject, GraspObjectRequest
from task_solver.srv import PlaceObject, PlaceObjectRequest
from task_solver.srv import ResetArm, ResetArmRequest

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
    
    def grasp(self, target_class, track_id=-1, grasp_only=True):
        """
        调用抓取服务
        :param target_class: 目标类别 'cup'/'plate'/'scissors'
        :param track_id: 指定track_id (-1表示自动选择最近的)
        :param grasp_only: True只抓取不释放, False抓取后释放
        :return: (success, track_id, hand)
        """
        try:
            req = GraspObjectRequest()
            req.target_class = target_class
            req.track_id = track_id
            req.grasp_only = grasp_only
            
            rospy.loginfo(f"[GraspClient] 调用抓取服务: {target_class}")
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
        :param mode: 'odom', 'aruco', 'gazebo'
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
        elif mode == 'aruco':
            # 二维码位置话题 (根据实际情况修改)
            self.aruco_sub = rospy.Subscriber('/aruco_pose', PoseStamped, self._aruco_callback, queue_size=1)
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
    
    def _aruco_callback(self, msg):
        self.current_x = msg.pose.position.x
        self.current_y = msg.pose.position.y
        q = msg.pose.orientation
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
    
    def move_backward(self, distance, speed=0.1):
        """
        后退指定距离
        :param distance: 后退距离(m)
        :param speed: 后退速度(m/s)
        """
        duration = distance / speed
        rospy.loginfo(f"后退 {distance}m...")
        
        start_time = time.time()
        rate = rospy.Rate(10)
        
        while not rospy.is_shutdown() and (time.time() - start_time < duration):
            self.move(-speed, 0, 0)  # 负速度 = 后退
            rate.sleep()
        
        self.stop()
        rospy.loginfo("后退完成")
    
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
    
    def move_to(self, tracker, target_x, target_y, linear_speed=0.15, angular_speed=0.3, tolerance=0.1):
        """
        简单的移动到目标点 (转向+前进)
        :return: True if reached
        """
        rate = rospy.Rate(10)
        
        while not rospy.is_shutdown():
            x, y, yaw = tracker.get_position()
            
            # 计算到目标的距离和角度
            dx = target_x - x
            dy = target_y - y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < tolerance:
                self.stop()
                rospy.loginfo(f"到达目标 ({target_x:.2f}, {target_y:.2f})")
                return True
            
            # 计算目标角度
            target_yaw = math.atan2(dy, dx)
            angle_diff = target_yaw - yaw
            
            # 归一化角度到 [-pi, pi]
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi
            
            # 控制，接近目标时减速
            actual_speed = min(linear_speed, distance * 0.5)
            actual_speed = max(actual_speed, 0.03)
            
            if abs(angle_diff) > 0.2:
                # 先转向
                self.move(0, 0, angular_speed if angle_diff > 0 else -angular_speed)
            else:
                # 前进
                self.move(actual_speed, 0, angle_diff * 0.3)
            
            rate.sleep()
        
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
        
        rospy.loginfo(f"[GraspDemo] 抓取位置: {self.grasp_position}")
        rospy.loginfo(f"[GraspDemo] 放置位置: {self.place_position}")
        rospy.loginfo(f"[GraspDemo] 精度: {self.position_tolerance}m, 速度: {self.move_speed}m/s")
    
    def run_task(self, target_class='cup', use_lateral=False):
        """
        执行完整的抓取放置任务
        :param target_class: 要抓取的物体类别
        :param use_lateral: 是否使用左右平移 (True) 或转向前进 (False)
        """
        rospy.loginfo(f"========== 开始任务: 抓取 {target_class} ==========")
        rospy.loginfo(f"移动方式: {'左右平移' if use_lateral else '转向前进'}")
        
        # 阶段1: 导航到抓取区
        self.state = TaskState.NAV_TO_GRASP
        rospy.loginfo(f"[1/4] 导航到抓取区 {self.grasp_position}")
        
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
        rospy.loginfo(f"[2/4] 抓取 {target_class}")
        
        success, track_id, hand = self.grasp_client.grasp(target_class, grasp_only=True)
        if not success:
            rospy.logerr(f"抓取 {target_class} 失败")
            return False
        
        time.sleep(1.0)
        
        # 阶段3: 导航到放置区
        self.state = TaskState.NAV_TO_PLACE
        rospy.loginfo(f"[3/4] 导航到放置区 {self.place_position}")
        
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
        
        # 阶段5: 后退1m，防止手臂复位时打倒桌子
        rospy.loginfo("[5/6] 后退离开桌子")
        self.robot.move_backward(1.0, speed=0.1)
        
        # 阶段6: 复位手臂
        rospy.loginfo("[6/6] 复位手臂")
        success = self.grasp_client.reset_arm(hand)
        if not success:
            rospy.logwarn("手臂复位失败")
        
        self.state = TaskState.DONE
        rospy.loginfo("========== 任务完成 ==========")
        return True
    
    def run_manual(self, target_class='cup'):
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
        success, _, hand = self.grasp_client.grasp(target_class, grasp_only=True)
        
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
        success = self.grasp_client.place(hand)
        
        self.state = TaskState.DONE
        rospy.loginfo("========== 任务完成 ==========")
        return success
    
    def grasp_at_current(self, target_class='cup'):
        """在当前位置抓取"""
        rospy.loginfo(f"在当前位置抓取 {target_class}")
        success, track_id, hand = self.grasp_client.grasp(target_class, grasp_only=True)
        return success, hand
    
    def place_at_current(self, hand=""):
        """在当前位置放置"""
        rospy.loginfo("在当前位置放置")
        return self.grasp_client.place(hand)


def main():
    parser = argparse.ArgumentParser(description="抓取放置演示")
    parser.add_argument("--mode", type=str, default="auto",
                        choices=["auto", "manual", "grasp", "place"],
                        help="运行模式: auto(自动导航), manual(等待外部控制), grasp(只抓取), place(只放置)")
    parser.add_argument("--position_mode", type=str, default="odom",
                        choices=["odom", "aruco", "gazebo"],
                        help="位置判断方式")
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
    parser.add_argument("--hand", type=str, default="",
                        help="放置时使用的手 (left/right)")
    parser.add_argument("--lateral", action="store_true",
                        help="使用左右平移移动 (默认转向前进)")
    parser.add_argument("--speed", type=float, default=0.1,
                        help="移动速度 (m/s)")
    parser.add_argument("--tolerance", type=float, default=0.1,
                        help="到达位置精度 (m)")
    args = parser.parse_args()
    
    try:
        demo = GraspDemo(
            position_mode=args.position_mode,
            robot_model=args.robot_model
        )
        
        # 设置位置
        demo.grasp_position = [args.grasp_x, args.grasp_y]
        demo.place_position = [args.place_x, args.place_y]
        demo.position_tolerance = args.tolerance
        demo.move_speed = args.speed
        
        if args.mode == "auto":
            demo.run_task(args.target, use_lateral=args.lateral)
        elif args.mode == "manual":
            demo.run_manual(args.target)
        elif args.mode == "grasp":
            demo.grasp_at_current(args.target)
        elif args.mode == "place":
            demo.place_at_current(args.hand)
    
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        rospy.loginfo("用户中断")


if __name__ == '__main__':
    main()
