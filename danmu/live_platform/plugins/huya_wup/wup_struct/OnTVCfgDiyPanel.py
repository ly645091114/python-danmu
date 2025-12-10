from live_platform.common.tars import tarscore

class HuyaOnTVCfgDiyPanel(tarscore.struct):
    __tars_class__ = "Huya.OnTVCfgDiyPanel"

    def __init__(self):
        self.sLogo = ""
        self.sButtonIcon = ""
        self.sAD = ""
        self.sName = ""
        self.sADJump = ""
        self.sUIJson = ""

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaOnTVCfgDiyPanel"):
        oos.write(tarscore.string, 0, value.sLogo)
        oos.write(tarscore.string, 1, value.sButtonIcon)
        oos.write(tarscore.string, 2, value.sAD)
        oos.write(tarscore.string, 3, value.sName)
        oos.write(tarscore.string, 4, value.sADJump)
        oos.write(tarscore.string, 5, value.sUIJson)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaOnTVCfgDiyPanel()
        value.sLogo = ios.read(tarscore.string, 0, False)
        value.sButtonIcon = ios.read(tarscore.string, 1, False)
        value.sAD = ios.read(tarscore.string, 2, False)
        value.sName = ios.read(tarscore.string, 3, False)
        value.sADJump = ios.read(tarscore.string, 4, False)
        value.sUIJson = ios.read(tarscore.string, 5, False)
        return value
    
    def debug(self):
        print("------- HuyaOnTVCfgDiyPanel DEBUG -------")
        print("sLogo:", self.sLogo.encode("utf-8"))
        print("sButtonIcon:", self.sButtonIcon.encode("utf-8"))
        print("sAD:", self.sAD.encode("utf-8"))
        print("sName:", self.sName.encode("utf-8"))
        print("sADJump:", self.sADJump.encode("utf-8"))
        print("sUIJson:", self.sUIJson.encode("utf-8"))
        print("--------------------------")
