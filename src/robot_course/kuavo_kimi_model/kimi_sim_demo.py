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
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from kuavo_msgs.msg import AudioReceiverData
from kuavo_audio_player.srv import audio_status, audio_statusResponse
from openai import OpenAI

try:
    import pyaudio
except ImportError:
    print("pyaudio 未安装，先安装 pyaudio")
    os.system("sudo apt-get install python3-pyaudio -y")
    import pyaudio

try:
    import samplerate
except ImportError:
    print("samplerate 未安装，先安装 samplerate")
    os.system("pip install samplerate -i https://mirrors.aliyun.com/pypi/simple/ --no-input")
    import samplerate

import subprocess

from tts_ws_python3_demo import tts_xunfei


def release_audio_device(device_name="MAXHUB"):
    """释放占用音频设备的进程"""
    try:
        # 查找占用设备的进程
        result = subprocess.run(
            ["fuser", "-v", "/dev/snd/*"],
            capture_output=True,
            text=True,
            shell=False
        )
        # fuser 输出在 stderr
        if result.stderr:
            print(f"当前占用音频设备的进程:\n{result.stderr}")
        
        # 尝试通过 pactl 暂停相关的 source
        try:
            sources_result = subprocess.run(
                ["pactl", "list", "sources", "short"],
                capture_output=True,
                text=True
            )
            for line in sources_result.stdout.split('\n'):
                if device_name.lower() in line.lower():
                    source_name = line.split()[1] if len(line.split()) > 1 else None
                    if source_name:
                        subprocess.run(
                            ["pactl", "suspend-source", source_name, "1"],
                            capture_output=True
                        )
                        print(f"已暂停音频源: {source_name}")
        except Exception as e:
            print(f"暂停音频源时出错: {e}")
            
    except Exception as e:
        print(f"释放音频设备时出错: {e}")

# 音频参数
CHANNELS = 1
RATE = 16000
THRESHOLD = 3000
SILENCE_DURATION = 1
RECORD_SECONDS = 60
INPUT_FILE = "input.pcm"

# 讯飞ASR配置
app_id = "XXXXXXXXXX"
api_key = "XXXXXXXXXX"

# Moonshot API 配置
MOONSHOT_API_KEY = "XXXXXXXXXX"


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
        """接收识别结果，只保留最终结果(type=0)"""
        try:
            # 只收集最终结果
            final_texts = []
            
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
                    data_dict = json.loads(data_str)
                    
                    # 获取结果类型: type=0 是最终结果, type=1 是中间结果
                    st = data_dict['cn']['st']
                    result_type = st.get('type', '1')
                    
                    # 提取当前结果的文字
                    words = []
                    for rt in st['rt']:
                        for ws in rt['ws']:
                            for cw in ws['cw']:
                                word = cw['w']
                                if word:
                                    words.append(word)
                    
                    current_text = ''.join(words)
                    
                    # 只保留最终结果(type=0)
                    if result_type == '0':
                        final_texts.append(current_text)
                        print(f"[最终结果]: {current_text}")
                    else:
                        print(f"[中间结果]: {current_text}")
                        
                if result_dict["action"] == "error":
                    print("rtasr error: " + result)
                    self.ws.close()
                    return
            
            # 合并所有最终结果
            if final_texts:
                self.sentence = ''.join(final_texts)
                # 去除末尾的标点符号
                self.sentence = self.sentence.rstrip('。，！？、；：')
                print(f"最终识别结果: {self.sentence}")
        except websocket.WebSocketConnectionClosedException:
            print("receive result end")
        except Exception as e:
            print(f"ASR接收错误: {e}")

    def close(self):
        self.ws.close()


