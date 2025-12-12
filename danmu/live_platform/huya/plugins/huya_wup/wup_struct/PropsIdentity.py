from live_platform.huya.common.tars import tarscore

class HuyaPropsIdentity(tarscore.struct):
    __tars_class__ = "Huya.PropsIdentity"

    def __init__(self):
        self.iPropsIdType = 0
        self.sPropsPic18 = ""
        self.sPropsPic24 = ""
        self.sPropsPicGif = ""
        self.sPropsBannerResource = ""
        self.sPropsBannerSize = ""
        self.sPropsBannerMaxTime = ""
        self.sPropsChatBannerResource = ""
        self.sPropsChatBannerSize = ""
        self.sPropsChatBannerMaxTime = ""
        self.iPropsChatBannerPos = 0
        self.iPropsChatBannerIsCombo = 0
        self.sPropsRollContent = ""
        self.iPropsBannerAnimationstyle = 0
        self.sPropFaceu = ""
        self.sPropH5Resource = ""
        self.sPropsWeb = ""
        self.sWitch = 0
        self.sCornerMark = ""
        self.iPropViewId = 0
        self.sPropStreamerResource = ""
        self.iStreamerFrameRate = 0
        self.sPropsPic108 = ""
        self.sPcBannerResource = ""
        self.sPropBigGiftPc = ""
        self.sPropBigGiftWeb = ""
        self.iWebBigGiftFrameRate = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaPropsIdentity"):
        oos.write(tarscore.int32, 1, value.iPropsIdType)
        oos.write(tarscore.string, 2, value.sPropsPic18)
        oos.write(tarscore.string, 3, value.sPropsPic24)
        oos.write(tarscore.string, 4, value.sPropsPicGif)
        oos.write(tarscore.string, 5, value.sPropsBannerResource)
        oos.write(tarscore.string, 6, value.sPropsBannerSize)
        oos.write(tarscore.string, 7, value.sPropsBannerMaxTime)
        oos.write(tarscore.string, 8, value.sPropsChatBannerResource)
        oos.write(tarscore.string, 9, value.sPropsChatBannerSize)
        oos.write(tarscore.string, 10, value.sPropsChatBannerMaxTime)
        oos.write(tarscore.int32, 11, value.iPropsChatBannerPos)
        oos.write(tarscore.int32, 12, value.iPropsChatBannerIsCombo)
        oos.write(tarscore.string, 13, value.sPropsRollContent)
        oos.write(tarscore.int32, 14, value.iPropsBannerAnimationstyle)
        oos.write(tarscore.string, 15, value.sPropFaceu)
        oos.write(tarscore.string, 16, value.sPropH5Resource)
        oos.write(tarscore.string, 17, value.sPropsWeb)
        oos.write(tarscore.int32, 18, value.sWitch)
        oos.write(tarscore.string, 19, value.sCornerMark)
        oos.write(tarscore.int32, 20, value.iPropViewId)
        oos.write(tarscore.string, 21, value.sPropStreamerResource)
        oos.write(tarscore.int16, 22, value.iStreamerFrameRate)
        oos.write(tarscore.string, 23, value.sPropsPic108)
        oos.write(tarscore.string, 24, value.sPcBannerResource)
        oos.write(tarscore.string, 25, value.sPropBigGiftPc)
        oos.write(tarscore.string, 26, value.sPropBigGiftWeb)
        oos.write(tarscore.int32, 27, value.iWebBigGiftFrameRate)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaPropsIdentity()
        value.iPropsIdType = ios.read(tarscore.int32, 1, False)
        value.sPropsPic18 = ios.read(tarscore.string, 2, False)
        value.sPropsPic24 = ios.read(tarscore.string, 3, False)
        value.sPropsPicGif = ios.read(tarscore.string, 4, False)
        value.sPropsBannerResource = ios.read(tarscore.string, 5, False)
        value.sPropsBannerSize = ios.read(tarscore.string, 6, False)
        value.sPropsBannerMaxTime = ios.read(tarscore.string, 7, False)
        value.sPropsChatBannerResource = ios.read(tarscore.string, 8, False)
        value.sPropsChatBannerSize = ios.read(tarscore.string, 9, False)
        value.sPropsChatBannerMaxTime = ios.read(tarscore.string, 10, False)
        value.iPropsChatBannerPos = ios.read(tarscore.int32, 11, False)
        value.iPropsChatBannerIsCombo = ios.read(tarscore.int32, 12, False)
        value.sPropsRollContent = ios.read(tarscore.string, 13, False)
        value.iPropsBannerAnimationstyle = ios.read(tarscore.int32, 14, False)
        value.sPropFaceu = ios.read(tarscore.string, 15, False)
        value.sPropH5Resource = ios.read(tarscore.string, 16, False)
        value.sPropsWeb = ios.read(tarscore.string, 17, False)
        value.sWitch = ios.read(tarscore.int32, 18, False)
        value.sCornerMark = ios.read(tarscore.string, 19, False)
        value.iPropViewId = ios.read(tarscore.int32, 20, False)
        value.sPropStreamerResource = ios.read(tarscore.string, 21, False)
        value.iStreamerFrameRate = ios.read(tarscore.int16, 22, False)
        value.sPropsPic108 = ios.read(tarscore.string, 23, False)
        value.sPcBannerResource = ios.read(tarscore.string, 24, False)
        value.sPropBigGiftPc = ios.read(tarscore.string, 25, False)
        value.sPropBigGiftWeb = ios.read(tarscore.string, 26, False)
        value.iWebBigGiftFrameRate = ios.read(tarscore.int32, 27, False)
        return value
