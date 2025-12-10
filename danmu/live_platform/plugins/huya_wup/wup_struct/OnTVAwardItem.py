from live_platform.common.tars import tarscore

class HuyaOnTVAwardItem(tarscore.struct):
    __tars_class__ = "Huya.OnTVAwardItem"

    def __init__(self):
        self.sAwardName = ""
        self.iAwardNum = 0
        self.iAwardType = 0
        self.sAwardArgs = ""
        self.iNum = -1
        self.sAwardTypeName = ""
        self.iCostType = 0
        self.iCostNum = 0
        self.sOtherType = ""
        self.sOtherSubType = ""
        self.sAwardIcon = ""
        self.iAwardItemType = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaOnTVAwardItem"):
        oos.write(tarscore.string, 0, value.sAwardName)
        oos.write(tarscore.int32, 1, value.iAwardNum)
        oos.write(tarscore.int32, 2, value.iAwardType)
        oos.write(tarscore.string, 3, value.sAwardArgs)
        oos.write(tarscore.int32, 4, value.iNum)
        oos.write(tarscore.string, 5, value.sAwardTypeName)
        oos.write(tarscore.int32, 6, value.iCostType)
        oos.write(tarscore.int32, 7, value.iCostNum)
        oos.write(tarscore.string, 8, value.sOtherType)
        oos.write(tarscore.string, 9, value.sOtherSubType)
        oos.write(tarscore.string, 10, value.sAwardIcon)
        oos.write(tarscore.int32, 11, value.iAwardItemType)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaOnTVAwardItem()
        value.sAwardName = ios.read(tarscore.string, 0, False)
        value.iAwardNum = ios.read(tarscore.int32, 1, False)
        value.iAwardType = ios.read(tarscore.int32, 2, False)
        value.sAwardArgs = ios.read(tarscore.string, 3, False)
        value.iNum = ios.read(tarscore.int32, 4, False)
        value.sAwardTypeName = ios.read(tarscore.string, 5, False)
        value.iCostType = ios.read(tarscore.int32, 6, False)
        value.iCostNum = ios.read(tarscore.int32, 7, False)
        value.sOtherType = ios.read(tarscore.string, 8, False)
        value.sOtherSubType = ios.read(tarscore.string, 9, False)
        value.sAwardIcon = ios.read(tarscore.string, 10, False)
        value.iAwardItemType = ios.read(tarscore.int32, 11, False)
        return value

    def debug(self):
        print("------- HuyaOnTVAwardItem DEBUG -------")
        print("sAwardName:", self.sAwardName.encode("utf-8"))
        print("iAwardNum:", int(self.iAwardNum))
        print("iAwardType:", int(self.iAwardType))
        print("sAwardArgs:", self.sAwardArgs.encode("utf-8"))
        print("iNum:", int(self.iNum))
        print("sAwardArgs:", self.sAwardArgs.encode("utf-8"))
        print("sAwardTypeName:", int(self.sAwardTypeName))
        print("iCostType:", int(self.iCostType))
        print("iCostNum:", int(self.iCostNum))
        print("sOtherType:", self.sOtherType.encode("utf-8"))
        print("sOtherSubType:", self.sOtherSubType.encode("utf-8"))
        print("sAwardIcon:", self.sAwardIcon.encode("utf-8"))
        print("iAwardItemType:", int(self.iAwardItemType))
        print("--------------------------")
