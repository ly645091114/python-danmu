from live_platform.huya.plugins.huya_wup.wup_struct.OnTVItemBarrageCount import HuyaOnTVItemBarrageCount
from live_platform.huya.plugins.huya_wup.wup_struct.OnTVUserAwardInfo import HuyaOnTVUserAwardInfo
from live_platform.huya.common.tars import tarscore

class HuyaOnTVAwardInfo(tarscore.struct):
    __tars_class__ = "Huya.OnTVAwardInfo"
    VctOnTVUserAwardInfo = tarscore.vctclass(HuyaOnTVUserAwardInfo)
    VctOnTVItemBarrageCount = tarscore.vctclass(HuyaOnTVItemBarrageCount)

    def __init__(self):
        self.lOnTVId = 0
        self.vInfo = HuyaOnTVAwardInfo.VctOnTVUserAwardInfo()
        self.iBarrageNum = 0
        self.iUserNum = 0
        self.iNewFansNum = 0
        self.vItemBarrageCount = HuyaOnTVAwardInfo.VctOnTVItemBarrageCount()
        self.iNewSubNum = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaOnTVAwardInfo"):
        oos.write(tarscore.int64, 0, value.lOnTVId)
        oos.write(HuyaOnTVAwardInfo.VctOnTVUserAwardInfo, 1, value.vInfo)
        oos.write(tarscore.int32, 2, value.iBarrageNum)
        oos.write(tarscore.int32, 3, value.iUserNum)
        oos.write(tarscore.int32, 4, value.iNewFansNum)
        oos.write(HuyaOnTVAwardInfo.VctOnTVItemBarrageCount, 5, value.vItemBarrageCount)
        oos.write(tarscore.int32, 7, value.iNewSubNum)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaOnTVAwardInfo()
        value.lOnTVId = ios.read(tarscore.int64, 0, False)
        value.vInfo = ios.read(HuyaOnTVAwardInfo.VctOnTVUserAwardInfo, 1, False)
        value.iBarrageNum = ios.read(tarscore.int32, 2, False)
        value.iUserNum = ios.read(tarscore.int32, 3, False)
        value.iNewFansNum = ios.read(tarscore.int32, 4, False)
        value.vItemBarrageCount = ios.read(HuyaOnTVAwardInfo.VctOnTVItemBarrageCount, 5, False)
        value.iNewSubNum = ios.read(tarscore.int32, 7, False)
        return value

    def debug(self):
        print("------- HuyaOnTVAwardInfo DEBUG -------")
        print("lOnTVId:", int(self.lOnTVId))
        print("vInfo:")
        if isinstance(self.vInfo, list):
            for i, item in enumerate(self.vInfo):
                item.debug()
        else:
            print("  <invalid type>", self.vInfo)
        print("iBarrageNum:", int(self.iBarrageNum))
        print("iUserNum:", int(self.iUserNum))
        print("iNewFansNum:", int(self.iNewFansNum))
        print("vItemBarrageCount:")
        if isinstance(self.vItemBarrageCount, list):
            for i, item in enumerate(self.vItemBarrageCount):
                item.debug()
        else:
            print("  <invalid type>", self.vItemBarrageCount)
        print("iNewSubNum:", int(self.iNewSubNum))
        print("--------------------------")
