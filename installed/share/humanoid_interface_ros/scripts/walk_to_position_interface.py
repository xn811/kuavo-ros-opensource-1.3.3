#!/usr/bin/env python3
import rospy
import numpy as np
from pub_command import KuavoSDK
from humanoid_interface_ros.msg import uwbdebug
from std_msgs.msg import Float64MultiArray
from apriltag_ros.msg import AprilTagDetectionArray, AprilTagDetection


POSE = 0
VELOCITY = 1

TAG_ID = 2

reach_target_position = False
reach_target_orientation = False
goal_position = [0,0,0]
goal_orientation = [0,0,0]
velocity = 0
current_orientation_yaw = 0
stage = 1

class WalkToPositionWithTagByUWB:
    def __init__(self):

        self.robot_instance_ = KuavoSDK()
        self.apriltag_ = AprilTagDetection() # 识别到的_apritag位置信息
        self.has_apriltag_ = False  # 已识别到 apriltag
        self.tag_position_ = None # apriltag位置信息
        

    def update_yaw(self,data):
        # rospy.loginfo("Recieved current orientation is: %s", data)
        global current_orientation_yaw
        current_orientation_yaw = data.data[0]
    
    def tag_callback(self,msg):

        if not msg.detections:
            self.has_apriltag_ = False
            rospy.logwarn("No apriltag detected")
            return
        
        for detection in msg.detections:
            if detection.id[0] == TAG_ID:
                self.apriltag_ = detection
                self.tag_position_ = self.apriltag_.pose.pose.pose.position
                print(self.tag_position_)
                self.has_apriltag_ = True
                break
        
        if not self.has_apriltag_:
            rospy.logwarn(f"No apriltag with ID {TAG_ID} detected")


    def next_action(self,data):
        global stage
        print(data)
        rospy.loginfo("Recieved current pose is: %s", data)
        msg = data
        current_position_x = msg.robot_uwb_fir_x
        current_position_y = msg.robot_uwb_fir_y

        dx = goal_position[0] - current_position_x
        dy = goal_position[1] - current_position_y
        target_dir = np.arctan2(dy, dx)
        diff_rot = target_dir - current_orientation_yaw
        if abs(diff_rot) > np.pi:
            diff_rot += 2 * np.pi if diff_rot < 0 else -2 * np.pi

        if stage == 1:
            print("------------------Stage 1--------------------")
            if abs(goal_position[0]-current_position_x) < 0.05 and abs(goal_position[1]-current_position_y) < 0.05:
                stage = 2
            else:
                if abs(diff_rot) < np.pi / 18:
                    rospy.loginfo("Go ahead")
                    self.robot_instance_.publish_command(VELOCITY, 0.1, 0.0, 0.0, 0.0)
                elif diff_rot > 0:
                    rospy.loginfo("Turn left")
                    self.robot_instance_.publish_command(VELOCITY, 0.0, 0.0, 0,0.3)
                else:
                    rospy.loginfo("Turn right")
                    self.robot_instance_.publish_command(VELOCITY, 0.0, 0.0, 0,-0.3)
        elif stage == 2:
            print("------------------Stage 2--------------------")
            diff_yawl = goal_orientation[2] - current_orientation_yaw
            if abs(diff_yawl) < (np.pi/180)*5:
                print("Reach the target orientation")
                self.robot_instance_.publish_command(VELOCITY, 0.0, 0.0, 0.0, 0.0)
                stage = 3
            else:
                if abs(diff_yawl) > np.pi:
                    diff_yawl += 2 * np.pi if diff_yawl < 0 else -2 * np.pi
                elif diff_yawl > 0:
                    rospy.loginfo("Reach the target position and Turn left")
                    self.robot_instance_.publish_command(VELOCITY, 0.0, 0.0,0, 0.3)
                else:
                    rospy.loginfo("Reach the target position and Turn right")
                    self.robot_instance_.publish_command(VELOCITY, 0.0, 0.0, 0,-0.3)
        elif stage == 3:
            rospy.loginfo("Move according to the tag")
            if not self.has_apriltag_ or self.tag_position_ == None:
                return
            if tag_x < 0.05 and tag_y < 0.05:
                stage = 4
                return 
            tag_x = self.tag_position_.x
            tag_y = self.tag_position_.y
            tag_z = self.tag_position_.z
            self.robot_instance_.publish_command(POSE, tag_x, tag_y,0, 0.0)

        elif stage == 4:
            rospy.loginfo("Reach the target pose and stop")
            rospy.signal_shutdown("Shut down the walk_to_position node")  
    

if __name__ == '__main__':
    rospy.init_node('walk_to_position', anonymous=True)
    robot_walk_to_position = WalkToPositionWithTagByUWB()
    sub_current_pose = rospy.Subscriber('/uwb_filter_output', uwbdebug, robot_walk_to_position.next_action, queue_size=1)
    sub_current_yaw = rospy.Subscriber('/state_estimate/base/angular_zyx',Float64MultiArray,robot_walk_to_position.update_yaw, queue_size=1)
    sub_tag_pose = rospy.Subscriber("/robot_tag_info", AprilTagDetectionArray, robot_walk_to_position.tag_callback, queue_size=1)
    rospy.spin()
