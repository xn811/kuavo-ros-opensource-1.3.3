#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
仿真版本的平移对齐程序
假设初始角度已对准，通过odom闭环控制保持角度，只做Y方向平移
"""

import rospy
import math
import numpy as np
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from kuavo_msgs.msg import AprilTagDetectionArray
import tf.transformations as tft

class KuavoOffsetAligner:
    def __init__(self):
        rospy.init_node('kuavo_offset_aligner', anonymous=True)

        self.tag_topic = "/robot_tag_info"
        self.odom_topic = "/odom"
        self.joy_pub = rospy.Publisher('/joy', Joy, queue_size=1)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

        self.TARGET_ID = 3
        
        # === 关键参数（全局变量，方便修改）===
        self.Y_TARGET = 0.27     # Y方向目标位置 0.27m
        self.LAT_TOL = 0.015      # Y方向允许 1.5cm 误差
        self.TARGET_YAW_OFFSET = math.radians(0.75)  # 目标yaw偏移：0.75度
        self.YAW_TOL = math.radians(1.5)  # yaw角度允许误差：1.5度
        
        # 速度参数
        self.MAX_SPEED_Y = 0.12
        self.MIN_SPEED_Y = 0.06
        self.MAX_SPEED_YAW = 0.15
        
        self.is_running = True
        self.initial_yaw = None  # 初始yaw角度

    def init_joy(self):
        msg = Joy()
        msg.axes = [0.0] * 8
        msg.buttons = [0] * 11
        return msg

    def stop_robot(self):
        stop_vel = Twist()
        for _ in range(10):
            self.cmd_vel_pub.publish(stop_vel)
            rospy.sleep(0.05)

    def stop_and_stance(self):
        self.is_running = False
        rospy.loginfo("\n[刹车] 停止并切换站立...")
        self.stop_robot()
        stop_msg = self.init_joy()
        stop_msg.buttons[0] = 1
        for _ in range(25):
            self.joy_pub.publish(stop_msg)
            rospy.sleep(0.04)

    def get_odom_yaw(self):
        """从odom获取当前yaw角度"""
        try:
            msg = rospy.wait_for_message(self.odom_topic, Odometry, timeout=0.3)
            q = msg.pose.pose.orientation
            euler = tft.euler_from_quaternion([q.x, q.y, q.z, q.w])
            return euler[2]  # yaw
        except Exception as e:
            rospy.logwarn(f"获取odom失败: {e}")
            return None

    def get_tag_pose(self):
        try:
            msg = rospy.wait_for_message(self.tag_topic, AprilTagDetectionArray, timeout=0.3)
            for d in msg.detections:
                tag_id = d.id[0] if hasattr(d.id, '__iter__') else d.id
                if tag_id == self.TARGET_ID:
                    p = d.pose.pose.pose.position
                    return p.x, p.y
        except Exception as e:
            rospy.logwarn(f"获取位姿失败: {e}")
            return None, None
        return None, None

    def align_y(self):
        """Y方向平移，同时用odom保持角度在目标偏移"""
        rospy.loginfo("\n===== 开始Y对齐（保持角度） =====")
        
        rate = rospy.Rate(10)
        stuck_count = 0
        last_error = None
        last_sign = None
        
        while not rospy.is_shutdown() and self.is_running:
            tag_x, tag_y = self.get_tag_pose()
            current_yaw = self.get_odom_yaw()
            
            if tag_x is None or current_yaw is None:
                rospy.logwarn("丢失目标或odom")
                continue
            
            y_error = tag_y  # 话题中的Y值就是误差
            
            # 目标yaw = 初始yaw + 目标偏移（-0.75度）
            target_yaw = self.initial_yaw + self.TARGET_YAW_OFFSET
            yaw_error = current_yaw - target_yaw
            
            # 处理yaw角度跨越±π的情况
            if yaw_error > math.pi:
                yaw_error -= 2 * math.pi
            elif yaw_error < -math.pi:
                yaw_error += 2 * math.pi
            
            # 计算Y控制误差（用于判断过冲）
            y_control_error = tag_y - self.Y_TARGET
            current_sign = 1 if y_control_error > 0 else -1
            
            print(f"\r[Y对齐] 当前Y:{tag_y:+.3f}m 目标偏移:{self.Y_TARGET:+.3f}m | yaw误差:{math.degrees(yaw_error):+.2f}°", end='', flush=True)
            
            # 判断是否到达目标（Y在目标偏移附近）
            if abs(tag_y - self.Y_TARGET) <= self.LAT_TOL:
                rospy.loginfo(f"\n[Y OK] 当前Y={tag_y:+.3f}m, 目标={self.Y_TARGET:+.3f}m, yaw误差={math.degrees(yaw_error):+.2f}°")
                return True
            
            # 过冲检测（Y控制误差符号变化）
            if last_sign is not None and current_sign != last_sign:
                rospy.loginfo(f"\n[过冲] 当前Y={tag_y:+.3f}m, 目标={self.Y_TARGET:+.3f}m")
                return True
            last_sign = current_sign
            
            # 卡住检测
            if last_error is not None:
                if abs(y_error - last_error) < 0.005:
                    stuck_count += 1
                    if stuck_count >= 15:
                        rospy.loginfo(f"\n[Y稳定] Y误差={y_error:+.3f}m")
                        return True
                else:
                    stuck_count = 0
            last_error = y_error
            
            cmd_vel = Twist()
            
            # Y方向控制：让tag_y接近目标偏移
            y_control_error = tag_y - self.Y_TARGET
            cmd_y = np.clip(y_control_error * 1.0, -self.MAX_SPEED_Y, self.MAX_SPEED_Y)
            if abs(cmd_y) < self.MIN_SPEED_Y:
                cmd_y = self.MIN_SPEED_Y if cmd_y > 0 else -self.MIN_SPEED_Y
            cmd_vel.linear.y = cmd_y
            
            # yaw角度闭环控制（保持在目标偏移）
            cmd_yaw = np.clip(-yaw_error * 2.0, -self.MAX_SPEED_YAW, self.MAX_SPEED_YAW)
            cmd_vel.angular.z = cmd_yaw
            
            self.cmd_vel_pub.publish(cmd_vel)
            rate.sleep()
        
        return False

    def run(self):
        rospy.on_shutdown(self.stop_and_stance)
        
        rospy.loginfo("======= [仿真] 平移对齐任务启动 =======")
        rospy.loginfo(f"目标: Y<{self.LAT_TOL*100}cm，yaw偏移={math.degrees(self.TARGET_YAW_OFFSET):.2f}°")
        
        # 获取初始yaw角度
        self.initial_yaw = self.get_odom_yaw()
        if self.initial_yaw is None:
            rospy.logerr("无法获取初始odom")
            return
        rospy.loginfo(f"初始yaw角度: {math.degrees(self.initial_yaw):.1f}°")
        
        tag_x, tag_y = self.get_tag_pose()
        if tag_x is None:
            rospy.logerr(f"找不到 ID {self.TARGET_ID}")
            return

        rospy.loginfo(f"初始: x={tag_x:.3f}, y={tag_y:.3f}")
        
        # 开始Y对齐
        if not self.align_y():
            self.stop_and_stance()
            return
        
        self.stop_and_stance()
        rospy.loginfo("======= 任务完成 =======")

if __name__ == '__main__':
    try:
        KuavoOffsetAligner().run()
    except rospy.ROSInterruptException:
        pass
