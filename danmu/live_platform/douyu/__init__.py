# platform/douyu_client.py
import asyncio
from dataclasses import dataclass
import random
import re
import ssl
from typing import Callable, Awaitable, Dict, Any

from live_platform import PlatformSocketBase
from live_platform.utils import setup_proxy_environment
from live_platform.douyu.message import format_msg
import websockets
from websockets.exceptions import ConnectionClosed, ConnectionClosedError, ConnectionClosedOK


pattern = re.compile(r"(\w+)@=([^/]+)")

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

class DouyuClient(PlatformSocketBase):

    def __init__(
        self,
        room_id: int,
        *,
        use_socks_proxy: bool = False,
        ws_url: str = "wss://danmuproxy.douyu.com:8501/",
        idle_timeout: int = 120,          # 假死检测：多少秒没收到任何数据就重连
        heartbeat_interval: int = 40,     # 心跳间隔（斗鱼/虎牙按你协议调）
    ):
        super().__init__(
            platform="douyu",
            room_id=room_id,
            heartbeat_interval=heartbeat_interval,
            idle_timeout=idle_timeout,
            use_socks_proxy=use_socks_proxy
        )
        self._ws_url = ws_url

    async def _connect_ws(self, ssl_context: ssl.SSLContext):
        # ping_interval=None：不使用 websockets 自带 ping，斗鱼用自定义心跳
        return await websockets.connect(self._ws_url, ssl=ssl_context, ping_interval=None)
    
    async def _login_and_join(self, ws):
        print(f"[INFO] 已连接斗鱼房间 {self.room_id}")

        # 登录房间
        await send_douyu_packet(ws, f"type@=loginreq/roomid@={self.room_id}/")
        await asyncio.sleep(0.5)

        # 加入分组（-9999 全部弹幕）
        await send_douyu_packet(ws, f"type@=joingroup/rid@={self.room_id}/gid@=-9999/")
        return
    
    async def _heartbeat_once(self, ws: websockets.WebSocketClientProtocol):
        """斗鱼心跳"""
        await send_douyu_packet(ws, "type@=mrkl/")
        return
            
    def _parse_messages(self, raw: Any) -> Any:
        return format_msg(raw, self.room_id)

