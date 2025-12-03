# main.py
import asyncio

from config import (
    PLATFORM,
    ROOM_ID,
    OBS_WS_HOST,
    OBS_WS_PORT,
    USE_SOCKS_PROXY,
    TTS_API_URL,
)
from app.tts_manager import TTSManager
from app.obs_overlay import start_overlay_server, broadcast_to_overlay

# 平台实现
from live_platform.douyu import connect_douyu
# 以后可以:
# from platform.huya_client import connect_huya
# from platform.bilibili_client import connect_bili


async def main():
    # 1. 初始化 TTS 管理器
    tts = TTSManager(mode="all", min_interval=0.5, tts_api_url=TTS_API_URL)

    # 2. 启动本地 OBS WebSocket 服务
    # await start_overlay_server(OBS_WS_HOST, OBS_WS_PORT)

    # 3. 根据 PLATFORM 启动相应平台的弹幕客户端
    if PLATFORM == "douyu":
        asyncio.create_task(
            connect_douyu(
                room_id=ROOM_ID,
                tts=tts,
                broadcast=broadcast_to_overlay,
                use_socks_proxy=USE_SOCKS_PROXY,
            )
        )
    # elif PLATFORM == "huya":
    #     asyncio.create_task(
    #         connect_huya(
    #             room_id=HUYA_ROOM_ID,
    #             tts=tts,
    #             broadcast=broadcast_to_overlay,
    #         )
    #     )
    else:
        raise ValueError(f"未知平台: {PLATFORM}")

    # 4. 挂起
    await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("已退出")
