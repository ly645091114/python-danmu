# main.py
import asyncio
from dataclasses import dataclass
import json
import os
from typing import Any, Dict, List, Optional, Tuple
from dotenv import load_dotenv

# 平台实现
from live_platform.douyu import DouyuClient
from live_platform.huya import HuyaClient

load_dotenv()

PLATFORM=os.getenv("PLATFORM", "douyu")
ROOM_ID=os.getenv("ROOM_ID", 242737)
USE_SOCKS_PROXY=os.getenv("USE_SOCKS_PROXY", False)
HOST=os.getenv("OBS_WS_HOST", "127.0.0.1")
PORT=os.getenv("OBS_WS_PORT", 8765)
CLIENT_HEARTBEAT_TIMEOUT=os.getenv("CLIENT_HEARTBEAT_TIMEOUT", 60)
ROOM_IDLE_SHUTDOWN_DELAY=os.getenv("ROOM_IDLE_SHUTDOWN_DELAY", 30)
CLIENT_SEND_QUEUE_MAXSIZE=os.getenv("CLIENT_SEND_QUEUE_MAXSIZE", 200)
SEND_TIMEOUT=os.getenv("SEND_TIMEOUT", 5)

RoomKey = Tuple[str, str]  # (platform, room_id)

# =========================
# 队列：丢旧保新（实时优先）
# =========================

class DropOldQueue(asyncio.Queue):
    def __init__(self, maxsize: int):
        super().__init__(maxsize=maxsize)

    def put_nowait(self, item):
        if self.full():
            try:
                _ = self.get_nowait()
            except Exception:
                pass
        return super().put_nowait(item)

# =========================
# 客户端会话
# =========================

@dataclass
class ClientSession:
    writer: asyncio.StreamWriter
    config: dict
    last_heartbeat: float
    send_queue: DropOldQueue
    send_task: Optional[asyncio.Task] = None
    hb_watch_task: Optional[asyncio.Task] = None

# =========================
# 平台源接口（你平台对接层应提供）
# =========================

class PlatformSource:
    """
    约定接口（你的平台层已完成，确保符合这个形态即可）：
      - await create_socket() -> 返回自身/实例
      - await destroy_socket()
      - await get_event() -> dict（阻塞等待一条标准化事件）
    """
    async def create_socket(self): ...
    async def destroy_socket(self): ...
    async def get_event(self) -> dict: ...

# =========================
# 平台工厂（你只要改这里对接你已完成的平台层）
# =========================

class PlatformFactory:
    @staticmethod
    def create(platform: str, room_id: str) -> PlatformSource:
        if platform == "douyu":
            return DouyuClient(
                room_id=room_id,
                use_socks_proxy=USE_SOCKS_PROXY,
            )

        elif platform == "huya":
            return HuyaClient(
                room_id=room_id,
                use_socks_proxy=USE_SOCKS_PROXY,
            )

        else:
            raise NotImplementedError(
                "请在 PlatformFactory.create() 中接入你已完成的平台对接层：返回一个支持 create_socket/destroy_socket/get_event 的对象"
            )
        
# =========================
# 房间上下文（每房间一个）
# =========================

@dataclass
class RoomContext:
    key: RoomKey
    source: PlatformSource
    clients: List[ClientSession]
    fanout_task: Optional[asyncio.Task] = None
    idle_shutdown_task: Optional[asyncio.Task] = None

# =========================
# Hub（核心：复用房间上游连接 + 只推送到对应房间客户端）
# =========================

