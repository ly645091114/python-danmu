from live_platform.huya.common.tars import tarscore

class HuyaDisplayInfo(tarscore.struct):
    __tars_class__ = "Huya.DisplayInfo"

    def __init__(self):
        self.iMarqueeScopeMin = 0
        self.iMarqueeScopeMax = 0
        self.iCurrentVideoNum = 0
        self.iCurrentVideoMin = 0
        self.iCurrentVideoMax = 0
        self.iAllVideoNum = 0
        self.iAllVideoMin = 0
        self.iAllVideoMax = 0
        self.iCurrentScreenNum = 0
        self.iCurrentScreenMin = 0
        self.iCurrentScreenMax = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaDisplayInfo"):
        oos.write(tarscore.int32, 1, value.iMarqueeScopeMin)
        oos.write(tarscore.int32, 2, value.iMarqueeScopeMax)
        oos.write(tarscore.int32, 3, value.iCurrentVideoNum)
        oos.write(tarscore.int32, 4, value.iCurrentVideoMin)
        oos.write(tarscore.int32, 5, value.iCurrentVideoMax)
        oos.write(tarscore.int32, 6, value.iAllVideoNum)
        oos.write(tarscore.int32, 7, value.iAllVideoMin)
        oos.write(tarscore.int32, 8, value.iAllVideoMax)
        oos.write(tarscore.int32, 9, value.iCurrentScreenNum)
        oos.write(tarscore.int32, 10, value.iCurrentScreenNum)
        oos.write(tarscore.int32, 11, value.iCurrentScreenMax)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaDisplayInfo()
        value.iMarqueeScopeMin = ios.read(tarscore.int32, 1, False)
        value.iMarqueeScopeMax = ios.read(tarscore.int32, 2, False)
        value.iCurrentVideoNum = ios.read(tarscore.int32, 3, False)
        value.iCurrentVideoMin = ios.read(tarscore.int32, 4, False)
        value.iCurrentVideoMax = ios.read(tarscore.int32, 5, False)
        value.iAllVideoNum = ios.read(tarscore.int32, 6, False)
        value.iAllVideoMin = ios.read(tarscore.int32, 7, False)
        value.iAllVideoMax = ios.read(tarscore.int32, 8, False)
        value.iCurrentScreenNum = ios.read(tarscore.int32, 9, False)
        value.iCurrentScreenNum = ios.read(tarscore.int32, 10, False)
        value.iCurrentScreenMax = ios.read(tarscore.int32, 11, False)
        return value

