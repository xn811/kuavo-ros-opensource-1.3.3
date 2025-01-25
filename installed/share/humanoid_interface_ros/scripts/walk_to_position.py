#!/usr/bin/env python3
import rospy
import numpy as np
import json
from pub_command import KuavoSDK
from std_msgs.msg import String
from humanoid_interface_ros.msg import uwbdebug
import argparse
from std_msgs.msg import Float64MultiArray

STEP = 0
VELOCITY = 1

reach_target_position = False
reach_target_orientation = False
goal_position = [0,0,0]
goal_orientation = [0,0,0]
velocity = 0
current_orientation_yaw = 0
stage = 1

class WalkToPositionWithTagByUWB:
    def __init__(self):
        rospy.init_node('walk_to_position', anonymous=True)
        self.robot_instance = KuavoSDK()
        self.robot_instance.connect()
        self.sub_current_pose = rospy.Subscriber('/uwb_filter_output', uwbdebug, next_action, queue_size=1)
        self.sub_current_yaw = rospy.Subscriber('/state_estimate/base/angular_zyx',Float64MultiArray,update_yaw, queue_size=1)
        rospy.spin()
        

def update_yaw(data):
    # rospy.loginfo("Recieved current orientation is: %s", data)
    global current_orientation_yaw
    current_orientation_yaw = data.data[0]

def next_action(data):
    global stage
    print(data)
    rospy.loginfo("Recieved current pose is: %s", data)
    msg = data
    current_position_x = msg.robot_uwb_fir_x
    current_position_y = msg.robot_uwb_fir_y
    
    # rpy = current_orientation_yaw*180/np.pi
    # rospy.loginfo("current_position is: %s", current_position)
    # rospy.loginfo("current_rpy is: %s", rpy)
    # rospy.loginfo("goal_position is: %s", goal_position)
    # rospy.loginfo("goal_orientation is: %s", goal_orientation)

    dx = goal_position[0] - current_position_x
    dy = goal_position[1] - current_position_y
    target_dir = np.arctan2(dy, dx)
    # print(f"dx:{dx}, dy:{dy}, target_dir:{target_dir}")
    diff_rot = target_dir - current_orientation_yaw
    # rospy.loginfo("diff_rot is: %s", diff_rot)
    if abs(diff_rot) > np.pi:
        diff_rot += 2 * np.pi if diff_rot < 0 else -2 * np.pi
    # print(f"1:{reach_target_position}")
    # print(f"2:{reach_target_orientation}")

    if stage == 1:
        print("------------------Stage 1--------------------")
        if abs(goal_position[0]-current_position_x) < 0.05 and abs(goal_position[1]-current_position_y) < 0.05:
            stage = 2
        else:
            if abs(diff_rot) < np.pi / 18:
                rospy.loginfo("Go ahead")
                robot_instance.publish_command(VELOCITY, 0.1, 0.0, 0.0, 0.0)
            elif diff_rot > 0:
                rospy.loginfo("Turn left")
                robot_instance.publish_command(VELOCITY, 0.0, 0.0, 0,0.4)
            else:
                rospy.loginfo("Turn right")
                robot_instance.publish_command(VELOCITY, 0.0, 0.0, 0,-0.4)
    elif stage == 2:
        print("------------------Stage 2--------------------")
        diff_yawl = goal_orientation[2] - current_orientation_yaw
        if abs(diff_yawl) < (np.pi/180)*5:
            print("Reach the target orientation")
            robot_instance.publish_command(VELOCITY, 0.0, 0.0, 0.0, 0.0)
            stage = 3
        else:
            if abs(diff_yawl) > np.pi:
                diff_yawl += 2 * np.pi if diff_yawl < 0 else -2 * np.pi
            elif diff_yawl > 0:
                rospy.loginfo("Reach the target position and Turn left")
                robot_instance.publish_command(VELOCITY, 0.0, 0.0,0, 0.4)
            else:
                rospy.loginfo("Reach the target position and Turn right")
                robot_instance.publish_command(VELOCITY, 0.0, 0.0, 0,-0.4)
    elif stage == 3:
        rospy.loginfo("Reach the target pose and stop")
        rospy.signal_shutdown("Shut down the walk_to_position node")  
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Walk to a specific position")
    parser.add_argument("--velocity", type=float, default=0.1, help="The velocity of the robot")
    parser.add_argument("--goal_position", nargs=3, type=float, default=[0.0, 0.0, 0.0], help="The goal position of the robot")
    parser.add_argument("--goal_orientation", nargs=3, type=float, default=[0.0, 0.0, 0.0], help="The goal orientation of the robot")
    args = parser.parse_args()

    velocity = 0.1
    goal_position = [1.86,2.9,0]
    goal_orientation = [0,0,0]
    rospy.init_node('walk_to_position', anonymous=True, disable_signals=False)
    rospy.loginfo("walk_to_position node is running")
    rospy.loginfo("set goal_position is: %s", goal_position)
    rospy.loginfo("set goal_orientation is: %s", goal_orientation)
    rospy.loginfo("set velocity is: %s", velocity)
    global robot_instance
    robot_instance = KuavoSDK()
    sub_current_pose = rospy.Subscriber('/uwb_filter_output', uwbdebug, next_action, queue_size=1)
    sub_current_yaw = rospy.Subscriber('/state_estimate/base/angular_zyx',Float64MultiArray,update_yaw, queue_size=1)
    rospy.spin()
    # while not rospy.is_shutdown():
    #     rospy.loginfo(current_orientation_yaw)
