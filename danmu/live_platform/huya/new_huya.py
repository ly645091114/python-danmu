import asyncio
import re
import ssl
from typing import Dict, Any

import aiohttp
import certifi

from live_platform.plugins.huya_wup.wup_struct.UserHeartBeatReq import HuyaUserHeartBeatReq
from live_platform.plugins.huya_wup.wup_struct.GetPropsListReq import HuyaGetPropsListReq
from live_platform.plugins.huya_wup.wup_struct.WSRegisterGroupReq import HuyaWSRegisterGroupReq
from live_platform.plugins.huya_wup import Wup, DEFAULT_TICKET_NUMBER
from live_platform.common.tars import tarscore
from live_platform.plugins.huya_wup.wup_struct.UserId import HuyaUserId
from live_platform.plugins.huya_wup.wup_struct import EClientTemplateType, EStreamLineType, EWebSocketCommandType
from live_platform.plugins.huya_wup.wup_struct.WebSocketCommand import HuyaWebSocketCommand
from live_platform.plugins.huya_wup.wup_struct.WSUserInfo import HuyaWSUserInfo

class HuyaDanmuClient:
    def __init__(self, room_id: str, cookies: str = "", ua: str = "", timeout: int = 5):
        self.room_id = room_id
        self.cookies = cookies
        self.ua = ua or (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 "
            "Mobile/15E148 Safari/604.1"
        )
        self.timeout = timeout

        self.http: aiohttp.ClientSession | None = None
        self.ws: aiohttp.ClientWebSocketResponse | None = None

        self.room_info: Dict[str, Any] = {}
        self.user_id = None
        self.gift_map: Dict[int, Dict[str, Any]] = {}

        self._running = False

    async def _get_room_info(self):
        url = f"https://m.huya.com/{self.room_id}"
        headers = {"user-agent": self.ua}
        async with self.http.get(url, headers=headers, timeout=self.timeout) as resp:
            if resp.status != 200:
                raise RuntimeError(f"获取房间信息失败 status={resp.status}")
            text = await resp.text()

        def pick(pattern: str) -> int:
            m = re.search(pattern, text)
            if not m or m.group(1) == "":
                return 0
            return int(m.group(1))

        info = {
            "presenterUid": pick(r'"lUid":(.*?),"iIsProfile"'),
            "yyuid":        pick(r'"lYyid":(.*?),"sNick"'),
            "lChannelId":   pick(r'"lChannelId":(.*?),"lSubChannelId"'),
            "lSubChannelId":pick(r'"lSubChannelId":(.*?),"lPresenterUid"'),
            "sGuid":        "",
        }

        if not info["presenterUid"] or not info["yyuid"]:
            raise RuntimeError(f"房间 {self.room_id} 不存在或已停播")

        self.room_info = info

    def _build_user_id(self):
        user = HuyaUserId()
        user.sHuYaUA = self.ua
        user.lUid = self.room_info["presenterUid"]
        user.sCookie = self.cookies
        user.sGuid = self.room_info["sGuid"]
        user.sToken = ""
        self.user_id = user

    def _build_register_packet(self) -> bytes:
        ws_user_info = HuyaWSUserInfo()
        ws_user_info.lUid = self.room_info["presenterUid"]
        ws_user_info.bAnonymous = False
        ws_user_info.lGroupId = ws_user_info.lUid
        ws_user_info.lGroupType = 3

        oos = tarscore.TarsOutputStream()
        ws_user_info.writeTo(oos, ws_user_info)

        ws_cmd = HuyaWebSocketCommand()
        ws_cmd.iCmdType = EWebSocketCommandType.EWSCmd_RegisterReq
        ws_cmd.vData = oos.getBuffer()

        oos2 = tarscore.TarsOutputStream()
        ws_cmd.writeTo(oos2, ws_cmd)
        return oos2.getBuffer()

    def _encode_wup(self, servant: str, func: str, req_struct) -> bytes:
        wup = Wup()
        wup.servant(servant)
        wup.func(func)
        wup_bytes = wup.encode()

        web_cmd = HuyaWebSocketCommand()
        web_cmd.iCmdType = EWebSocketCommandType.EWSCmd_WupReq
        web_cmd.vData = wup_bytes

        oos = tarscore.TarsOutputStream()
        web_cmd.writeTo(oos, web_cmd)
        return oos.getBuffer()

    async def _ws_send_bytes(self, data: bytes):
        if self.ws is None:
            return
        await self.ws.send_bytes(data)

    async def _register_group(self):
        req = HuyaWSRegisterGroupReq()
        req.vGroupId.append(f"live:{self.room_info['presenterUid']}")
        req.vGroupId.append(f"chat:{self.room_info['presenterUid']}")

        oos = tarscore.TarsOutputStream()
        req.writeTo(oos, req)

        cmd = HuyaWebSocketCommand()
        cmd.iCmdType = EWebSocketCommandType.EWSCmdC2S_RegisterGroupReq
        cmd.vData = oos.getBuffer()

        oos2 = tarscore.TarsOutputStream()
        cmd.writeTo(oos2, cmd)

        await self._ws_send_bytes(oos2.getBuffer())

    async def _get_gift(self):
        prop_req = HuyaGetPropsListReq()
        prop_req.tUserId = self.user_id
        prop_req.iTemplateType = EClientTemplateType.TPL_MIRROR

        data = self._encode_wup("PropsUIServer", "getPropsList", prop_req)
        await self._ws_send_bytes(data)

    async def _send_heartbeat(self):
        hb = HuyaUserHeartBeatReq()
        hb.tId = self.user_id
        hb.lTid = self.room_info["lChannelId"]
        hb.lSid = self.room_info["lSubChannelId"]
        hb.lPid = self.room_info["yyuid"]
        hb.eLineType = EStreamLineType.STREAM_LINE_AL
        hb.bWatchVideo = True
        hb.iFps = 0
        hb.iAttendee = 0
        hb.iLastHeartElapseTime = 0

        data = self._encode_wup("onlineui", "OnUserHeartBeat", hb)
        await self._ws_send_bytes(data)

    async def _heartbeat_loop(self):
        while self._running:
            try:
                await self._send_heartbeat()
            except Exception as e:
                print("heartbeat error:", e)
            await asyncio.sleep(60)

    async def _recv_loop(self):
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.BINARY:
                await self._handle_binary(msg.data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break

    async def _handle_binary(self, data: bytes):
        # 伪代码：按你自己的 tars 解码方式来写
        ios = tarscore.TarsInputStream(data)
        cmd = HuyaWebSocketCommand()
        cmd.readFrom(ios, cmd)

        if cmd.iCmdType == EWebSocketCommandType.EWSCmd_WupRsp:
            await self._handle_wup_response(cmd.vData)
        elif cmd.iCmdType == EWebSocketCommandType.EWSCmdS2C_MsgPushReq:
            await self._handle_msg_push(cmd.vData)
        else:
            # 其他类型暂时忽略
            pass

    async def _handle_wup_response(self, message: bytes):
        try:
            from_stream = tarscore.TarsInputStream(message)

            web_cmd = HuyaWebSocketCommand()
            web_cmd.readFrom(from_stream)

            cmd_type = web_cmd.iCmdType

            # # 1) WUP 回调
            # if cmd_type == EWebSocketCommandType.EWSCmd_WupRsp:
            #     try:
            #         wup = Wup()
            #         wup.decode(web_cmd.vData)
            #         func_name = wup.__code.sFuncName      # 或者 wup.getFuncName()
            #         mapping_cls = TafMx.WupMapping[func_name]
            #         rsp_obj = mapping_cls()

            #         # JS: wup.readStruct("tRsp", map, TafMx.WupMapping[wup.sFuncName]);
            #         wup.readStruct("tRsp", rsp_obj, mapping_cls)

            #         # JS: this.emit(wup.sFuncName, map);
            #         self.emit(func_name, rsp_obj)

            #     except Exception as e:
            #         print("Wup decode error:", e)

            # 2) 系统推送（MsgPush）
            if cmd_type == EWebSocketCommandType.EWSCmdS2C_MsgPushReq:
                from_stream = tarscore.TarsInputStream(web_cmd.vData)
                push_msg = HUYA.WSPushMessage()
                push_msg.readFrom(from_stream)

                mcs = push_msg.iUri

                inner_stream = tarscore.TarsInputStream(push_msg.sMsg)

                # JS: var uriMapping = TafMx.UriMapping[pushMessage.iUri];
                uri_cls = TafMx.UriMapping.get(mcs)
                if uri_cls:
                    msg = uri_cls()
                    msg.readFrom(inner_stream)

                    # 弹幕：mcs == 1400
                    if mcs == 1400:
                        # JS:
                        # this.emit("onChat", {
                        #   room_id: this.config.roomid,
                        #   timestamp: new Date().getTime() + "",
                        #   uid: msg.tUserInfo.lUid + "",
                        #   nickName: msg.tUserInfo.sNickName,
                        #   txt: msg.sContent,
                        # });
                        self.emit("onChat", {
                            "room_id": self.config.roomid,
                            "timestamp": str(int(time.time() * 1000)),
                            "uid": str(msg.tUserInfo.lUid),
                            "nickName": msg.tUserInfo.sNickName,
                            "txt": msg.sContent,
                        })

                    # 礼物：mcs in [6501, 6502, 6507]
                    if mcs in (6501, 6502, 6507):
                        # JS: let gift = this._gift_info[msg.iItemType + ""] || { price: 0 };
                        gift = self._gift_info.get(str(msg.iItemType), {"price": 0, "name": "", "icon": ""})

                        self.emit("onGift", {
                            "room_id": self.config.roomid,
                            "timestamp": str(int(time.time() * 1000)),
                            "uid": str(msg.lSenderUid),
                            "nickName": msg.sSenderNick,
                            "type": mcs,
                            "gfid": msg.iItemType,
                            "gfcnt": msg.iItemCount,
                            "gift_name": gift.get("name", ""),
                            "gift_icon": gift.get("icon", ""),
                            "price_big": gift.get("price", 0),
                            "price_total": msg.iItemCount * gift.get("price", 0),
                        })

            # 其他类型：忽略
            else:
                pass

        except Exception as e:
            # JS: this.emit("onError", { type: 1, error: e });
            self.emit("onError", {
                "type": 1,
                "error": e,
            })

    async def _handle_msg_push(self, payload: bytes):
        """
        MsgPush 里会包含各种广播：弹幕、礼物、入场等。
        你在 HUYA 协议文件里找对应的结构（一般名字里有 Item/Gift/SubBroadcast）。
        """
        # 这里的具体解法要看你的 HUYA 定义，给你个方向：
        # 1. 解成 HUYA.WSMsgItem / HUYA.LiveMsg / HUYA.SendItemSubBroadcastPacket
        # 2. 判断是弹幕还是礼物
        # 3. 如果是礼物，就用 self.gift_map[prop_id] 补全名字、价格，输出事件

    # ------------ 对外启动 ------------

    async def start(self):
        """
        总控：HTTP -> 构造 user -> 建 WS -> 注册 -> 拉礼物 -> 心跳 + 收消息
        """
        self._running = True

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        ssl_context.options |= ssl.OP_NO_SSLv2
        ssl_context.options |= ssl.OP_NO_SSLv3
        ssl_context.options |= ssl.OP_NO_TLSv1
        ssl_context.options |= ssl.OP_NO_TLSv1_1
        ssl_context.set_ciphers("DEFAULT")

        async with aiohttp.ClientSession() as self.http:
            # 1. 获取房间信息
            await self._get_room_info()
            # 2. 构造 UserId
            self._build_user_id()

            # 3. 建立 WebSocket 连接
            async with self.http.ws_connect(
                HUYA.wss_url,  # 你原来 get_ws_info 里的 wss url
                ssl=ssl_context,
            ) as self.ws:
                # 4. 发送 RegisterReq
                reg_packet = self._build_register_packet()
                await self._ws_send_bytes(reg_packet)

                # 5. 注册 group（弹幕+礼物）
                await self._register_group()

                # 6. 请求礼物列表
                await self._get_gift()

                # 7. 并发跑心跳 + 收包
                hb_task = asyncio.create_task(self._heartbeat_loop())
                recv_task = asyncio.create_task(self._recv_loop())

                await asyncio.gather(hb_task, recv_task)

        self._running = False