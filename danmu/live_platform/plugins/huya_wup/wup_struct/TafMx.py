from live_platform.plugins.huya_wup.wup_struct.OnTVPanel import HuyaOnTVPanel
from live_platform.plugins.huya_wup.wup_struct.OnTVBarrageNotice import HuyaOnTVBarrageNotice
from live_platform.plugins.huya_wup.wup_struct.UserHeartBeatRsp import HuyaUserHeartBeatRsp
from live_platform.plugins.huya_wup.wup_struct.GetPropsListRsp import HuyaGetPropsListRsp
from live_platform.plugins.huya_wup.wup_struct.SendItemNoticeGameBroadcastPacket import HuyaSendItemNoticeGameBroadcastPacket
from live_platform.plugins.huya_wup.wup_struct.SendItemNoticeWordBroadcastPacket import HuyaSendItemNoticeWordBroadcastPacket
from live_platform.plugins.huya_wup.wup_struct.SendItemSubBroadcastPacket import HuyaSendItemSubBroadcastPacket
from live_platform.plugins.huya_wup.wup_struct.MessageNotice import HuyaMessageNotice


class TafMx:
    WupMapping = {
        'getPropsList': HuyaGetPropsListRsp,
        'OnUserHeartBeat': HuyaUserHeartBeatRsp,
        'getOnTVPanel': HuyaOnTVPanel,
    }
    # iUri -> 消息结构类
    UriMapping = {
        1400: HuyaMessageNotice,
        # 6110: HUYA.VipEnterBanner,
        # 6210: HUYA.VipBarListRsp,
        6298: HuyaOnTVBarrageNotice,
        6501: HuyaSendItemSubBroadcastPacket,
        6502: HuyaSendItemNoticeWordBroadcastPacket,
        6507: HuyaSendItemNoticeGameBroadcastPacket,
        # 8006: HUYA.AttendeeCountNotice,
    }
