from live_platform.common.tars import tarscore

class HuyaSendItemNoticeWordBroadcastPacket:
    __tars_class__ = "Huya.SendItemNoticeWordBroadcastPacket"

    def __init__(self):
        self.iItemType: tarscore.int32 = 0
        self.iItemCount: tarscore.int32 = 0
        self.lSenderSid: tarscore.int64 = 0
        self.lSenderUid: tarscore.int64 = 0
        self.sSenderNick: tarscore.string = ""
        self.lPresenterUid: tarscore.int64 = 0
        self.sPresenterNick: tarscore.string = ""
        self.lNoticeChannelCount: tarscore.int64 = 0
        self.iItemCountByGroup: tarscore.int32 = 0
        self.iItemGroup: tarscore.int32 = 0
        self.iDisplayInfo: tarscore.int32 = 0
        self.iSuperPupleLevel: tarscore.int32 = 0
        self.iTemplateType: tarscore.int32 = 0
        self.sExpand: tarscore.string = ""
        self.bBusi: tarscore.boolean = False
        self.iShowTime: tarscore.int32 = 0
        self.lPresenterYY: tarscore.int64 = 0
        self.lSid: tarscore.int64 = 0
        self.lSubSid: tarscore.int64 = 0
        self.lRoomId: tarscore.int64 = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaSendItemNoticeWordBroadcastPacket"):
        oos.write(tarscore.int32, 0, value.iItemType)
        oos.write(tarscore.int32, 1, value.iItemCount)
        oos.write(tarscore.int64, 2, value.lSenderSid)
        oos.write(tarscore.int64, 3, value.lSenderUid)
        oos.write(tarscore.string, 4, value.sSenderNick)
        oos.write(tarscore.int64, 5, value.lPresenterUid)
        oos.write(tarscore.string, 6, value.sPresenterNick)
        oos.write(tarscore.int64, 7, value.lNoticeChannelCount)
        oos.write(tarscore.int32, 8, value.iItemCountByGroup)
        oos.write(tarscore.int32, 9, value.iItemGroup)
        oos.write(tarscore.int32, 10, value.iDisplayInfo)
        oos.write(tarscore.int32, 11, value.iSuperPupleLevel)
        oos.write(tarscore.int32, 12, value.iTemplateType)
        oos.write(tarscore.string, 13, value.sExpand)
        oos.write(tarscore.boolean, 14, value.bBusi)
        oos.write(tarscore.int32, 15, value.iShowTime)
        oos.write(tarscore.int64, 16, value.lPresenterYY)
        oos.write(tarscore.int64, 17, value.lSid)
        oos.write(tarscore.int64, 18, value.lSubSid)
        oos.write(tarscore.int64, 19, value.lRoomId)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaSendItemNoticeWordBroadcastPacket()
        value.iItemType = ios.read(tarscore.int32, 0, False)
        value.iItemCount = ios.read(tarscore.int32, 1, False)
        value.lSenderSid = ios.read(tarscore.int64, 2, False)
        value.lSenderUid = ios.read(tarscore.int64, 3, False)
        value.sSenderNick = ios.read(tarscore.string, 4, False)
        value.lPresenterUid = ios.read(tarscore.int64, 5, False)
        value.sPresenterNick = ios.read(tarscore.string, 6, False)
        value.lNoticeChannelCount = ios.read(tarscore.int64, 7, False)
        value.iItemCountByGroup = ios.read(tarscore.int32, 8, False)
        value.iItemGroup = ios.read(tarscore.int32, 9, False)
        value.iDisplayInfo = ios.read(tarscore.int32, 10, False)
        value.iSuperPupleLevel = ios.read(tarscore.int32, 11, False)
        value.iTemplateType = ios.read(tarscore.int32, 12, False)
        value.sExpand = ios.read(tarscore.string, 13, False)
        value.bBusi = ios.read(tarscore.boolean, 14, False)
        value.iShowTime = ios.read(tarscore.int32, 15, False)
        value.lPresenterYY = ios.read(tarscore.int64, 16, False)
        value.lSid = ios.read(tarscore.int64, 17, False)
        value.lSubSid = ios.read(tarscore.int64, 18, False)
        value.lRoomId = ios.read(tarscore.int64, 19, False)
        return value
