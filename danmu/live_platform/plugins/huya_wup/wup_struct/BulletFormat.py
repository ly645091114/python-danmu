from live_platform.plugins.huya_wup.wup_struct.BulletBorderGroundFormat import HuyaBulletBorderGroundFormat
from live_platform.common.tars import tarscore

class HuyaBulletFormat(tarscore.struct):
    __tars_class__ = "Huya.BulletFormat"

    def __init__(self):
        self.iFontColor: tarscore.int32 = -1
        self.iFontSize: tarscore.int32 = 4
        self.iTextSpeed: tarscore.int32 = 0
        self.iTransitionType: tarscore.int32 = 1
        self.iPopupStyle: tarscore.int32 = 0
        self.tBorderGroundFormat: tarscore.struct = HuyaBulletBorderGroundFormat()

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value):
        oos.write(tarscore.int32, 0, value.iFontColor)
        oos.write(tarscore.int32, 1, value.iFontSize)
        oos.write(tarscore.int32, 2, value.iTextSpeed)
        oos.write(tarscore.int32, 3, value.iTransitionType)
        oos.write(tarscore.int32, 4, value.iPopupStyle)
        oos.write(tarscore.struct, 5, value.tBorderGroundFormat)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaBulletFormat()
        value.iFontColor = ios.read(tarscore.int32, 0, False)
        value.iFontSize = ios.read(tarscore.int32, 1, False)
        value.iTextSpeed = ios.read(tarscore.int32, 2, False)
        value.iTransitionType = ios.read(tarscore.int32, 3, False)
        value.iPopupStyle = ios.read(tarscore.int32, 4, False)
        value.tBorderGroundFormat = ios.read(tarscore.struct, 5, False)
