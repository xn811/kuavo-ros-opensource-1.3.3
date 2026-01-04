# -*- encoding:utf-8 -*-
"""
仿真版本：图像和语音输入都改为订阅ROS话题
订阅话题: 
  - /camera/color/image_raw (sensor_msgs/Image) - 图像输入
  - /micphone_data (kuavo_msgs/AudioReceiverData) - 麦克风音频输入
"""
import os
import re
import json
import time
import base64
import hashlib
import hmac
import threading
import collections
import audioop
import numpy as np
import cv2
import websocket
from websocket import create_connection
from urllib.parse import quote

import rospy
from std_msgs.msg import Int16MultiArray
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from kuavo_msgs.msg import AudioReceiverData
from kuavo_audio_player.srv import audio_status
from std_srvs.srv import Trigger
from openai import OpenAI

from tts_ws_python3_demo import tts_xunfei

# 音频参数
CHANNELS = 1
RATE = 16000
THRESHOLD = 3000
SILENCE_DURATION = 1
RECORD_SECONDS = 60
INPUT_FILE = "input.pcm"

# 讯飞ASR配置
app_id = "XXXXXXXX"  # 替换为实际的app_id
api_key = "XXXXXXXXXXXXXXXXXXXXX"  # 替换为实际的api_key


class Microphone:
    """ROS麦克风数据订阅器"""
    def __init__(self, subscribe_topic="/micphone_data"):
        self._buffer = collections.deque()
        self._lock = threading.Lock()
        self.subscriber = rospy.Subscriber(subscribe_topic, AudioReceiverData, self._audio_callback)
        rospy.loginfo(f"麦克风订阅话题: {subscribe_topic}")

    def _audio_callback(self, msg):
        with self._lock:
            self._buffer.append(msg.data)

    def get_data(self):
        """获取缓冲区中的所有数据"""
        with self._lock:
            if not self._buffer:
                return None
            data_batch = b''.join(self._buffer)
            self._buffer.clear()
            return data_batch

    def clear_buffer(self):
        """清空缓冲区"""
        with self._lock:
            self._buffer.clear()


