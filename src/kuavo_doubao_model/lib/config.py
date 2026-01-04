import uuid
import pyaudio

# 配置信息
ws_connect_config = {
    "base_url": "wss://openspeech.bytedance.com/api/v3/realtime/dialogue",
    "headers": {
        "X-Api-App-ID": "",
        "X-Api-Access-Key": "",
        "X-Api-Resource-Id": "volc.speech.dialog",  # 固定值
        "X-Api-App-Key": "PlgvMymc7f3tQnJ6",  # 固定值
        "X-Api-Connect-Id": str(uuid.uuid4()),
    }
}

start_session_req = {
    "tts": {
        "audio_config": {
            "channel": 1,
            "format": "pcm",
            "sample_rate": 24000
        },
    },
    "dialog": {
        "bot_name": "夸父",
        "system_role":  """你叫夸父，是由乐聚机器人研发的功能丰富的人形机器人，回答要专业。

你具备以下能力：
1. 移动能力：只能向前、向后、向左、向右各走十步，超出了就说目前步数限制是十步，然后不要数步数。
2. 转向能力：只能向左转1~180度和向右转1~180度，超出了就说转不了。
3. 打太极

例如，用户说"向前走五步"，你应该这样回应：
"向前走五步"

超出了就说目前步数限制是十步，然后不要数步数
例如，用户说"向前走二十步"，你应该这样回应：
"目前步数限制是十步，走不了二十步哦"



注意：
- 语调要平稳，不要急促
- 整个过程只要关键词识别到：“打太极”就回答：“起势，野马分鬃”。
- 让你向左转的时候你要说向左转，让你向右转的时候你要说向右转
""",
        "speaking_style": "你的说话风格专业，语速适中，语调自然。",
        "location": {
          "city": "深圳",
        },
        "extra": {
            "strict_audit": False
        }
    }
}

input_audio_config = {
    "chunk": 3200,
    "format": "pcm",
    "channels": 1,
    "sample_rate": 16000,
    "bit_size": pyaudio.paInt16
}

output_audio_config = {
    "chunk": 3200,
    "format": "pcm",
    "channels": 1,
    "sample_rate": 24000,
    "bit_size": pyaudio.paFloat32
}
