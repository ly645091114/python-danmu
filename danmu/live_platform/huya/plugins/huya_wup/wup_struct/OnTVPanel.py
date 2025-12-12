from live_platform.huya.plugins.huya_wup.wup_struct.OnTVCfgDiy import HuyaOnTVCfgDiy
from live_platform.huya.plugins.huya_wup.wup_struct.OnTVGameInfo import HuyaOnTVGameInfo
from live_platform.huya.plugins.huya_wup.wup_struct.OnTVAwardInfo import HuyaOnTVAwardInfo
from live_platform.huya.common.tars import tarscore

class HuyaOnTVPanel(tarscore.struct):
    __tars_class__ = "Huya.OnTVPanel"

    def __init__(self):
        self.iState = 0
        self.tAward = HuyaOnTVAwardInfo()
        self.tInfo = HuyaOnTVGameInfo()
        self.iIsDiy = 0
        self.tDiy = HuyaOnTVCfgDiy()
        self.iOpenTips = 0
        self.sTipsDesc = ""
        self.sAppJumpUrl = ""

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaOnTVPanel"):
        oos.write(tarscore.int32, 0, value.iState)
        oos.write(HuyaOnTVAwardInfo, 1, value.tAward)
        oos.write(HuyaOnTVGameInfo, 2, value.tInfo)
        oos.write(tarscore.int32, 3, value.iIsDiy)
        oos.write(HuyaOnTVCfgDiy, 4, value.tDiy)
        oos.write(tarscore.int32, 5, value.iOpenTips)
        oos.write(tarscore.string, 6, value.sTipsDesc)
        oos.write(tarscore.string, 7, value.sAppJumpUrl)


    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaOnTVPanel()
        value.iState = ios.read(tarscore.int32, 0, False)
        value.tAward = ios.read(HuyaOnTVAwardInfo, 1, False)
        value.tInfo = ios.read(HuyaOnTVGameInfo, 2, False)
        value.iIsDiy = ios.read(tarscore.int32, 3, False)
        value.tDiy = ios.read(HuyaOnTVCfgDiy, 4, False)
        value.iOpenTips = ios.read(tarscore.int32, 5, False)
        value.sTipsDesc = ios.read(tarscore.string, 6, False)
        value.sAppJumpUrl = ios.read(tarscore.string, 7, False)
        return value
    
    def debug(self):
        print("------- HuyaOnTVPanel DEBUG -------")
        print("iState:", int(self.iState))
        print("tAward:")
        self.tAward.debug()
        print("tInfo:")
        self.tInfo.debug()
        print("iIsDiy:", int(self.iIsDiy))
        print("HuyaOnTVCfgDiy:")
        self.tDiy.debug()
        print("iOpenTips:", int(self.iOpenTips))
        print("sTipsDesc:", self.sTipsDesc.encode("utf-8"))
        print("sAppJumpUrl:", self.sAppJumpUrl.encode("utf-8"))
        print("--------------------------")
