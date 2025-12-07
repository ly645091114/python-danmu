from live_platform.common.tars import tarscore

class HuyaWSPushMessage(tarscore.struct):
    __tars_class__ = "Huya.WSPushMessage"

    def __init__(self):
        self.ePushType: tarscore.int32 = 0
        self.iUri: tarscore.int64 = 0
        self.sMsg: tarscore.bytes = b""
        self.iProtocolType: tarscore.int32 = 0
        self.sGroupId: tarscore.string = ""

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value):
        oos.write(tarscore.int32, 0, value.ePushType)
        oos.write(tarscore.int64, 1, value.iUri)
        oos.write(tarscore.bytes, 2, value.sMsg)
        oos.write(tarscore.int32, 3, value.iProtocolType)
        oos.write(tarscore.string, 4, value.sGroupId)


    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaWSPushMessage()
        value.ePushType = ios.read(tarscore.int32, 0, False)
        value.iUri = ios.read(tarscore.int64, 1, False)
        value.sMsg = ios.read(tarscore.bytes, 2, False)
        value.iProtocolType = ios.read(tarscore.int32, 3, False)
        value.sGroupId = ios.read(tarscore.string, 4, False)

