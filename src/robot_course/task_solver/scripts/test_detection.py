#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试YOLO检测和抓取系统
"""

import rospy
from std_msgs.msg import String
import json


def detection_callback(msg):
    """打印检测结果"""
    try:
        detections = json.loads(msg.data)
        print("\n" + "="*50)
        print(f"检测到 {len(detections)} 个物品:")
        for i, det in enumerate(detections, 1):
            print(f"\n物品 {i}:")
            print(f"  类别: {det['class_name']}")
            print(f"  置信度: {det['confidence']:.2%}")
            print(f"  中心位置: ({det['x_center']:.1f}, {det['y_center']:.1f})")
            print(f"  尺寸: {det['width']:.1f} x {det['height']:.1f}")
        print("="*50)
    except json.JSONDecodeError as e:
        print(f"解析错误: {e}")


def main():
    rospy.init_node('test_detection', anonymous=True)
    
    print("等待YOLO检测结果...")
    print("订阅话题: /yolo/detections")
    print("按 Ctrl+C 退出\n")
    
    rospy.Subscriber('/yolo/detections', String, detection_callback)
    
    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
