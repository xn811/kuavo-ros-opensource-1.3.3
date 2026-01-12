#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整课程解决方案 - 整合抓取放置和搬箱子任务

流程：
0. (可选) 导航到识别点 (move_base)
1. 基于AprilTag的抓取放置任务 (grasp_demo.py)
2. 搬箱子任务 (grasp_box_course_solver.py)

用法:
  rosrun task_solver full_course_solver.py --sim
  rosrun task_solver full_course_solver.py --sim --skip_grasp  # 跳过抓取任务
  rosrun task_solver full_course_solver.py --sim --skip_box    # 跳过搬箱子任务
  
  # 先导航到识别点再抓取
  rosrun task_solver full_course_solver.py --nav_to_start --nav_x 1.0 --nav_y 2.0 --nav_z 0.0 --nav_w 1.0
"""

import rospy
import subprocess
import sys
import os
import argparse
import time
import actionlib
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


def navigate_to_start(args):
    """
    使用move_base导航到识别点
    """
    rospy.loginfo("=" * 50)
    rospy.loginfo("阶段0: 导航到识别点")
    rospy.loginfo("=" * 50)
    
    rospy.loginfo(f"目标位置: x={args.nav_x}, y={args.nav_y}")
    rospy.loginfo(f"目标朝向: z={args.nav_z}, w={args.nav_w}")
    
    # 连接move_base action server
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    rospy.loginfo("等待move_base服务...")
    
    if not client.wait_for_server(rospy.Duration(10.0)):
        rospy.logerr("❌ 无法连接move_base服务")
        return False
    
    rospy.loginfo("move_base服务已连接")
    
    # 构建目标
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = args.nav_x
    goal.target_pose.pose.position.y = args.nav_y
    goal.target_pose.pose.position.z = 0.0
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = args.nav_z
    goal.target_pose.pose.orientation.w = args.nav_w
    
    # 发送目标
    rospy.loginfo("发送导航目标...")
    client.send_goal(goal)
    
    # 等待结果
    finished = client.wait_for_result(rospy.Duration(120.0))  # 最多等待2分钟
    
    if finished:
        state = client.get_state()
        if state == actionlib.GoalStatus.SUCCEEDED:
            rospy.loginfo("✅ 导航到识别点完成")
            return True
        else:
            rospy.logerr(f"❌ 导航失败，状态码: {state}")
            return False
    else:
        rospy.logerr("❌ 导航超时")
        client.cancel_goal()
        return False


def run_grasp_demo(args):
    """
    运行抓取放置任务
    """
    rospy.loginfo("=" * 50)
    rospy.loginfo("阶段1: 开始抓取放置任务")
    rospy.loginfo("=" * 50)
    
    # 构建命令
    cmd = [
        "rosrun", "task_solver", "grasp_demo.py",
        "--use_apriltag",
        "--tag_id", str(args.grasp_tag_id),
        "--lateral_offset", str(args.lateral_offset),
        "--forward_offset", str(args.forward_offset),
        "--grasp_offset", str(args.grasp_offset),
        "--place_offset", str(args.place_offset),
        "--place_lateral_offset", str(args.place_lateral_offset),
        "--backward_distance", str(args.backward_distance),
        "--target", args.target,
        "--grasp_hand", args.grasp_hand,
        "--speed", str(args.speed),
        "--tolerance", str(args.tolerance),
    ]
    
    if args.lateral:
        cmd.append("--lateral")
    
    rospy.loginfo(f"执行命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        if result.returncode == 0:
            rospy.loginfo("✅ 抓取放置任务完成")
            return True
        else:
            rospy.logerr(f"❌ 抓取放置任务失败，返回码: {result.returncode}")
            return False
    except subprocess.CalledProcessError as e:
        rospy.logerr(f"❌ 抓取放置任务执行出错: {e}")
        return False
    except Exception as e:
        rospy.logerr(f"❌ 抓取放置任务异常: {e}")
        return False


def run_box_grasp(args):
    """
    运行搬箱子任务
    """
    rospy.loginfo("=" * 50)
    rospy.loginfo("阶段2: 开始搬箱子任务")
    rospy.loginfo("=" * 50)
    
    # 构建命令
    script_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
        "kuavo_humanoid_sdk", "examples", "strategies", "grasp_box_course_solver.py"
    )
    
    cmd = ["python3", script_path]
    
    if args.sim:
        cmd.append("--sim")
    
    if args.velocity_turn:
        cmd.append("--velocity-turn")
    
    if args.max_yaw_step is not None:
        cmd.extend(["--max-yaw-step", str(args.max_yaw_step)])
    
    rospy.loginfo(f"执行命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        if result.returncode == 0:
            rospy.loginfo("✅ 搬箱子任务完成")
            return True
        else:
            rospy.logerr(f"❌ 搬箱子任务失败，返回码: {result.returncode}")
            return False
    except subprocess.CalledProcessError as e:
        rospy.logerr(f"❌ 搬箱子任务执行出错: {e}")
        return False
    except Exception as e:
        rospy.logerr(f"❌ 搬箱子任务异常: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="完整课程解决方案")
    
    # 通用参数
    parser.add_argument("--sim", action="store_true", help="仿真模式")
    parser.add_argument("--skip_grasp", action="store_true", help="跳过抓取放置任务")
    parser.add_argument("--skip_box", action="store_true", help="跳过搬箱子任务")
    parser.add_argument("--wait_between", type=float, default=3.0,
                        help="两个任务之间的等待时间(秒)")
    
    # 导航到识别点参数
    parser.add_argument("--nav_to_start", action="store_true",
                        help="启用导航到识别点（使用move_base）")
    parser.add_argument("--nav_x", type=float, default=0.0,
                        help="识别点X坐标")
    parser.add_argument("--nav_y", type=float, default=0.0,
                        help="识别点Y坐标")
    parser.add_argument("--nav_z", type=float, default=0.0,
                        help="识别点朝向四元数z分量")
    parser.add_argument("--nav_w", type=float, default=1.0,
                        help="识别点朝向四元数w分量")
    
    # 抓取放置任务参数
    parser.add_argument("--target", type=str, default="cup", help="抓取目标")
    parser.add_argument("--grasp_tag_id", type=int, default=0, help="抓取用AprilTag ID")
    parser.add_argument("--lateral_offset", type=float, default=0.75,
                        help="物品横向偏移(正=右，负=左)")
    parser.add_argument("--forward_offset", type=float, default=0.0,
                        help="物品前向偏移")
    parser.add_argument("--grasp_offset", type=float, default=0.15,
                        help="抓取距离")
    parser.add_argument("--place_offset", type=float, default=0.32,
                        help="放置距离")
    parser.add_argument("--place_lateral_offset", type=float, default=-0.50,
                        help="放置点横向偏移")
    parser.add_argument("--backward_distance", type=float, default=0.5,
                        help="放置后后退距离")
    parser.add_argument("--grasp_hand", type=str, default="right",
                        choices=["left", "right", "auto"], help="抓取用手")
    parser.add_argument("--lateral", action="store_true", help="使用左右平移")
    parser.add_argument("--speed", type=float, default=0.1, help="移动速度")
    parser.add_argument("--tolerance", type=float, default=0.1, help="位置精度")
    
    # 搬箱子任务参数
    parser.add_argument("--velocity_turn", action="store_true", default=True,
                        help="使用速度控制转向（默认启用）")
    parser.add_argument("--no_velocity_turn", action="store_true",
                        help="禁用速度控制转向")
    parser.add_argument("--max_yaw_step", type=float, default=None,
                        help="单步最大转向角度")
    
    args = parser.parse_args()
    
    # 处理velocity_turn参数
    if args.no_velocity_turn:
        args.velocity_turn = False
    
    # 初始化ROS节点
    rospy.init_node('full_course_solver', anonymous=True)
    
    rospy.loginfo("=" * 60)
    rospy.loginfo("完整课程解决方案 - 开始执行")
    rospy.loginfo("=" * 60)
    rospy.loginfo(f"模式: {'仿真' if args.sim else '实物'}")
    rospy.loginfo(f"导航到识别点: {args.nav_to_start}")
    rospy.loginfo(f"跳过抓取: {args.skip_grasp}, 跳过搬箱子: {args.skip_box}")
    
    success = True
    
    # 阶段0: 导航到识别点（可选）
    if args.nav_to_start:
        if not navigate_to_start(args):
            rospy.logerr("导航到识别点失败，终止流程")
            success = False
        else:
            rospy.loginfo(f"等待 {args.wait_between} 秒后开始下一阶段...")
            time.sleep(args.wait_between)
    
    # 阶段1: 抓取放置任务
    if success and not args.skip_grasp:
        if not run_grasp_demo(args):
            rospy.logerr("抓取放置任务失败，终止流程")
            success = False
        else:
            rospy.loginfo(f"等待 {args.wait_between} 秒后开始下一阶段...")
            time.sleep(args.wait_between)
    else:
        rospy.loginfo("跳过抓取放置任务")
    
    # 阶段2: 搬箱子任务
    if success and not args.skip_box:
        if not run_box_grasp(args):
            rospy.logerr("搬箱子任务失败")
            success = False
    else:
        if args.skip_box:
            rospy.loginfo("跳过搬箱子任务")
    
    # 总结
    rospy.loginfo("=" * 60)
    if success:
        rospy.loginfo("✅ 完整课程任务全部完成!")
    else:
        rospy.logerr("❌ 课程任务执行过程中出现错误")
    rospy.loginfo("=" * 60)
    
    return 0 if success else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        rospy.loginfo("用户中断")
