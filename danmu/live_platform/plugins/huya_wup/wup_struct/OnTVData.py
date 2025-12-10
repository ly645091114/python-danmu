from live_platform.plugins.huya_wup.wup_struct.OnTVItemBarrageCount import HuyaOnTVItemBarrageCount
from live_platform.common.tars import tarscore

class HuyaOnTVData(tarscore.struct):
    __tars_class__ = "Huya.OnTVData"
    VctOnTVItemBarrageCount = tarscore.vctclass(HuyaOnTVItemBarrageCount)

    def __init__(self):
        self.lOnTVId = 0
        self.iBarrageNum = 0
        self.lStartTS = 0
        self.iLeftTime = 0
        self.iUserNum = 0
        self.lEndTS = 0
        self.vItemBarrageCount = HuyaOnTVData.VctOnTVItemBarrageCount()

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaOnTVData"):
        oos.write(tarscore.int64, 0, value.lOnTVId)
        oos.write(tarscore.int32, 1, value.iBarrageNum)
        oos.write(tarscore.int64, 2, value.lStartTS)
        oos.write(tarscore.int32, 3, value.iLeftTime)
        oos.write(tarscore.int32, 4, value.iUserNum)
        oos.write(tarscore.int32, 5, value.lEndTS)
        oos.write(HuyaOnTVData.VctOnTVItemBarrageCount, 6, value.vItemBarrageCount)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaOnTVData()
        value.lOnTVId = ios.read(tarscore.int64, 0, False)
        value.iBarrageNum = ios.read(tarscore.int32, 1, False)
        value.lStartTS = ios.read(tarscore.int64, 2, False)
        value.iLeftTime = ios.read(tarscore.int32, 3, False)
        value.iUserNum = ios.read(tarscore.int32, 4, False)
        value.lEndTS = ios.read(tarscore.int32, 5, False)
        value.vItemBarrageCount = ios.read(HuyaOnTVData.VctOnTVItemBarrageCount, 6, False)
        return value
    
    def debug(self):
        print("------- HuyaOnTVData DEBUG -------")
        print("lOnTVId:", int(self.lOnTVId))
        print("iBarrageNum:", int(self.iBarrageNum))
        print("lStartTS:", int(self.lStartTS))
        print("iLeftTime:", int(self.iLeftTime))
        print("iUserNum:", int(self.iUserNum))
        print("lEndTS:", int(self.lEndTS))
        print("vItemBarrageCount:")
        if isinstance(self.vItemBarrageCount, list):
            for i, item in enumerate(self.vItemBarrageCount):
                item.debug()
        else:
            print("  <invalid type>", self.vItemBarrageCount)
        print("--------------------------")
