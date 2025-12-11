import os
import requests
import time

TTS_URL = "http://127.0.0.1:9522/tts"

def save_tts(text: str):
    if not text:
        return

    # 发送 POST 请求
    resp = requests.post(
        TTS_URL,
        json={"text": text},
        timeout=None,  # 永不超时
    )

    resp.raise_for_status()

    # 创建保存目录 ./test/
    output_dir = "test"
    os.makedirs(output_dir, exist_ok=True)

    # 生成文件名
    filepath = os.path.join(output_dir, f"{text}_{int(time.time())}.wav")

    # 保存 wav 文件
    with open(filepath, "wb") as f:
        f.write(resp.content)

    print(f"保存成功：{filepath}")


if __name__ == "__main__":
    save_tts("国危思良将，曾焦阳你准备好了么")