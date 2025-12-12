import re
import ssl
from typing import Any
import aiohttp
import certifi
import websockets
import asyncio

from live_platform.huya.plugins.huya_wup.wup import Wup
from live_platform.huya.plugins.huya_wup.wup_struct.TafMx import TafMx
from live_platform.huya.message import formatMsg

from live_platform import PlatformSocketBase
from live_platform.huya.common.tars import tarscore
from live_platform.huya.plugins.huya_wup.wup_struct.UserId import HuyaUserId
from live_platform.huya.plugins.huya_wup.wup_struct.GetPropsListReq import HuyaGetPropsListReq
from live_platform.huya.plugins.huya_wup.wup_struct import EClientTemplateType, EStreamLineType, EWebSocketCommandType
from live_platform.huya.plugins.huya_wup.wup_struct.WebSocketCommand import HuyaWebSocketCommand
from live_platform.huya.plugins.huya_wup.wup_struct.WSRegisterGroupReq import HuyaWSRegisterGroupReq
from live_platform.huya.plugins.huya_wup.wup_struct.UserHeartBeatReq import HuyaUserHeartBeatReq
from live_platform.huya.plugins.huya_wup.wup_struct.OnTVUserReq import HuyaOnTVUserReq

class HuyaClient(PlatformSocketBase):

    def __init__(
        self,
        room_id: int,
        *,
        use_socks_proxy: bool = False,
        ws_url: str = "wss://cdnws.api.huya.com/",
        idle_timeout: int = 120,          # 假死检测：多少秒没收到任何数据就重连
        heartbeat_interval: int = 60,     # 心跳间隔（斗鱼/虎牙按你协议调）
    ):
        super().__init__(
            platform="huya",
            room_id=room_id,
            heartbeat_interval=heartbeat_interval,
            idle_timeout=idle_timeout,
            use_socks_proxy=use_socks_proxy
        )
        self.headers = {
            'user-agent': "'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/91.0.4472.124'",
        }
        self._ws_url = ws_url
        self.timeout = 60
        self.sHuYaUA = "webh5&1.0.0&huya"
        self.cookies = ""
        self.info = None
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
        
                async with session.get(f'https://m.huya.com/{self.room_id}', ssl_context=ssl_context, headers=self.headers, timeout=self.timeout *  1000) as resp:
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
                raise RuntimeError(f"房间 {self.room_id} 不存在或已停播")
            
            return info
        except Exception as e:
            print("onError:", e)
            return
    
    def _get_gift(self, ws):
        prop_req = HuyaGetPropsListReq()
        prop_req.tUserId = self._get_user_id()
        prop_req.iTemplateType = EClientTemplateType.TPL_MIRROR
        self.send_packet("PropsUIServer", "getPropsList", prop_req, ws)
    
    def _get_chat(self, ws):
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
        asyncio.create_task(self._sendMsg(stream.getBuffer(), ws))

    def _get_on_tv_panel(self, ws):
        req = HuyaOnTVUserReq()
        req.tUserId = self._get_user_id()
        req.lPid = self.info["presenterUid"]
        req.lTid = self.info["lChannelId"]
        req.lSid = self.info["lSubChannelId"]
        req.iSupportFlag = 1
        self.send_packet("revenueui", "getOnTVPanel", req, ws)

    def send_packet(self, servant: str, func: str, req, ws):
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
            asyncio.create_task(self._sendMsg(jceStream.getBuffer(), ws))
        except Exception as e:
            print("onError:", e)
            return

    async def _sendMsg(self, message, ws):
        await ws.send(message)

    def _heartbeat(self, ws):
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
        self.send_packet("onlineui", "OnUserHeartBeat", heart_beat_req, ws)

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

    async def _connect_ws(self, ssl_context: ssl.SSLContext):
        self.info = await self._get_room_info()
        # ping_interval=None：不使用 websockets 自带 ping，斗鱼用自定义心跳
        return await websockets.connect(self._ws_url, ssl=ssl_context, compression=None, open_timeout=self.timeout, max_size=None)
    
    async def _login_and_join(self, ws):
        print(f"已连接虎牙弹幕服务器，房间 {self.room_id}")
        self._get_gift(ws)
        self._get_on_tv_panel(ws)
        self._get_chat(ws)
        return
    
    async def _heartbeat_once(self, ws: websockets.WebSocketClientProtocol):
        """斗鱼心跳"""
        self._heartbeat(ws)
        return
    
    def _parse_messages(self, raw: Any) -> Any:
        buf = memoryview(raw).tobytes()
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
                return formatMsg(resData.vData, self.room_id, self._gift_info)
            except Exception as e:
                print("WupRsp decode error:", e)
        return
