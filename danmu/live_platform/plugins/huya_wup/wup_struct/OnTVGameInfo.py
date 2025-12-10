from live_platform.plugins.huya_wup.wup_struct.OnTVData import HuyaOnTVData
from live_platform.plugins.huya_wup.wup_struct.OnTVSettingInfo import HuyaOnTVSettingInfo
from live_platform.common.tars import tarscore

class HuyaOnTVGameInfo(tarscore.struct):
    __tars_class__ = "Huya.OnTVGameInfo"

    def __init__(self):
        self.lOnTVId = 0
        self.tSettingInfo = HuyaOnTVSettingInfo()
        self.tData = HuyaOnTVData()

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaOnTVGameInfo"):
        oos.write(tarscore.int64, 0, value.lOnTVId)
        oos.write(HuyaOnTVSettingInfo, 1, value.tSettingInfo)
        oos.write(HuyaOnTVData, 2, value.tData)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaOnTVGameInfo()
        value.lOnTVId = ios.read(tarscore.int64, 0, False)
        value.tSettingInfo = ios.read(HuyaOnTVSettingInfo, 1, False)
        value.tData = ios.read(HuyaOnTVData, 2, False)
        return value

    def debug(self):
        print("------- HuyaOnTVGameInfo DEBUG -------")
        print("lOnTVId:", int(self.lOnTVId))
        print("tSettingInfo:")
        self.tSettingInfo.debug()
        print("tData:")
        self.tData.debug()
        print("--------------------------")
