#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从Gazebo仿真中采集图像数据集
用于训练自定义YOLO模型
"""

import rospy
import cv2
import os
import time
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from datetime import datetime


class DatasetCollector:
    def __init__(self):
        rospy.init_node('dataset_collector', anonymous=True)
        
        # 参数配置
        self.output_dir = rospy.get_param('~output_dir', '/root/kuavo_ws/src/robot_course/task_solver/dataset/images')
        self.image_topic = rospy.get_param('~image_topic', '/camera/color/image_raw')
        self.save_interval = rospy.get_param('~save_interval', 1.0)  # 保存间隔（秒）
        self.auto_mode = rospy.get_param('~auto_mode', False)  # 自动模式
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.bridge = CvBridge()
        self.latest_image = None
        self.image_count = 0
        self.last_save_time = time.time()
        
        # 订阅相机话题
        self.image_sub = rospy.Subscriber(
            self.image_topic,
            Image,
            self.image_callback,
            queue_size=1
        )
        
        rospy.loginfo("Dataset collector initialized")
        rospy.loginfo(f"Output directory: {self.output_dir}")
        rospy.loginfo(f"Image topic: {self.image_topic}")
        rospy.loginfo(f"Auto mode: {self.auto_mode}")
        
        if not self.auto_mode:
            rospy.loginfo("\n=== 手动模式 ===")
            rospy.loginfo("按 's' 保存当前图像")
            rospy.loginfo("按 'q' 退出")
            rospy.loginfo("按 'a' 切换到自动模式")
    
    def image_callback(self, msg):
        """接收图像"""
        try:
            self.latest_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(f"CV Bridge Error: {e}")
    
    def save_image(self):
        """保存当前图像"""
        if self.latest_image is None:
            rospy.logwarn("No image received yet")
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"img_{timestamp}.jpg"
        filepath = os.path.join(self.output_dir, filename)
        
        cv2.imwrite(filepath, self.latest_image)
        self.image_count += 1
        rospy.loginfo(f"Saved: {filename} (Total: {self.image_count})")
        return True
    
    def run_manual_mode(self):
        """手动模式：按键保存"""
        cv2.namedWindow('Dataset Collector', cv2.WINDOW_NORMAL)
        
        rate = rospy.Rate(30)  # 30 Hz
        
        while not rospy.is_shutdown():
            if self.latest_image is not None:
                # 显示图像
                display_img = self.latest_image.copy()
                
                # 添加文字提示
                cv2.putText(display_img, f"Images: {self.image_count}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(display_img, "Press 's' to save, 'q' to quit, 'a' for auto", 
                           (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                cv2.imshow('Dataset Collector', display_img)
                
                # 处理按键
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('s'):
                    self.save_image()
                elif key == ord('q'):
                    rospy.loginfo("Quitting...")
                    break
                elif key == ord('a'):
                    rospy.loginfo("Switching to auto mode...")
                    self.auto_mode = True
                    cv2.destroyAllWindows()
                    self.run_auto_mode()
                    break
            
            rate.sleep()
        
        cv2.destroyAllWindows()
    
    def run_auto_mode(self):
        """自动模式：定时保存"""
        rospy.loginfo(f"\n=== 自动模式 ===")
        rospy.loginfo(f"Save interval: {self.save_interval}s")
        rospy.loginfo("Press Ctrl+C to stop")
        
        rate = rospy.Rate(10)  # 10 Hz
        
        while not rospy.is_shutdown():
            current_time = time.time()
            
            if current_time - self.last_save_time >= self.save_interval:
                if self.save_image():
                    self.last_save_time = current_time
            
            rate.sleep()
    
    def run(self):
        """运行采集器"""
        rospy.loginfo("Waiting for images...")
        
        # 等待第一张图像
        while self.latest_image is None and not rospy.is_shutdown():
            rospy.sleep(0.1)
        
        rospy.loginfo("Image stream received, starting collection...")
        
        if self.auto_mode:
            self.run_auto_mode()
        else:
            self.run_manual_mode()
        
        rospy.loginfo(f"\nCollection finished. Total images: {self.image_count}")
        rospy.loginfo(f"Images saved to: {self.output_dir}")


if __name__ == '__main__':
    try:
        collector = DatasetCollector()
        collector.run()
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        rospy.loginfo("\nInterrupted by user")
