import re
from datetime import datetime
from typing import Dict

from live_platform.utils import EmitMessage

pattern = re.compile(r"(\w+)@=([^/]+)")
PLATFORM = "douyu"

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
    
def format_msg(raw, room_id):
    msgs = decode_douyu_message(raw)
    now = datetime.now().strftime("%H:%M:%S")

    for msg in msgs:
        msg_type = msg.get("type", "")
        msg_body = EmitMessage()
        msg_body.platform = PLATFORM
        msg_body.roomId = room_id
        msg_body.time = now

        # 普通弹幕
        if msg_type == "chatmsg":
            uname = msg.get("nn", "某位观众")
            text = msg.get("txt", "")
            print(f"[{now}] [弹幕] {uname}：{text}")
            msg_body.type = "msg"
            msg_body.data = {
                "user": uname,
                "content": text,
            }
            return msg_body
        # # 礼物
        # elif msg_type == "dgb":
        #     uname = msg.get("nn", "某位观众")
        #     gs = msg.get("gs", "")
        #     bg = msg.get("bg", "")
        #     cnt = msg.get("gfc", "1")
        #     print(f"[礼物] {uname} 送出 {cnt} 个 {gs}")
        #     msg_body.type = "gift"
        #     msg_body.data = {
        #         "user": uname,
        #         "gs": gs,
        #         "bg": bg,
        #         "count": cnt,
        #     }
        #     return msg_body

        # 高能弹幕（SuperChat）
        elif msg_type == "voice_trlt":
            list_raw = msg.get("list", "")
            data_map = parse_douyu_list(list_raw) if list_raw else {}

            if data_map:
                try:
                    uname = data_map.get("un", "")
                    text = data_map.get("content", "")
                    raw_price = data_map.get("price") or "0"
                    price_fen = int(raw_price)
                    price_yuan = price_fen / 100.0
                    print(f"[{now}] [高能] {uname} ({price_yuan} 元): {text}")
                    msg_body.type = "highenergy"
                    msg_body.data = {
                        "user": uname,
                        "content": text,
                        "amount": price_yuan,
                    }
                    return msg_body
                except ValueError:
                    pass