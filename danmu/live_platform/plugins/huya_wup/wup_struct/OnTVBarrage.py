from live_platform.common.tars import tarscore

class HuyaOnTVBarrage(tarscore.struct):
    __tars_class__ = "Huya.OnTVBarrage"

    def __init__(self):
        self.lUid = 0
        self.sContent = ""
        self.iTVType = 0
        self.iTVColor = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaOnTVBarrage"):
        oos.write(tarscore.int64, 0, value.lUid)
        oos.write(tarscore.string, 1, value.sContent)
        oos.write(tarscore.int32, 2, value.iTVType)
        oos.write(tarscore.int32, 3, value.iTVColor)


    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaOnTVBarrage()
        value.lUid = ios.read(tarscore.int64, 0, False)
        value.sContent = ios.read(tarscore.string, 1, False)
        value.iTVType = ios.read(tarscore.int32, 2, False)
        value.iTVColor = ios.read(tarscore.int32, 3, False)
        return value
    
    def debug(self):
        print("------- HuyaOnTVBarrage DEBUG -------")
        print("iState:", int(self.lUid))
        print("sContent:", self.sContent.encode("utf-8"))
        print("iTVType:", int(self.iTVType))
        print("iTVColor:", int(self.iTVColor))
        print("--------------------------")
