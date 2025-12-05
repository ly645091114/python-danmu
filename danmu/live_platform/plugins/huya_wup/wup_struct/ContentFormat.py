from live_platform.common.tars import tarscore

class HuyaContentFormat(tarscore.struct):
    __tars_class__ = "Huya.ContentFormat"

    def __init__(self):
        self.iFontColor: tarscore.int64 = -1
        self.iFontSize: tarscore.int64 = 4
        self.iPopupStyle: tarscore.string = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value):
        oos.write(tarscore.int32, 0, value.iFontColor)
        oos.write(tarscore.int32, 1, value.iFontSize)
        oos.write(tarscore.int32, 2, value.iPopupStyle)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaContentFormat()
        value.iFontColor = ios.read(tarscore.int32, 0, False)
        value.iFontSize = ios.read(tarscore.int32, 1, False)
        value.iPopupStyle = ios.read(tarscore.int32, 2, False)
