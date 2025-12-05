from live_platform.plugins.huya_wup.wup_struct.DecorationInfo import HuyaDecorationInfo
from live_platform.common.tars import tarscore

class HuyaUserIdentityInfo(tarscore.struct):
    __tars_class__ = "Huya.UserIdentityInfo"

    def __init__(self):
        self.vDecorationPrefix: tarscore.vctclass = tarscore.vctclass(HuyaDecorationInfo)
        self.vDecorationSuffix: tarscore.vctclass = tarscore.vctclass(HuyaDecorationInfo)

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value):
        oos.write(tarscore.vctclass, 0, value.vDecorationPrefix)
        oos.write(tarscore.vctclass, 1, value.vDecorationSuffix)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaUserIdentityInfo()
        value.vDecorationPrefix = ios.read(tarscore.vctclass, 0, False)
        value.vDecorationSuffix = ios.read(tarscore.vctclass, 1, False)

