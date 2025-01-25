#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import String
import json
from datetime import datetime
from geometry_msgs.msg import Twist

LEFT_RIGHT_TRIGGER = 6
FORWARD_BACK_TRIGGER = 7
RIGHT_STICK_YAW = 3
RIGHT_STICK_Z = 4


GAIT_STANCE = 0
GAIT_TROT = 1
GAIT_WALK = 3

POSE = 0
VELOCITY = 1

tag = 0

class KuavoSDK:
    def __init__(self):
        self.pub_joy = rospy.Publisher('/joy', Joy, queue_size=10)
        self.pub_pose = rospy.Publisher('/my_target_pose', String, queue_size=10)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.pub_torso_pose = rospy.Publisher('/cmd_pose', Twist, queue_size=10)
        rospy.sleep(2)



    def publish_command(self,mode,x,y,z,yaw):
        if mode == POSE:
            # target_pose_msg_json = {
            #     "x" : x,
            #     "y" : y,
            #     "z" : z,
            #     "yaw" : yaw
            # }
            # self.pub_pose.publish(json.dumps(target_pose_msg_json))
            twist = Twist()
            # 发布torso的位姿
            twist.linear.x = x  
            twist.linear.y = y  
            twist.linear.z = z 
            twist.angular.z = yaw  
            self.pub_torso_pose.publish(twist)

        elif mode == VELOCITY:
            twist = Twist()
            twist.linear.x = x  # 线速度，沿x轴
            twist.linear.y = y  # 线速度，沿y轴
            twist.linear.z = z  # 线速度，沿z轴
            twist.angular.z = yaw  # 角rate = rospy.Rate(10)  # 设置发布频率
            self.pub.publish(twist)
            
    def switch_gait(self,gait):
        # rospy.sleep(1)
        joy_msg = Joy()
        joy_msg.axes = [0.0] * 8  # 初始化8个轴
        joy_msg.buttons = [0] * 11  # 初始化11个按钮
        joy_msg.buttons[gait] = 1
        self.pub_joy.publish(joy_msg)


if __name__ == '__main__':
    rospy.init_node('test_gait_switch')
    KuavoSDK = KuavoSDK()
    rospy.Rate(10)
    KuavoSDK.publish_command(POSE, 0.9,0,0,0)
    