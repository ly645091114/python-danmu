from live_platform.huya.common.tars import tarscore

class HuyaOnTVItemPackage(tarscore.struct):
    __tars_class__ = "Huya.OnTVItemPackage"

    def __init__(self):
        self.iItemId = 0
        self.iItemNum = 0
        self.iTVType = 0
        self.iTVColor = 0
        self.sContent = ""

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaOnTVItemPackage"):
        oos.write(tarscore.int32, 0, value.iItemId)
        oos.write(tarscore.int32, 1, value.iItemNum)
        oos.write(tarscore.int32, 2, value.iTVType)
        oos.write(tarscore.int32, 3, value.iTVColor)
        oos.write(tarscore.string, 4, value.sContent)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaOnTVItemPackage()
        value.iItemId = ios.read(tarscore.int32, 0, False)
        value.iItemNum = ios.read(tarscore.int32, 1, False)
        value.iTVType = ios.read(tarscore.int32, 2, False)
        value.iTVColor = ios.read(tarscore.int32, 3, False)
        value.sContent = ios.read(tarscore.string, 4, False)
        return value
    
    def debug(self):
        print("------- HuyaOnTVItemPackage DEBUG -------")
        print("iItemId:", int(self.iItemId))
        print("iItemNum:", int(self.iItemNum))
        print("iTVType:", int(self.iTVType))
        print("iTVColor:", int(self.iTVColor))
        print("sContent:", self.sContent.encode("utf-8"))
        print("--------------------------")
