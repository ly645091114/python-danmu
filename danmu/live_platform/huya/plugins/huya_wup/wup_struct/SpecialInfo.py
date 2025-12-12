from live_platform.huya.common.tars import tarscore

class HuyaSpecialInfo(tarscore.struct):
    __tars_class__ = "Huya.SpecialInfo"

    def __init__(self):
        self.iFirstSingle = 0
        self.iFirstGroup = 0
        self.sFirstTips = ""
        self.iSecondSingle = 0
        self.iSecondGroup = 0
        self.sSecondTips = ""
        self.iThirdSingle = 0
        self.iThirdGroup = 0
        self.sThirdTips = ""
        self.iWorldSingle = 0
        self.iWorldGroup = 0
        self.iAmbilightNum = 0
        self.iAmbilightUpgradeNum = 0
        self.iWorldBannerNum = 0
        self.iShowType = 0
        self.iOpenFaceu = 0
        self.iOpenGesture = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaSpecialInfo"):
        oos.write(tarscore.int32, 1, value.iFirstSingle)
        oos.write(tarscore.int32, 2, value.iFirstGroup)
        oos.write(tarscore.string, 3, value.sFirstTips)
        oos.write(tarscore.int32, 4, value.iSecondSingle)
        oos.write(tarscore.int32, 5, value.iSecondGroup)
        oos.write(tarscore.string, 6, value.sSecondTips)
        oos.write(tarscore.int32, 7, value.iThirdSingle)
        oos.write(tarscore.int32, 8, value.iThirdGroup)
        oos.write(tarscore.string, 9, value.sThirdTips)
        oos.write(tarscore.int32, 10, value.iWorldSingle)
        oos.write(tarscore.int32, 11, value.iWorldGroup)
        oos.write(tarscore.int32, 12, value.iAmbilightNum)
        oos.write(tarscore.int32, 13, value.iAmbilightUpgradeNum)
        oos.write(tarscore.int32, 14, value.iWorldBannerNum)
        oos.write(tarscore.int16, 15, value.iShowType)
        oos.write(tarscore.int16, 16, value.iOpenFaceu)
        oos.write(tarscore.int16, 17, value.iOpenGesture)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaSpecialInfo()
        value.iFirstSingle = ios.read(tarscore.int32, 1, False)
        value.iFirstGroup = ios.read(tarscore.int32, 2, False)
        value.sFirstTips = ios.read(tarscore.string, 3, False)
        value.iSecondSingle = ios.read(tarscore.int32, 4, False)
        value.iSecondGroup = ios.read(tarscore.int32, 5, False)
        value.sSecondTips = ios.read(tarscore.string, 6, False)
        value.iThirdSingle = ios.read(tarscore.int32, 7, False)
        value.iThirdGroup = ios.read(tarscore.int32, 8, False)
        value.sThirdTips = ios.read(tarscore.string, 9, False)
        value.iWorldSingle = ios.read(tarscore.int32, 10, False)
        value.iWorldGroup = ios.read(tarscore.int32, 11, False)
        value.iAmbilightNum = ios.read(tarscore.int32, 12, False)
        value.iAmbilightUpgradeNum = ios.read(tarscore.int32, 13, False)
        value.iWorldBannerNum = ios.read(tarscore.int32, 14, False)
        value.iShowType = ios.read(tarscore.int16, 15, False)
        value.iOpenFaceu = ios.read(tarscore.int16, 16, False)
        value.iOpenGesture = ios.read(tarscore.int16, 17, False)
        return value
