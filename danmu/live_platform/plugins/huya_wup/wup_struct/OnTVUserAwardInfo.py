from live_platform.plugins.huya_wup.wup_struct.OnTVBarrage import HuyaOnTVBarrage
from live_platform.common.tars import tarscore

class HuyaOnTVUserAwardInfo(tarscore.struct):
    __tars_class__ = "Huya.OnTVUserAwardInfo"
    VctHuyaOnTVBarrage = tarscore.vctclass(HuyaOnTVBarrage)

    def __init__(self):
        self.lUid = 0
        self.lYYid = 0
        self.sNickName = ""
        self.sLogo = ""
        self.sAwardName = ""
        self.tBarrage = HuyaOnTVUserAwardInfo.VctHuyaOnTVBarrage()

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaOnTVUserAwardInfo"):
        oos.write(tarscore.int64, 0, value.lUid)
        oos.write(tarscore.int64, 1, value.lYYid)
        oos.write(tarscore.string, 2, value.sNickName)
        oos.write(tarscore.string, 3, value.sLogo)
        oos.write(tarscore.string, 4, value.sAwardName)
        oos.write(HuyaOnTVUserAwardInfo.VctHuyaOnTVBarrage, 5, value.tBarrage)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaOnTVUserAwardInfo()
        value.lUid = ios.read(tarscore.int64, 0, False)
        value.lYYid = ios.read(tarscore.int64, 1, False)
        value.sNickName = ios.read(tarscore.string, 2, False)
        value.sLogo = ios.read(tarscore.string, 3, False)
        value.sAwardName = ios.read(tarscore.string, 4, False)
        value.tBarrage = ios.read(HuyaOnTVUserAwardInfo.VctHuyaOnTVBarrage, 5, False)
        return value

    def debug(self):
        print("------- HuyaOnTVUserAwardInfo DEBUG -------")
        print("lUid:", int(self.lUid))
        print("lYYid:", int(self.lYYid))
        print("sNickName:", self.sNickName.encode("utf-8"))
        print("sLogo:", self.sLogo.encode("utf-8"))
        print("sAwardName:", self.sAwardName.encode("utf-8"))
        print("tBarrage:")
        if isinstance(self.tBarrage, list):
            for i, item in enumerate(self.tBarrage):
                item.debug()
        else:
            print("  <invalid type>", self.tBarrage)
        print("--------------------------")
