# platform/douyu_client.py
import asyncio
import errno
import re
import ssl
from datetime import datetime
from typing import Callable, Awaitable, Dict, Any

import certifi
from live_platform.utils import setup_proxy_environment
import websockets

from app.tts_manager import TTSManager


pattern = re.compile(r"(\w+)@=([^/]+)")


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


def parse_douyu_list(list_str: str) -> Dict[str, str]:
    """
    解析斗鱼压缩在 list 字段里的 key@AA=value@AS... 数据
    返回一个 dict
    """
    if not list_str:
        return {}

    # 还原转义：@AAS -> /
    list_str = list_str.replace("@AAS", "/")

    parts = list_str.split("@AS")
    result: Dict[str, str] = {}
    for p in parts:
        if "@AA=" in p:
            k, v = p.split("@AA=", 1)
            if k:
                result[k] = v
    return result


async def connect_douyu(
    room_id: int,
    tts: TTSManager,
    broadcast: Callable[[Dict[str, Any]], Awaitable[None]],
    use_socks_proxy: bool = False,
    ws_url: str = "wss://danmuproxy.douyu.com:8501/",
    min_price: int = 0,
    max_price: int = 10,
    speak_txt = ["highenergy"]
):
    """
    连接斗鱼并转发消息到 OBS & TTS
    - room_id: 斗鱼房间号
    - tts: TTSManager 实例
    - broadcast: 调用 overlay_server.broadcast_to_overlay
    """
    setup_proxy_environment(use_socks_proxy)

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
                ws_url,
                ssl=ssl_context,
                ping_interval=None,
            ) as ws:
                print(f"已连接斗鱼弹幕服务器，房间 {room_id}")

                # 登录房间
                await send_douyu_packet(ws, f"type@=loginreq/roomid@={room_id}/")
                await asyncio.sleep(0.5)

                # 加入分组（-9999 全部弹幕）
                await send_douyu_packet(ws, f"type@=joingroup/rid@={room_id}/gid@=-9999/")

                # 心跳
                asyncio.create_task(keep_alive(ws))

                while True:
                    data = await ws.recv()
                    msgs = decode_douyu_message(data)
                    now = datetime.now().strftime("%H:%M:%S")

                    for msg in msgs:
                        msg_type = msg.get("type", "")

                        # 普通弹幕
                        if msg_type == "chatmsg" and "normal" in speak_txt:
                            uname = msg.get("nn", "某位观众")
                            text = msg.get("txt", "")
                            print(f"[{now}] [弹幕] {uname}：{text}")

                            event = {
                                "event": "chat",
                                "platform": "douyu",
                                "user": uname,
                                "content": text,
                                "time": now,
                            }
                            asyncio.create_task(broadcast(event))
                            tts.speak_normal(f"{uname}说{text}")

                        # 礼物
                        elif msg_type == "dgb" and "gift" in speak_txt:
                            uname = msg.get("nn", "某位观众")
                            gname = msg.get("gft", "礼物")
                            cnt = msg.get("gfc", "1")
                            print(f"[礼物] {uname} 送出 {cnt} 个 {gname}")

                            event = {
                                "event": "gift",
                                "user": uname,
                                "gift_name": gname,
                                "count": cnt,
                                "time": now,
                            }
                            asyncio.create_task(broadcast(event))
                            tts.speak_force(f"谢谢{uname}的{int(cnt)}个{gname}")

                        # 高能弹幕（SuperChat）
                        elif msg_type == "voice_trlt" and "highenergy" in speak_txt:
                            list_raw = msg.get("list", "")
                            data_map = parse_douyu_list(list_raw) if list_raw else {}

                            if data_map:
                                try:
                                    uname = data_map.get("un", "")
                                    text = data_map.get("content", "")
                                    raw_price = data_map.get("price") or "0"
                                    price_fen = int(raw_price)
                                    price_yuan = price_fen / 100.0
                                    print(f"[高能] {uname} ({price_yuan} 元): {text}")

                                    if (
                                        price_yuan >= min_price
                                        and (
                                            not max_price or price_yuan < max_price + 1
                                        )
                                    ):
                                        event = {
                                            "event": "superchat",
                                            "platform": "douyu",
                                            "user": uname,
                                            "content": text,
                                            "amount": price_yuan,
                                            "time": now,
                                        }
                                        asyncio.create_task(broadcast(event))
                                        tts.speak_force(f"${uname}说{text}")
                                except ValueError:
                                    pass

        except websockets.exceptions.ConnectionClosedError as e:
            print(f"[WARN] 斗鱼连接关闭，code={e.code}, reason={e.reason}，{retry_delay}秒后重连")
        except OSError as e:
            if e.errno in (errno.ECONNRESET, 10054):
                print(f"[WARN] 斗鱼连接被对方重置（Connection reset by peer），{retry_delay}秒后重连")
            else:
                print(f"[ERROR] 网络错误: {e}，{retry_delay}秒后重连")
        except Exception as e:
            print(f"[ERROR] 未知错误: {e}，{retry_delay}秒后重连")

        await asyncio.sleep(retry_delay)
