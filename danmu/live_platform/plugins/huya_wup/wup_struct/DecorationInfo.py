from live_platform.common.tars import tarscore

class HuyaDecorationInfo(tarscore.struct):
    __tars_class__ = "Huya.DecorationInfo"

    def __init__(self):
        self.iAppId: tarscore.int32 = -1
        self.iViewType: tarscore.int32 = 4
        self.vData: tarscore.bytes = b''

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value):
        oos.write(tarscore.int32, 0, value.iAppId)
        oos.write(tarscore.int32, 1, value.iViewType)
        oos.write(tarscore.bytes, 2, value.vData)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaDecorationInfo()
        value.iAppId = ios.read(tarscore.int32, 0, False)
        value.iViewType = ios.read(tarscore.int32, 1, False)
        value.vData = ios.read(tarscore.bytes, 2, False)