class AudioPlayer:
    """直接播放音频文件，支持选择播放设备，自动处理采样率和声道转换"""
    
    # 常用采样率列表（按优先级）
    SUPPORTED_RATES = [48000, 44100, 32000, 22050, 16000, 8000]
    
    def __init__(self, device_index=None, alsa_device=None, force_rate=None, force_channels=None):
        self.p = pyaudio.PyAudio()
        self.device_index = device_index
        self.alsa_device = alsa_device  # 直接指定 ALSA 设备名，如 "hw:3,0"
        self._playing = False
        self._lock = threading.Lock()
        
        # 如果指定了强制参数，使用指定值；否则自动检测
        if force_rate is not None and force_channels is not None:
            self.device_sample_rate = force_rate
            self.device_channels = force_channels
            print(f"使用指定输出参数: {force_rate}Hz, {force_channels}声道")
        else:
            self.device_sample_rate, self.device_channels = self._detect_device_params()
        
    def _detect_device_params(self):
        """检测设备支持的采样率和声道数"""
        try:
            if self.device_index is not None:
                device_info = self.p.get_device_info_by_index(self.device_index)
            else:
                device_info = self.p.get_default_output_device_info()
            
            default_rate = int(device_info.get('defaultSampleRate', 48000))
            max_channels = int(device_info.get('maxOutputChannels', 2))
            print(f"检测到输出设备: 默认采样率={default_rate}Hz, 最大声道数={max_channels}")
            
            # 尝试验证采样率和声道数（优先双声道，因为很多USB设备不支持单声道）
            for rate in [default_rate] + self.SUPPORTED_RATES:
                for channels in [2, 1]:  # 优先尝试双声道
                    try:
                        stream = self.p.open(
                            format=pyaudio.paInt16,
                            channels=channels,
                            rate=rate,
                            output=True,
                            output_device_index=self.device_index,
                            frames_per_buffer=1024,
                            start=False
                        )
                        stream.close()
                        print(f"使用输出参数: {rate}Hz, {channels}声道")
                        return rate, channels
                    except Exception:
                        continue
            
            print(f"警告: 无法验证参数，使用默认值 {default_rate}Hz, 2声道")
            return default_rate, 2
            
        except Exception as e:
            print(f"检测设备参数失败: {e}，使用默认 48000Hz, 2声道")
            return 48000, 2
        
    @staticmethod
    def list_devices():
        """列出所有可用的音频输出设备"""
        p = pyaudio.PyAudio()
        print("\n可用的音频输出设备:")
        print("-" * 50)
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxOutputChannels'] > 0:
                print(f"  [{i}] {info['name']}")
                print(f"      采样率: {int(info['defaultSampleRate'])}Hz, 输出通道: {info['maxOutputChannels']}")
        print("-" * 50)
        p.terminate()
    
    def set_device(self, device_index):
        """设置播放设备"""
        self.device_index = device_index
        self.device_sample_rate, self.device_channels = self._detect_device_params()
        print(f"已设置播放设备索引: {device_index}")
    
    def is_playing(self):
        """返回当前是否正在播放"""
        with self._lock:
            return self._playing
    
    def _resample_audio(self, audio_array, source_rate, target_rate):
        """重采样音频数据"""
        if source_rate == target_rate:
            return audio_array
        
        # 转换为 float32 进行重采样
        audio_float = audio_array.astype(np.float32) / 32768.0
        ratio = target_rate / source_rate
        resampled = samplerate.resample(audio_float, ratio, converter_type='sinc_fastest')
        # 转回 int16
        return np.clip(resampled * 32768, -32768, 32767).astype(np.int16)
    
    def _mono_to_stereo(self, audio_array):
        """单声道转双声道"""
        # 将单声道数据复制到左右声道
        stereo = np.column_stack((audio_array, audio_array))
        return stereo.flatten()
    
    def play_pcm(self, pcm_file_path, sample_rate=16000, channels=1, max_retries=3):
        """
        使用 aplay 直接播放PCM文件（阻塞式，播放完才返回）
        自动处理采样率和声道转换
        
        Args:
            pcm_file_path: PCM文件路径
            sample_rate: 源文件采样率，默认16000
            channels: 源文件声道数，默认1
            max_retries: 设备被占用时最大重试次数
        """
        if not os.path.exists(pcm_file_path):
            print(f"错误: 找不到文件 {pcm_file_path}")
            return False
        
        with self._lock:
            self._playing = True
        
        try:
            # 读取PCM数据
            with open(pcm_file_path, 'rb') as f:
                pcm_data = f.read()
            
            audio_array = np.frombuffer(pcm_data, dtype=np.int16)
            duration = len(audio_array) / sample_rate
            
            output_rate = self.device_sample_rate
            output_channels = self.device_channels
            
            # 先转换声道数（单声道转双声道），再重采样
            if channels == 1 and output_channels == 2:
                print(f"声道转换: 单声道 -> 双声道")
                audio_array = self._mono_to_stereo(audio_array)
            
            # 重采样（如果需要）
            if sample_rate != output_rate:
                print(f"重采样: {sample_rate}Hz -> {output_rate}Hz")
                # 双声道数据需要分开重采样再合并
                if output_channels == 2:
                    # 分离左右声道
                    left = audio_array[0::2]
                    right = audio_array[1::2]
                    left_resampled = self._resample_audio(left, sample_rate, output_rate)
                    right_resampled = self._resample_audio(right, sample_rate, output_rate)
                    # 交错合并
                    audio_array = np.empty(len(left_resampled) + len(right_resampled), dtype=np.int16)
                    audio_array[0::2] = left_resampled
                    audio_array[1::2] = right_resampled
                else:
                    audio_array = self._resample_audio(audio_array, sample_rate, output_rate)
            
            # 保存处理后的数据到临时文件
            temp_pcm = "/tmp/kimi_audio_output.pcm"
            with open(temp_pcm, 'wb') as f:
                f.write(audio_array.tobytes())
            
            print(f"开始播放: {pcm_file_path} ({duration:.2f}秒)")
            
            # 使用 aplay 播放，设备被占用时重试
            # 根据设备索引确定 ALSA 设备名称
            # device_index 8 对应 hw:3,0 (MAXHUB BM31)
            alsa_device = self._get_alsa_device_name()
            
            for attempt in range(max_retries):
                try:
                    cmd = [
                        "aplay",
                        "-D", alsa_device,
                        "-f", "S16_LE",
                        "-r", str(output_rate),
                        "-c", str(output_channels),
                        temp_pcm
                    ]
                    print(f"执行: {' '.join(cmd)}")
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration + 10)
                    
                    if result.returncode == 0:
                        print("播放完成")
                        return True
                    else:
                        error_msg = result.stderr
                        print(f"aplay 错误: {error_msg}")
                        
                        if "Device or resource busy" in error_msg or "Channels count non available" in error_msg:
                            print(f"设备被占用 (尝试 {attempt + 1}/{max_retries})，等待重试...")
                            release_audio_device("MAXHUB")
                            time.sleep(1.0)
                        else:
                            break
                            
                except subprocess.TimeoutExpired:
                    print("播放超时")
                    break
                except Exception as e:
                    print(f"播放出错: {e}")
                    break
            
            print("播放失败")
            return False
            
        except Exception as e:
            print(f"播放失败: {e}")
            return False
        finally:
            with self._lock:
                self._playing = False
    
    def _get_alsa_device_name(self):
        """根据 PyAudio 设备索引获取 ALSA 设备名称"""
        # 如果直接指定了 ALSA 设备名，优先使用
        if self.alsa_device:
            return self.alsa_device
        
        # 尝试从 PyAudio 设备信息中提取
        if self.device_index is not None:
            try:
                device_info = self.p.get_device_info_by_index(self.device_index)
                device_name = device_info.get('name', '')
                
                # 尝试从设备名称中提取 hw:X,Y
                # 例如 "MAXHUB BM31: USB Audio (hw:3,0)"
                match = re.search(r'hw:(\d+),(\d+)', device_name)
                if match:
                    return f"hw:{match.group(1)},{match.group(2)}"
                    
            except Exception as e:
                print(f"获取设备名称失败: {e}")
        
        # 默认使用系统默认设备
        return "default"
    
    def close(self):
        """释放资源"""
        if self.p:
            self.p.terminate()


