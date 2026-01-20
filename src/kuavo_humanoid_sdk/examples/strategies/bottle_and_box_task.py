#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合任务 - 先抓水瓶，再搬箱子（优化版 - 并行启动）

优化策略：
1. 先启动搬箱子程序（带 --wait-for-bottle 参数），让它提前初始化SDK
2. 再启动抓水瓶程序
3. 抓水瓶完成后发布信号，搬箱子程序收到信号后立即开始执行

这样可以节省搬箱子程序的SDK初始化时间（约5-10秒）

用法:
  python3 bottle_and_box_task.py
"""

import rospy
import subprocess
import sys
import os
import time
from std_msgs.msg import Bool

# ==================== 全局配置：脚本路径 ====================
# 水瓶抓取脚本路径
BOTTLE_SCRIPT_PATH = "../../../demo/yolo_object_capture/yolo_apriltag_grasp.py"

# 搬箱子脚本路径
BOX_SCRIPT_PATH = "./grasp_box_example.py"
# ============================================================

# 将相对路径转换为绝对路径
BOTTLE_SCRIPT_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), BOTTLE_SCRIPT_PATH
))
BOX_SCRIPT_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), BOX_SCRIPT_PATH
))

# 检查路径是否存在
if not os.path.exists(BOTTLE_SCRIPT_PATH):
    print(f"❌ 错误: 找不到水瓶抓取脚本: {BOTTLE_SCRIPT_PATH}")
    sys.exit(1)

if not os.path.exists(BOX_SCRIPT_PATH):
    print(f"❌ 错误: 找不到搬箱子脚本: {BOX_SCRIPT_PATH}")
    sys.exit(1)

print(f"✅ 水瓶抓取脚本: {BOTTLE_SCRIPT_PATH}")
print(f"✅ 搬箱子脚本: {BOX_SCRIPT_PATH}")


def main():
    # 初始化ROS节点
    rospy.init_node('bottle_and_box_task_parallel', anonymous=True)
    
    rospy.loginfo("=" * 60)
    rospy.loginfo("综合任务 - 并行启动优化版")
    rospy.loginfo("=" * 60)
    
    start_time = time.time()
    
    # ========== 步骤1：启动搬箱子程序（后台运行，等待信号） ==========
    rospy.loginfo("步骤1: 启动搬箱子程序（后台等待模式）...")
    box_cmd = ["python3", BOX_SCRIPT_PATH, "--velocity-control", "--wait-for-bottle"]
    
    try:
        # 使用 Popen 在后台启动搬箱子程序
        box_process = subprocess.Popen(
            box_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        rospy.loginfo(f"✅ 搬箱子程序已启动 (PID: {box_process.pid})")
        rospy.loginfo("   程序正在初始化SDK并等待抓水瓶任务完成信号...")
    except Exception as e:
        rospy.logerr(f"❌ 启动搬箱子程序失败: {e}")
        return 1
    
    # 等待搬箱子程序初始化（给它几秒钟时间初始化SDK）
    rospy.loginfo("等待搬箱子程序初始化...")
    time.sleep(3.0)
    
    # ========== 步骤2：执行抓水瓶任务 ==========
    rospy.loginfo("=" * 60)
    rospy.loginfo("步骤2: 开始抓水瓶任务")
    rospy.loginfo("=" * 60)
    
    bottle_cmd = ["python3", BOTTLE_SCRIPT_PATH]
    rospy.loginfo(f"执行命令: {' '.join(bottle_cmd)}")
    
    bottle_success = False
    try:
        result = subprocess.run(bottle_cmd, check=True)
        if result.returncode == 0:
            rospy.loginfo("✅ 水瓶抓取任务完成")
            bottle_success = True
        else:
            rospy.logerr(f"❌ 水瓶抓取任务失败，返回码: {result.returncode}")
    except subprocess.CalledProcessError as e:
        rospy.logerr(f"❌ 水瓶抓取任务执行出错: {e}")
    except Exception as e:
        rospy.logerr(f"❌ 水瓶抓取任务异常: {e}")
    
    # ========== 步骤3：发布任务完成信号 ==========
    rospy.loginfo("=" * 60)
    rospy.loginfo("步骤3: 发布任务完成信号给搬箱子程序")
    rospy.loginfo("=" * 60)
    
    # 直接在这里发布信号，不需要单独的脚本
    try:
        pub = rospy.Publisher('/bottle_task_done', Bool, queue_size=1)
        rospy.sleep(0.5)  # 等待订阅者连接
        
        msg = Bool()
        msg.data = bottle_success
        pub.publish(msg)
        
        status = "成功" if bottle_success else "失败"
        rospy.loginfo(f"✅ 已发布抓水瓶任务{status}信号")
        rospy.sleep(0.5)  # 确保消息发送
    except Exception as e:
        rospy.logerr(f"❌ 发布信号失败: {e}")
    
    # 如果抓水瓶失败，终止搬箱子程序
    if not bottle_success:
        rospy.logerr("❌ 抓水瓶任务失败，终止搬箱子程序")
        box_process.terminate()
        box_process.wait(timeout=5.0)
        rospy.logerr("=" * 60)
        return 1
    
    # ========== 步骤4：等待搬箱子程序完成 ==========
    rospy.loginfo("=" * 60)
    rospy.loginfo("步骤4: 等待搬箱子程序完成...")
    rospy.loginfo("=" * 60)
    
    try:
        # 实时打印搬箱子程序的输出
        for line in box_process.stdout:
            print(line, end='')
        
        # 等待程序结束
        box_returncode = box_process.wait()
        
        if box_returncode == 0:
            rospy.loginfo("✅ 搬箱子任务完成")
        else:
            rospy.logerr(f"❌ 搬箱子任务失败，返回码: {box_returncode}")
            return 1
    except Exception as e:
        rospy.logerr(f"❌ 等待搬箱子程序时发生错误: {e}")
        box_process.terminate()
        return 1
    
    # ========== 总结 ==========
    total_time = time.time() - start_time
    rospy.loginfo("=" * 60)
    rospy.loginfo(f"✅ 综合任务全部完成! 总耗时: {total_time:.2f}秒")
    rospy.loginfo("=" * 60)
    
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        rospy.loginfo("用户中断")
