#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from kuavo_msgs.srv import changeArmCtrlMode, changeArmCtrlModeRequest
from kuavo_msgs.msg import armTargetPoses
from gazebo_ros_link_attacher.srv import Grasp, GraspRequest

def set_arm_control_mode(mode):
    """
    设置OCS2手臂控制模式。
    - 0: keep pose 保持姿势 
    - 1: auto_swing_arm 行走时自动摆手
    - 2: external_control 外部控制
    """
    try:
        arm_traj_change_mode_client = rospy.ServiceProxy("/arm_traj_change_mode", changeArmCtrlMode)
        request = changeArmCtrlModeRequest()
        request.control_mode = mode
        response = arm_traj_change_mode_client(request)

        if response.result:
            rospy.loginfo("Successfully changed arm control mode to %d: %s", mode, response.message)
        else:
            rospy.logwarn("Failed to change arm control mode to %d: %s", mode, response.message)

    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s", e)

def publish_arm_target_poses(times, values):
    """
    发布手臂目标姿态到指定话题。
    """
    pub = rospy.Publisher('kuavo_arm_target_poses', armTargetPoses, queue_size=10)
    rospy.sleep(0.5)
    
    msg = armTargetPoses()
    msg.times = times
    msg.values = values

    rospy.loginfo("正在将手臂目标姿态发布到话题 'kuavo_arm_target_poses'")

    rate = rospy.Rate(10)
    while pub.get_num_connections() == 0 and not rospy.is_shutdown():
        rospy.loginfo("等待订阅者连接...")
        rate.sleep()

    pub.publish(msg)
    rospy.loginfo("消息已发布。")

def grasp(arm, action):
    """
    调用抓取服务
    :param arm: "left" 或 "right"
    :param action: "grasp" 或 "release"
    :return: (success, message, object_name)
    """
    service_name = '/kuavo_attacher_node/grasp'
    rospy.wait_for_service(service_name)
    
    try:
        grasp_srv = rospy.ServiceProxy(service_name, Grasp)
        req = GraspRequest()
        req.arm = arm
        req.action = action
        
        resp = grasp_srv(req)
        
        if resp.ok:
            rospy.loginfo("Grasp %s successful: %s (object: %s, distance: %.3f m)", 
                         action, resp.message, resp.object_name, resp.distance)
        else:
            rospy.logwarn("Grasp %s failed: %s", action, resp.message)
        
        return resp.ok, resp.message, resp.object_name
        
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s", e)
        return False, str(e), ""

def main():
    rospy.init_node('grasp_cup_test', anonymous=True)

    # 设置手臂为外部控制模式
    set_arm_control_mode(2)
    
    # 手臂运动到初始位置
    publish_arm_target_poses([3], [20, 0, 0, -30, 0, 0, 0, 20, -90, 0, -30, 0, 0, 0])
    rospy.sleep(5.0)
    
    # 手臂运动到中间位置
    publish_arm_target_poses([3], [20, 0, 0, -30, 0, 0, 0, 20, 0, 0, -110, 0, 0, 0])
    rospy.sleep(5.0)
    
    # 手臂运动到抓取位置
    publish_arm_target_poses([3], [20, 0, 0, -30, 0, 0, 0, -68, -5, 0, 0, 0, 0, 0])
    rospy.sleep(5.0)

    # 使用新的grasp服务进行右手抓取
    success, message, obj_name = grasp("right", "grasp")
    
    if success:
        rospy.loginfo("成功抓取物品: %s", obj_name)
        
        # 抬起手臂
        publish_arm_target_poses([3], [20, 0, 0, -30, 0, 0, 0, 20, 0, 0, -110, 0, 0, 0])
        rospy.sleep(5.0)
        
        # 可选：释放物品

















    else:
        rospy.logwarn("抓取失败: %s", message)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
