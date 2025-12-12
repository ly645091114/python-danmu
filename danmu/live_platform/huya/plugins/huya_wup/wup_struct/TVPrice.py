from live_platform.huya.common.tars import tarscore

class HuyaTVPrice(tarscore.struct):
    __tars_class__ = "Huya.TVPrice"

    def __init__(self):
        self.iTVType = 0
        self.iPrice = 0
        self.iFreeFansLevel = 0
        self.iFreeSFansLevel = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaTVPrice"):
        oos.write(tarscore.int32, 0, value.iTVType)
        oos.write(tarscore.int32, 1, value.iPrice)
        oos.write(tarscore.int32, 2, value.iFreeFansLevel)
        oos.write(tarscore.int32, 3, value.iFreeSFansLevel)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaTVPrice()
        value.iTVType = ios.read(tarscore.int32, 0, False)
        value.iPrice = ios.read(tarscore.int32, 1, False)
        value.iFreeFansLevel = ios.read(tarscore.int32, 2, False)
        value.iFreeSFansLevel = ios.read(tarscore.int32, 3, False)
        return value
    
    def debug(self):
        print("------- HuyaTVPrice DEBUG -------")
        print("iTVType:", int(self.iTVType))
        print("iPrice:", int(self.iPrice))
        print("iFreeFansLevel:", int(self.iFreeFansLevel))
        print("iFreeSFansLevel:", int(self.iFreeSFansLevel))
        print("--------------------------")

