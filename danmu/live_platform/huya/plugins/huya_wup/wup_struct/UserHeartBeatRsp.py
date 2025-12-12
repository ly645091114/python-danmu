from live_platform.huya.plugins.huya_wup.wup_struct.UserId import HuyaUserId
from live_platform.huya.plugins.huya_wup.wup_struct import EStreamLineType
from live_platform.huya.common.tars import tarscore

class HuyaUserHeartBeatRsp(tarscore.struct):
    __tars_class__ = "Huya.UserHeartBeatRsp"

    def __init__(self):
        self.iRet = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaUserHeartBeatRsp"):
        oos.write(tarscore.int32, 0, value.iRet)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaUserHeartBeatRsp()
        value.iRet = ios.read(tarscore.int32, 0, False)
        return value
