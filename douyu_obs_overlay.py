from pathlib import Path
import asyncio
import errno
import platform
import numpy as np
# import subprocess
import threading
import websockets
import ssl
import certifi
import re
import json
import os
import sys
import time
from queue import Queue
from datetime import datetime
import torch
import sounddevice as sd
from TTS.api import TTS

class TTSManager:
    def __init__(self,
                 mode="all",          # 这里保留参数接口，暂时只用 "all"
                 max_backlog=50,
                 min_interval=0.3):
        """
        当前策略：
        - 所有播报任务进入我们自己的 Queue
        - worker 线程里「阻塞式」调用系统 TTS（mac 用 `say`）
        - 正在进行中的播报不会被任何新任务打断

        mode / max_backlog 暂时只保留接口，将来要做防洪再用
        """
        self.mode = mode
        self.max_backlog = max_backlog
        self.min_interval = min_interval
        self._last_time = 0.0
        self.sourceList = self._get_wav_list()
        # 1. 设备
        self.device = self.select_device_for_tts()

        # 2. 加载 XTTS-v2（多语种 + 声音克隆）
        #   第一次会自动从 HuggingFace 下载模型
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        self.tts.to(self.device)

        self.queue: Queue[str] = Queue()
        self.system = platform.system()

        t = threading.Thread(target=self._worker, daemon=True)
        t.start()

    # 获取source 文件夹下所有 wav 文件路径
    def select_device_for_tts(self):
        """
        显卡架构判断：
        - 50 系（sm_120）强制 CPU
        - 40 系（sm_89 / sm_90） 可使用 GPU
        - 30 / 20 / 10 系等都可使用 GPU
        """
        if not torch.cuda.is_available():
            print("[TTS] 未检测到 GPU，使用 CPU")
            return "cpu"

        try:
            major, minor = torch.cuda.get_device_capability()
            print(f"[TTS] 当前显卡 Compute Capability: {major}.{minor}")

            # RTX 50 系（Blackwell 架构）= sm_120
            if major >= 12:  
                print("[TTS] 检测到 50 系显卡（sm_120），强制使用 CPU")
                return "cpu"

            # 其他情况全部用 GPU（包含 40 系 / 30 系 / 20 系）
            print("[TTS] 使用 GPU")
            return "cuda"

        except Exception as e:
            print("[TTS] 检测 GPU 架构失败，使用 CPU:", e)
            return "cpu"

    def _get_wav_list(self, folder="source"):
        folder_path = Path(folder)

        if not folder_path.exists():
            print(f"[TTS] 警告：目录不存在：{folder_path.resolve()}")
            return []

        wav_paths = [str(p.resolve()) for p in folder_path.glob("*.wav")]
        print("[TTS] 加载到的 wav 文件：", wav_paths)
        return wav_paths

    # —— 真正的「阻塞式播报」逻辑，全程在一个线程里 —— #
    def _speak_blocking(self, text: str):
        try:
            wav = self.tts.tts(
                text=text,
                speaker_wav=self.sourceList,  # 也可以传多段 wav 做平均，比如 ["a.wav","b.wav"]
                language="zh",
                split_sentences=True        # 长文本会自动按句切分
            )

            # 有些版本返回的是 list，保险起见转成 np.array
            wav = np.array(wav, dtype=np.float32)

            # 采样率从底层 synthesizer 里拿
            sample_rate = self.tts.synthesizer.output_sample_rate

            # 用 sounddevice 播放
            sd.stop()
            sd.play(wav, samplerate=sample_rate, blocking=True)
        except Exception as e:
            print("Windows SAPI error:", e)
        # if self.system == "Darwin":  # macOS，用系统 say 命令
        #     try:
        #         # 你可以换成自己喜欢的中文语音，比如 "Ting-Ting"、"Xiao Na" 等
        #         subprocess.run(
        #             ["say", "-v", "Ting-Ting", text],
        #             check=False
        #         )
        #     except Exception as e:
        #         print("macOS say error:", e)

        # elif self.system == "Windows":  # Windows 仍然用
        #     try:
        #         subprocess.run([
        #             "powershell",
        #             "-Command",
        #             f"Add-Type -AssemblyName System.Speech; "
        #             f"(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{text}')"
        #         ])
        #     except Exception as e:
        #         print("Windows SAPI error:", e)

        # else:  # Linux 等，尝试用 espeak
        #     try:
        #         subprocess.run(
        #             ["espeak", text],
        #             check=False
        #         )
        #     except Exception as e:
        #         print("espeak error:", e)

    # —— worker 线程：严格串行、不会被打断 —— #
    def _worker(self):
        while True:
            text = self.queue.get()

            # 简单节流，避免两条挤得太紧
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
    def speak_normal(self, text):
        """
        普通弹幕语音：仅当 TTS 当前空闲时才加入队列
        """
        if not text:
            return

        if self.queue.empty():        # 只有空闲才入队
            self.queue.put_nowait(text)
            print("[TTS] 普通弹幕已加入队列：", text)
        else:
            print("[TTS] 跳过普通弹幕（系统正忙）：", text)

    def speak_force(self, text):
        """
        高能弹幕：无论如何都必须加入队列
        """
        if not text:
            return
        self.queue.put_nowait(text)
        print("[TTS] 高能弹幕已加入队列：", text)

