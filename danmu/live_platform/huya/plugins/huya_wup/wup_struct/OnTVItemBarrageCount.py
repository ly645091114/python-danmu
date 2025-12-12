from live_platform.huya.common.tars import tarscore

class HuyaOnTVItemBarrageCount(tarscore.struct):
    __tars_class__ = "Huya.OnTVItemBarrageCount"

    def __init__(self):
        self.iTVType = 0
        self.iTVColor = 0
        self.iNum = 0
        self.sContent = ""
        self.iItemId = 0
        self.iItemNum = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaOnTVItemBarrageCount"):
        oos.write(tarscore.int32, 0, value.iTVType)
        oos.write(tarscore.int32, 1, value.iTVColor)
        oos.write(tarscore.int32, 2, value.iNum)
        oos.write(tarscore.string, 3, value.sContent)
        oos.write(tarscore.int32, 4, value.iItemId)
        oos.write(tarscore.int32, 5, value.iItemNum)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaOnTVItemBarrageCount()
        value.iTVType = ios.read(tarscore.int32, 0, False)
        value.iTVColor = ios.read(tarscore.int32, 1, False)
        value.iNum = ios.read(tarscore.int32, 2, False)
        value.sContent = ios.read(tarscore.string, 3, False)
        value.iItemId = ios.read(tarscore.int32, 4, False)
        value.iItemNum = ios.read(tarscore.int32, 5, False)
        return value
    
    def debug(self):
        print("------- HuyaOnTVItemBarrageCount DEBUG -------")
        print("iTVType:", int(self.iTVType))
        print("iTVColor:", int(self.iTVColor))
        print("iNum:", int(self.iNum))
        print("sContent:", self.sContent.encode("utf-8"))
        print("iItemId:", int(self.iItemId))
        print("iItemNum:", int(self.iItemNum))
        print("--------------------------")