class Client:
    """讯飞实时语音转写客户端"""
    def __init__(self):
        base_url = "ws://rtasr.xfyun.cn/v1/ws"
        ts = str(int(time.time()))
        tt = (app_id + ts).encode('utf-8')
        md5 = hashlib.md5()
        md5.update(tt)
        baseString = md5.hexdigest()
        baseString = bytes(baseString, encoding='utf-8')

        apiKey = api_key.encode('utf-8')
        signa = hmac.new(apiKey, baseString, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        self.end_tag = "{\"end\": true}"

        self.sentence = None
        self.ws = create_connection(base_url + "?appid=" + app_id + "&ts=" + ts + "&signa=" + quote(signa))
        self.trecv = threading.Thread(target=self.recv)
        self.trecv.start()

    def send_data(self, audio_data):
        """直接发送音频数据（bytes）"""
        try:
            # 分块发送
            for i in range(0, len(audio_data), 1280):
                chunk = audio_data[i:i+1280]
                if not chunk:
                    break
                self.ws.send(chunk)
                time.sleep(0.04)
        finally:
            self.ws.send(bytes(self.end_tag.encode('utf-8')))
            print("send end tag success")

    def recv(self):
        try:
            data_str = None
            while self.ws.connected:
                result = str(self.ws.recv())
                if len(result) == 0:
                    print("receive result end")
                    break
                result_dict = json.loads(result)
                if result_dict["action"] == "started":
                    print("handshake success")
                if result_dict["action"] == "result":
                    data_str = result_dict["data"]
                    print("rtasr result: " + data_str)
                if result_dict["action"] == "error":
                    print("rtasr error: " + result)
                    self.ws.close()
                    return
            if data_str:
                data_dict = json.loads(data_str)
                words = []
                for rt in data_dict['cn']['st']['rt']:
                    for ws in rt['ws']:
                        for cw in ws['cw']:
                            words.append(cw['w'])
                self.sentence = ''.join(words)
                print(f"识别结果: {self.sentence}")
        except websocket.WebSocketConnectionClosedException:
            print("receive result end")
        except Exception as e:
            print(f"ASR接收错误: {e}")

    def close(self):
        self.ws.close()


class ROSKimiSimBot:
    def __init__(self):
        rospy.init_node('kimi_sim_chat_bot', anonymous=True)
        
        # 音频数据发布器
        self.audio_data_pub = rospy.Publisher('/audio_data', Int16MultiArray, queue_size=10)
        
        # 订阅图像话题
        self.bridge = CvBridge()
        self.current_image = None
        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.image_callback, queue_size=1)
        
        # 订阅麦克风话题
        self.microphone = Microphone("/micphone_data")
        
        rospy.sleep(1)
        
        self.network_pattern = r"联网|查询|搜"
        
        print("=" * 50)
        print("仿真版 Kimi 语音视觉聊天机器人已启动")
        print("图像输入: 订阅 /camera/color/image_raw")
        print("语音输入: 订阅 /micphone_data")
        print("=" * 50)

    def image_callback(self, msg):
        """接收图像的回调函数"""
        try:
            self.current_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            rospy.logerr(f"图像转换失败: {e}")

    def record_from_topic(self):
        """从ROS话题录音，基于音量阈值自动开始/结束"""
        print("请开始提问...")
        self.microphone.clear_buffer()
        
        frames = []
        recording = False
        silence_start = None
        start_time = time.time()
        
        while not rospy.is_shutdown():
            data = self.microphone.get_data()
            if data:
                # 计算音量
                rms = audioop.rms(data, 2)
                
                if rms > THRESHOLD:
                    if not recording:
                        recording = True
                        start_time = time.time()
                        print("开始录音")
                    frames.append(data)
                    silence_start = None
                else:
                    if recording:
                        frames.append(data)  # 静默期间也录制
                        if silence_start is None:
                            silence_start = time.time()
                        elif time.time() - silence_start > SILENCE_DURATION:
                            print("录音结束")
                            break
            
            if time.time() - start_time > RECORD_SECONDS:
                print("达到最大录音时间")
                break
            
            rospy.sleep(0.01)
        
        if frames:
            return b''.join(frames)
        return None

    def publish_pcm_audio_data(self, pcm_file_path, sample_rate=16000, chunk_size=1024):
        """将PCM文件发布到audio_data话题"""
        try:
            print(f"开始发布PCM音频数据: {pcm_file_path}")
            with open(pcm_file_path, 'rb') as f:
                pcm_data = f.read()
            audio_array = np.frombuffer(pcm_data, dtype=np.int16)
            print(f"音频长度: {len(audio_array)} 采样点, {len(audio_array)/sample_rate:.2f}秒")
            
            for i in range(0, len(audio_array), chunk_size):
                if rospy.is_shutdown():
                    break
                audio_chunk = audio_array[i:i+chunk_size]
                msg = Int16MultiArray()
                msg.data = audio_chunk.tolist()
                self.audio_data_pub.publish(msg)
                duration = chunk_size / sample_rate
                time.sleep(duration * 0.8)
        except FileNotFoundError:
            print(f"错误: 找不到文件 {pcm_file_path}")
        except Exception as e:
            print(f"发布失败: {str(e)}")

    def wait_for_audio_completion(self):
        """等待音频播放完成"""
        try:
            rospy.wait_for_service('audio_status', timeout=5)
            rospy.wait_for_service('get_used_audio_buffer_size', timeout=5)
            audio_status_service = rospy.ServiceProxy('audio_status', audio_status)
            buffer_status_service = rospy.ServiceProxy('get_used_audio_buffer_size', Trigger)
            consecutive_empty_count = 0
            
            while not rospy.is_shutdown():
                try:
                    status_response = audio_status_service()
                    buffer_response = buffer_status_service()
                    buffer_size = int(buffer_response.message) if buffer_response.success else 0
                    is_playing = status_response.is_playing or buffer_size > 0
                    if not is_playing:
                        consecutive_empty_count += 1
                        if consecutive_empty_count >= 3:
                            print("音频播放完成")
                            break
                    else:
                        consecutive_empty_count = 0
                    time.sleep(0.3)
                except rospy.ServiceException as e:
                    print(f"调用服务失败: {e}")
                    break
        except rospy.ROSException:
            print("音频服务不可用，跳过等待")
        except Exception as e:
            print(f"等待音频完成时出错: {e}")

    def kimi_vision_chat(self, text):
        """视觉推理对话 - 使用订阅的图像"""
        if self.current_image is None:
            print("未收到图像数据，切换到纯文本对话")
            self.kimi_network_chat(text)
            return

        frame = self.current_image.copy()
        cv2.imwrite('picture.jpg', frame)
        print("图片已保存: picture.jpg")

        client = OpenAI(
            api_key="XXXXXXXXXXXXXXXXXXXXXXXXXXX",  # 替换为实际的api_key
            base_url="https://api.moonshot.cn/v1",
        )
        
        with open("picture.jpg", "rb") as f:
            image_data = f.read()
        image_url = f"data:image/jpg;base64,{base64.b64encode(image_data).decode('utf-8')}"
        
        completion = client.chat.completions.create(
            model="moonshot-v1-8k-vision-preview",
            messages=[
                {"role": "system", "content": "你叫夸父，是由乐聚机器人研发的功能丰富的人形机器人，回答要简洁专业，控制在60字内,我输出给你的是你摄像头看到的画面，你可以回答我看到了......。"},
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": image_url}},
                        {"type": "text", "text": text},
                    ],
                },
            ],
        )
        
        response_text = completion.choices[0].message.content
        print(f"提问: {text}")
        print(f"回答: {response_text}")
        self._play_tts_response(response_text)

    def kimi_network_chat(self, text):
        """联网搜索对话"""
        client = OpenAI(
            base_url="https://api.moonshot.cn/v1",
            api_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",  # 替换为实际的api_key
        )
        
        messages = [
            {"role": "system", "content": "你叫夸父，是由乐聚机器人研发的功能丰富的人形机器人，回答要简洁专业，控制在60字内."},
            {"role": "user", "content": text}
        ]

        finish_reason = None
        while finish_reason is None or finish_reason == "tool_calls":
            completion = client.chat.completions.create(
                model="moonshot-v1-128k",
                messages=messages,
                temperature=0.3,
                tools=[{"type": "builtin_function", "function": {"name": "$web_search"}}]
            )
            choice = completion.choices[0]
            finish_reason = choice.finish_reason
            
            if finish_reason == "tool_calls":
                messages.append(choice.message)
                for tool_call in choice.message.tool_calls:
                    tool_call_arguments = json.loads(tool_call.function.arguments)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": json.dumps(tool_call_arguments),
                    })

        response_text = choice.message.content
        print(f"提问: {text}")
        print(f"回答: {response_text}")
        self._play_tts_response(response_text)

    def _play_tts_response(self, text):
        """TTS转语音并播放"""
        tts_xunfei(text)
        if os.path.exists("output.pcm"):
            self.publish_pcm_audio_data("output.pcm")
            time.sleep(0.5)
            self.wait_for_audio_completion()

    def run(self):
        """主循环：从话题录音 -> ASR -> 对话"""
        while not rospy.is_shutdown():
            print("\n检查音频播放状态...")
            self.wait_for_audio_completion()
            
            print("开始新一轮语音识别...")
            audio_data = self.record_from_topic()
            
            if audio_data:
                client = Client()
                client.send_data(audio_data)
                client.trecv.join()
                
                if client.sentence:
                    if re.search(self.network_pattern, client.sentence):
                        self.kimi_network_chat(client.sentence)
                    else:
                        self.kimi_vision_chat(client.sentence)
            else:
                print("未录到有效音频")
                rospy.sleep(0.5)


def main():
    try:
        bot = ROSKimiSimBot()
        bot.run()
    except rospy.ROSInterruptException:
        print("ROS节点被中断")
    except KeyboardInterrupt:
        print("\n检测到Ctrl+C，正在退出...")
    finally:
        cv2.destroyAllWindows()
        print("资源已释放，程序退出")


if __name__ == '__main__':
    main()
