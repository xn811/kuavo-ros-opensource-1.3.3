#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合任务服务 - 通过ROS服务触发抓水瓶+搬箱子任务

提供ROS服务接口，可以被语音系统或其他程序调用
"""

import rospy
import subprocess
import sys
import os
import time
import threading
from std_msgs.msg import Bool, String
from std_srvs.srv import Trigger, TriggerResponse

# ==================== 全局配置：脚本路径 ====================
# 水瓶抓取脚本路径
BOTTLE_SCRIPT_PATH = "../../../demo/yolo_object_capture/yolo_apriltag_grasp.py"

# 搬箱子脚本路径
BOX_SCRIPT_PATH = "./grasp_box_example.py"
# ============================================================


class BottleAndBoxTaskService:
    """综合任务服务类"""
    
    def __init__(self):
        rospy.init_node('bottle_and_box_task_service', anonymous=True)
        
        # 将相对路径转换为绝对路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.bottle_script = os.path.abspath(os.path.join(script_dir, BOTTLE_SCRIPT_PATH))
        self.box_script = os.path.abspath(os.path.join(script_dir, BOX_SCRIPT_PATH))
        
        # 检查路径是否存在
        if not os.path.exists(self.bottle_script):
            rospy.logerr(f"找不到水瓶抓取脚本: {self.bottle_script}")
            sys.exit(1)
        
        if not os.path.exists(self.box_script):
            rospy.logerr(f"找不到搬箱子脚本: {self.box_script}")
            sys.exit(1)
        
        rospy.loginfo(f"水瓶抓取脚本: {self.bottle_script}")
        rospy.loginfo(f"搬箱子脚本: {self.box_script}")
        
        # 任务状态
        self.is_running = False
        self.task_thread = None
        
        # 状态发布者
        self.status_pub = rospy.Publisher('/task_status', String, queue_size=10)
        
        # 创建服务
        self.service = rospy.Service('/start_bottle_box_task', Trigger, self.handle_start_task)
        
        rospy.loginfo("=" * 60)
        rospy.loginfo("综合任务服务已启动")
        rospy.loginfo("服务名称: /start_bottle_box_task")
        rospy.loginfo("等待语音触发...")
        rospy.loginfo("=" * 60)
    
    def publish_status(self, status: str):
        """发布任务状态"""
        msg = String()
        msg.data = status
        self.status_pub.publish(msg)
        rospy.loginfo(f"[状态] {status}")
    
    def handle_start_task(self, req):
        """处理启动任务的服务请求"""
        if self.is_running:
            return TriggerResponse(
                success=False,
                message="任务正在执行中，请等待完成"
            )
        
        # 在新线程中执行任务，避免阻塞服务
        self.task_thread = threading.Thread(target=self.run_task)
        self.task_thread.daemon = True
        self.task_thread.start()
        
        return TriggerResponse(
            success=True,
            message="综合任务已启动"
        )
    
    def run_task(self):
        """执行综合任务"""
        self.is_running = True
        
        try:
            rospy.loginfo("=" * 60)
            rospy.loginfo("开始执行综合任务")
            rospy.loginfo("=" * 60)
            
            self.publish_status("任务开始")
            start_time = time.time()
            
            # ========== 步骤1：启动搬箱子程序（后台等待） ==========
            self.publish_status("步骤1: 启动搬箱子程序（后台等待模式）")
            box_cmd = ["python3", self.box_script, "--velocity-control", "--wait-for-bottle"]
            
            try:
                box_process = subprocess.Popen(
                    box_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1
                )
                rospy.loginfo(f"✅ 搬箱子程序已启动 (PID: {box_process.pid})")
                self.publish_status("搬箱子程序已启动，正在初始化SDK")
            except Exception as e:
                rospy.logerr(f"❌ 启动搬箱子程序失败: {e}")
                self.publish_status("任务失败：搬箱子程序启动失败")
                self.is_running = False
                return
            
            # 等待搬箱子程序初始化
            rospy.loginfo("等待搬箱子程序初始化...")
            time.sleep(3.0)
            
            # ========== 步骤2：执行抓水瓶任务 ==========
            self.publish_status("步骤2: 开始抓水瓶任务")
            rospy.loginfo("=" * 60)
            rospy.loginfo("步骤2: 开始抓水瓶任务")
            rospy.loginfo("=" * 60)
            
            bottle_cmd = ["python3", self.bottle_script]
            rospy.loginfo(f"执行命令: {' '.join(bottle_cmd)}")
            
            bottle_success = False
            try:
                result = subprocess.run(bottle_cmd, check=True)
                if result.returncode == 0:
                    rospy.loginfo("✅ 水瓶抓取任务完成")
                    self.publish_status("水瓶抓取任务完成")
                    bottle_success = True
                else:
                    rospy.logerr(f"❌ 水瓶抓取任务失败，返回码: {result.returncode}")
                    self.publish_status("水瓶抓取任务失败")
            except subprocess.CalledProcessError as e:
                rospy.logerr(f"❌ 水瓶抓取任务执行出错: {e}")
                self.publish_status("水瓶抓取任务执行出错")
            except Exception as e:
                rospy.logerr(f"❌ 水瓶抓取任务异常: {e}")
                self.publish_status("水瓶抓取任务异常")
            
            # ========== 步骤3：发布任务完成信号 ==========
            self.publish_status("步骤3: 发布任务完成信号")
            rospy.loginfo("=" * 60)
            rospy.loginfo("步骤3: 发布任务完成信号给搬箱子程序")
            rospy.loginfo("=" * 60)
            
            try:
                pub = rospy.Publisher('/bottle_task_done', Bool, queue_size=1)
                rospy.sleep(0.5)
                
                msg = Bool()
                msg.data = bottle_success
                pub.publish(msg)
                
                status = "成功" if bottle_success else "失败"
                rospy.loginfo(f"✅ 已发布抓水瓶任务{status}信号")
                rospy.sleep(0.5)
            except Exception as e:
                rospy.logerr(f"❌ 发布信号失败: {e}")
            
            # 如果抓水瓶失败，终止搬箱子程序
            if not bottle_success:
                rospy.logerr("❌ 抓水瓶任务失败，终止搬箱子程序")
                self.publish_status("任务失败：抓水瓶失败")
                box_process.terminate()
                box_process.wait(timeout=5.0)
                self.is_running = False
                return
            
            # ========== 步骤4：等待搬箱子程序完成 ==========
            self.publish_status("步骤4: 等待搬箱子程序完成")
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
                    self.publish_status("搬箱子任务完成")
                else:
                    rospy.logerr(f"❌ 搬箱子任务失败，返回码: {box_returncode}")
                    self.publish_status("搬箱子任务失败")
                    self.is_running = False
                    return
            except Exception as e:
                rospy.logerr(f"❌ 等待搬箱子程序时发生错误: {e}")
                self.publish_status("搬箱子任务异常")
                box_process.terminate()
                self.is_running = False
                return
            
            # ========== 总结 ==========
            total_time = time.time() - start_time
            rospy.loginfo("=" * 60)
            rospy.loginfo(f"✅ 综合任务全部完成! 总耗时: {total_time:.2f}秒")
            rospy.loginfo("=" * 60)
            
            self.publish_status(f"任务完成！总耗时: {total_time:.2f}秒")
            
        except Exception as e:
            rospy.logerr(f"任务执行异常: {e}")
            self.publish_status(f"任务异常: {str(e)}")
        finally:
            self.is_running = False
            rospy.loginfo("等待下一次语音触发...")
    
    def spin(self):
        """保持服务运行"""
        rospy.spin()


def main():
    try:
        service = BottleAndBoxTaskService()
        service.spin()
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        rospy.loginfo("用户中断")


if __name__ == '__main__':
    main()
