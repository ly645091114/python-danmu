# tts_manager.py
import platform
import threading
import time
from queue import Queue
import io

import requests
import sounddevice as sd
import soundfile as sf


class TTSManager:
    def __init__(self,
                 mode: str = "all",
                 max_backlog: int = 50,
                 min_interval: float = 0.3,
                 tts_api_url: str = "http://127.0.0.1:9522/tts"):
        """
        - 所有播报任务进入我们自己的 Queue
        - worker 线程里阻塞式调用 TTS 接口
        - 正在进行中的播报不会被新任务打断
        """
        self.mode = mode
        self.max_backlog = max_backlog
        self.min_interval = min_interval
        self.tts_api_url = tts_api_url

        self._last_time = 0.0
        self.queue: Queue[str] = Queue()
        self.system = platform.system()

        t = threading.Thread(target=self._worker, daemon=True)
        t.start()

    # —— 真正的「阻塞式播报」逻辑 —— #
    def _speak_blocking(self, text: str):
        if not text:
            return

        try:
            print(f"[TTS] 请求接口: {self.tts_api_url} ...")
            resp = requests.post(
                self.tts_api_url,
                json={"text": text},
                timeout=None,  # 永不超时
            )
            resp.raise_for_status()
            wav_bytes = resp.content
        except Exception as e:
            print("[TTS] 调用接口失败:", e)
            return

        # 直接播放音频
        try:
            buf = io.BytesIO(wav_bytes)
            data, samplerate = sf.read(buf, dtype="float32")
            sd.play(data, samplerate)
            sd.wait()
        except Exception as e:
            print("[TTS] 播放失败:", e)

    # —— worker 线程：严格串行 —— #
    def _worker(self):
        while True:
            text = self.queue.get()

            now = time.time()
            delta = now - self._last_time
            if delta < self.min_interval:
                time.sleep(self.min_interval - delta)

            print("[TTS] 开始播报：", text)
            self._speak_blocking(text)
            print("[TTS] 播报结束：", text)

            self._last_time = time.time()
            self.queue.task_done()

    # —— 外部调用入口：只排队，不直接播放 —— #
    def speak_normal(self, text: str):
        """普通弹幕：仅当队列空闲时才入队"""
        if not text:
            return

        if self.queue.empty():
            self.queue.put_nowait(text)
            print("[TTS] 普通弹幕已加入队列：", text)
        else:
            print("[TTS] 跳过普通弹幕（系统正忙）：", text)

    def speak_force(self, text: str):
        """高能弹幕：无论如何都加入队列"""
        if not text:
            return
        self.queue.put_nowait(text)
        print("[TTS] 高能弹幕已加入队列：", text)
