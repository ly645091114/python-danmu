import re
import ssl
import aiohttp
import certifi
import websockets
import asyncio
from live_platform.plugins.huya_wup.wup import Wup
from live_platform.plugins.huya_wup.wup_struct.TafMx import TafMx

from live_platform.common.tars import tarscore
from live_platform.plugins.huya_wup.wup_struct.UserId import HuyaUserId
from live_platform.plugins.huya_wup.wup_struct.GetPropsListReq import HuyaGetPropsListReq
from live_platform.plugins.huya_wup.wup_struct import EClientTemplateType, EStreamLineType, EWebSocketCommandType
from live_platform.plugins.huya_wup.wup_struct.WebSocketCommand import HuyaWebSocketCommand
from live_platform.plugins.huya_wup.wup_struct.WSRegisterGroupReq import HuyaWSRegisterGroupReq
from live_platform.plugins.huya_wup.wup_struct.UserHeartBeatReq import HuyaUserHeartBeatReq
from live_platform.plugins.huya_wup.wup_struct.WSPushMessage import HuyaWSPushMessage


class Huya:
    
    def __init__(self, room_Id, sHuYaUA="webh5&2106011457&websocket", sCookie=""):
        self.wss_url = 'wss://cdnws.api.huya.com/'
        self.heartbeat = b'\x00\x03\x1d\x00\x00\x69\x00\x00\x00\x69\x10\x03\x2c\x3c\x4c\x56\x08\x6f\x6e\x6c\x69\x6e\x65\x75' \
                b'\x69\x66\x0f\x4f\x6e\x55\x73\x65\x72\x48\x65\x61\x72\x74\x42\x65\x61\x74\x7d\x00\x00\x3c\x08\x00' \
                b'\x01\x06\x04\x74\x52\x65\x71\x1d\x00\x00\x2f\x0a\x0a\x0c\x16\x00\x26\x00\x36\x07\x61\x64\x72\x5f' \
                b'\x77\x61\x70\x46\x00\x0b\x12\x03\xae\xf0\x0f\x22\x03\xae\xf0\x0f\x3c\x42\x6d\x52\x02\x60\x5c\x60' \
                b'\x01\x7c\x82\x00\x0b\xb0\x1f\x9c\xac\x0b\x8c\x98\x0c\xa8\x0c '
        self.heartbeatInterval = 60
        self.headers = {
            'user-agent': "'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/91.0.4472.124'",
        }
        self._client = None
        self._heartbeat_task = None
        self.room_Id = room_Id
        self.info = None
        self.timeout = 60
        self.heartbeatTime = 60
        self.sHuYaUA = sHuYaUA
        self.cookies = sCookie
        self._gift_info = {}


    def _get_user_id(self):
        user = HuyaUserId()
        user.sHuYaUA = self.sHuYaUA
        user.lUid = int(self.info["presenterUid"])
        user.sCookie = self.cookies
        user.sGuid = self.info.get("sGuid", "")
        user.sToken = ""
        return user

    async def _get_room_info(self):
        try:
            async with aiohttp.ClientSession() as session:
                ssl_context = ssl.create_default_context(cafile=certifi.where())
                ssl_context.options |= ssl.OP_NO_SSLv2
                ssl_context.options |= ssl.OP_NO_SSLv3
                ssl_context.options |= ssl.OP_NO_TLSv1
                ssl_context.options |= ssl.OP_NO_TLSv1_1
                ssl_context.set_ciphers("DEFAULT")
        
                async with session.get(f'https://m.huya.com/{self.room_Id}', ssl_context=ssl_context, headers=self.headers, timeout=self.timeout *  1000) as resp:
                    if resp.status != 200:
                        raise RuntimeError(f"获取房间信息失败 status={resp.status}")
                    room_page = await resp.text()
            
            def pick(pattern: str) -> int:
                m = re.search(pattern, room_page)
                if not m or m.group(1) == "":
                    return 0
                return int(m.group(1))
            
            info = {
                "presenterUid": pick(r'"lUid":(.*?),"iIsProfile"'),
                "yyuid": pick(r'"lYyid":(.*?),"sNick"'),
                "lChannelId": pick(r'"lChannelId":(.*?),"lSubChannelId"'),
                "lSubChannelId": pick(r'"lSubChannelId":(.*?),"lPresenterUid"'),
                "sGuid": "",
            }
            
            if not info["presenterUid"] or not info["yyuid"]:
                return
            if not info["lChannelId"]:
                raise RuntimeError(f"房间 {self.room_Id} 不存在或已停播")
            
            return info
        except Exception as e:
            print("onError:", e)
            return

    @staticmethod
    async def get_ws_info(url):
        room_id = url.split('huya.com/')[1].split('/')[0].split('?')[0]
        room_info = await Huya._get_room_info(room_id)
        return room_info
    
    def _get_gift(self):
        prop_req = HuyaGetPropsListReq()
        prop_req.tUserId = self._get_user_id()
        prop_req.iTemplateType = EClientTemplateType.TPL_MIRROR
        self.send_packet("PropsUIServer", "getPropsList", prop_req)
    
    def _get_chat(self):
        req = HuyaWSRegisterGroupReq()
        req.vGroupId.append(f'live:{self.info["presenterUid"]}')
        req.vGroupId.append(f'chat:{self.info["presenterUid"]}')
        stream = tarscore.TarsOutputStream()
        req.writeTo(stream, req)
        webCommand = HuyaWebSocketCommand()
        webCommand.iCmdType = EWebSocketCommandType.EWSCmdC2S_RegisterGroupReq
        webCommand.vData = stream.getBuffer()
        stream = tarscore.TarsOutputStream()
        webCommand.writeTo(stream, webCommand)
        asyncio.create_task(self._sendMsg(stream.getBuffer()))

    def _heartbeat(self):
        heart_beat_req = HuyaUserHeartBeatReq()
        heart_beat_req.tId = self._get_user_id()
        heart_beat_req.lTid = self.info["lChannelId"]
        heart_beat_req.lSid = self.info["lSubChannelId"]
        heart_beat_req.lPid = self.info["yyuid"]
        heart_beat_req.bWatchVideo = True
        heart_beat_req.eLineType = EStreamLineType.STREAM_LINE_AL
        heart_beat_req.iFps = 0
        heart_beat_req.iAttendee = 0
        heart_beat_req.iLastHeartElapseTime = 0
        self.send_packet("onlineui", "OnUserHeartBeat", heart_beat_req)

    def send_packet(self, servant: str, func: str, req):
        try:
            wup_req = Wup()
            wup_req.servant = servant
            wup_req.func = func
            wup_req.put(vtype=tarscore.struct, name="tReq", value=req)
            webCommand = HuyaWebSocketCommand()
            webCommand.iCmdType = EWebSocketCommandType.EWSCmd_WupReq
            webCommand.vData = wup_req.encode_v3()
            jceStream = tarscore.TarsOutputStream()
            webCommand.writeTo(jceStream, webCommand)
            asyncio.create_task(self._sendMsg(jceStream.getBuffer()))
        except Exception as e:
            print("onError:", e)
            return

    async def _sendMsg(self, message):
        await self._client.send(message)
    
    async def _start_ws(self):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        ssl_context.options |= ssl.OP_NO_SSLv2
        ssl_context.options |= ssl.OP_NO_SSLv3
        ssl_context.options |= ssl.OP_NO_TLSv1
        ssl_context.options |= ssl.OP_NO_TLSv1_1
        ssl_context.set_ciphers("DEFAULT")
        self._client = await websockets.connect(self.wss_url, ssl=ssl_context, compression=None, open_timeout=self.timeout, max_size=None)

        asyncio.create_task(self._recv_loop())
        self._get_gift()
        self._get_chat()
        self._heartbeat()
        self._heartbeat_task = asyncio.create_task(self._heartbeat_interval())

    async def _heartbeat_interval(self):
        while True:
            await asyncio.sleep(self.heartbeatTime)
            self._heartbeat()

    async def _recv_loop(self):
        try:
            while True:
                msg = await self._client.recv()   # <- 逐条收消息
                self._on_message(msg)
        except Exception as e:
            print("WebSocket recv error:", e)

    def handle_gift_info(self, message):
        for item in message.vPropsItemList:
            name = item.sPropsName.decode("utf8")
            icon = ""
            try:
                if item.vPropView and len(item.vPropView) > 0:
                    name = item.vPropView[0].name.decode("utf8")

                if item.vPropsIdentity and len(item.vPropsIdentity) > 0:
                    raw = item.vPropsIdentity[0].sPropsWeb.decode("utf8") or ""
                    icon = raw.split("&")[0]

                self._gift_info[str(item.iPropsId)] = {
                    "name": name,
                    "price": int(item.iPropsYb) / 100,
                    "icon": icon,
                }
            except Exception:
                pass

    def _on_message(self, message):
        buf = memoryview(message).tobytes()
        stream = tarscore.TarsInputStream(buf)
        webCommand = HuyaWebSocketCommand()
        resData = webCommand.readFrom(stream)
        if resData.iCmdType == EWebSocketCommandType.EWSCmd_WupRsp:
            try:
                wup = Wup()
                wup.decode_v3(resData.vData)
                funcName = wup.func.decode("utf8")
                rsp_cls = TafMx.WupMapping.get(funcName)
                if rsp_cls is not None:
                    rsp_obj = wup.get(vtype=rsp_cls, name="tRsp")
                    if funcName == "getPropsList":
                        self.handle_gift_info(rsp_obj)
            except Exception as e:
                print("WupRsp decode error:", e)

        if resData.iCmdType == EWebSocketCommandType.EWSCmdS2C_MsgPushReq:
            try:
                ios = tarscore.TarsInputStream(resData.vData)
                push_message = HuyaWSPushMessage()
                data = push_message.readFrom(ios)
                mcs = int(data.iUri)
                print(mcs)
                # ios_msg = tarscore.TarsInputStream(data.sMsg)
                # uri_cls = TafMx.UriMapping.get(mcs)
                # if uri_cls is not None:
                #     msg = uri_cls()
                #     msg.readFrom(ios_msg)

                #     if mcs == 1400:
                #         print({
                #             "timestamp": str(int(self._now_ms())),
                #             "uid": str(msg.tUserInfo.lUid),
                #             "nickName": msg.tUserInfo.sNickName.decode("utf8"),
                #             "txt": msg.sContent.decode("utf8"),
                #         })
                #     if mcs in (6501, 6502, 6507):
                #         gift = self._gift_info.get(str(msg.iItemType), {"price": 0})
                #         print({
                #             "timestamp": str(int(self._now_ms())),
                #             "uid": str(msg.lSenderUid),
                #             "nickName": msg.sSenderNick.decode("utf8"),
                #             "type": mcs,
                #             "gfid": msg.iItemType.decode("utf8"),
                #             "gfcnt": int(msg.iItemCount),
                #             "gift_name": gift.get("name"),
                #             "gift_icon": gift.get("icon"),
                #             "price_big": gift.get("price", 0),
                #             "price_total": int(msg.iItemCount) * gift.get("price", 0),
                #         })
            except Exception as e:
                print("WupRsp decode error:", e)

    
    async def start(self):
        self.info = await self._get_room_info()
        if self.info:
            await self._start_ws()
