from live_platform.plugins.huya_wup.wup_struct.UserId import HuyaUserId
from live_platform.plugins.huya_wup.wup_struct import EStreamLineType
from live_platform.common.tars import tarscore

class HuyaUserHeartBeatReq(tarscore.struct):
    __tars_class__ = "Huya.UserHeartBeatReq"

    def __init__(self):
        self.tId: tarscore.struct = HuyaUserId()
        self.lTid: tarscore.int64 = 0
        self.lSid: tarscore.int64 = 0
        self.lPid: tarscore.int64 = 0
        self.bWatchVideo: tarscore.boolean = False
        self.eLineType: tarscore.int32 = EStreamLineType.STREAM_LINE_OLD_YY
        self.iFps: tarscore.int32 = 0
        self.iAttendee: tarscore.int32 = 0
        self.iBandwidth: tarscore.int32 = 0
        self.iLastHeartElapseTime: tarscore.int32 = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaUserHeartBeatReq"):
        oos.write(tarscore.struct, 0, value.tId)
        oos.write(tarscore.int64, 1, value.lTid)
        oos.write(tarscore.int64, 2, value.lSid)
        oos.write(tarscore.int64, 4, value.lPid)
        oos.write(tarscore.boolean, 5, value.bWatchVideo)
        oos.write(tarscore.int32, 6, value.eLineType)
        oos.write(tarscore.int32, 7, value.iFps)
        oos.write(tarscore.int32, 8, value.iAttendee)
        oos.write(tarscore.int32, 9, value.iBandwidth)
        oos.write(tarscore.int32, 10, value.iLastHeartElapseTime)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaUserHeartBeatReq()
        value.tId = ios.read(tarscore.struct, 0, False)
        value.lTid = ios.read(tarscore.int64, 1, False)
        value.lSid = ios.read(tarscore.int64, 2, False)
        value.lPid = ios.read(tarscore.int64, 4, False)
        value.bWatchVideo = ios.read(tarscore.boolean, 5, False)
        value.eLineType = ios.read(tarscore.int32, 6, False)
        value.iFps = ios.read(tarscore.int32, 7, False)
        value.iAttendee = ios.read(tarscore.int32, 8, False)
        value.iBandwidth = ios.read(tarscore.int32, 9, False)
        value.iLastHeartElapseTime = ios.read(tarscore.int32, 10, False)

    def debug(self):
        print("------- HuyaUserHeartBeatReq DEBUG -------")
        print("tId:")
        if hasattr(self.tId, "__dict__"):
            for field, val in self.tId.__dict__.items():
                print(f"   {field}: {val}")
        else:
            print("   <non-struct value>", self.tId)
        print("lTid:", int(self.lTid))
        print("lSid:", int(self.lSid))
        print("lPid:", int(self.lPid))
        print("bWatchVideo:", bool(self.bWatchVideo))
        print("eLineType:", int(self.eLineType))
        print("iFps:", int(self.iFps))
        print("iAttendee:", int(self.iAttendee))
        print("iBandwidth:", int(self.iBandwidth))
        print("iLastHeartElapseTime:", int(self.iLastHeartElapseTime))
        print("--------------------------")
