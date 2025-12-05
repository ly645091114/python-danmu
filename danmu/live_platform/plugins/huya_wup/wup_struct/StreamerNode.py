from live_platform.plugins.huya_wup.wup_struct.DecorationInfo import HuyaDecorationInfo
from live_platform.common.tars import tarscore

class HuyaStreamerNode(tarscore.struct):
    __tars_class__ = "Huya.StreamerNode"

    def __init__(self):
        self.iGiftLevel: tarscore.int16 = 0
        self.iStreamerLevel: tarscore.int16  = 0
        self.iMaterialType: tarscore.int16  = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value):
        oos.write(tarscore.int16, 0, value.iGiftLevel)
        oos.write(tarscore.int16, 1, value.iStreamerLevel)
        oos.write(tarscore.int16, 2, value.iMaterialType)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaStreamerNode()
        value.iGiftLevel = ios.read(tarscore.int16, 0, False)
        value.iStreamerLevel = ios.read(tarscore.int16, 1, False)
        value.iMaterialType = ios.read(tarscore.int16, 2, False)
