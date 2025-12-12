from live_platform.huya.common.tars import tarscore

class HuyaItemEffectBizData(tarscore.struct):
    __tars_class__ = "Huya.ItemEffectBizData"

    def __init__(self):
        self.iType = 0
        self.vData = b""

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaItemEffectBizData"):
        oos.write(tarscore.int32, 0, value.iType)
        oos.write(tarscore.bytes, 1, value.vData)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaItemEffectBizData()
        value.iType = ios.read(tarscore.int32, 0, False)
        value.vData = ios.read(tarscore.bytes, 1, False)
        return value