tts = TTSManager(mode="all", min_interval=0.5)

# ========= 配置区域 =========
# ROOM_ID = 242737   # TODO：改成你的斗鱼房间号
ROOM_ID = 12268074   # TODO：改成你的斗鱼房间号

# OBS 浏览器叠加层的本地 WebSocket 服务
OBS_WS_HOST = "127.0.0.1"
OBS_WS_PORT = 8765             # OBS Browser 用 ws://127.0.0.1:8765 连接

# 斗鱼弹幕服务器地址
DOUYU_WS_URL = "wss://danmuproxy.douyu.com:8501/"

# 是否真的要使用 SOCKS 代理（例如你全局走 v2ray / clash 等）
# 大多数情况下：False（推荐），避免 python-socks 相关错误
USE_SOCKS_PROXY = False
# ===========================

# 斗鱼协议解析用
pattern = re.compile(r"(\w+)@=([^/]+)")

# WebSocket 连接集合（给 OBS 前端）
overlay_clients: set[websockets.WebSocketServerProtocol] = set()


# ---------- 代理 & 环境检查 ----------

def setup_proxy_environment():
    """
    处理代理相关问题：
    - 默认关闭环境变量中的 HTTP(S)/SOCKS 代理，避免 python-socks 报错
    - 如果 USE_SOCKS_PROXY = True，则检查 python-socks 是否已安装
    """
    proxy_keys = [
        "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
        "http_proxy", "https_proxy", "all_proxy",
    ]

    if not USE_SOCKS_PROXY:
        found = {}
        for k in proxy_keys:
            v = os.environ.get(k)
            if v:
                found[k] = v

        if found:
            print("检测到系统/环境中配置了代理（可能导致 SOCKS 相关错误），已自动清理：")
            for k, v in found.items():
                print(f"  {k} = {v}")
                os.environ.pop(k, None)
            print("已清除以上代理环境变量，如需使用 SOCKS 代理，请将脚本中的 USE_SOCKS_PROXY = True")
        else:
            print("未检测到代理环境变量，直接连接斗鱼服务器。")
    else:
        # 允许代理，但需要 python-socks 依赖
        print("已开启 SOCKS 代理模式（USE_SOCKS_PROXY = True）")
        try:
            import python_socks  # noqa: F401
        except ImportError:
            print(
                "\n[错误] 你开启了 SOCKS 代理模式，但未安装 python-socks。\n"
                "请先安装依赖：\n"
                "    pip install python-socks\n"
            )
            sys.exit(1)


