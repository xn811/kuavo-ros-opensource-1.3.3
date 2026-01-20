#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音任务控制器 - 监听语音识别结果，触发综合任务

独立于动作控制器，专门处理复杂任务的语音触发
"""

import rospy
from std_msgs.msg import String
from std_srvs.srv import Trigger
import re


class TaskVoiceController:
    """语音任务控制器"""
    
    def __init__(self):
        rospy.init_node('task_voice_controller', anonymous=True)
        
        # 任务关键词配置
        self.task_triggers = {
            "水瓶任务": {
                "service": "/start_bottle_box_task",
                "description": "抓水瓶+搬箱子综合任务",
                "keywords": [
                    # 直接关键词
                    "水瓶任务", "综合任务", "完整任务",
                    # 组合关键词
                    "水瓶和箱子", "抓水瓶搬箱子",
                    # 变体关键词
                    "水瓶分拣", "分拣水瓶", "水瓶搬运",
                    "箱子任务", "搬运任务", "抓取任务"
                ]
            }
        }
        
        # 任务状态
        self.is_task_running = False
        self.last_trigger_time = rospy.Time.now()
        self.trigger_cooldown = rospy.Duration(5.0)  # 5秒冷却时间，避免重复触发
        
        # 订阅语音识别结果（假设豆包系统会发布到这个话题）
        # 注意：你需要在豆包系统中添加一个发布者，发布ASR结果
        self.asr_sub = rospy.Subscriber('/voice_asr_result', String, self.handle_voice_input)
        
        # 订阅任务状态
        self.status_sub = rospy.Subscriber('/task_status', String, self.handle_task_status)
        
        rospy.loginfo("=" * 60)
        rospy.loginfo("语音任务控制器已启动")
        rospy.loginfo("=" * 60)
        rospy.loginfo("支持的任务触发关键词：")
        for task_name, config in self.task_triggers.items():
            rospy.loginfo(f"  - {task_name}: {', '.join(config['keywords'])}")
        rospy.loginfo("=" * 60)
        rospy.loginfo("等待语音输入...")
    
    def handle_task_status(self, msg):
        """处理任务状态更新"""
        status = msg.data
        
        # 更新任务运行状态
        if "任务开始" in status or "步骤" in status:
            self.is_task_running = True
        elif "任务完成" in status or "任务失败" in status or "任务异常" in status:
            self.is_task_running = False
        
        rospy.loginfo(f"[任务状态] {status}")
    
    def handle_voice_input(self, msg):
        """处理语音识别结果"""
        text = msg.data.strip()
        
        if not text:
            return
        
        rospy.loginfo(f"[语音输入] {text}")
        
        # 检查冷却时间
        current_time = rospy.Time.now()
        if (current_time - self.last_trigger_time) < self.trigger_cooldown:
            rospy.logwarn("[语音任务] 触发冷却中，请稍后再试")
            return
        
        # 检查是否有任务正在运行
        if self.is_task_running:
            rospy.logwarn("[语音任务] 任务正在执行中，请等待完成")
            return
        
        # 方法1：精确匹配关键词
        for task_name, config in self.task_triggers.items():
            for keyword in config['keywords']:
                if keyword in text:
                    rospy.loginfo(f"[语音任务] 检测到关键词: '{keyword}'")
                    rospy.loginfo(f"[语音任务] 准备执行: {config['description']}")
                    
                    # 触发任务
                    success = self.trigger_task(config['service'], task_name)
                    
                    if success:
                        self.last_trigger_time = current_time
                    
                    return  # 只触发第一个匹配的任务
        
        # 方法2：模糊匹配（如果精确匹配失败）
        # 检查是否包含任务相关的核心词
        task_core_words = ["水瓶", "箱子", "搬运", "分拣", "抓取"]
        task_trigger_words = ["任务", "开始", "执行", "做"]
        
        matched_core = [word for word in task_core_words if word in text]
        matched_trigger = [word for word in task_trigger_words if word in text]
        
        # 需要至少1个核心词 + 1个触发词
        if len(matched_core) >= 1 and len(matched_trigger) >= 1:
            rospy.loginfo(f"[语音任务] 模糊匹配成功")
            rospy.loginfo(f"[语音任务] 核心词: {matched_core}, 触发词: {matched_trigger}")
            rospy.loginfo(f"[语音任务] 准备执行: 抓水瓶+搬箱子综合任务")
            
            # 触发默认任务
            success = self.trigger_task("/start_bottle_box_task", "综合任务")
            
            if success:
                self.last_trigger_time = current_time
            
            return
    
    def trigger_task(self, service_name, task_name):
        """触发任务服务"""
        try:
            rospy.loginfo(f"[语音任务] 正在调用服务: {service_name}")
            
            # 等待服务可用
            rospy.wait_for_service(service_name, timeout=2.0)
            
            # 调用服务
            trigger_service = rospy.ServiceProxy(service_name, Trigger)
            response = trigger_service()
            
            if response.success:
                rospy.loginfo(f"[语音任务] ✅ {response.message}")
                return True
            else:
                rospy.logerr(f"[语音任务] ❌ {response.message}")
                return False
                
        except rospy.ROSException as e:
            rospy.logerr(f"[语音任务] ❌ 服务调用超时: {e}")
            rospy.logerr(f"[语音任务] 提示：请先启动任务服务")
            rospy.logerr(f"[语音任务] 命令：python3 bottle_and_box_task_service.py")
            return False
        except Exception as e:
            rospy.logerr(f"[语音任务] ❌ 触发任务失败: {e}")
            return False
    
    def spin(self):
        """保持节点运行"""
        rospy.spin()


def main():
    try:
        controller = TaskVoiceController()
        controller.spin()
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        rospy.loginfo("用户中断")


if __name__ == '__main__':
    main()
