from live_platform.huya.plugins.huya_wup.wup_struct.OnTVCfgDiyPanel import HuyaOnTVCfgDiyPanel
from live_platform.huya.plugins.huya_wup.wup_struct.OnTVCfgDiyFlag import HuyaOnTVCfgDiyFlag
from live_platform.huya.plugins.huya_wup.wup_struct.OnTVCfgDiyBarrage import HuyaOnTVCfgDiyBarrage
from live_platform.huya.common.tars import tarscore

class HuyaOnTVCfgDiy(tarscore.struct):
    __tars_class__ = "Huya.OnTVCfgDiy"

    def __init__(self):
        self.tBarrage = HuyaOnTVCfgDiyBarrage()
        self.tFlag = HuyaOnTVCfgDiyFlag()
        self.tPanel = HuyaOnTVCfgDiyPanel()

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaOnTVCfgDiy"):
        oos.write(HuyaOnTVCfgDiyBarrage, 0, value.tBarrage)
        oos.write(HuyaOnTVCfgDiyFlag, 1, value.tFlag)
        oos.write(HuyaOnTVCfgDiyPanel, 2, value.tPanel)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaOnTVCfgDiy()
        value.tBarrage = ios.read(HuyaOnTVCfgDiyBarrage, 0, False)
        value.tFlag = ios.read(HuyaOnTVCfgDiyFlag, 1, False)
        value.tPanel = ios.read(HuyaOnTVCfgDiyPanel, 2, False)
        return value

    def debug(self):
        print("------- HuyaOnTVCfgDiy DEBUG -------")
        print("tBarrage:")
        self.tBarrage.debug()
        print("tFlag:")
        self.tFlag.debug()
        print("tPanel:")
        self.tPanel.debug()
        print("--------------------------")