# ---------- 斗鱼协议相关 ----------

def decode_douyu_message(data: bytes):
    """斗鱼弹幕解包，返回若干条消息 dict"""
    try:
        text = data.decode("utf-8", errors="ignore")
        msgs = text.split("type@=")
        results = []
        for msg in msgs:
            if "/" not in msg:
                continue
            msg = "type@=" + msg
            kvs = dict(pattern.findall(msg))
            if kvs:
                results.append(kvs)
        return results
    except Exception:
        return []


async def send_douyu_packet(ws, text: str):
    """按斗鱼协议封装并发送"""
    body = text.encode("utf-8") + b"\x00"
    length = len(body) + 8
    packet = (
        length.to_bytes(4, "little")
        + length.to_bytes(4, "little")
        + b"\xb1\x02\x00\x00"
        + body
    )
    await ws.send(packet)


async def keep_alive(ws):
    """斗鱼心跳"""
    while True:
        try:
            await send_douyu_packet(ws, "type@=mrkl/")
        except Exception as e:
            print("心跳失败:", e)
            return
        await asyncio.sleep(40)

def parse_douyu_list(list_str: str) -> dict:
    """
    解析斗鱼压缩在 list 字段里的 key@AA=value@AS... 数据
    返回一个 dict，比如:
    {
      'vrId': '1993...',
      'content': 'the last',
      'un': '凉瓜牛肉饭',
      'price': '1000',
      'realPrice': '1000',
      ...
    }
    """
    if not list_str:
        return {}

    # 还原转义：@AAS -> @AS
    list_str = list_str.replace("@AAS", "/")

    parts = list_str.split("@AS")
    result = {}
    for p in parts:
        if "@AA=" in p:
            k, v = p.split("@AA=", 1)
            if k:
                result[k] = v
    return result


# ---------- 给 OBS 前端的 WebSocket ----------

async def broadcast_to_overlay(event: dict):
    """把弹幕事件广播给所有连接的 OBS Browser"""
    if not overlay_clients:
        return
    msg = json.dumps(event, ensure_ascii=False)
    dead_clients = []
    for client in overlay_clients:
        try:
            await client.send(msg)
        except Exception:
            dead_clients.append(client)
    # 移除断开的客户端
    for c in dead_clients:
        overlay_clients.discard(c)


async def overlay_ws_handler(ws, path):
    """本地给 OBS Browser 用的 WebSocket 服务"""
    print("Overlay client connected")
    overlay_clients.add(ws)
    try:
        async for _ in ws:
            pass
    finally:
        overlay_clients.discard(ws)
        print("Overlay client disconnected")


# ---------- 斗鱼连接 & 主逻辑 ----------

