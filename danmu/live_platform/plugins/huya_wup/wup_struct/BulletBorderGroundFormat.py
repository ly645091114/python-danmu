from live_platform.common.tars import tarscore

class HuyaBulletBorderGroundFormat(tarscore.struct):
    __tars_class__ = "Huya.BulletBorderGroundFormat"

    def __init__(self):
        self.iEnableUse: tarscore.int32 = 0
        self.iBorderThickness: tarscore.int32 = 0
        self.iBorderColour: tarscore.int32 = -1
        self.iBorderDiaphaneity: tarscore.int32 = 100
        self.iGroundColour: tarscore.int32 = -1
        self.iGroundColourDiaphaneity: tarscore.int32 = 100
        self.sAvatarDecorationUrl: tarscore.string = ""
        self.iFontColor: tarscore.int32 = -1

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value):
        oos.write(tarscore.int32, 0, value.iEnableUse)
        oos.write(tarscore.int32, 1, value.iBorderThickness)
        oos.write(tarscore.int32, 2, value.iBorderColour)
        oos.write(tarscore.int32, 3, value.iBorderDiaphaneity)
        oos.write(tarscore.int32, 4, value.iGroundColour)
        oos.write(tarscore.int32, 5, value.iGroundColourDiaphaneity)
        oos.write(tarscore.string, 6, value.sAvatarDecorationUrl)
        oos.write(tarscore.int32, 7, value.iFontColor)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaBulletBorderGroundFormat()
        value.iEnableUse = ios.read(tarscore.int32, 0, False)
        value.iBorderThickness = ios.read(tarscore.int32, 1, False)
        value.iBorderColour = ios.read(tarscore.int32, 2, False)
        value.iBorderDiaphaneity = ios.read(tarscore.int32, 3, False)
        value.iGroundColour = ios.read(tarscore.int32, 4, False)
        value.iGroundColourDiaphaneity = ios.read(tarscore.int32, 5, False)
        value.sAvatarDecorationUrl = ios.read(tarscore.string, 6, False)
        value.iFontColor = ios.read(tarscore.int32, 7, False)
