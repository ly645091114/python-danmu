from live_platform.huya.plugins.huya_wup.wup_struct.CustomBadgeDynamicExternal import HuyaCustomBadgeDynamicExternal
from live_platform.huya.plugins.huya_wup.wup_struct.NobleLevelInfo import HuyaNobleLevelInfo
from live_platform.huya.plugins.huya_wup.wup_struct.OnTVBarrage import HuyaOnTVBarrage
from live_platform.huya.common.tars import tarscore

class HuyaOnTVBarrageNotice(tarscore.struct):
    __tars_class__ = "Huya.OnTVBarrageNotice"

    def __init__(self):
        self.lUid = 0
        self.tBarrage = HuyaOnTVBarrage()
        self.sNickName = ""
        self.iNobleLevel = 0
        self.lBadgeId = 0
        self.sBadgeName = ""
        self.iBadgeLevel = 0
        self.lNobleValidDate = 0
        self.iAwardMode = 0
        self.lPid = 0
        self.sDiyIcon = ""
        self.iBadgeType = 0
        self.sAvatarUrl = ""
        self.tNobleLv = HuyaNobleLevelInfo()
        self.iSFFlag = 0
        self.iCustomBadgeFlag = 0
        self.tCustomBadgeEx = HuyaCustomBadgeDynamicExternal()
        self.iExtinguished = 0
        self.iSFVariety = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaOnTVBarrageNotice"):
        oos.write(tarscore.int64, 0, value.lUid)
        oos.write(HuyaOnTVBarrage, 1, value.tBarrage)
        oos.write(tarscore.string, 2, value.sNickName)
        oos.write(tarscore.int32, 3, value.iNobleLevel)
        oos.write(tarscore.int64, 4, value.lBadgeId)
        oos.write(tarscore.string, 5, value.sBadgeName)
        oos.write(tarscore.int32, 6, value.iBadgeLevel)
        oos.write(tarscore.int32, 7, value.lNobleValidDate)
        oos.write(tarscore.int32, 8, value.iAwardMode)
        oos.write(tarscore.int64, 9, value.lPid)
        oos.write(tarscore.string, 10, value.sDiyIcon)
        oos.write(tarscore.int32, 11, value.iBadgeType)
        oos.write(tarscore.string, 12, value.sAvatarUrl)
        oos.write(HuyaNobleLevelInfo, 13, value.tNobleLv)
        oos.write(tarscore.int32, 14, value.iSFFlag)
        oos.write(tarscore.int32, 15, value.iCustomBadgeFlag)
        oos.write(HuyaCustomBadgeDynamicExternal, 16, value.tCustomBadgeEx)
        oos.write(tarscore.int32, 17, value.iExtinguished)
        oos.write(tarscore.int32, 18, value.iSFVariety)


    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaOnTVBarrageNotice()
        value.lUid = ios.read(tarscore.int64, 0, False)
        value.tBarrage = ios.read(HuyaOnTVBarrage, 1, False)
        value.sNickName = ios.read(tarscore.string, 2, False)
        value.iNobleLevel = ios.read(tarscore.int32, 3, False)
        value.lBadgeId = ios.read(tarscore.int64, 4, False)
        value.sBadgeName = ios.read(tarscore.string, 5, False)
        value.iBadgeLevel = ios.read(tarscore.int32, 6, False)
        value.lNobleValidDate = ios.read(tarscore.int32, 7, False)
        value.iAwardMode = ios.read(tarscore.int64, 8, False)
        value.lPid = ios.read(tarscore.int64, 9, False)
        value.sDiyIcon = ios.read(tarscore.string, 10, False)
        value.iBadgeType = ios.read(tarscore.int32, 11, False)
        value.sAvatarUrl = ios.read(tarscore.string, 12, False)
        value.tNobleLv = ios.read(HuyaNobleLevelInfo, 13, False)
        value.iSFFlag = ios.read(tarscore.int32, 14, False)
        value.iCustomBadgeFlag = ios.read(tarscore.int32, 15, False)
        value.tCustomBadgeEx = ios.read(HuyaCustomBadgeDynamicExternal, 16, False)
        value.iExtinguished = ios.read(tarscore.int32, 17, False)
        value.iSFVariety = ios.read(tarscore.int32, 18, False)
        return value
