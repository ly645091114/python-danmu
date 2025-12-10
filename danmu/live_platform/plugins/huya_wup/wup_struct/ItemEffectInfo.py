from live_platform.common.tars import tarscore

class HuyaItemEffectInfo(tarscore.struct):
    __tars_class__ = "Huya.ItemEffectInfo"

    def __init__(self):
        self.iPriceLevel = 0
        self.iStreamDuration = 0
        self.iShowType = 0
        self.iStreamId = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaItemEffectInfo"):
        oos.write(tarscore.int32, 0, value.iPriceLevel)
        oos.write(tarscore.int32, 1, value.iStreamDuration)
        oos.write(tarscore.int32, 2, value.iShowType)
        oos.write(tarscore.int32, 3, value.iStreamId)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaItemEffectInfo()
        value.iPriceLevel = ios.read(tarscore.int32, 0, False)
        value.iStreamDuration = ios.read(tarscore.int32, 1, False)
        value.iShowType = ios.read(tarscore.int32, 2, False)
        value.iStreamId = ios.read(tarscore.int32, 3, False)
        return value