class ROSKimiSimBot:
    def __init__(self, audio_device_index=None, alsa_device=None, sample_rate=None, channels=None):
        rospy.init_node('kimi_sim_chat_bot', anonymous=True)
        
        # 初始化音频播放器（直接播放，不走话题）
        self.audio_player = AudioPlayer(
            device_index=audio_device_index,
            alsa_device=alsa_device,
            force_rate=sample_rate,
            force_channels=channels
        )
        
        # 提供 audio_status 服务（供麦克风节点查询播放状态）
        # 注意：服务需要在其他初始化之前创建，确保麦克风节点能连接
        self.audio_status_service = rospy.Service('audio_status', audio_status, self.audio_status_callback)
        rospy.loginfo("已创建 audio_status 服务")
        
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
        print("音频播放: 直接输出到声卡")
        print("音频状态服务: audio_status (供麦克风节点查询)")
        if audio_device_index is not None:
            print(f"播放设备索引: {audio_device_index}")
        print("=" * 50)

    def audio_status_callback(self, req):
        """返回当前音频播放状态"""
        is_playing = self.audio_player.is_playing()
        rospy.logdebug(f"audio_status 查询: is_playing={is_playing}")
        return audio_statusResponse(is_playing=is_playing)

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
        no_data_count = 0
        
        while not rospy.is_shutdown():
            data = self.microphone.get_data()
            if data:
                no_data_count = 0
                # 计算音量
                rms = audioop.rms(data, 2)
                
                if rms > THRESHOLD:
                    if not recording:
                        recording = True
                        start_time = time.time()
                        print(f"开始录音 (音量: {rms})")
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
            else:
                no_data_count += 1
                # 每5秒提示一次没有收到数据
                if no_data_count % 500 == 0:
                    print(f"警告: 已等待 {no_data_count * 0.01:.1f} 秒未收到麦克风数据，请检查 /micphone_data 话题")
            
            if time.time() - start_time > RECORD_SECONDS:
                print("达到最大录音时间")
                break
            
            rospy.sleep(0.01)
        
        if frames:
            return b''.join(frames)
        return None

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
            api_key=MOONSHOT_API_KEY,
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
            api_key=MOONSHOT_API_KEY,
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
        """TTS转语音并直接播放（阻塞式）"""
        tts_xunfei(text)
        if os.path.exists("output.pcm"):
            # 直接播放，播放完才返回
            self.audio_player.play_pcm("output.pcm", sample_rate=16000)

    def run(self):
        """主循环：从话题录音 -> ASR -> 对话"""
        while not rospy.is_shutdown():
            # 确保音频播放完成才开始录音
            while self.audio_player.is_playing():
                print("等待音频播放完成...")
                rospy.sleep(0.1)
            
            print("\n开始新一轮语音识别...")
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
    import argparse
    parser = argparse.ArgumentParser(description='Kimi语音视觉聊天机器人')
    parser.add_argument('--list-devices', action='store_true', help='列出所有可用的音频输出设备')
    parser.add_argument('--device', type=int, default=None, help='指定 PyAudio 设备索引')
    parser.add_argument('--alsa-device', type=str, default=None, help='直接指定 ALSA 设备名，如 hw:3,0')
    parser.add_argument('--sample-rate', type=int, default=None, help='强制指定输出采样率，如 48000')
    parser.add_argument('--channels', type=int, default=None, help='强制指定输出声道数，如 2')
    args = parser.parse_args()
    
    if args.list_devices:
        AudioPlayer.list_devices()
        print("\n提示: 使用 'aplay -l' 可查看 ALSA 设备列表")
        return
    
    try:
        bot = ROSKimiSimBot(
            audio_device_index=args.device,
            alsa_device=args.alsa_device,
            sample_rate=args.sample_rate,
            channels=args.channels
        )
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
