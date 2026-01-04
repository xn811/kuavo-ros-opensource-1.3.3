#!/usr/bin/env python3

import subprocess
import re
import random
import os
from typing import List


class ActionController:
    
    def __init__(self):
        self.action_mode = True  # True: 执行随机手臂动作
        
        # 获取当前脚本所在目录（kuavo_doubao_model）
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"[动作] 基础目录: {self.base_dir}")
        
        # 中文数字映射
        self.chinese_numbers = {
            "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
            "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
            "两": 2, "零": 0,
        }
        
        # 方向动作命令映射（使用相对路径）
        self.direction_commands = {
            "前走": ["python3", "step_control/simStepControl_forward.py"],
            "后走": ["python3", "step_control/simStepControl_back.py"],
            "左走": ["python3", "step_control/simStepControl_left.py"],
            "右走": ["python3", "step_control/simStepControl_right.py"],
            "左转": ["python3", "cmd_pose_control/cmd_pose_control.py"],
            "右转": ["python3", "cmd_pose_control/cmd_pose_control.py"]
        }
        
        # 特殊动作命令
        self.special_actions = {
            "表演一下打太极": [
                ["python3", "taiji/step_player_csv_ocs2.py", 
                 "taiji/actions/taiji_wuhan_step_part.csv"],
                ["python3", "play_music.py"]
            ]
        }
        
        # 常规动作库
        self.normal_actions = {
            "握手": ["python3", "hand_plan_arm_trajectory/plan_arm_traj_bezier_demo.py", "--act", "握手.tact"],
            "打招呼": ["python3", "hand_plan_arm_trajectory/plan_arm_traj_bezier_demo.py", "--act", "打招呼_45.tact"],
            "点赞": ["python3", "hand_plan_arm_trajectory/plan_arm_traj_bezier_demo.py", "--act", "点赞_45.tact"]
        }
        
        # 随机动作命令
        self.random_action_cmd = ["python3", "hand_plan_arm_trajectory/plan_arm_traj_bezier_demo_random.py"]
        
        print(f"[动作] 初始化完成，模式: {'开启' if self.action_mode else '关闭'}")

    def _extract_number(self, text: str) -> int:
        """从文本中提取数字，支持中文大数字"""
        # 移除数字中的逗号
        text_clean = text.replace(',', '')
        
        # 先尝试提取阿拉伯数字
        match = re.search(r'\d+', text_clean)
        if match:
            num = int(match.group())
            print(f"读取数字:{num}")
            return num
        
        # 如果文本中包含"万"或"亿"，使用中文数字转换
        if any(unit in text for unit in ["亿", "万", "千", "百", "十"]):
            return self._convert_chinese_large_number(text_clean)
        
        # 单字中文数字
        for chinese, num in self.chinese_numbers.items():
            if chinese in text:
                return num
        
        # 默认值
        return 0

    def _convert_chinese_large_number(self, text: str) -> int:
        """转换中文大数字"""
        # 扩展中文数字映射
        chinese_digits = {
            '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, 
            '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
            '两': 2
        }
        
        chinese_units = {
            '十': 10,
            '百': 100,
            '千': 1000,
            '万': 10000,
            '亿': 100000000
        }
        
        result = 0
        temp = 0
        last_unit = 1
        has_unit = False
        
        for char in text:
            if char in chinese_digits:
                # 处理数字
                if has_unit:
                    # 如果有单位，先加上前面的部分
                    result += temp
                    temp = chinese_digits[char]
                    has_unit = False
                else:
                    temp = temp * 10 + chinese_digits[char]
            elif char in chinese_units:
                # 处理单位
                unit = chinese_units[char]
                if temp == 0:
                    temp = 1 
                
                if unit in [10000, 100000000]:
                    # 万或亿单位，需要特殊处理
                    result += temp * unit
                    temp = 0
                    last_unit = unit
                else:
                    # 千、百、十单位
                    temp *= unit
                    last_unit = unit
                
                has_unit = True
            else:
                # 非数字字符，结束当前数字的解析
                if temp > 0 or has_unit:
                    result += temp
                    temp = 0
                    has_unit = False
        
        # 添加最后的部分
        result += temp
        
        print(f"转换中文数字: {text} -> {result}")
        return result

    def _run_command(self, command: List[str], delay: float = 0):
        """运行命令"""
        if delay > 0:
            import time
            time.sleep(delay)
        
        try:
            # 构建完整路径
            full_command = []
            for part in command:
                if part.endswith('.py') or part.endswith('.csv'):
                    # Python脚本文件，使用绝对路径
                    script_path = os.path.join(self.base_dir, part)
                    full_command.append(script_path)
                elif part == "python3":
                    full_command.append(part)
                else:
                    full_command.append(part)
            
            print(f"[动作] 执行: {' '.join(full_command)}")
            subprocess.Popen(full_command)
            return True
        except Exception as e:
            print(f"[动作] 错误: {e}")
            return False

    def _run_with_number(self, base_cmd: List[str], number: int):
        """带数字参数运行命令"""
        
        # 构建带参数的命令
        cmd = base_cmd.copy()
        cmd.extend(["--num", str(number)])
        
        return self._run_command(cmd)

    def handle(self, text: str, action_mode: bool) -> bool:
        self.action_mode = action_mode
        """处理语音文本"""
        if not text or not text.strip():
            return self.action_mode
            
        print(f"[动作] 收到: {text}")

        # 1. 模式切换指令
        if "说话" in text and "动作" in text:
            self.action_mode = True
            cmd = self.random_action_cmd
            self._run_command(cmd)
            print("[动作] 已开启动作模式")
            print("[动作] 执行随机动作")
            return self.action_mode
        
        if "别做动作" in text or "不做动作" in text or "停止做动作" in text:
            self.action_mode = False
            print("[动作] 已关闭动作模式")
            return self.action_mode

	    # # 2. 特殊动作
        # for action_name, command in self.special_actions.items():
        #     if action_name in text:
        #         if isinstance(command[0], list):  # 组合动作
        #             for cmd in command:
        #                 self._run_command(cmd)
        #         else:  # 单动作
        #             self._run_command(command)
        #         print(f"[动作] 执行: {action_name}")
        #         return self.action_mode
        # 3. 方向动作（涉及步数）
        for direction, base_cmd in self.direction_commands.items():
            if direction in text:
                # 判断是否有步数（检查"步"字或"走"字）
                if "步" in text or "走" in text:
                    number = self._extract_number(text)
                    if number < 1 or number > 10:
                        print("超出步数范围")
                    else:
                        success = self._run_with_number(base_cmd, number)
                        if success:
                            print(f"[动作] 向{direction[1:]}走了 {number} 步")
                elif "转" in text:
                    number = self._extract_number(text)
                    if number < 1 or number > 180:
                        print("超出角度范围")
                    else:
                        if "左" in text:
                            success = self._run_with_number(base_cmd, number)
                            if success:
                                print(f"[动作] 向左转 {number} 度")
                        elif "右" in text:
                            success = self._run_with_number(base_cmd, (number*(-1)))
                            if success:
                                print(f"[动作] 向右转 {number*(-1)} 度")
                return self.action_mode

        # 4. 常规动作
        for action_name, command in self.normal_actions.items():
            if action_name in text:
                self._run_command(command)
                print(f"[动作] 执行: {action_name}")
                return self.action_mode

        # 5. 随机动作（如果没有匹配到特定动作）
        if self.action_mode:
            cmd = self.random_action_cmd
            self._run_command(cmd)
            print("[动作] 执行随机动作")
        return self.action_mode