async def connect_douyu():
    """连接斗鱼并转发消息到 OBS & TTS"""
    retry_delay = 5
    while True:
        try:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            ssl_context.options |= ssl.OP_NO_SSLv2
            ssl_context.options |= ssl.OP_NO_SSLv3
            ssl_context.options |= ssl.OP_NO_TLSv1
            ssl_context.options |= ssl.OP_NO_TLSv1_1
            ssl_context.set_ciphers("DEFAULT")
            async with websockets.connect(
                DOUYU_WS_URL, ssl=ssl_context, ping_interval=None,
            ) as ws:
                print(f"已连接斗鱼弹幕服务器，房间 {ROOM_ID}")

                # 登录房间
                await send_douyu_packet(ws, f"type@=loginreq/roomid@={ROOM_ID}/")
                await asyncio.sleep(0.5)

                # 加入分组（-9999 全部弹幕）
                await send_douyu_packet(ws, f"type@=joingroup/rid@={ROOM_ID}/gid@=-9999/")

                # 心跳
                asyncio.create_task(keep_alive(ws))

                while True:
                    data = await ws.recv()
                    msgs = decode_douyu_message(data)
                    now = datetime.now().strftime("%H:%M:%S")

                    for msg in msgs:
                        msg_type = msg.get("type", "")

                        #普通弹幕
                        if msg_type == "chatmsg":
                            uname = msg.get("nn", "某位观众")
                            text = msg.get("txt", "")
                            print(f"[{now}] [弹幕] {uname}：{text}")

                            event = {
                                "event": "chat",
                                "user": uname,
                                "content": text,
                                "time": now,
                            }
                            asyncio.create_task(broadcast_to_overlay(event))
                            tts.speak_normal(f"{uname}说：{text}")

                        # # 礼物
                        # elif msg_type == "dgb":
                        #     uname = msg.get("nn", "某位观众")
                        #     gname = msg.get("gft", "礼物")
                        #     cnt = msg.get("gfc", "1")
                        #     print(f"[{now}] [礼物] {uname} 送出 {cnt} 个 {gname}")

                        #     event = {
                        #         "event": "gift",
                        #         "user": uname,
                        #         "gift_name": gname,
                        #         "count": cnt,
                        #         "time": now,
                        #     }
                        #     asyncio.create_task(broadcast_to_overlay(event))
                        #     tts.speak_normal(f"{uname}送出了{cnt}个{gname}")

                        # 高能弹幕（SuperChat）
                        elif msg_type == "voice_trlt":
                            # 默认从普通字段里兜底
                            # 如果有 list 字段，优先从 list 里解析（voice_trlt 会走这里）
                            list_raw = msg.get("list", "")
                            data = parse_douyu_list(list_raw) if list_raw else {}

                            if data:
                                try:
                                    print(data)
                                    # 昵称优先用 list 里的 un
                                    uname = data.get("un", "")
                                    # 内容优先用 list 里的 content
                                    text = data.get("content", "")

                                    # 金额（单位：分）， price
                                    raw_price = data.get("price") or "0"
                                    price_fen = int(raw_price)
                                    price_yuan = price_fen / 100.0
                                    print(f"[{now}] [高能] {uname} ({price_yuan} 元): {text}")

                                    # 只处理 / 播报 10 元的高能
                                    if price_fen == 1000:
                                        event = {
                                            "event": "superchat",
                                            "user": uname,
                                            "content": text,
                                            "amount": price_yuan,
                                            "time": now,
                                        }
                                        asyncio.create_task(broadcast_to_overlay(event))
                                        tts.speak_force(f"{uname}说：{text}")
                                except ValueError:
                                    price_fen = 0

                            

        except websockets.exceptions.ConnectionClosedError as e:
            # WebSocket 层的关闭（服务器主动关、网络闪断等）
            print(f"[WARN] 斗鱼连接关闭，code={e.code}, reason={e.reason}，{retry_delay}秒后重连")
        except OSError as e:
            # TCP 层的 "Connection reset by peer" 一般在这里
            if e.errno in (errno.ECONNRESET, 10054):  # 10054 是 Windows 的 WSAECONNRESET
                print(f"[WARN] 斗鱼连接被对方重置（Connection reset by peer），{retry_delay}秒后重连")
            else:
                print(f"[ERROR] 网络错误: {e}，{retry_delay}秒后重连")
        except Exception as e:
            print(f"[ERROR] 未知错误: {e}，{retry_delay}秒后重连")

        # 走到这里说明上面 try 出错/断线了，等待一下再来一轮
        await asyncio.sleep(retry_delay)


async def main():
    # 1. 启动前先处理代理环境，避免 python-socks 报错
    setup_proxy_environment()

    # 2. 启动本地 WebSocket 服务（给 OBS Browser）
    overlay_server = await websockets.serve(
        overlay_ws_handler,
        OBS_WS_HOST,
        OBS_WS_PORT,
    )
    print(f"本地 OBS WebSocket 已启动：ws://{OBS_WS_HOST}:{OBS_WS_PORT}")

    # 4. 启动斗鱼连接协程
    asyncio.create_task(connect_douyu())

    # 5. 挂起
    await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("已退出")