import re
import ssl
import aiohttp
import certifi
import websockets
import asyncio
from live_platform.plugins.huya_wup.wup import Wup
from live_platform.plugins.huya_wup.wup_struct.TafMx import TafMx
from app.tts_manager import TTSManager

from live_platform.common.tars import tarscore
from live_platform.plugins.huya_wup.wup_struct.UserId import HuyaUserId
from live_platform.plugins.huya_wup.wup_struct.GetPropsListReq import HuyaGetPropsListReq
from live_platform.plugins.huya_wup.wup_struct import EClientTemplateType, EStreamLineType, EWebSocketCommandType
from live_platform.plugins.huya_wup.wup_struct.WebSocketCommand import HuyaWebSocketCommand
from live_platform.plugins.huya_wup.wup_struct.WSRegisterGroupReq import HuyaWSRegisterGroupReq
from live_platform.plugins.huya_wup.wup_struct.UserHeartBeatReq import HuyaUserHeartBeatReq
from live_platform.plugins.huya_wup.wup_struct.WSPushMessage import HuyaWSPushMessage
from live_platform.plugins.huya_wup.wup_struct.OnTVUserReq import HuyaOnTVUserReq


class Huya:
    
    def __init__(
            self,
            room_Id,
            sHuYaUA="webh5&1.0.0&huya",
            sCookie="",
            tts: TTSManager = None,
            speak_txt = ["highenergy"],
            min_price: int = 0,
            max_price: int = 10,
    ):
        self.wss_url = 'wss://cdnws.api.huya.com/'
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
        self.tts = tts
        self.speak_txt = speak_txt
        self.min_price = min_price
        self.max_price = max_price


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

    def _get_on_tv_panel(self):
        req = HuyaOnTVUserReq()
        req.tUserId = self._get_user_id()
        req.lPid = self.info["presenterUid"]
        req.lTid = self.info["lChannelId"]
        req.lSid = self.info["lSubChannelId"]
        req.iSupportFlag = 1
        self.send_packet("revenueui", "getOnTVPanel", req)

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
        self._get_on_tv_panel()
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
                ios_msg = tarscore.TarsInputStream(data.sMsg)
                uri_cls = TafMx.UriMapping.get(mcs)
                if uri_cls is not None:
                    source = uri_cls()
                    msg =  source.readFrom(ios_msg)
                    if mcs == 1400 and "normal" in self.speak_txt:
                        nickName = msg.tUserInfo.sNickName.decode("utf8")
                        txt = msg.sContent.decode("utf8")
                        print(f"{nickName}说: {txt}")
                        self.tts.speak_normal(f"{nickName}说{txt}")

                    elif mcs == 6501:
                        gift = self._gift_info.get(str(msg.iItemType), {"price": 0})
                        nickName = msg.sSenderNick.decode("utf8"),
                        price = gift.get("price", 0)
                        text = msg.sCustomText.decode("utf8")
                        # 如果有 custom_text 说明是上头条走上头条逻辑
                        if text and "highenergy" in self.speak_txt and price > self.min_price and price < self.max_price + 1:
                            print(f"[高能] {nickName} ({price} 元): {text}")
                            self.tts.speak_normal(f"{nickName}说{text}")
                        else:
                            print(f"[礼物] {nickName} 送出 {int(msg.iItemCount)} 个 {gift.get('name')}")

                    elif mcs in (6502, 6507):
                        gift = self._gift_info.get(str(msg.iItemType), {"price": 0})
                        print(f"[礼物] {nickName} 送出 {int(msg.iItemCount)} 个 {gift.get('name')}")
            except Exception as e:
                print("WupRsp decode error:", e)

    
    async def start(self):
        self.info = await self._get_room_info()
        if self.info:
            await self._start_ws()
