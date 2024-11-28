#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import rospy
import argparse
import argparse
from std_msgs.msg import Float32, Float32MultiArray
from sensor_msgs.msg import JointState
from handcontrollerdemorosnode.msg import armPoseWithTimeStamp, robotHandPosition
import time
import math
import sys
import struct
import threading
import ctypes      




control_robot_hand_position_pub = rospy.Publisher(
            "control_robot_hand_position", robotHandPosition, queue_size=10
        )


if __name__ == "__main__":
    rospy.init_node("diff_ik_node", anonymous=True)
    control_robot_hand_position_pub = rospy.Publisher(
                "control_robot_hand_position", robotHandPosition, queue_size=10
            )
    
    while not rospy.is_shutdown():

        left_hand_position = [20 for i in range(6)]
        right_hand_position = [20 for i in range(6)]
        left_hand_position[0] = 100
        right_hand_position[0] = 100
        left_hand_position[1] = 0
        right_hand_position[1] = 0
        robot_hand_position = robotHandPosition()
        robot_hand_position.header.stamp = rospy.Time.now()

            
        robot_hand_position.left_hand_position = left_hand_position
        robot_hand_position.right_hand_position = right_hand_position
        control_robot_hand_position_pub.publish(robot_hand_position)