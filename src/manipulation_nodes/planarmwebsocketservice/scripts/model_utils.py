#!/usr/bin/env python
import rospy
import rospkg
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from kuavo_msgs.msg import yoloOutputData, yoloDetection

import argparse
import cv2
import torch
import torchvision.transforms as transforms 
from ultralytics import YOLO
import numpy
import threading


class YOLO_detection:
    def __init__(self):
        self.bridge = CvBridge()
        self.latest_image = None
        self.lock = threading.Lock()

        self.yolo_detections_pub = None

    def load_model(self, model_path):
        try:
            model = YOLO(model_path)
            print(f"Model loaded successfully from {model_path}")
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None

    def detect_objects(self, model):
        with self.lock:
            image = self.latest_image.copy() if self.latest_image is not None else None

        if image is not None:
            results = None
            results = model.predict(image, show = True, verbose = False)
            return results
        else:
            rospy.loginfo("No Camera Image...")
            return None

    def init_ros_node(self):
        rospy.init_node('YOLO_detection', anonymous=True)
        rospy.Subscriber("/camera/color/image_raw", Image, self.image_callback)
        self.yolo_detections_pub = rospy.Publisher('/model_output_data', yoloDetection, queue_size=1, tcp_nodelay=True)

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            with self.lock:
                self.latest_image = cv_image
        except CvBridgeError as e:
            rospy.logerr("CvBridge Error: {0}".format(e))
            return

    def node_spin(self):
        rospy.spin()

    def node_is_shutdown(self):
        return rospy.is_shutdown()

    def tensor_to_msg(self, results):
        if not results:
            return None
        else:
            yolo_detections = yoloDetection()
            for result in results:
                boxes = result.boxes.cpu().numpy()

                xywh = boxes.xywh  # center-x(i,0), center-y(i,1), width(i,2), height(i,3)
                names = [result.names[cls.item()] for cls in result.boxes.cls.int()]  # class name of each box
                confs = boxes.conf  # confidence score of each box

                for i in range(len(xywh)):
                    yolo_output_data = yoloOutputData(object_class=names[i], confidence=confs[i], x_pos=xywh[i][0], y_pos=xywh[i][1], height=xywh[i][2], width=xywh[i][3])
                    yolo_detections.data.append(yolo_output_data)
            return yolo_detections

    def show_results(self, results):
        if not results:
            print("No results to show.")
        else:
            yolo_detections = self.tensor_to_msg(results)
            print(yolo_detections)

    def publish_results(self, results):
        if not results:
            print("No results to publish.")
        else:
            yolo_detections = self.tensor_to_msg(results)
            self.yolo_detections_pub.publish(yolo_detections)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='LOAD YOLO model path')
    parser.add_argument('--model_path', type=str, default="")
    args = parser.parse_args()
    
    yolo_detection = YOLO_detection()

    yolo_detection.init_ros_node()

    model = yolo_detection.load_model(args.model_path)

    rate = rospy.Rate(20)
    
    while not yolo_detection.node_is_shutdown():

        results = yolo_detection.detect_objects(model)

        yolo_detection.show_results(results)

        yolo_detection.publish_results(results)

        rate.sleep() 
