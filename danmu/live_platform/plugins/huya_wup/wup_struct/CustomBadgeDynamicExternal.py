from live_platform.common.tars import tarscore

class HuyaCustomBadgeDynamicExternal(tarscore.struct):
    __tars_class__ = "Huya.CustomBadgeDynamicExternal"

    def __init__(self):
        self.sFloorExter = ""
        self.iFansIdentity = 0
        self.iBadgeSize = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaCustomBadgeDynamicExternal"):
        oos.write(tarscore.string, 0, value.sFloorExter)
        oos.write(tarscore.int32, 1, value.iFansIdentity)
        oos.write(tarscore.int32, 2, value.iBadgeSize)


    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaCustomBadgeDynamicExternal()
        value.sFloorExter = ios.read(tarscore.string, 0, False)
        value.iFansIdentity = ios.read(tarscore.int32, 1, False)
        value.iBadgeSize = ios.read(tarscore.int32, 2, False)
        return value
