from enum import IntEnum

class EWebSocketCommandType(IntEnum):
    EWSCmd_NULL = 0
    EWSCmd_RegisterReq = 1
    EWSCmd_RegisterRsp = 2
    EWSCmd_WupReq = 3
    EWSCmd_WupRsp = 4
    EWSCmdC2S_HeartBeat = 5
    EWSCmdS2C_HeartBeatAck = 6
    EWSCmdS2C_MsgPushReq = 7
    EWSCmdC2S_DeregisterReq = 8
    EWSCmdS2C_DeRegisterRsp = 9
    EWSCmdC2S_VerifyCookieReq = 10
    EWSCmdS2C_VerifyCookieRsp = 11
    EWSCmdC2S_VerifyHuyaTokenReq = 12
    EWSCmdS2C_VerifyHuyaTokenRsp = 13
    EWSCmdC2S_UNVerifyReq = 14
    EWSCmdS2C_UNVerifyRsp = 15
    EWSCmdC2S_RegisterGroupReq = 16
    EWSCmdS2C_RegisterGroupRsp = 17
    EWSCmdC2S_UnRegisterGroupReq = 18
    EWSCmdS2C_UnRegisterGroupRsp = 19
    EWSCmdC2S_HeartBeatReq = 20
    EWSCmdS2C_HeartBeatRsp = 21
    EWSCmdS2C_MsgPushReq_V2 = 22
    EWSCmdC2S_UpdateUserExpsReq = 23
    EWSCmdS2C_UpdateUserExpsRsp = 24
    EWSCmdC2S_WSHistoryMsgReq = 25
    EWSCmdS2C_WSHistoryMsgRsp = 26
    EWSCmdS2C_EnterP2P = 27
    EWSCmdS2C_EnterP2PAck = 28
    EWSCmdS2C_ExitP2P = 29
    EWSCmdS2C_ExitP2PAck = 30
    EWSCmdC2S_SyncGroupReq = 31
    EWSCmdS2C_SyncGroupRsp = 32
    EWSCmdC2S_UpdateUserInfoReq = 33
    EWSCmdS2C_UpdateUserInfoRsp = 34
    EWSCmdC2S_MsgAckReq = 35
    EWSCmdS2C_MsgAckRsp = 36

class EClientTemplateType(IntEnum):
    PL_LIANYUN = 128
    TPL_PC = 64
    TPL_WEB = 32
    TPL_JIEDAI = 16
    TPL_TEXAS = 8
    TPL_MATCH = 4
    TPL_HUYAAPP = 2
    TPL_MIRROR = 1

class EStreamLineType(IntEnum):
    STREAM_LINE_OLD_YY = 0
    STREAM_LINE_WS = 1
    STREAM_LINE_NEW_YY = 2
    STREAM_LINE_AL = 3
    STREAM_LINE_HUYA = 4
    STREAM_LINE_TX = 5
    STREAM_LINE_CDN = 8
