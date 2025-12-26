#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
仿真版本的旋转对齐程序
与实物版本的区别：方向逻辑相反（仿真环境坐标系差异）
"""

import rospy
import math
import numpy as np
import time
from sensor_msgs.msg import Joy
from kuavo_msgs.msg import AprilTagDetectionArray
from geometry_msgs.msg import Twist

class KuavoAdaptiveAlignTask:
    def __init__(self):
        rospy.init_node('kuavo_adaptive_align_node', anonymous=True)
        self.cmd_pub = rospy.Publisher('/cmd_pose', Twist, queue_size=10)
        self.joy_pub = rospy.Publisher('/joy', Joy, queue_size=1)
        self.tag_topic = "/robot_tag_info"
        
        # --- 参数配置 ---
        self.SEARCH_STEP_RAD = math.radians(-15) # 大步搜索：-15度
        self.STEP_INTERVAL = 0.6                # 缩短间隔，提高响应
        
        # 动态微调参数
        self.MIN_STEP_RAD = math.radians(3.0)    # 最小步长改为3度
        self.MAX_STEP_RAD = math.radians(8.0)    # 最大微调步长
        self.CENTER_THRESHOLD_RAD = math.radians(2.0) # 2度以内视为对齐
        
        self.is_running = True
        
        # 检测是否卡住
        self.last_error = None
        self.stuck_count = 0
        self.STUCK_THRESHOLD = 5  # 连续5次偏差不变则认为卡住

    def init_joy(self):
        msg = Joy()
        msg.axes = [0.0] * 8
        msg.buttons = [0] * 11
        return msg

    def stop_and_stance(self):
        """停止并切换到站立模式"""
        self.is_running = False
        rospy.loginfo("\n[停止] 切换到站立模式...")
        # 发送零旋转
        stop_msg = Twist()
        for _ in range(5):
            self.cmd_pub.publish(stop_msg)
            rospy.sleep(0.05)
        # 切换站立
        stance_msg = self.init_joy()
        stance_msg.buttons[0] = 1  # BUTTON_STANCE
        for _ in range(20):
            self.joy_pub.publish(stance_msg)
            rospy.sleep(0.04)

    def send_rotate_cmd(self, rad):
        """发布旋转指令"""
        msg = Twist()
        msg.angular.z = rad
        self.cmd_pub.publish(msg)
        rospy.loginfo(f"--- 实际发送指令: {math.degrees(rad):.2f} 度 ---")

    def fetch_tag_position(self, target_id):
        try:
            msg = rospy.wait_for_message(self.tag_topic, AprilTagDetectionArray, timeout=1.0)
            for d in msg.detections:
                if d.id[0] == target_id:
                    p = d.pose.pose.pose.position
                    return p.x, p.y
        except:
            return None, None
        return None, None

    def get_stable_yaw_error(self, target_id):
        samples_yaw = []
        for _ in range(3):
            tx, ty = self.fetch_tag_position(target_id)
            if tx is not None:
                yaw_error = math.atan2(-ty, tx)
                samples_yaw.append(yaw_error)
            rospy.sleep(0.02)
        return np.mean(samples_yaw) if samples_yaw else None

    def main_logic(self):
        rospy.on_shutdown(self.stop_and_stance)
        rospy.loginfo("======= [仿真] 任务启动：等待识别 ID 0 =======")
        
        while not rospy.is_shutdown() and self.is_running:
            tx, _ = self.fetch_tag_position(0)
            if tx is not None:
                rospy.loginfo(">> 发现 ID 0，开始向右搜寻 ID 1...")
                break
            rospy.sleep(0.5)

        # 搜索阶段
        found_id1 = False
        while not rospy.is_shutdown() and not found_id1 and self.is_running:
            tx, ty = self.fetch_tag_position(1)
            if tx is not None:
                rospy.loginfo(f">> 捕捉到 ID 1，进入动态微调模式")
                found_id1 = True
            else:
                self.send_rotate_cmd(self.SEARCH_STEP_RAD)
                time.sleep(self.STEP_INTERVAL)

        # 动态微调阶段
        rospy.loginfo("======= 开始动态对齐 =======")
        align_success = False
        while not rospy.is_shutdown() and self.is_running:
            error = self.get_stable_yaw_error(1)
            if error is None:
                rospy.logwarn(">> 丢失目标")
                break
                
            deg_error = math.degrees(error)
            rospy.loginfo(f">> 当前偏差: {deg_error:.2f} 度")

            if abs(error) < self.CENTER_THRESHOLD_RAD:
                rospy.loginfo("======= 成功正对 ID 1 =======")
                align_success = True
                break
            
            # 检测是否卡住（偏差连续不变）
            if self.last_error is not None:
                if abs(error - self.last_error) < math.radians(0.5):  # 偏差变化小于0.5度
                    self.stuck_count += 1
                    if self.stuck_count >= self.STUCK_THRESHOLD:
                        rospy.loginfo(f"======= 偏差稳定在 {deg_error:.2f} 度，视为对齐完成 =======")
                        align_success = True
                        break
                else:
                    self.stuck_count = 0
            self.last_error = error
            
            # 仿真版本：方向逻辑与实物相反
            direction = -1 if error > 0 else 1
            
            suggested_step = abs(error) * 0.6 
            actual_step = max(self.MIN_STEP_RAD, min(suggested_step, self.MAX_STEP_RAD))
            
            if abs(error) < actual_step:
                actual_step = abs(error)

            self.send_rotate_cmd(direction * actual_step)
            time.sleep(self.STEP_INTERVAL)

        # 对齐完成后停止
        self.stop_and_stance()
        if align_success:
            rospy.loginfo("======= 任务完成 =======")

if __name__ == '__main__':
    try:
        task = KuavoAdaptiveAlignTask()
        task.main_logic()
    except rospy.ROSInterruptException:
        pass
