
import asyncio
import random
import ssl
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import certifi
import websockets
from live_platform.utils import setup_proxy_environment
from websockets.exceptions import ConnectionClosed, ConnectionClosedError, ConnectionClosedOK

class DropOldQueue(asyncio.Queue):
    """
    队列满时丢掉最旧的一条，保证实时性。
    """
    def __init__(self, maxsize: int):
        super().__init__(maxsize=maxsize)

    def put_nowait(self, item):
        if self.full():
            try:
                _ = self.get_nowait()
            except Exception:
                pass
        return super().put_nowait(item)

@dataclass
class Backoff:
    base: float = 2.0
    cap: float = 60.0
    jitter: float = 0.3
    attempt: int = 0

    def next_delay(self, *, severe: bool = False) -> float:
        """
        severe=True 表示疑似风控/握手失败等，退避加重
        """
        self.attempt += 1
        mult = 2.5 if severe else 1.0
        delay = min(self.cap, (self.base * (2 ** (self.attempt - 1))) * mult)
        
        j = delay * self.jitter
        return max(0.5, delay + random.uniform(-j, j))

    def reset(self):
        self.attempt = 0

class PlatformSocketBase:
    def __init__(
        self,
        platform: str,
        room_id: str,
        *,
        out_queue_maxsize: int = 5000,
        use_socks_proxy: bool = False,
        idle_timeout: int = 120,          # 假死检测：多少秒没收到任何数据就重连
        heartbeat_interval: int = 45,     # 心跳间隔（斗鱼/虎牙按你协议调）
        send_raw: bool = False            # 是否在事件里带 raw
    ):
        self.platform = platform
        self.room_id = str(room_id)
        self.use_socks_proxy = use_socks_proxy

        self._queue: DropOldQueue = DropOldQueue(maxsize=out_queue_maxsize)
        self._idle_timeout = idle_timeout
        self._heartbeat_interval = heartbeat_interval
        self._send_raw = send_raw

        self._ws: Optional[websockets.WebSocketClientProtocol] = None
        self._main_task: Optional[asyncio.Task] = None
        self._heartbeat_task: Optional[asyncio.Task] = None

        self._running: bool = False
        self._lock = asyncio.Lock()

        self._last_recv_ts: float = 0.0
        self._last_error: Optional[str] = None
        self._state: str = "INIT"

        self._backoff = Backoff()

    async def create_socket(self) -> "PlatformSocketBase":
        """
        启动实例（幂等）。返回 socket 实例（自身）。
        """
        async with self._lock:
            if self._main_task and not self._main_task.done():
                return self
            self._running = True
            self._main_task = asyncio.create_task(self._run())
            return self

    async def destroy_socket(self):
        """
        销毁实例（幂等）。会停止心跳/主循环并关闭 ws。
        """
        async with self._lock:
            self._state = "STOPPING"
            self._running = False

            # 先停心跳
            await self._stop_heartbeat()

            # 再关 ws（触发 recv loop 退出）
            await self._close_ws()

            # 再停主循环
            if self._main_task and not self._main_task.done():
                self._main_task.cancel()
                try:
                    await self._main_task
                except asyncio.CancelledError:
                    pass
                except Exception:
                    pass
            self._main_task = None

            self._state = "STOPPED"

    # ----------------
    # 提供给“房间聚合器/Hub”的消息输出
    # ----------------

    async def get_event(self) -> Dict[str, Any]:
        """
        从该房间的上游输出队列取一条标准事件。
        """
        return await self._queue.get()
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "platform": self.platform,
            "room_id": self.room_id,
            "state": self._state,
            "last_error": self._last_error,
            "last_recv_ts": self._last_recv_ts,
            "backoff_attempt": self._backoff.attempt,
        }

    # ----------------
    # 主循环：连接 + 登录 + 心跳 + 收包 + 假死检测 + 重连
    # ----------------

    async def _run(self):
        # socks 代理环境设置（保留你原来的逻辑）
        if self.use_socks_proxy:
            setup_proxy_environment(self.use_socks_proxy)

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        ssl_context.options |= ssl.OP_NO_SSLv2
        ssl_context.options |= ssl.OP_NO_SSLv3
        ssl_context.options |= ssl.OP_NO_TLSv1
        ssl_context.options |= ssl.OP_NO_TLSv1_1
        ssl_context.set_ciphers("DEFAULT")

        while self._running:
            self._state = "CONNECTING"
            severe = False
            try:
                ws = await self._connect_ws(ssl_context)
                self._ws = ws
                self._state = "RUNNING"
                self._last_error = None
                self._backoff.reset()

                self._last_recv_ts = time.time()

                # 登录/入组
                await self._login_and_join(ws)

                # 启动心跳（确保同一实例只有一个）
                await self._start_heartbeat(ws)

                # 收包循环（async for 更安全）
                async for raw in ws:
                    self._last_recv_ts = time.time()

                    # 解析 raw -> 多条消息（list/dict）
                    msgs = self._parse_messages(raw)

                    self._queue.put_nowait(msgs.to_dict())

                    # 假死检测：如果你想更激进，可以在这里偶尔检查
                    # （通常放到一个单独监控也行，这里为了简化放在循环间隙）

            except ConnectionClosedOK as e:
                # 正常关闭
                self._last_error = f"ConnectionClosedOK code={getattr(e, 'code', None)} reason={getattr(e, 'reason', None)}"
                severe = False

            except ConnectionClosedError as e:
                # 非正常关闭（可能网络抖动/服务器踢）
                self._last_error = f"ConnectionClosedError code={getattr(e, 'code', None)} reason={getattr(e, 'reason', None)}"
                # code=1006 常见于网络中断；不一定 severe
                severe = False

            except ConnectionClosed as e:
                self._last_error = f"ConnectionClosed code={getattr(e, 'code', None)} reason={getattr(e, 'reason', None)}"
                severe = False

            except OSError as e:
                self._last_error = f"OSError {repr(e)}"
                severe = False

            except Exception as e:
                # 包括握手失败、403等（websockets 可能抛 InvalidStatusCode/InvalidHandshake）
                self._last_error = f"Exception {repr(e)}"
                # 经验：握手失败/HTTP状态码异常更可能是风控/协议变化 → severe
                severe = True

            finally:
                # 收尾：停心跳、关 ws
                await self._stop_heartbeat()
                await self._close_ws()

            if not self._running:
                break

            # 假死检测：如果长时间没有任何消息，也主动重连
            # （有时 NAT/中间网络会让连接“看似还在但没数据”）
            if self._idle_timeout > 0 and self._last_recv_ts:
                if time.time() - self._last_recv_ts > self._idle_timeout:
                    self._last_error = f"IdleTimeout > {self._idle_timeout}s"
                    severe = False

            self._state = "RECONNECTING"
            delay = self._backoff.next_delay(severe=severe)
            await asyncio.sleep(delay)

        self._state = "STOPPED"

    # ----------------
    # 心跳：同实例唯一 + 与 ws 绑定
    # ----------------

    async def _start_heartbeat(self, ws: websockets.WebSocketClientProtocol):
        # 先停旧的
        await self._stop_heartbeat()

        async def loop():
            try:
                while self._running and self._ws is ws:
                    await asyncio.sleep(self._heartbeat_interval)
                    # 每次心跳发一次（子类实现）
                    await self._heartbeat_once(ws)
            except asyncio.CancelledError:
                pass
            except Exception as e:
                # 心跳异常通常意味着连接异常，交给外层重连
                self._last_error = f"HeartbeatError {repr(e)}"

        self._heartbeat_task = asyncio.create_task(loop())

    async def _stop_heartbeat(self):
        if self._heartbeat_task and not self._heartbeat_task.done():
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass
            except Exception:
                pass
        self._heartbeat_task = None

    async def _close_ws(self):
        if self._ws is not None:
            try:
                await self._ws.close()
            except Exception:
                pass
            self._ws = None

    # ----------------
    # 子类必须实现的4个方法
    # ----------------

    async def _connect_ws(self, ssl_context: ssl.SSLContext) -> websockets.WebSocketClientProtocol:
        raise NotImplementedError

    async def _login_and_join(self, ws: websockets.WebSocketClientProtocol):
        raise NotImplementedError

    def _parse_messages(self, raw: Any) -> Any:
        raise NotImplementedError

    async def _heartbeat_once(self, ws: websockets.WebSocketClientProtocol):
        raise NotImplementedError