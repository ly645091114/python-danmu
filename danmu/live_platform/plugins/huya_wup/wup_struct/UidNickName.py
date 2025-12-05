from live_platform.common.tars import tarscore

class HuyaUidNickName(tarscore.struct):
    __tars_class__ = "Huya.UidNickName"

    def __init__(self):
        self.lUid: tarscore.int64 = 0
        self.sNickName: tarscore.string = ""

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value):
        oos.write(tarscore.int64, 0, value.lUid)
        oos.write(tarscore.string, 1, value.sNickName)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaUidNickName()
        value.lUid = ios.read(tarscore.int64, 0, False)
        value.sNickName = ios.read(tarscore.string, 1, False)
