from live_platform.plugins.huya_wup.wup_struct.UserId import HuyaUserId
from live_platform.common.tars import tarscore

class HuyaOnTVUserReq(tarscore.struct):
    __tars_class__ = "Huya.OnTVUserReq"

    def __init__(self):
        self.tUserId = HuyaUserId()
        self.lPid = 0
        self.lTid = 0
        self.lSid = 0
        self.iSupportFlag = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaOnTVUserReq"):
        oos.write(HuyaUserId, 0, value.tUserId)
        oos.write(tarscore.int64, 1, value.lPid)
        oos.write(tarscore.int64, 2, value.lTid)
        oos.write(tarscore.int64, 3, value.lSid)
        oos.write(tarscore.int32, 4, value.iSupportFlag)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaOnTVUserReq()
        value.tUserId = ios.read(HuyaUserId, 0, False)
        value.lPid = ios.read(tarscore.int64, 1, False)
        value.lTid = ios.read(tarscore.int64, 2, False)
        value.lSid = ios.read(tarscore.int64, 3, False)
        value.iSupportFlag = ios.read(tarscore.int32, 4, False)

    def debug(self):
        print("------- HuyaOnTVUserReq DEBUG -------")
        print(f"tUserId")
        self.tUserId()
        print(f"lPid: {int(self.lPid)}")
        print(f"lTid: {int(self.lTid)}")
        print(f"lSid: {int(self.lSid)}")
        print(f"iSupportFlag: {int(self.iSupportFlag)}")
        print("--------------------------------------------")
