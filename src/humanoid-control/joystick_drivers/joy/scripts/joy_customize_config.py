#!/usr/bin/env python3
import rospy
import rospkg
import json
import threading
import subprocess
import time
from typing import Dict, Any
from sensor_msgs.msg import Joy
from std_msgs.msg import String
from kuavo_msgs.srv import playmusic, playmusicRequest
from kuavo_msgs.srv import ExecuteArmAction, ExecuteArmActionRequest


class JoyCustomizeConfigNode:
    def __init__(self) -> None:
        rospy.init_node("joy_customize_config")

        # Params
        self.joystick_type = rospy.get_param("~joystick_type", rospy.get_param("joystick_type", "bt2pro"))
        self.channel_map_path = rospy.get_param(
            "~channel_map_path",
            rospy.get_param("channel_map_path", "")
        )
        self.joystick_sensitivity = float(rospy.get_param("~joystick_sensitivity", rospy.get_param("joystick_sensitivity", 20)))

        # Resolve default channel_map_path if empty
        if not self.channel_map_path:
            try:
                humanoid_controllers_path = rospkg.RosPack().get_path("humanoid_controllers")
                self.channel_map_path = f"{humanoid_controllers_path}/launch/joy/{self.joystick_type}.json"
            except Exception as e:
                rospy.logwarn(f"Failed to resolve humanoid_controllers path: {e}")

        # Load mappings
        self.joy_button_map: Dict[str, int] = {}
        self.joy_axis_map: Dict[str, int] = {}
        self._load_joy_channel_mapping(self.channel_map_path)

        # Load customize config.json (within joy package)
        self.customize_config_path = self._resolve_customize_config_path()
        self.customize_config: Dict[str, Any] = {}
        self._load_customize_config()

        # Subscribers
        self.joy_sub = rospy.Subscriber("/joy", Joy, self._joy_callback, queue_size=10)
        self.update_sub = rospy.Subscriber("/update_joy_customize_config", String, self._update_config_callback, queue_size=1)

        # Internal state for edge detection
        self._prev_buttons = []
        self._prev_axes = []
        
        # M1/M2 button states for combination detection
        self._m1_pressed = False
        self._m2_pressed = False

        self.JOYSTICK_BUTTON_NUM = 16
        self.JOYSTICK_AXIS_NUM = 8

        rospy.loginfo(f"joy_customize_config started. joystick_type={self.joystick_type}, map={self.channel_map_path}")
        rospy.loginfo(f"customize_config={self.customize_config_path}")

    def _resolve_customize_config_path(self) -> str:
        try:
            joy_pkg_path = rospkg.RosPack().get_path("joy")
            return f"{joy_pkg_path}/config/customize_config.json"
        except Exception:
            # Fallback to local package location
            try:
                local_pkg_path = rospkg.RosPack().get_path("joy")
                return f"{local_pkg_path}/config/customize_config.json"
            except Exception:
                # Final fallback: relative known repo layout
                return rospy.get_param(
                    "~customize_config_path",
                    "/home/lmx/real_ws/kuavo-ros-control/src/humanoid-control/joystick_drivers/joy/config/customize_config.json",
                )

    def _convert_button_names(self, button_map: Dict[str, int]) -> Dict[str, int]:
        """Convert standard button names to custom button names"""
        button_name_mapping = {
            "BUTTON_STANCE": "BUTTON_A",
            "BUTTON_TROT": "BUTTON_B", 
            "BUTTON_JUMP": "BUTTON_X",
            "BUTTON_WALK": "BUTTON_Y"
        }
        
        converted_map = {}
        for original_name, idx in button_map.items():
            # Use converted name if mapping exists, otherwise keep original
            converted_name = button_name_mapping.get(original_name, original_name)
            converted_map[converted_name] = idx
            
        return converted_map

    def _load_joy_channel_mapping(self, path: str) -> None:
        try:
            with open(path, "r") as f:
                data = json.load(f)
            button = data.get("JoyButton", {})
            axis = data.get("JoyAxis", {})
            # Convert all values to int just in case
            raw_button_map = {str(k): int(v) for k, v in button.items()}
            self.joy_button_map = self._convert_button_names(raw_button_map)
            self.joy_axis_map = {str(k): int(v) for k, v in axis.items()}
            rospy.set_param("joystick_type", self.joystick_type)
            rospy.set_param("channel_map_path", path)
            rospy.loginfo(f"Loaded joystick mapping from {path}")
            rospy.loginfo(f"Buttons: {self.joy_button_map}")
            rospy.loginfo(f"Axes: {self.joy_axis_map}")
        except Exception as e:
            rospy.logwarn(f"Failed to load joystick mapping from {path}: {e}")

    def _load_customize_config(self) -> None:
        try:
            with open(self.customize_config_path, "r") as f:
                self.customize_config = json.load(f)
            rospy.loginfo(f"Loaded customize_config.json with {len(self.customize_config)} entries")
        except Exception as e:
            rospy.logwarn(f"Failed to load customize_config.json: {self.customize_config_path}, error: {e}")
            self.customize_config = {}

    def _update_config_callback(self, msg: String) -> None:
        rospy.loginfo("Received update_joy_customize_config, reloading customize_config.json ...")
        self._load_customize_config()

    def _execute_arm_poses(self, arm_pose_names):
        """执行手臂动作的线程函数"""
        for arm_pose in arm_pose_names:
            if arm_pose:  # 检查动作名称不为空
                rospy.loginfo(f"Executing arm pose: {arm_pose}")
                try:
                    self._call_execute_arm_action(arm_pose)
                    time.sleep(1.0)  # 等待动作完成
                except Exception as e:
                    rospy.logerr(f"Failed to execute arm pose {arm_pose}: {e}")

    def _play_music(self, music_names):
        """播放音乐的线程函数"""
        for music in music_names:
            if music:  # 检查音乐名称不为空
                rospy.loginfo(f"Playing music: {music}")
                try:
                    self._set_robot_play_music(music, 100)
                except Exception as e:
                    rospy.logerr(f"Failed to play music {music}: {e}")

    def _set_robot_play_music(self, music_file_name: str, music_volume: int) -> bool:
        """机器人播放指定文件的音乐"""
        try:
            _robot_music_play_client = rospy.ServiceProxy("/play_music", playmusic)
            request = playmusicRequest()
            request.music_number = music_file_name
            request.volume = music_volume
            response = _robot_music_play_client(request)
            rospy.loginfo(f"Service call /play_music: {response.success_flag}")
            return response.success_flag
        except Exception as e:
            rospy.logerr(f"Service /play_music call failed: {e}")
            return False

    def _call_execute_arm_action(self, action_name):
        """调用手臂动作执行服务"""
        try:
            _execute_arm_action_client = rospy.ServiceProxy('/execute_arm_action', ExecuteArmAction)
            request = ExecuteArmActionRequest()
            request.action_name = action_name
            response = _execute_arm_action_client(request)
            rospy.loginfo(f"ExecuteArmAction service response: success={response.success}, message={response.message}")
            return response.success, response.message
        except Exception as e:
            rospy.logerr(f"Service call to '/execute_arm_action' failed: {e}")
            return False, f"Service exception: {e}"

    def _joy_callback(self, joy_msg: Joy) -> None:
        # 检查按钮和轴的数量是否正确
        if len(joy_msg.buttons) != self.JOYSTICK_BUTTON_NUM or len(joy_msg.axes) != self.JOYSTICK_AXIS_NUM:
            rospy.logwarn(f"Invalid joy msg. Buttons: {len(joy_msg.buttons)}, Axes: {len(joy_msg.axes)}")
            return

        # Initialize previous states on first message
        if not self._prev_buttons:
            self._prev_buttons = list(joy_msg.buttons)
        if not self._prev_axes:
            self._prev_axes = list(joy_msg.axes)

        try:
            # 检查M1和M2按键状态
            m1_idx = self.joy_button_map.get("BUTTON_M1", -1)
            m2_idx = self.joy_button_map.get("BUTTON_M2", -1)
            a_idx = self.joy_button_map.get("BUTTON_A", -1)
            b_idx = self.joy_button_map.get("BUTTON_B", -1)
            x_idx = self.joy_button_map.get("BUTTON_X", -1)
            y_idx = self.joy_button_map.get("BUTTON_Y", -1)

            # 检查M1按键状态
            if 0 <= m1_idx < len(joy_msg.buttons):
                m1_current = joy_msg.buttons[m1_idx]
                m1_prev = self._prev_buttons[m1_idx] if m1_idx < len(self._prev_buttons) else 0
                
                if m1_prev == 0 and m1_current == 1:
                    # M1按下
                    self._m1_pressed = True
                    rospy.loginfo("M1 button pressed")
                elif m1_prev == 1 and m1_current == 0:
                    # M1释放
                    self._m1_pressed = False
                    rospy.loginfo("M1 button released")

            # 检查M2按键状态
            if 0 <= m2_idx < len(joy_msg.buttons):
                m2_current = joy_msg.buttons[m2_idx]
                m2_prev = self._prev_buttons[m2_idx] if m2_idx < len(self._prev_buttons) else 0
                
                if m2_prev == 0 and m2_current == 1:
                    # M2按下
                    self._m2_pressed = True
                    rospy.loginfo("M2 button pressed")
                elif m2_prev == 1 and m2_current == 0:
                    # M2释放
                    self._m2_pressed = False
                    rospy.loginfo("M2 button released")

            # 检查 A/B/X/Y 按键的释放
            for button_name, button_idx in [("A", a_idx), ("B", b_idx), ("X", x_idx), ("Y", y_idx)]:
                if 0 <= button_idx < len(joy_msg.buttons):
                    button_current = joy_msg.buttons[button_idx]
                    button_prev = self._prev_buttons[button_idx] if button_idx < len(self._prev_buttons) else 0

                    if button_prev == 1 and button_current == 0:
                        # 情况 1: M1 按下、M2 未按下
                        if self._m1_pressed and not self._m2_pressed:
                            action_key = f"customize_action_M1_{button_name}"
                            rospy.loginfo(f"M1 + {button_name} released, triggering {action_key}")
                            self._execute_customize_action(action_key)

                        # 情况 2: M2 按下、M1 未按下
                        elif self._m2_pressed and not self._m1_pressed:
                            action_key = f"customize_action_M2_{button_name}"
                            rospy.loginfo(f"M2 + {button_name} released, triggering {action_key}")
                            self._execute_customize_action(action_key)

                        # 情况 3: M1 和 M2 同时按下
                        elif self._m1_pressed and self._m2_pressed:
                            action_key = f"customize_action_M1M2_{button_name}"
                            rospy.loginfo(f"M1 + M2 + {button_name} released, triggering {action_key}")
                            self._execute_customize_action(action_key)

            # Update previous states
            self._prev_buttons = list(joy_msg.buttons)
            self._prev_axes = list(joy_msg.axes)
            
        except Exception as e:
            rospy.logwarn(f"Error in joy callback: {e}")

    def _execute_customize_action(self, action_key: str) -> None:
        """执行自定义动作"""
        try:
            if action_key in self.customize_config:
                action_config = self.customize_config[action_key]
                arm_pose_names = action_config.get("arm_pose_name", [])
                music_names = action_config.get("music_name", [])
                
                rospy.loginfo(f"Executing action: {action_key}")
                rospy.loginfo(f"Arm poses: {arm_pose_names}")
                rospy.loginfo(f"Music: {music_names}")
                
                # 创建线程执行动作和音乐
                if arm_pose_names:
                    arm_pose_thread = threading.Thread(target=self._execute_arm_poses, args=(arm_pose_names,))
                    arm_pose_thread.start()
                
                if music_names:
                    music_thread = threading.Thread(target=self._play_music, args=(music_names,))
                    music_thread.start()
                
                # 等待线程完成
                if arm_pose_names:
                    arm_pose_thread.join()
                if music_names:
                    music_thread.join()
                    
            else:
                rospy.logwarn(f"No configuration found for action: {action_key}")
                
        except Exception as e:
            rospy.logerr(f"Error executing customize action {action_key}: {e}")

    def spin(self) -> None:
        rospy.spin()


if __name__ == "__main__":
    try:
        node = JoyCustomizeConfigNode()
        node.spin()
    except rospy.ROSInterruptException:
        pass
