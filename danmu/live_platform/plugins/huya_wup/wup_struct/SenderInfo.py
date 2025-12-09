from live_platform.common.tars import tarscore

class HuyaSenderInfo(tarscore.struct):
    __tars_class__ = "Huya.SenderInfo"

    def __init__(self):
        self.lUid: tarscore.int64 = 0
        self.lImid: tarscore.int64 = 0
        self.sNickName: tarscore.string = ""
        self.iGender: tarscore.int32 = 0
        self.sAvatarUrl: tarscore.string = ""
        self.iNobleLevel: tarscore.int32 = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaSenderInfo"):
        oos.write(tarscore.int64, 0, value.lUid)
        oos.write(tarscore.int64, 1, value.lImid)
        oos.write(tarscore.string, 2, value.sNickName)
        oos.write(tarscore.int32, 3, value.iGender)
        oos.write(tarscore.string, 4, value.sAvatarUrl)
        oos.write(tarscore.int32, 5, value.iNobleLevel)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaSenderInfo()
        value.lUid = ios.read(tarscore.int64, 0, False)
        value.lImid = ios.read(tarscore.int64, 1, False)
        value.sNickName = ios.read(tarscore.string, 2, False)
        value.iGender = ios.read(tarscore.int32, 3, False)
        value.sAvatarUrl = ios.read(tarscore.string, 4, False)
        value.iNobleLevel = ios.read(tarscore.int32, 5, False)
        return value
