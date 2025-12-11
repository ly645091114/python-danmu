# main.py
import asyncio
from app.tts_manager import TTSManager
from app.obs_overlay import broadcast_to_overlay

# 平台实现
from live_platform.douyu import connect_douyu
from live_platform.huya import Huya
# 以后可以:
# from platform.huya_client import connect_huya
# from platform.bilibili_client import connect_bili

from app.utils import load_config_txt

config = load_config_txt("config.txt")

PLATFORM = config.get("PLATFORM", "douyu")
ROOM_ID = config.get("ROOM_ID", 242737)
TTS_API_URL = config.get("TTS_API_URL", "http://127.0.0.1:9522/tts")
USE_SOCKS_PROXY = config.get("USE_SOCKS_PROXY", False)
OBS_WS_HOST = config.get("OBS_WS_HOST", "127.0.0.1")
OBS_WS_PORT = config.get("OBS_WS_PORT", 8765)
MIN_PRICE=config.get("MIN_PRICE", 0)
MAX_PRICE=config.get("MAX_PRICE", 10)
SPEAK_TXT=config.get("SPEAK_TXT", "normal,highenergy").split(",")
GIFT_MIN_PRICE=config.get("GIFT_MIN_PRICE", 100)
GIFT_MAX_PRICE=config.get("GIFT_MAX_PRICE", 0)

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
                min_price=MIN_PRICE,
                max_price=MAX_PRICE,
                use_socks_proxy=USE_SOCKS_PROXY,
            )
        )
    elif PLATFORM == "huya":
        client = Huya(
            room_Id=ROOM_ID,
            tts=tts,
            speak_txt=SPEAK_TXT,
            min_price=MIN_PRICE,
            max_price=MAX_PRICE,
            gift_min_price=GIFT_MIN_PRICE,
            gift_max_price=GIFT_MAX_PRICE
        )
        # client.start()
        asyncio.create_task(client.start())
    else:
        raise ValueError(f"未知平台: {PLATFORM}")

    # 4. 挂起
    await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("已退出")
