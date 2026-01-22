#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合任务服务（仿真版） - 通过ROS服务触发抓取物品+搬箱子任务

提供ROS服务接口，可以被语音系统或其他程序调用
"""

import rospy
import subprocess
import sys
import os
import time
import threading
from std_msgs.msg import String
from std_srvs.srv import Trigger, TriggerResponse


class FullTaskService:
    """综合任务服务类（仿真版）"""
    
    def __init__(self):
        rospy.init_node('full_task_service', anonymous=True)
        
        # 任务状态
        self.is_running = False
        self.task_thread = None
        
        # 状态发布者
        self.status_pub = rospy.Publisher('/task_status', String, queue_size=10)
        
        # 创建服务
        self.service = rospy.Service('/start_full_task', Trigger, self.handle_start_task)
        
        rospy.loginfo("=" * 60)
        rospy.loginfo("综合任务服务已启动（仿真版）")
        rospy.loginfo("服务名称: /start_full_task")
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
            rospy.loginfo("开始执行综合任务（仿真版）")
            rospy.loginfo("=" * 60)
            
            self.publish_status("任务开始")
            start_time = time.time()
            
            # 使用 full_course_solver.py 执行综合任务
            cmd = ["rosrun", "task_solver", "full_course_solver.py", "--sim"]
            
            rospy.loginfo(f"执行命令: {' '.join(cmd)}")
            self.publish_status("正在执行综合任务...")
            
            try:
                result = subprocess.run(cmd, check=True)
                
                if result.returncode == 0:
                    total_time = time.time() - start_time
                    rospy.loginfo("=" * 60)
                    rospy.loginfo(f"✅ 综合任务全部完成! 总耗时: {total_time:.2f}秒")
                    rospy.loginfo("=" * 60)
                    self.publish_status(f"任务完成！总耗时: {total_time:.2f}秒")
                else:
                    rospy.logerr(f"❌ 综合任务失败，返回码: {result.returncode}")
                    self.publish_status("任务失败")
                    
            except subprocess.CalledProcessError as e:
                rospy.logerr(f"❌ 综合任务执行出错: {e}")
                self.publish_status("任务执行出错")
            except Exception as e:
                rospy.logerr(f"❌ 综合任务异常: {e}")
                self.publish_status(f"任务异常: {str(e)}")
            
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
        service = FullTaskService()
        service.spin()
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        rospy.loginfo("用户中断")


if __name__ == '__main__':
    main()
