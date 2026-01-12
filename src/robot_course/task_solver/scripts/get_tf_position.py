#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TF位置查询工具
获取两个坐标系之间的相对位置

用法:
    rosrun task_solver get_tf_position.py base_link zarm_l7_link
    rosrun task_solver get_tf_position.py base_link zarm_r7_link
    rosrun task_solver get_tf_position.py --monitor base_link zarm_l7_link  # 持续监控
"""

import rospy
import tf2_ros
import argparse
import sys


def get_transform(tf_buffer, base_frame, target_frame, timeout=2.0):
    """
    获取target_frame相对于base_frame的变换
    :param tf_buffer: TF2缓冲区
    :param base_frame: 基坐标系
    :param target_frame: 目标坐标系
    :param timeout: 超时时间
    :return: (position, rotation) 或 None
    """
    try:
        transform = tf_buffer.lookup_transform(
            base_frame, 
            target_frame, 
            rospy.Time(0),  # 获取最新的变换
            rospy.Duration(timeout)
        )
        
        pos = transform.transform.translation
        rot = transform.transform.rotation
        
        return {
            'position': {'x': pos.x, 'y': pos.y, 'z': pos.z},
            'rotation': {'x': rot.x, 'y': rot.y, 'z': rot.z, 'w': rot.w}
        }
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, 
            tf2_ros.ExtrapolationException) as e:
        rospy.logerr(f"TF查询失败: {e}")
        return None


def print_transform(base_frame, target_frame, transform):
    """打印变换信息"""
    pos = transform['position']
    rot = transform['rotation']
    
    print(f"\n{'='*50}")
    print(f"坐标系变换: {target_frame} 相对于 {base_frame}")
    print(f"{'='*50}")
    print(f"位置 (Position):")
    print(f"  x: {pos['x']:.6f} m")
    print(f"  y: {pos['y']:.6f} m")
    print(f"  z: {pos['z']:.6f} m")
    print(f"\n四元数 (Quaternion):")
    print(f"  x: {rot['x']:.6f}")
    print(f"  y: {rot['y']:.6f}")
    print(f"  z: {rot['z']:.6f}")
    print(f"  w: {rot['w']:.6f}")
    print(f"\nPython字典格式:")
    print(f"  {{'x': {pos['x']:.5f}, 'y': {pos['y']:.5f}, 'z': {pos['z']:.5f}}}")
    print(f"{'='*50}\n")


def monitor_transform(tf_buffer, base_frame, target_frame, rate_hz=1.0):
    """持续监控变换"""
    rate = rospy.Rate(rate_hz)
    
    print(f"\n持续监控: {target_frame} 相对于 {base_frame}")
    print("按 Ctrl+C 退出\n")
    print(f"{'时间':<12} {'X':>10} {'Y':>10} {'Z':>10}")
    print("-" * 45)
    
    while not rospy.is_shutdown():
        transform = get_transform(tf_buffer, base_frame, target_frame, timeout=1.0)
        if transform:
            pos = transform['position']
            time_str = rospy.Time.now().to_sec() % 1000  # 只显示秒的后几位
            print(f"{time_str:>10.2f}s {pos['x']:>10.4f} {pos['y']:>10.4f} {pos['z']:>10.4f}")
        rate.sleep()


def list_frames(tf_buffer):
    """列出所有可用的坐标系"""
    try:
        # 等待TF树建立
        rospy.sleep(1.0)
        
        # 获取所有frame
        frames = tf_buffer.all_frames_as_yaml()
        print("\n可用的坐标系:")
        print("-" * 30)
        print(frames)
    except Exception as e:
        rospy.logerr(f"获取坐标系列表失败: {e}")


def main():
    parser = argparse.ArgumentParser(description="TF位置查询工具")
    parser.add_argument("base_frame", nargs='?', default="base_link",
                        help="基坐标系 (默认: base_link)")
    parser.add_argument("target_frame", nargs='?', default="zarm_l7_link",
                        help="目标坐标系 (默认: zarm_l7_link)")
    parser.add_argument("--monitor", "-m", action="store_true",
                        help="持续监控模式")
    parser.add_argument("--rate", "-r", type=float, default=1.0,
                        help="监控频率 Hz (默认: 1.0)")
    parser.add_argument("--list", "-l", action="store_true",
                        help="列出所有可用坐标系")
    parser.add_argument("--both", "-b", action="store_true",
                        help="同时查询左右手末端")
    
    args, unknown = parser.parse_known_args()
    
    rospy.init_node('get_tf_position', anonymous=True)
    
    # 创建TF2监听器
    tf_buffer = tf2_ros.Buffer()
    tf_listener = tf2_ros.TransformListener(tf_buffer)
    
    # 等待TF数据
    rospy.loginfo("等待TF数据...")
    rospy.sleep(1.0)
    
    # 列出所有坐标系
    if args.list:
        list_frames(tf_buffer)
        return
    
    # 同时查询左右手
    if args.both:
        print("\n查询双手末端位置...")
        
        # 左手
        left_transform = get_transform(tf_buffer, args.base_frame, "zarm_l7_link")
        if left_transform:
            print_transform(args.base_frame, "zarm_l7_link (左手)", left_transform)
        
        # 右手
        right_transform = get_transform(tf_buffer, args.base_frame, "zarm_r7_link")
        if right_transform:
            print_transform(args.base_frame, "zarm_r7_link (右手)", right_transform)
        
        # 输出配置格式
        if left_transform and right_transform:
            lpos = left_transform['position']
            rpos = right_transform['position']
            print("\nROBOT_ZERO_CONFIG 格式:")
            print(f"  'left':  {{'x': {lpos['x']:.5f}, 'y': {lpos['y']:.5f}, 'z': {lpos['z']:.5f}}}")
            print(f"  'right': {{'x': {rpos['x']:.5f}, 'y': {rpos['y']:.5f}, 'z': {rpos['z']:.5f}}}")
        return
    
    # 监控模式
    if args.monitor:
        monitor_transform(tf_buffer, args.base_frame, args.target_frame, args.rate)
        return
    
    # 单次查询
    transform = get_transform(tf_buffer, args.base_frame, args.target_frame)
    if transform:
        print_transform(args.base_frame, args.target_frame, transform)
    else:
        print(f"\n无法获取 {args.target_frame} 相对于 {args.base_frame} 的变换")
        print("请检查:")
        print("  1. 坐标系名称是否正确")
        print("  2. 机器人是否已启动")
        print("  3. TF树是否正常发布")
        print("\n使用 --list 查看所有可用坐标系")


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        print("\n用户中断")
