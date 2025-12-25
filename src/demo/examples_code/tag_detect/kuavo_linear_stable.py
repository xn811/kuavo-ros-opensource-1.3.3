#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import numpy as np
from sensor_msgs.msg import Joy
from apriltag_ros.msg import AprilTagDetectionArray

class KuavoOffsetAligner:
    def __init__(self):
        rospy.init_node('kuavo_offset_aligner', anonymous=True)

        self.tag_topic = "/tag_detections"
        self.joy_pub = rospy.Publisher('/joy', Joy, queue_size=1) 

        self.TARGET_ID = 3
        
        # === 关键参数修改区 ===
        # 请观察：当你觉得机器人物理上已经对准了 ID 3 时，屏幕显示的 Y 是多少？
        # 假设那个数值是 0.35，我们就填 0.35
        self.Y_TARGET = 0.35      
        self.LAT_TOL = 0.02       # 允许 2cm 的误差
        
        self.MAX_SPEED = 0.30     # 降低最大速度，防止冲过头
        self.MIN_SPEED = 0.18     # 最小维持速度
        self.is_running = True

    def init_joy(self):
        msg = Joy()
        msg.axes = [0.0] * 8
        msg.buttons = [0] * 11
        return msg

    def stop_and_stance(self):
        self.is_running = False
        rospy.loginfo("\n[刹车] 达到补偿目标，强制切换站立...")
        stop_msg = self.init_joy()
        stop_msg.buttons[0] = 1 # C键
        for _ in range(25):
            self.joy_pub.publish(stop_msg)
            rospy.sleep(0.04)

    def get_tag_y(self):
        try:
            msg = rospy.wait_for_message(self.tag_topic, AprilTagDetectionArray, timeout=0.2)
            for d in msg.detections:
                tag_id = d.id[0] if hasattr(d.id, '__iter__') else d.id
                if tag_id == self.TARGET_ID:
                    p = d.pose.pose.pose.position
                    # 实时计算当前值与目标值的偏差
                    error = p.y - self.Y_TARGET
                    print(f"\r[监控] 当前Y:{p.y:.3f} | 目标:{self.Y_TARGET:.3f} | 偏差:{error:+.3f}m", end='', flush=True)
                    return p.y
        except:
            return None
        return None

    def run(self):
        rospy.on_shutdown(self.stop_and_stance)
        
        y_start = self.get_tag_y()
        if y_start is None:
            rospy.logerr("\n找不到 ID 3")
            return

        # 激活行走模式
        walk_msg = self.init_joy()
        walk_msg.buttons[3] = 1 # R键
        for _ in range(10):
            self.joy_pub.publish(walk_msg)
            rospy.sleep(0.05)

        rate = rospy.Rate(10)
        while not rospy.is_shutdown() and self.is_running:
            current_y = self.get_tag_y()
            if current_y is None: continue

            # 计算相对于目标的偏差
            error = current_y - self.Y_TARGET

            # 如果偏差足够小，就停下
            if abs(error) <= self.LAT_TOL:
                rospy.loginfo("\n[成功] 已对齐到补偿位置！")
                break
            
            # 或者：如果原本在目标左边，现在跑到了目标右边（符号翻转），也立即停下
            # 这能有效防止“走过头”
            
            joy_cmd = self.init_joy()
            # 比例控制：error 为正说明还没到目标（需要继续向右走，发负速度）
            cmd_y = np.clip(error * -1.5, -self.MAX_SPEED, self.MAX_SPEED)

            if abs(cmd_y) < self.MIN_SPEED:
                cmd_y = self.MIN_SPEED if cmd_y > 0 else -self.MIN_SPEED
            
            joy_cmd.axes[0] = cmd_y
            self.joy_pub.publish(joy_cmd)
            rate.sleep()

        self.stop_and_stance()

if __name__ == '__main__':
    try:
        KuavoOffsetAligner().run()
    except rospy.ROSInterruptException:
        pass