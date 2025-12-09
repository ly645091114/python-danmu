
from live_platform.plugins.huya_wup.wup_struct.UserId import HuyaUserId
from live_platform.common.tars import tarscore

class HuyaGetPropsListReq(tarscore.struct):
    __tars_class__ = "Huya.GetPropsListReq"

    def __init__(self):
        self.tUserId: tarscore.struct = HuyaUserId()
        self.sMd5: tarscore.string = ""
        self.iTemplateType: tarscore.int32 = 64
        self.sVersion: tarscore.string = ""
        self.iAppId: tarscore.int32 = 0
        self.lPresenterUid: tarscore.int64 = 0
        self.lSid: tarscore.int64 = 0
        self.lSubSid: tarscore.int64 = 0
        self.iGameId: tarscore.int32 = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaGetPropsListReq"):
        oos.write(tarscore.struct, 1, value.tUserId)
        oos.write(tarscore.string, 2, value.sMd5)
        oos.write(tarscore.int32, 3, value.iTemplateType)
        oos.write(tarscore.string, 4, value.sVersion)
        oos.write(tarscore.int32, 5, value.iAppId)
        oos.write(tarscore.int64, 6, value.lPresenterUid)
        oos.write(tarscore.int64, 7, value.lSid)
        oos.write(tarscore.int64, 8, value.lSubSid)
        oos.write(tarscore.int32, 9, value.iGameId)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaGetPropsListReq()
        value.tUserId = ios.read(tarscore.struct, 1, False)
        value.sMd5 = ios.read(tarscore.string, 2, False)
        value.iTemplateType = ios.read(tarscore.int32, 3, False)
        value.sVersion = ios.read(tarscore.string, 4, False)
        value.iAppId = ios.read(tarscore.int32, 5, False)
        value.lPresenterUid = ios.read(tarscore.int64, 6, False)
        value.lSid = ios.read(tarscore.int64, 7, False)
        value.lSubSid = ios.read(tarscore.int64, 8, False)
        value.iGameId = ios.read(tarscore.int32, 9, False)

    def debug(self):
        print("------- HuyaGetPropsListReq DEBUG -------")
        print("tUserId:")
        if hasattr(self.tUserId, "__dict__"):
            for field, val in self.tUserId.__dict__.items():
                print(f"   {field}: {val}")
        else:
            print("   <non-struct value>", self.tUserId)
        print("sMd5:", self.sMd5)
        print("iTemplateType:", int(self.iTemplateType))
        print("sVersion:", self.sVersion)
        print("iAppId:", self.iAppId)
        print("lPresenterUid:", self.lPresenterUid)
        print("lSid:", self.lSid)
        print("lSubSid:", self.lSubSid)
        print("iGameId:", self.iGameId)
        print("--------------------------")