from live_platform.huya.common.tars import tarscore

class HuyaOnTVCfgDiyBarrage(tarscore.struct):
    __tars_class__ = "Huya.OnTVCfgDiyBarrage"

    def __init__(self):
        self.sIcon = ""

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaOnTVCfgDiyBarrage"):
        oos.write(tarscore.string, 1, value.sIcon)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaOnTVCfgDiyBarrage()
        value.sIcon = ios.read(tarscore.string, 1, False)
        return value
    
    def debug(self):
        print("------- HuyaOnTVCfgDiyBarrage DEBUG -------")
        print("sIcon:", self.sIcon.encode("utf-8"))
        print("--------------------------")
