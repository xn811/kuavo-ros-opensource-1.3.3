#!/usr/bin/env python3
import rospy
from kuavo_audio_player.srv import playmusic, playmusicResponse, playmusicRequest
import os
import subprocess  # 引入 subprocess 模块


# 从ROS参数服务器获取音频路径参数，如果未设置则使用默认值
audio_path = rospy.get_param('audio_path', '/home/lab/.config/lejuconfig/music')
rospy.loginfo("音频文件路径: %s", audio_path)

class MusicPlayerNode:
    def __init__(self):
        rospy.init_node('music_player_node')
        self.service = rospy.Service('play_music', playmusic, self.play_music_callback)
        self.music_directory = audio_path  # 替换为你的音乐文件目录

    def play_music_callback(self, req):
        try:
            # 获取服务请求的音乐文件序号和声音大小
            music_number = req.music_number
            volume = req.volume

            # 构建音乐文件路径
            music_file = os.path.join(self.music_directory, f"{music_number}")

            # 初始化设备及调整音量
            # setting_command = ['pactl', 'set-default-sink', '2']
            # subprocess.call(setting_command)
            # volume_command = ['pactl', 'set-sink-volume', '2', f'{volume}%']
            # subprocess.call(volume_command)

            # 使用 subprocess 调用 play 命令播放音乐
            play_command = ['play', '-q', music_file]
            subprocess.call(play_command)

            rospy.loginfo(f"Playing music {music_file} with volume {volume}%")
            
            # 创建 playmusic 类型的响应
            response = playmusicResponse()
            response.success_flag = True

            return response

        except Exception as e:
            rospy.logerr(f"Error playing music: {str(e)}")
            response = playmusicResponse()
            response.success_flag = False
            return response

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    player_node = MusicPlayerNode()
    player_node.run()