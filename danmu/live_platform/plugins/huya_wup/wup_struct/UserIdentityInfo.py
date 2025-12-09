from live_platform.plugins.huya_wup.wup_struct.DecorationInfo import HuyaDecorationInfo
from live_platform.common.tars import tarscore

class HuyaUserIdentityInfo(tarscore.struct):
    __tars_class__ = "Huya.UserIdentityInfo"
    VctHuyaDecorationInfo = tarscore.vctclass(HuyaDecorationInfo)

    def __init__(self):
        self.vDecorationPrefix = HuyaUserIdentityInfo.VctHuyaDecorationInfo()
        self.vDecorationSuffix = HuyaUserIdentityInfo.VctHuyaDecorationInfo()

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaUserIdentityInfo"):
        oos.write(HuyaUserIdentityInfo.VctHuyaDecorationInfo, 0, value.vDecorationPrefix)
        oos.write(HuyaUserIdentityInfo.VctHuyaDecorationInfo, 1, value.vDecorationSuffix)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaUserIdentityInfo()
        value.vDecorationPrefix = ios.read(HuyaUserIdentityInfo.VctHuyaDecorationInfo, 0, False)
        value.vDecorationSuffix = ios.read(HuyaUserIdentityInfo.VctHuyaDecorationInfo, 1, False)
        return value

