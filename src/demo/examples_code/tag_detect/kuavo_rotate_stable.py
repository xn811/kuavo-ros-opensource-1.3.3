#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import math
import numpy as np
import time
from kuavo_msgs.msg import AprilTagDetectionArray
from geometry_msgs.msg import Twist

class KuavoAdaptiveAlignTask:
    def __init__(self):
        rospy.init_node('kuavo_adaptive_align_node', anonymous=True)
        self.cmd_pub = rospy.Publisher('/cmd_pose', Twist, queue_size=10)
        self.tag_topic = "/robot_tag_info"
        
        # --- 参数配置 ---
        self.SEARCH_STEP_RAD = math.radians(-15) # 大步搜索：-15度
        self.STEP_INTERVAL = 0.6                # 缩短间隔，提高响应
        
        # 动态微调参数
        self.MIN_STEP_RAD = math.radians(3.0)    # 最小步长改为3度，确保能克服摩擦力带动电机
        self.MAX_STEP_RAD = math.radians(8.0)    # 最大微调步长，防止动作过猛丢失目标
        self.CENTER_THRESHOLD_RAD = math.radians(2.0) # 2度以内视为对齐
        
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
        for _ in range(3): # 稍微减少采样次数提高频率
            tx, ty = self.fetch_tag_position(target_id)
            if tx is not None:
                # 坐标修正：-ty
                yaw_error = math.atan2(-ty, tx)
                samples_yaw.append(yaw_error)
            rospy.sleep(0.02)
        return np.mean(samples_yaw) if samples_yaw else None

    def main_logic(self):
        rospy.loginfo("======= 任务启动：等待识别 ID 0 =======")
        
        while not rospy.is_shutdown():
            tx, _ = self.fetch_tag_position(0)
            if tx is not None:
                rospy.loginfo(">> 发现 ID 0，开始向右搜寻 ID 1...")
                break
            rospy.sleep(0.5)

        # 搜索阶段
        found_id1 = False
        while not rospy.is_shutdown() and not found_id1:
            tx, ty = self.fetch_tag_position(1)
            if tx is not None:
                rospy.loginfo(f">> 捕捉到 ID 1，进入动态微调模式")
                found_id1 = True
            else:
                self.send_rotate_cmd(self.SEARCH_STEP_RAD)
                time.sleep(self.STEP_INTERVAL)

        # 动态微调阶段
        rospy.loginfo("======= 开始动态对齐 =======")
        while not rospy.is_shutdown():
            error = self.get_stable_yaw_error(1)
            if error is None:
                rospy.logwarn(">> 丢失目标")
                break
                
            deg_error = math.degrees(error)
            rospy.loginfo(f">> 当前偏差: {deg_error:.2f} 度")

            if abs(error) < self.CENTER_THRESHOLD_RAD:
                rospy.loginfo("======= 成功正对 ID 1 =======")
                break
            
            # 计算步长：采用比例控制，但限制在 [MIN, MAX] 之间
            # 这样在 22 度偏差时，它会走大约 5-8 度，而不是 1 度
            direction = 1 if error > 0 else -1
            
            # 计算建议步长 (这里取偏差的一半，但不超过MAX，不小于MIN)
            suggested_step = abs(error) * 0.6 
            actual_step = max(self.MIN_STEP_RAD, min(suggested_step, self.MAX_STEP_RAD))
            
            # 如果剩余总误差都很小了，就直接用误差值
            if abs(error) < actual_step:
                actual_step = abs(error)

            self.send_rotate_cmd(direction * actual_step)
            time.sleep(self.STEP_INTERVAL)

if __name__ == '__main__':
    try:
        task = KuavoAdaptiveAlignTask()
        task.main_logic()
    except rospy.ROSInterruptException:
        pass