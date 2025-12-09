
from live_platform.plugins.huya_wup.wup_struct.PropView import HuyaPropView
from live_platform.plugins.huya_wup.wup_struct.SpecialInfo import HuyaSpecialInfo
from live_platform.plugins.huya_wup.wup_struct.DisplayInfo import HuyaDisplayInfo
from live_platform.plugins.huya_wup.wup_struct.PropsIdentity import HuyaPropsIdentity
from live_platform.common.tars import tarscore

class HuyaPropsItem(tarscore.struct):
    __tars_class__ = "Huya.PropsItem"
    VctInt32 = tarscore.vctclass(tarscore.int32)
    VctInt64 = tarscore.vctclass(tarscore.int64)
    VctString = tarscore.vctclass(tarscore.string)
    VctHuyaPropsIdentity = tarscore.vctclass(HuyaPropsIdentity)
    VctHuyaPropView = tarscore.vctclass(HuyaPropView)

    def __init__(self):
        self.iPropsId = 0
        self.sPropsName = ""
        self.iPropsYb = 0
        self.iPropsGreenBean = 0
        self.iPropsWhiteBean = 0
        self.iPropsGoldenBean = 0
        self.iPropsRed = 0
        self.iPropsPopular = 0
        self.iPropsExpendNum = -1
        self.iPropsFansValue = -1
        self.vPropsNum = HuyaPropsItem.VctInt32()
        self.iPropsMaxNum = 0
        self.iPropsBatterFlag = 0
        self.vPropsChannel = HuyaPropsItem.VctInt32()
        self.sPropsToolTip = ""
        self.vPropsIdentity = HuyaPropsItem.VctHuyaPropsIdentity()
        self.iPropsWeights = 0
        self.iPropsLevel = 0
        self.tDisplayInfo = HuyaDisplayInfo()
        self.tSpecialInfo = HuyaSpecialInfo()
        self.iPropsGrade = 0
        self.iPropsGroupNum = 0
        self.sPropsCommBannerResource = ""
        self.sPropsOwnBannerResource = ""
        self.iPropsShowFlag = 0
        self.iTemplateType = 0
        self.iShelfStatus = 0
        self.sAndroidLogo = ""
        self.sIpadLogo = ""
        self.sIphoneLogo = ""
        self.sPropsCommBannerResourceEx = ""
        self.sPropsOwnBannerResourceEx = ""
        self.vPresenterUid = HuyaPropsItem.VctInt64()
        self.vPropView = HuyaPropsItem.VctHuyaPropView()
        self.iFaceUSwitch = 0
        self.iDisplayCd = 0
        self.iCount = 0
        self.iVbCount = 0
        self.vWebPropsNum = HuyaPropsItem.VctString()

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaPropsItem"):
        oos.write(tarscore.int32, 1, value.iPropsId)
        oos.write(tarscore.string, 2, value.sPropsName)
        oos.write(tarscore.int32, 3, value.iPropsYb)
        oos.write(tarscore.int32, 4, value.iPropsGreenBean)
        oos.write(tarscore.int32, 5, value.iPropsWhiteBean)
        oos.write(tarscore.int32, 6, value.iPropsGoldenBean)
        oos.write(tarscore.int32, 7, value.iPropsRed)
        oos.write(tarscore.int32, 8, value.iPropsPopular)
        oos.write(tarscore.int32, 9, value.iPropsExpendNum)
        oos.write(tarscore.int32, 10, value.iPropsFansValue)
        oos.write(HuyaPropsItem.VctInt32, 11, value.vPropsNum)
        oos.write(tarscore.int32, 12, value.iPropsMaxNum)
        oos.write(tarscore.int32, 13, value.iPropsBatterFlag)
        oos.write(HuyaPropsItem.VctInt32, 14, value.vPropsChannel)
        oos.write(tarscore.string, 15, value.sPropsToolTip)
        oos.write(HuyaPropsItem.VctHuyaPropsIdentity, 16, value.vPropsIdentity)
        oos.write(tarscore.int32, 17, value.iPropsWeights)
        oos.write(tarscore.int32, 18, value.iPropsLevel)
        oos.write(tarscore.struct, 19, value.tDisplayInfo)
        oos.write(tarscore.struct, 20, value.tSpecialInfo)
        oos.write(tarscore.int32, 21, value.iPropsGrade)
        oos.write(tarscore.int32, 22, value.iPropsGroupNum)
        oos.write(tarscore.string, 23, value.sPropsCommBannerResource)
        oos.write(tarscore.string, 24, value.sPropsOwnBannerResource)
        oos.write(tarscore.int32, 25, value.iPropsShowFlag)
        oos.write(tarscore.int32, 26, value.iTemplateType)
        oos.write(tarscore.int32, 27, value.iShelfStatus)
        oos.write(tarscore.string, 28, value.sAndroidLogo)
        oos.write(tarscore.string, 29, value.sIpadLogo)
        oos.write(tarscore.string, 30, value.sIphoneLogo)
        oos.write(tarscore.string, 31, value.sPropsCommBannerResourceEx)
        oos.write(tarscore.string, 32, value.sPropsOwnBannerResourceEx)
        oos.write(HuyaPropsItem.VctInt64, 33, value.vPresenterUid)
        oos.write(HuyaPropsItem.VctHuyaPropView, 34, value.vPropView)
        oos.write(tarscore.int16, 35, value.iFaceUSwitch)
        oos.write(tarscore.int16, 36, value.iDisplayCd)
        oos.write(tarscore.int16, 37, value.iCount)
        oos.write(tarscore.int32, 38, value.iVbCount)
        oos.write(HuyaPropsItem.VctString, 39, value.vWebPropsNum)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaPropsItem()
        value.iPropsId = ios.read(tarscore.int32, 1, False)
        value.sPropsName = ios.read(tarscore.string, 2, False)
        value.iPropsYb = ios.read(tarscore.int32, 3, False)
        value.iPropsGreenBean = ios.read(tarscore.int32, 4, False)
        value.iPropsWhiteBean = ios.read(tarscore.int32, 5, False)
        value.iPropsGoldenBean = ios.read(tarscore.int32, 6, False)
        value.iPropsRed = ios.read(tarscore.int32, 7, False)
        value.iPropsPopular = ios.read(tarscore.int32, 8, False)
        value.iPropsExpendNum = ios.read(tarscore.int32, 9, False)
        value.iPropsFansValue = ios.read(tarscore.int32, 10, False)
        value.vPropsNum = ios.read(HuyaPropsItem.VctInt32, 11, False)
        value.iPropsMaxNum = ios.read(tarscore.int32, 12, False)
        value.iPropsBatterFlag = ios.read(tarscore.int32, 13, False)
        value.vPropsChannel = ios.read(HuyaPropsItem.VctInt32, 14, False)
        value.sPropsToolTip = ios.read(tarscore.string, 15, False)
        value.vPropsIdentity = ios.read(HuyaPropsItem.VctHuyaPropsIdentity, 16, False)
        value.iPropsWeights = ios.read(tarscore.int32, 17, False)
        value.iPropsLevel = ios.read(tarscore.int32, 18, False)
        value.tDisplayInfo = ios.read(HuyaDisplayInfo, 19, False)
        value.tSpecialInfo = ios.read(HuyaSpecialInfo, 20, False)
        value.iPropsGrade = ios.read(tarscore.int32, 21, False)
        value.iPropsGroupNum = ios.read(tarscore.int32, 22, False)
        value.sPropsCommBannerResource = ios.read(tarscore.string, 23, False)
        value.sPropsOwnBannerResource = ios.read(tarscore.string, 24, False)
        value.iPropsShowFlag = ios.read(tarscore.int32, 25, False)
        value.iTemplateType = ios.read(tarscore.int32, 26, False)
        value.iShelfStatus = ios.read(tarscore.int32, 27, False)
        value.sAndroidLogo = ios.read(tarscore.string, 28, False)
        value.sIpadLogo = ios.read(tarscore.string, 29, False)
        value.sIphoneLogo = ios.read(tarscore.string, 30, False)
        value.sPropsCommBannerResourceEx = ios.read(tarscore.string, 31, False)
        value.sPropsOwnBannerResourceEx = ios.read(tarscore.string, 32, False)
        value.vPresenterUid = ios.read(HuyaPropsItem.VctInt64, 33, False)
        value.vPropView = ios.read(HuyaPropsItem.VctHuyaPropView, 34, False)
        value.iFaceUSwitch = ios.read(tarscore.int16, 35, False)
        value.iDisplayCd = ios.read(tarscore.int16, 36, False)
        value.iCount = ios.read(tarscore.int16, 37, False)
        value.iVbCount = ios.read(tarscore.int32, 38, False)
        value.vWebPropsNum = ios.read(HuyaPropsItem.VctString, 39, False)
        return value
