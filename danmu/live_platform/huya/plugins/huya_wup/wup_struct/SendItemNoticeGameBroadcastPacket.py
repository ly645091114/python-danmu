from live_platform.huya.common.tars import tarscore

class HuyaSendItemNoticeGameBroadcastPacket(tarscore.struct):
    __tars_class__ = "Huya.SendItemNoticeGameBroadcastPacket"

    def __init__(self):
        self.iItemType: tarscore.int32 = 0
        self.iItemCount: tarscore.int32 = 0
        self.lSenderUid: tarscore.int64 = 0
        self.sSenderNick: tarscore.string = ""
        self.lPresenterUid: tarscore.int64 = 0
        self.sPresenterNick: tarscore.string = ""
        self.lSid: tarscore.int64 = 0
        self.lSubSid: tarscore.int64 = 0
        self.lRoomId: tarscore.int64 = 0
        self.iTemplateType: tarscore.int32 = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaSendItemNoticeGameBroadcastPacket"):
        oos.write(tarscore.int32, 0, value.iItemType)
        oos.write(tarscore.int32, 1, value.iItemCount)
        oos.write(tarscore.int64, 3, value.lSenderUid)
        oos.write(tarscore.string, 4, value.sSenderNick)
        oos.write(tarscore.int64, 5, value.lPresenterUid)
        oos.write(tarscore.string, 6, value.sPresenterNick)
        oos.write(tarscore.int64, 7, value.lSid)
        oos.write(tarscore.int64, 8, value.lSubSid)
        oos.write(tarscore.int64, 9, value.lRoomId)
        oos.write(tarscore.int32, 10, value.iTemplateType)


    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaSendItemNoticeGameBroadcastPacket()
        value.iItemType = ios.read(tarscore.int32, 0, False)
        value.iItemCount = ios.read(tarscore.int32, 1, False)
        value.lSenderUid = ios.read(tarscore.int64, 3, False)
        value.sSenderNick = ios.read(tarscore.string, 4, False)
        value.lPresenterUid = ios.read(tarscore.int64, 5, False)
        value.sPresenterNick = ios.read(tarscore.string, 6, False)
        value.lSid = ios.read(tarscore.int64, 7, False)
        value.lSubSid = ios.read(tarscore.int64, 8, False)
        value.lRoomId = ios.read(tarscore.int64, 9, False)
        value.iTemplateType = ios.read(tarscore.int32, 10, False)
        return value
