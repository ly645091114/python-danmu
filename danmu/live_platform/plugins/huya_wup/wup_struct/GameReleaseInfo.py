from live_platform.common.tars import tarscore

class HuyaGameReleaseInfo(tarscore.struct):
    __tars_class__ = "Huya.GameReleaseInfo"

    def __init__(self):
        self.iGameId = 0
        self.vBuffer = b""

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaGameReleaseInfo"):
        oos.write(tarscore.int32, 0, value.iGameId)
        oos.write(tarscore.bytes, 1, value.vBuffer)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaGameReleaseInfo()
        value.iGameId = ios.read(tarscore.int32, 0, False)
        value.vBuffer = ios.read(tarscore.bytes, 1, False)
        return value

    def debug(self):
        print("------- HuyaGameReleaseInfo DEBUG -------")
        print("iGameId:", int(self.iGameId))
        print("vBuffer:", self.vBuffer)
        print("--------------------------")
