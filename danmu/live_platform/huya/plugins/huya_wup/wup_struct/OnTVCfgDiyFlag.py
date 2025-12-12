from live_platform.huya.common.tars import tarscore

class HuyaOnTVCfgDiyFlag(tarscore.struct):
    __tars_class__ = "Huya.OnTVCfgDiyFlag"

    def __init__(self):
        self.sName = "上电视"
        self.sPic = "http://livewebbs2.msstatic.com/ontv_<ua>.png"

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaOnTVCfgDiyFlag"):
        oos.write(tarscore.string, 0, value.sName)
        oos.write(tarscore.string, 1, value.sPic)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaOnTVCfgDiyFlag()
        value.sName = ios.read(tarscore.string, 0, False)
        value.sPic = ios.read(tarscore.string, 1, False)
        return value

    def debug(self):
        print("------- HuyaOnTVCfgDiyFlag DEBUG -------")
        print("sName:", self.sName.encode("utf-8"))
        print("sPic:", self.sPic.encode("utf-8"))
        print("--------------------------")
