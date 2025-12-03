# overlay_server.py
import json
from typing import Dict, Any, Set

import websockets
from websockets import WebSocketServerProtocol

overlay_clients: Set[WebSocketServerProtocol] = set()


async def broadcast_to_overlay(event: Dict[str, Any]):
    """把弹幕事件广播给所有 OBS Browser 客户端"""
    if not overlay_clients:
        return
    msg = json.dumps(event, ensure_ascii=False)
    dead = []
    for ws in overlay_clients:
        try:
            await ws.send(msg)
        except Exception:
            dead.append(ws)
    for d in dead:
        overlay_clients.discard(d)


async def overlay_ws_handler(ws: WebSocketServerProtocol, path: str):
    print("Overlay client connected")
    overlay_clients.add(ws)
    try:
        async for _ in ws:
            # 前端如果有消息发回来，这里可以按需处理
            pass
    finally:
        overlay_clients.discard(ws)
        print("Overlay client disconnected")


async def start_overlay_server(host: str, port: int):
    """启动本地 WS 服务，返回 server 对象"""
    server = await websockets.serve(
        overlay_ws_handler,
        host,
        port,
    )
    print(f"本地 OBS WebSocket 已启动：ws://{host}:{port}")
    return server
