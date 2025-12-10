from live_platform.plugins.huya_wup.wup_struct.GameReleaseInfo import HuyaGameReleaseInfo
from live_platform.plugins.huya_wup.wup_struct.OnTVItemPackage import HuyaOnTVItemPackage
from live_platform.plugins.huya_wup.wup_struct.TVPrice import HuyaTVPrice
from live_platform.plugins.huya_wup.wup_struct.OnTVAwardItem import HuyaOnTVAwardItem
from live_platform.common.tars import tarscore

class HuyaOnTVSettingInfo(tarscore.struct):
    __tars_class__ = "Huya.OnTVSettingInfo"
    VctTVPrice = tarscore.vctclass(HuyaTVPrice)
    VctOnTVItemPackage = tarscore.vctclass(HuyaOnTVItemPackage)
    MapStringInt64 = tarscore.mapclass(tarscore.string, tarscore.int64)

    def __init__(self):
        self.sTitle = "",
        self.tAward = HuyaOnTVAwardItem()
        self.vTVPrice = HuyaOnTVSettingInfo.VctTVPrice()
        self.lPid = 0
        self.sLogo = ""
        self.iAwardMode = 0
        self.vPack = HuyaOnTVSettingInfo.VctOnTVItemPackage()
        self.iPartic = 0
        self.iPartic2 = 0
        self.mSuggestBarrage = HuyaOnTVSettingInfo.MapStringInt64()
        self.tGameRelease = HuyaGameReleaseInfo()

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaOnTVSettingInfo"):
        oos.write(tarscore.string, 0, value.sTitle)
        oos.write(HuyaOnTVAwardItem, 1, value.tAward)
        oos.write(HuyaOnTVSettingInfo.VctTVPrice, 2, value.vTVPrice)
        oos.write(tarscore.int64, 3, value.lPid)
        oos.write(tarscore.string, 4, value.sLogo)
        oos.write(tarscore.int32, 5, value.iAwardMode)
        oos.write(HuyaOnTVSettingInfo.VctOnTVItemPackage, 6, value.vPack)
        oos.write(tarscore.int32, 7, value.iPartic)
        oos.write(tarscore.int32, 8, value.iPartic2)
        oos.write(HuyaOnTVSettingInfo.MapStringInt64, 9, value.mSuggestBarrage)
        oos.write(HuyaGameReleaseInfo, 10, value.tGameRelease)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaOnTVSettingInfo()
        value.sTitle = ios.read(tarscore.string, 0, False)
        value.tAward = ios.read(HuyaOnTVAwardItem, 1, False)
        value.vTVPrice = ios.read(HuyaOnTVSettingInfo.VctTVPrice, 2, False)
        value.lPid = ios.read(tarscore.int64, 3, False)
        value.sLogo = ios.read(tarscore.string, 4, False)
        value.iAwardMode = ios.read(tarscore.int32, 5, False)
        value.vPack = ios.read(HuyaOnTVSettingInfo.VctOnTVItemPackage, 6, False)
        value.iPartic = ios.read(tarscore.int32, 7, False)
        value.iPartic2 = ios.read(tarscore.int32, 8, False)
        value.mSuggestBarrage = ios.read(HuyaOnTVSettingInfo.MapStringInt64, 9, False)
        value.tGameRelease = ios.read(HuyaGameReleaseInfo, 10, False)
        return value
    
    def debug(self):
        print("------- HuyaOnTVSettingInfo DEBUG -------")
        print("sTitle:", self.sTitle.encode("utf-8"))
        print("tAward:")
        self.tAward.debug()
        print("vTVPrice:")
        if isinstance(self.vTVPrice, list):
            for i, item in enumerate(self.vTVPrice):
                item.debug()
        else:
            print("  <invalid type>", self.vTVPrice)
        print("lPid:", int(self.lPid))
        print("sLogo:", self.sLogo.encode("utf-8"))
        print("iAwardMode:", int(self.iAwardMode))
        print("vPack:")
        if isinstance(self.vPack, list):
            for i, item in enumerate(self.vPack):
                item.debug()
        else:
            print("  <invalid type>", self.vPack)
        print("iPartic:", int(self.iPartic))
        print("iPartic2:", int(self.iPartic2))
        print("mSuggestBarrage:")
        if isinstance(self.mSuggestBarrage, dict):
            for k, v in self.mSuggestBarrage.items():
                print(f"mSuggestBarrage[{k}]:{int(v)}")
            return
        else:
            print("  <invalid type>", self.mSuggestBarrage)
        print("tGameRelease:")
        self.tGameRelease.debug()
        print("--------------------------")
