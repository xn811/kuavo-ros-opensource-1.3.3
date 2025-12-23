#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
抓取服务客户端
用法:
    rosrun gazebo_ros_link_attacher grasp_client.py left grasp
    rosrun gazebo_ros_link_attacher grasp_client.py right grasp
    rosrun gazebo_ros_link_attacher grasp_client.py left release
    rosrun gazebo_ros_link_attacher grasp_client.py right release
"""

import rospy
import sys
from gazebo_ros_link_attacher.srv import Grasp, GraspRequest


def grasp_client(arm, action):
    """调用抓取服务"""
    rospy.init_node('grasp_client', anonymous=True)
    
    service_name = '/kuavo_attacher_node/grasp'
    rospy.loginfo("Waiting for service: %s", service_name)
    rospy.wait_for_service(service_name)
    
    try:
        grasp_srv = rospy.ServiceProxy(service_name, Grasp)
        
        req = GraspRequest()
        req.arm = arm
        req.action = action
        
        rospy.loginfo("Calling grasp service: arm=%s, action=%s", arm, action)
        resp = grasp_srv(req)
        
        if resp.ok:
            rospy.loginfo("Success: %s", resp.message)
            if resp.object_name:
                rospy.loginfo("Object: %s", resp.object_name)
            if resp.distance > 0:
                rospy.loginfo("Distance: %.3f m", resp.distance)
        else:
            rospy.logwarn("Failed: %s", resp.message)
        
        return resp.ok
        
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s", e)
        return False


def print_usage():
    print("Usage: grasp_client.py <arm> <action>")
    print("  arm: left | right")
    print("  action: grasp | release")
    print("")
    print("Examples:")
    print("  rosrun gazebo_ros_link_attacher grasp_client.py left grasp")
    print("  rosrun gazebo_ros_link_attacher grasp_client.py right release")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)
    
    arm = sys.argv[1].lower()
    action = sys.argv[2].lower()
    
    if arm not in ['left', 'right']:
        print("Error: arm must be 'left' or 'right'")
        print_usage()
        sys.exit(1)
    
    if action not in ['grasp', 'release']:
        print("Error: action must be 'grasp' or 'release'")
        print_usage()
        sys.exit(1)
    
    success = grasp_client(arm, action)
    sys.exit(0 if success else 1)
