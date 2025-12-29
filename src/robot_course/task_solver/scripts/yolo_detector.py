#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOLOv8物品检测节点
订阅相机图像，使用自定义训练的YOLOv8模型检测杯子、盘子、剪刀
"""

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from ultralytics import YOLO
import json


class YOLODetector:
    def __init__(self):
        rospy.init_node('yolo_detector', anonymous=True)
        
        # 加载参数
        self.model_path = rospy.get_param('~model_path', 'yolov8n.pt')
        self.confidence_threshold = rospy.get_param('~confidence_threshold', 0.5)
        self.image_topic = rospy.get_param('~image_topic', '/camera/color/image_raw')
        self.publish_image = rospy.get_param('~publish_image', True)
        
        # 加载YOLO模型
        rospy.loginfo(f"Loading YOLO model: {self.model_path}")
        try:
            self.model = YOLO(self.model_path)
            self.class_names = self.model.names  # 从模型获取类别名称
            rospy.loginfo("YOLO model loaded successfully")
            rospy.loginfo(f"Model classes: {self.class_names}")
        except Exception as e:
            rospy.logerr(f"Failed to load YOLO model: {e}")
            return
        
        self.bridge = CvBridge()
        
        # 订阅相机话题
        self.image_sub = rospy.Subscriber(
            self.image_topic,
            Image,
            self.image_callback,
            queue_size=1
        )
        
        # 发布检测结果（JSON格式）
        self.detection_pub = rospy.Publisher(
            '/yolo/detections',
            String,
            queue_size=10
        )
        
        # 发布可视化图像
        if self.publish_image:
            self.image_pub = rospy.Publisher(
                '/yolo/image_annotated',
                Image,
                queue_size=1
            )
        
        rospy.loginfo("YOLO detector initialized")
        rospy.loginfo(f"Subscribing to: {self.image_topic}")
        rospy.loginfo(f"Confidence threshold: {self.confidence_threshold}")
    
    def image_callback(self, msg):
        """处理图像消息"""
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(f"CV Bridge Error: {e}")
            return
        
        # YOLO检测
        results = self.model(cv_image, verbose=False)
        
        # 处理检测结果
        detections = self.process_results(results[0], cv_image)
        
        # 发布检测结果（即使为空也发布）
        detection_msg = String()
        detection_msg.data = json.dumps(detections)
        self.detection_pub.publish(detection_msg)
        
        # 发布可视化图像
        if self.publish_image:
            annotated_image = results[0].plot()
            try:
                image_msg = self.bridge.cv2_to_imgmsg(annotated_image, "bgr8")
                image_msg.header = msg.header
                self.image_pub.publish(image_msg)
            except CvBridgeError as e:
                rospy.logerr(f"Failed to publish annotated image: {e}")
    
    def process_results(self, result, image):
        """处理YOLO检测结果"""
        detections = []
        
        if result.boxes is None or len(result.boxes) == 0:
            rospy.loginfo_throttle(5.0, "No objects detected")
            return detections
        
        boxes = result.boxes.cpu().numpy()
        
        for box in boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            
            # 过滤置信度
            if conf < self.confidence_threshold:
                continue
            
            # 从模型获取类别名称
            class_name = self.class_names[cls_id]
            
            # 获取边界框坐标 (xyxy格式)
            x1, y1, x2, y2 = box.xyxy[0]
            
            # 计算中心点和尺寸
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2
            width = x2 - x1
            height = y2 - y1
            
            detection = {
                'class_name': class_name,
                'confidence': conf,
                'x_center': float(x_center),
                'y_center': float(y_center),
                'width': float(width),
                'height': float(height),
                'bbox': [float(x1), float(y1), float(x2), float(y2)]
            }
            
            detections.append(detection)
        
        # 注释掉频繁的检测日志，避免刷屏
        # if detections:
        #     rospy.loginfo(f"Detected {len(detections)} objects")
        #     for det in detections:
        #         rospy.loginfo(f"  {det['class_name']}: {det['confidence']:.2f}")
        
        return detections
    
    def run(self):
        rospy.loginfo("YOLO detector running...")
        rospy.spin()


if __name__ == '__main__':
    try:
        detector = YOLODetector()
        detector.run()
    except rospy.ROSInterruptException:
        pass
