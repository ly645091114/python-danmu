import re
import ssl
import aiohttp
import certifi
from live_platform.plugins.huya_wup.wup_struct.WSRegisterGroupReq import HuyaWSRegisterGroupReq
from live_platform.plugins.huya_wup.wup_struct.WSPushMessage import HuyaWSPushMessage

from live_platform.common.tars import tarscore
from live_platform.plugins import match1
from live_platform.plugins.huya_wup.wup_struct import EWebSocketCommandType
from live_platform.plugins.huya_wup.wup_struct.WebSocketCommand import HuyaWebSocketCommand
from live_platform.plugins.huya_wup.wup_struct.WSUserInfo import HuyaWSUserInfo


class Huya:
    wss_url = 'wss://cdnws.api.huya.com/'
    heartbeat = b'\x00\x03\x1d\x00\x00\x69\x00\x00\x00\x69\x10\x03\x2c\x3c\x4c\x56\x08\x6f\x6e\x6c\x69\x6e\x65\x75' \
                b'\x69\x66\x0f\x4f\x6e\x55\x73\x65\x72\x48\x65\x61\x72\x74\x42\x65\x61\x74\x7d\x00\x00\x3c\x08\x00' \
                b'\x01\x06\x04\x74\x52\x65\x71\x1d\x00\x00\x2f\x0a\x0a\x0c\x16\x00\x26\x00\x36\x07\x61\x64\x72\x5f' \
                b'\x77\x61\x70\x46\x00\x0b\x12\x03\xae\xf0\x0f\x22\x03\xae\xf0\x0f\x3c\x42\x6d\x52\x02\x60\x5c\x60' \
                b'\x01\x7c\x82\x00\x0b\xb0\x1f\x9c\xac\x0b\x8c\x98\x0c\xa8\x0c '
    heartbeatInterval = 60
    # 等待统一ua后修改
    headers = {
        'user-agent': "'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/91.0.4472.124'",
    }

    @staticmethod
    async def get_ws_info(url):
        reg_datas = []
        room_id = url.split('huya.com/')[1].split('/')[0].split('?')[0]
        async with aiohttp.ClientSession() as session:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            ssl_context.options |= ssl.OP_NO_SSLv2
            ssl_context.options |= ssl.OP_NO_SSLv3
            ssl_context.options |= ssl.OP_NO_TLSv1
            ssl_context.options |= ssl.OP_NO_TLSv1_1
            ssl_context.set_ciphers("DEFAULT")
    
            async with session.get(f'https://m.huya.com/{room_id}', ssl_context=ssl_context, headers=Huya.headers, timeout=60 *  1000) as resp:
                room_page = await resp.text()
        
        def pick(pattern: str) -> int:
            m = re.search(pattern, room_page)
            if not m or m.group(1) == "":
                return 0
            return int(m.group(1))
        
        uid = int(pick(r'"lUid":(.*?),"iIsProfile"'))
        print(uid)
        req = HuyaWSRegisterGroupReq()
        req.vGroupId.append(f"live:{uid}")
        req.vGroupId.append(f"chat:{uid}")
        stream = tarscore.TarsOutputStream()
        req.writeTo(stream)
        # ws_user_info = HuyaWSUserInfo()
        # ws_user_info.iUid = uid
        # ws_user_info.bAnonymous = False
        # ws_user_info.lGroupId = uid
        # ws_user_info.lGroupType = 3
        # oos = tarscore.TarsOutputStream()
        # ws_user_info.writeTo(oos, ws_user_info)

        ws_cmd = HuyaWebSocketCommand()
        ws_cmd.iCmdType = EWebSocketCommandType.EWSCmdC2S_RegisterGroupReq
        ws_cmd.vData = stream.getBinBuffer()
        print(ws_cmd.vData)
        stream = tarscore.TarsOutputStream()
        ws_cmd.writeTo(stream)

        reg_datas.append(stream.getBuffer())

        return Huya.wss_url, reg_datas
    

    @staticmethod
    def decode_msg(data):
        class User(tarscore.struct):
            @staticmethod
            def readFrom(ios):
                return ios.read(tarscore.string, 2, False).decode("utf8")
        ios = tarscore.TarsInputStream(data)
        name = ""
        content = ""
        msgs = []
        iCmdType = ios.read(tarscore.int32, 0, False)
        print(iCmdType)
        vData = ios.read(tarscore.bytes, 1, False)
        if iCmdType == 7:
            ios = tarscore.TarsInputStream(vData)
            iUri = ios.read(tarscore.int64, 1, False)
            if iUri == 1400:
                ios = tarscore.TarsInputStream(ios.read(tarscore.bytes, 2, False))
                name = ios.read(User, 0, False)  # username
                content = ios.read(tarscore.string, 3, False).decode("utf8")  # content

        if name != "":
            msg = {"name": name, "content": content}
            # print(msg)
        return msgs