class SocketHub:
    def __init__(self):
        self._rooms: Dict[RoomKey, RoomContext] = {}
        self._lock = asyncio.Lock()

    # ---------- 客户端入口 ----------

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info("peername")
        print(f"[CLIENT] connect {addr}")

        room_key: Optional[RoomKey] = None
        session: Optional[ClientSession] = None

        try:
            # 1) 读第一行配置（JSON）
            line = await reader.readline()
            if not line:
                return

            cfg = self._parse_config_line(line.decode("utf-8").strip())
            platform = str(cfg.get("platform", "")).strip()
            room_id = str(cfg.get("room_id", "")).strip()
            if not platform or not room_id:
                await self._send_line(writer, {"type": "err", "msg": "missing platform/room_id"})
                return

            room_key = (platform, room_id)

            # 2) 注册订阅（复用/创建房间上游连接）
            session = await self._register(room_key, writer, cfg)

            # 3) 回复订阅成功
            await self._send_line(writer, {"type": "sub_ok", "platform": platform, "room_id": room_id})

            # 4) 读客户端消息（心跳）
            loop = asyncio.get_running_loop()
            while True:
                data = await reader.readline()
                if not data:
                    break
                text = data.decode("utf-8").strip()
                if not text:
                    continue

                # 简单协议：PING
                if text.upper() == "PING":
                    session.last_heartbeat = loop.time()
                    writer.write(b"PONG\n")
                    await writer.drain()
                    continue

                # JSON 心跳
                try:
                    obj = json.loads(text)
                    if obj.get("type") == "heartbeat":
                        session.last_heartbeat = loop.time()
                        await self._send_line(writer, {"type": "heartbeat_ack"})
                        continue
                except json.JSONDecodeError:
                    pass

        except Exception as e:
            print(f"[CLIENT] error {addr}: {e}")
        finally:
            if room_key and session:
                await self._unregister(room_key, session)
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            print(f"[CLIENT] disconnect {addr}")

    # ---------- 房间/订阅管理 ----------

    async def _register(self, key: RoomKey, writer: asyncio.StreamWriter, cfg: dict) -> ClientSession:
        loop = asyncio.get_running_loop()
        session = ClientSession(
            writer=writer,
            config=cfg,
            last_heartbeat=loop.time(),
            send_queue=DropOldQueue(CLIENT_SEND_QUEUE_MAXSIZE),
        )

        async with self._lock:
            # 如果房间存在，取消“空闲关闭”任务并复用上游连接
            room = self._rooms.get(key)
            if room is None:
                # 创建房间：建立平台上游连接（只建一次）
                platform, room_id = key
                source = PlatformFactory.create(platform, room_id, cfg)
                room = RoomContext(key=key, source=source, clients=[])
                self._rooms[key] = room

                # 启动平台 socket
                await room.source.create_socket()

                # 启动 fanout（从平台层拉事件，推给该房间客户端）
                room.fanout_task = asyncio.create_task(self._fanout_loop(room))

                print(f"[ROOM] created {key}")

            # 如果之前挂了 idle 关闭任务，取消
            if room.idle_shutdown_task and not room.idle_shutdown_task.done():
                room.idle_shutdown_task.cancel()
                try:
                    await room.idle_shutdown_task
                except asyncio.CancelledError:
                    pass
                room.idle_shutdown_task = None

            # 加入客户端
            room.clients.append(session)
            print(f"[ROOM] {key} add client, n={len(room.clients)}")

            # 启动客户端发送任务 + 心跳监控
            session.send_task = asyncio.create_task(self._client_send_loop(key, session))
            session.hb_watch_task = asyncio.create_task(self._client_heartbeat_watch(key, session))

        return session

    async def _unregister(self, key: RoomKey, session: ClientSession):
        async with self._lock:
            room = self._rooms.get(key)
            if not room:
                return

            # 移除 session
            if session in room.clients:
                room.clients.remove(session)
            print(f"[ROOM] {key} remove client, n={len(room.clients)}")

            # 停止客户端任务
            await self._stop_client_tasks(session)

            # 如果房间没人了，启动延迟关闭（防抖）
            if not room.clients:
                if room.idle_shutdown_task and not room.idle_shutdown_task.done():
                    # 已经有一个延迟关闭任务在跑了
                    return
                room.idle_shutdown_task = asyncio.create_task(self._idle_shutdown(key))

    async def _idle_shutdown(self, key: RoomKey):
        await asyncio.sleep(ROOM_IDLE_SHUTDOWN_DELAY)

        async with self._lock:
            room = self._rooms.get(key)
            if not room:
                return
            if room.clients:
                return  # 期间又有人订阅了

            # 关闭 fanout
            if room.fanout_task and not room.fanout_task.done():
                room.fanout_task.cancel()
                try:
                    await room.fanout_task
                except asyncio.CancelledError:
                    pass
                room.fanout_task = None

            # 关闭平台上游连接
            try:
                await room.source.destroy_socket()
            except Exception as e:
                print(f"[ROOM] destroy source error {key}: {e}")

            # 删除房间
            self._rooms.pop(key, None)
            print(f"[ROOM] closed {key}")

    # ---------- fanout：只推送给该房间的客户端 ----------

    async def _fanout_loop(self, room: RoomContext):
        key = room.key
        try:
            while True:
                evt = await room.source.get_event()  # 平台层产出的标准 event

                # 只发给该房间客户端
                async with self._lock:
                    clients = list(room.clients)

                # 可选：这里加过滤 match_by_config(evt, session.config)
                for s in clients:
                    if s.writer.is_closing():
                        continue
                    try:
                        s.send_queue.put_nowait(evt)
                    except Exception:
                        # 队列异常则忽略
                        pass

        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f"[FANOUT] {key} error: {e}")

    # ---------- 客户端发送：慢客户端不拖全局 ----------

    async def _client_send_loop(self, key: RoomKey, session: ClientSession):
        writer = session.writer
        try:
            while True:
                evt = await session.send_queue.get()
                # 单次发送超时保护
                await asyncio.wait_for(self._send_line(writer, evt), timeout=SEND_TIMEOUT)
        except asyncio.CancelledError:
            pass
        except (asyncio.TimeoutError, ConnectionError, BrokenPipeError):
            # 发送太慢或连接问题：让上层去 unregister
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        except Exception:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

    # ---------- 客户端心跳监控：超时踢掉并触发房间关闭判定 ----------

    async def _client_heartbeat_watch(self, key: RoomKey, session: ClientSession):
        loop = asyncio.get_running_loop()
        try:
            while True:
                await asyncio.sleep(CLIENT_HEARTBEAT_TIMEOUT / 2)
                if loop.time() - session.last_heartbeat > CLIENT_HEARTBEAT_TIMEOUT:
                    # 心跳超时：主动断开
                    try:
                        session.writer.close()
                        await session.writer.wait_closed()
                    except Exception:
                        pass
                    # 触发 unregister（不要在锁内调用）
                    await self._unregister(key, session)
                    break
        except asyncio.CancelledError:
            pass

    # ---------- 工具 ----------

    async def _stop_client_tasks(self, session: ClientSession):
        if session.hb_watch_task and not session.hb_watch_task.done():
            session.hb_watch_task.cancel()
            try:
                await session.hb_watch_task
            except asyncio.CancelledError:
                pass
        session.hb_watch_task = None

        if session.send_task and not session.send_task.done():
            session.send_task.cancel()
            try:
                await session.send_task
            except asyncio.CancelledError:
                pass
        session.send_task = None

    async def _send_line(self, writer: asyncio.StreamWriter, obj: Any):
        data = json.dumps(obj, ensure_ascii=False) + "\n"
        writer.write(data.encode("utf-8"))
        await writer.drain()

    def _parse_config_line(self, line: str) -> dict:
        """
        首行 JSON 配置（只允许 platform + roomId）
        兼容大小写 & roomId / room_id 写法

        示例：
        {"platform":"douyu","roomId":"123"}
        {"PLATFORM":"douyu","ROOM_ID":"123"}
        """
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            raise ValueError("config must be valid JSON")

        # 统一 platform
        platform = (
            raw.get("platform")
            or raw.get("PLATFORM")
        )

        # 统一 room_id（兼容 roomId / ROOM_ID）
        room_id = (
            raw.get("room_id")
            or raw.get("roomId")
            or raw.get("ROOM_ID")
            or raw.get("ROOMID")
        )

        if not platform or not room_id:
            raise ValueError("config must contain platform and roomId")

        return {
            "platform": str(platform).lower(),
            "room_id": str(room_id),
        }

# =========================
# main 启动
# =========================

async def main():
    hub = SocketHub()

    server = await asyncio.start_server(
        hub.handle_client,
        host=HOST,
        port=PORT,
    )

    print(f"[SERVER] listening on {HOST}:{PORT}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[SERVER] exit")
