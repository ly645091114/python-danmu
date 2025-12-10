from live_platform.common.tars import tarscore

class HuyaNobleLevelInfo(tarscore.struct):
    __tars_class__ = "Huya.NobleLevelInfo"

    def __init__(self):
        self.iNobleLevel = 0
        self.iAttrType = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaNobleLevelInfo"):
        oos.write(tarscore.int32, 0, value.iNobleLevel)
        oos.write(tarscore.int32, 1, value.iAttrType)


    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaNobleLevelInfo()
        value.iNobleLevel = ios.read(tarscore.int32, 0, False)
        value.iAttrType = ios.read(tarscore.int32, 1, False)
        return value
