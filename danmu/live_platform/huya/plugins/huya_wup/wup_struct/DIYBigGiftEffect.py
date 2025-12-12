from live_platform.huya.common.tars import tarscore

class HuyaDIYBigGiftEffect(tarscore.struct):
    __tars_class__ = "Huya.DIYBigGiftEffect"

    def __init__(self):
        self.sResourceUrl = ""
        self.sResourceAttr = ""
        self.sWebResourceUrl = ""
        self.sPCResourceUrl = ""

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaDIYBigGiftEffect"):
        oos.write(tarscore.string, 0, value.sResourceUrl)
        oos.write(tarscore.string, 1, value.sResourceAttr)
        oos.write(tarscore.string, 2, value.sWebResourceUrl)
        oos.write(tarscore.string, 3, value.sPCResourceUrl)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaDIYBigGiftEffect()
        value.sResourceUrl = ios.read(tarscore.string, 0, False)
        value.sResourceAttr = ios.read(tarscore.string, 1, False)
        value.sWebResourceUrl = ios.read(tarscore.string, 2, False)
        value.sPCResourceUrl = ios.read(tarscore.string, 3, False)
        return value

