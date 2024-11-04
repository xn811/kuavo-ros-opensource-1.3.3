#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import sys
import os
import json
import time
import signal
import rospy
import tf
import numpy as np
import math
from pprint import pprint
from kuavo_ros_interfaces.msg import robotHeadMotionData
from noitom_hi5_hand_udp_python.msg import PoseInfoList, PoseInfo, JoySticks
from geometry_msgs.msg import Point, Quaternion

# Add the parent directory to the system path to allow relative imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Import the hand_pose_pb2 module
import protos.hand_pose_pb2 as event_pb2

class Quest3BoneFramePublisher:
    def __init__(self):
        self.bone_names = [
            "LeftArmUpper", "LeftArmLower", "RightArmUpper", "RightArmLower",
            "LeftHandPalm", "RightHandPalm", "LeftHandThumbMetacarpal",
            "LeftHandThumbProximal", "LeftHandThumbDistal", "LeftHandThumbTip",
            "LeftHandIndexTip", "LeftHandMiddleTip", "LeftHandRingTip",
            "LeftHandLittleTip", "RightHandThumbMetacarpal", "RightHandThumbProximal",
            "RightHandThumbDistal", "RightHandThumbTip", "RightHandIndexTip",
            "RightHandMiddleTip", "RightHandRingTip", "RightHandLittleTip",
            "Root", "Chest", "Neck", "Head"
        ]
        
        self.bone_name_to_index = {name: index for index, name in enumerate(self.bone_names)}
        self.index_to_bone_name = {index: name for index, name in enumerate(self.bone_names)}
        
        self.current_file_dir = os.path.dirname(os.path.abspath(__file__))
        self.CONFIG_FILE = os.path.join(self.current_file_dir, "config.json")
        self.calibrated_head_quat_matrix_inv = None
        self.head_motion_range = self.get_head_motion_range()
        
        self.sock = None
        self.server_address = None
        self.port = None
        
        rospy.init_node('Quest3_bone_frame_publisher', anonymous=True)
        self.rate = rospy.Rate(100.0)
        
        self.br = tf.TransformBroadcaster()
        self.pose_pub = rospy.Publisher('/leju_quest_bone_poses', PoseInfoList, queue_size=10)
        self.head_data_pub = rospy.Publisher('/robot_head_motion_data', robotHeadMotionData, queue_size=10)
        self.joysticks_pub = rospy.Publisher('quest_joystick_data', JoySticks, queue_size=10)
        
        signal.signal(signal.SIGINT, self.signal_handler)

    def load_config(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {}

    def save_config(self, config):
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)

    def get_head_motion_range(self):
        config = self.load_config()
        return config.get("head_motion_range", None)

    def signal_handler(self, sig, frame):
        print('Exiting gracefully...')
        if self.sock:
            self.sock.close()
        sys.exit(0)

    def setup_socket(self, server_address, port):
        self.server_address = (server_address, port)
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1)
        return (server_address, port)

    def send_initial_message(self):
        message = b'hi'
        max_retries = 200
        for attempt in range(max_retries):
            try:
                self.sock.sendto(message, self.server_address)
                self.sock.recvfrom(1024)
                print(f"Acknowledgment received on attempt {attempt + 1}, start to receiving data...")
                return True
            except socket.timeout:
                print(f"Attempt {attempt + 1} timed out. Retrying...")
            except KeyboardInterrupt:
                print("Force quit by Ctrl-c.")
                self.signal_handler(signal.SIGINT, None)
        print("Failed to send message after 200 attempts.")
        return False

    def convert_position_to_right_hand(self, left_hand_position):
        return {
            "x": 0 - left_hand_position["z"],
            "y": 0 - left_hand_position["x"],
            "z": left_hand_position["y"]
        }

    def convert_quaternion_to_right_hand(self, left_hand_quat):
        return (
            0 - left_hand_quat[2],
            0 - left_hand_quat[0],
            left_hand_quat[1],
            left_hand_quat[3]
        )

    def updateAFrame(self, frame_name, frame_position, frame_rotation_quat, time_now):
        self.br.sendTransform((frame_position["x"], frame_position["y"], frame_position["z"]), 
                              frame_rotation_quat, time_now, frame_name, "torso")

    def normalize_degree_in_180(self, degree):
        if degree > 180:
            degree -= 180
        elif degree < -180:
            degree += 180
        return degree

    def pub_head_motion_data(self, cur_quat):
        if self.calibrated_head_quat_matrix_inv is None:
            calibrated_head_quat_matrix = tf.transformations.quaternion_matrix(cur_quat)
            self.calibrated_head_quat_matrix_inv = tf.transformations.inverse_matrix(calibrated_head_quat_matrix)
        else:
            current_quat_matrix = tf.transformations.quaternion_matrix(cur_quat)
            relative_quat_matrix = tf.transformations.concatenate_matrices(self.calibrated_head_quat_matrix_inv, current_quat_matrix)
            relative_quat = tf.transformations.quaternion_from_matrix(relative_quat_matrix)
            rpy = tf.transformations.euler_from_quaternion(relative_quat)
            rpy_deg = [r * 180 / math.pi for r in rpy]
            pitch = max(min(self.normalize_degree_in_180(round(rpy_deg[0], 2)), self.head_motion_range["pitch"][1]), self.head_motion_range["pitch"][0])
            yaw = max(min(self.normalize_degree_in_180(round(rpy_deg[1], 2)), self.head_motion_range["yaw"][1]), self.head_motion_range["yaw"][0])
            msg = robotHeadMotionData()
            msg.joint_data = [yaw , pitch]
            self.head_data_pub.publish(msg)

    def run(self):
        loop_count = 0
        while not rospy.is_shutdown():
            try:
                loop_count += 1
                data, _ = self.sock.recvfrom(4096)
                event = event_pb2.LejuHandPoseEvent()
                event.ParseFromString(data)
                
                time_now = rospy.Time.now()
                pose_info_list = PoseInfoList()
                joysticks_msg = JoySticks()
                
                # Process joystick data
                self.process_joystick_data(event, joysticks_msg, loop_count)
                
                # Process pose data
                self.process_pose_data(event, pose_info_list, time_now)
                
                # Publish data
                pose_info_list.timestamp_ms = event.timestamp
                pose_info_list.is_high_confidence = event.IsDataHighConfidence
                pose_info_list.is_hand_tracking = event.IsHandTracking
                self.pose_pub.publish(pose_info_list)
                
                self.rate.sleep()
            except socket.timeout:
                print('Timeout occurred, no data received. Restarting socket...')
                if not self.restart_socket():
                    break
            except Exception as e:
                print(f'An error occurred: {e}')
                if not self.restart_socket():
                    break

    def process_joystick_data(self, event, joysticks_msg, loop_count):
        joysticks_msg.left_x = event.left_joystick.x
        joysticks_msg.left_y = event.left_joystick.y
        joysticks_msg.left_trigger = event.left_joystick.trigger
        joysticks_msg.left_grip = event.left_joystick.grip
        joysticks_msg.left_first_button_pressed = event.left_joystick.firstButtonPressed
        joysticks_msg.left_second_button_pressed = event.left_joystick.secondButtonPressed
        joysticks_msg.left_first_button_touched = event.left_joystick.firstButtonTouched
        joysticks_msg.left_second_button_touched = event.left_joystick.secondButtonTouched
        joysticks_msg.right_x = event.right_joystick.x
        joysticks_msg.right_y = event.right_joystick.y
        joysticks_msg.right_trigger = event.right_joystick.trigger
        joysticks_msg.right_grip = event.right_joystick.grip
        joysticks_msg.right_first_button_pressed = event.right_joystick.firstButtonPressed
        joysticks_msg.right_second_button_pressed = event.right_joystick.secondButtonPressed
        joysticks_msg.right_first_button_touched = event.right_joystick.firstButtonTouched
        joysticks_msg.right_second_button_touched = event.right_joystick.secondButtonTouched
        # if loop_count % 20 == 0:
            # rospy.loginfo(joysticks_msg)
        self.joysticks_pub.publish(joysticks_msg)

    def process_pose_data(self, event, pose_info_list, time_now):
        scale_factor = {"x": 3.0, "y": 3.0, "z": 3.0}
        for i, pose in enumerate(event.poses):
            bone_name = self.index_to_bone_name[i]
            frame_position = {"x": pose.position.x, "y": pose.position.y, "z": pose.position.z}
            frame_rotation_quat = (pose.quaternion.x, pose.quaternion.y, pose.quaternion.z, pose.quaternion.w)
            
            right_hand_position = self.convert_position_to_right_hand(frame_position)
            right_hand_quat = self.convert_quaternion_to_right_hand(frame_rotation_quat)
            
            pose_info = PoseInfo()
            pose_info.position = Point(x=right_hand_position["x"], y=right_hand_position["y"], z=right_hand_position["z"])
            pose_info.orientation = Quaternion(x=right_hand_quat[0], y=right_hand_quat[1], z=right_hand_quat[2], w=right_hand_quat[3])
            pose_info_list.poses.append(pose_info)
            
            for axis in ["x", "y", "z"]:
                right_hand_position[axis] *= scale_factor[axis]
            
            self.updateAFrame(bone_name, right_hand_position, right_hand_quat, time_now)
            
            if bone_name == "Head":
                self.pub_head_motion_data(right_hand_quat)

    def restart_socket(self):
        print("Restarting socket connection...")
        self.sock.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1)
        if not self.send_initial_message():
            print("Failed to restart socket connection.")
            return False
        print("Socket connection restarted successfully.")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2 or "." not in sys.argv[1]:
        print("Usage: python test_unity.py <server_address[:port]> ")
        sys.exit(1)

    try:
        if ':' in sys.argv[1]:
            server_address, port = sys.argv[1].split(':')
            port = int(port)
        else:
            server_address = sys.argv[1]
            port = 10019
    except ValueError:
        print("Argument must be in the format <server_address[:port]> and port must be an integer")
        sys.exit(1)

    publisher = Quest3BoneFramePublisher()
    publisher.setup_socket(server_address, port)
    if publisher.send_initial_message():
        publisher.run()
    else:
        print("Failed to establish initial connection.")
