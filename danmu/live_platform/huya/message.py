from datetime import datetime

from live_platform.utils import EmitMessage
from live_platform.huya.common.tars import tarscore
from live_platform.huya.plugins.huya_wup.wup_struct.TafMx import TafMx
from live_platform.huya.plugins.huya_wup.wup_struct.WSPushMessage import HuyaWSPushMessage


def formatMsg(data, room_id, gift_info):
    try:
        now = datetime.now().strftime("%H:%M:%S")
        msg_body = EmitMessage()
        msg_body.platform = "huya"
        msg_body.roomId = room_id
        msg_body.time = now

        ios = tarscore.TarsInputStream(data)
        push_message = HuyaWSPushMessage()
        data = push_message.readFrom(ios)
        mcs = int(data.iUri)
        ios_msg = tarscore.TarsInputStream(data.sMsg)
        uri_cls = TafMx.UriMapping.get(mcs)
        if uri_cls is not None:
            source = uri_cls()
            msg =  source.readFrom(ios_msg)
            if mcs == 1400:
                nickName = msg.tUserInfo.sNickName.decode("utf8")
                txt = msg.sContent.decode("utf8")
                print(f"[{now}] [弹幕] {nickName}：{txt}")
                msg_body.type = "msg"
                msg_body.data = {
                    "user": nickName,
                    "content": txt,
                }
                return msg_body

            elif mcs == 6501:
                gift = gift_info.get(str(msg.iItemType), {"price": 0})
                nickName = msg.sSenderNick.decode("utf8"),
                price = gift.get("price", 0)
                text = msg.sCustomText.decode("utf8")
                # 如果有 custom_text 说明是上头条走上头条逻辑
                if text:
                    print(f"[{now}] [高能] {nickName} ({price} 元): {text}")
                    msg_body.type = "highenergy"
                    msg_body.data = {
                        "user": nickName,
                        "content": text,
                        "amount": price,
                    }
                    return msg_body
                else:
                    print(f"[{now}] [礼物] {nickName} 送出 {int(msg.iItemCount)} 个 {gift.get('name')}")
                    msg_body.type = "gift"
                    msg_body.data = {
                        "user": nickName,
                        "giftName": gift.get('name'),
                        "amount": price,
                        "count": int(msg.iItemCount)
                    }
                    return msg_body

            elif mcs in (6502, 6507):
                gift = gift_info.get(str(msg.iItemType), {"price": 0})
                price = gift.get("price", 0)
                print(f"[{now}] [礼物] {nickName} 送出 {int(msg.iItemCount)} 个 {gift.get('name')}")
                msg_body.type = "gift"
                msg_body.data = {
                    "user": nickName,
                    "giftName": gift.get('name'),
                    "amount": price,
                    "count": int(msg.iItemCount)
                }
                return msg_body
        return
    except Exception as e:
        print("WupRsp decode error:", e)