from live_platform.plugins.huya_wup.wup_struct.ItemEffectBizData import HuyaItemEffectBizData
from live_platform.plugins.huya_wup.wup_struct.DIYBigGiftEffect import HuyaDIYBigGiftEffect
from live_platform.plugins.huya_wup.wup_struct.ItemEffectInfo import HuyaItemEffectInfo
from live_platform.plugins.huya_wup.wup_struct.NobleLevelInfo import HuyaNobleLevelInfo
from live_platform.plugins.huya_wup.wup_struct.StreamerNode import HuyaStreamerNode
from live_platform.plugins.huya_wup.wup_struct.UserIdentityInfo import HuyaUserIdentityInfo
from live_platform.common.tars import tarscore

class HuyaSendItemSubBroadcastPacket(tarscore.struct):
    __tars_class__ = "Huya.SendItemSubBroadcastPacket"
    VctInt64 = tarscore.vctclass(tarscore.int64)
    VctHuyaItemEffectBizData = tarscore.vctclass(HuyaItemEffectBizData)

    def __init__(self):
        self.iItemType: tarscore.int64 = 0
        self.strPayId: tarscore.string = ""
        self.iItemCount: tarscore.int32 = 0
        self.lPresenterUid: tarscore.int64 = 0
        self.lSenderUid: tarscore.int64 = 0
        self.sPresenterNick: tarscore.string = ""
        self.sSenderNick: tarscore.string = ""
        self.sSendContent: tarscore.string = ""
        self.iItemCountByGroup: tarscore.int32 = 0
        self.iItemGroup: tarscore.int32 = 0
        self.iSuperPupleLevel: tarscore.int32 = 0
        self.iComboScore: tarscore.int32 = 0
        self.iDisplayInfo: tarscore.int32 = 0
        self.iEffectType: tarscore.int32 = 0
        self.iSenderIcon: tarscore.string = ""
        self.iPresenterIcon: tarscore.string = ""
        self.iTemplateType: tarscore.int32 = 0
        self.sExpand: tarscore.string = ""
        self.bBusi: tarscore.boolean = False
        self.iColorEffectType: tarscore.int32 = 0
        self.sPropsName: tarscore.string = ""
        self.iAccpet: tarscore.int16 = 0
        self.iEventType: tarscore.int16 = 0
        self.userInfo = HuyaUserIdentityInfo()
        self.lRoomId: tarscore.int64 = 0
        self.lHomeOwnerUid: tarscore.int64 = 0
        self.streamerInfo = HuyaStreamerNode()
        self.iPayType = -1
        self.iNobleLevel = 0
        self.tNobleLevel = HuyaNobleLevelInfo
        self.tEffectInfo = HuyaItemEffectInfo()
        self.vExUid = HuyaSendItemSubBroadcastPacket.VctInt64()
        self.iComboStatus = 0
        self.iPidColorType = 0
        self.iMultiSend = 0
        self.iVFanLevel = 0
        self.iUpgradeLevel = 0
        self.sCustomText = ""
        self.tDIYEffect = HuyaDIYBigGiftEffect()
        self.lComboSeqId = 0
        self.lPayTotal = 0
        self.vBizData = HuyaSendItemSubBroadcastPacket.VctHuyaItemEffectBizData()

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaSendItemSubBroadcastPacket"):
        oos.write(tarscore.int64, 0, value.iItemType)
        oos.write(tarscore.string, 1, value.strPayId)
        oos.write(tarscore.int32, 2, value.iItemCount)
        oos.write(tarscore.int64, 3, value.lPresenterUid)
        oos.write(tarscore.int64, 4, value.lSenderUid)
        oos.write(tarscore.string, 5, value.sSenderNick)
        oos.write(tarscore.string, 7, value.sSendContent)
        oos.write(tarscore.int32, 8, value.iItemCountByGroup)
        oos.write(tarscore.int32, 9, value.iItemGroup)
        oos.write(tarscore.int32, 10, value.iSuperPupleLevel)
        oos.write(tarscore.int32, 11, value.iComboScore)
        oos.write(tarscore.int32, 12, value.iDisplayInfo)
        oos.write(tarscore.int32, 13, value.iEffectType)
        oos.write(tarscore.string, 14, value.iSenderIcon)
        oos.write(tarscore.string, 15, value.iPresenterIcon)
        oos.write(tarscore.int32, 16, value.iTemplateType)
        oos.write(tarscore.string, 17, value.sExpand)
        oos.write(tarscore.boolean, 18, value.bBusi)
        oos.write(tarscore.int32, 19, value.iColorEffectType)
        oos.write(tarscore.string, 20, value.sPropsName)
        oos.write(tarscore.int16, 21, value.iAccpet)
        oos.write(tarscore.int64, 22, value.iEventType)
        oos.write(HuyaUserIdentityInfo, 23, value.userInfo)
        oos.write(tarscore.int64, 24, value.lRoomId)
        oos.write(tarscore.int64, 25, value.lHomeOwnerUid)
        oos.write(HuyaStreamerNode, 26, value.streamerInfo)
        oos.write(tarscore.int32, 27, value.iPayType)
        oos.write(tarscore.int32, 28, value.iNobleLevel)
        oos.write(HuyaNobleLevelInfo, 29, value.tNobleLevel)
        oos.write(HuyaItemEffectInfo, 30, value.tEffectInfo)
        oos.write(HuyaSendItemSubBroadcastPacket.VctInt64, 31, value.vExUid)
        oos.write(tarscore.int32, 32, value.iComboStatus)
        oos.write(tarscore.int32, 33, value.iPidColorType)
        oos.write(tarscore.int32, 34, value.iMultiSend)
        oos.write(tarscore.int32, 35, value.iVFanLevel)
        oos.write(tarscore.int32, 36, value.iUpgradeLevel)
        oos.write(tarscore.string, 37, value.sCustomText)
        oos.write(HuyaDIYBigGiftEffect, 38, value.tDIYEffect)
        oos.write(tarscore.int64, 39, value.lComboSeqId)
        oos.write(tarscore.int64, 41, value.lPayTotal)
        oos.write(HuyaSendItemSubBroadcastPacket.VctHuyaItemEffectBizData, 42, value.vBizData)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaSendItemSubBroadcastPacket()
        value.iItemType = ios.read(tarscore.int32, 0, False)
        value.strPayId = ios.read(tarscore.string, 1, False)
        value.iItemCount = ios.read(tarscore.int32, 2, False)
        value.lPresenterUid = ios.read(tarscore.int64, 3, False)
        value.lSenderUid = ios.read(tarscore.int64, 4, False)
        value.sPresenterNick = ios.read(tarscore.string, 5, False)
        value.sSenderNick = ios.read(tarscore.string, 6, False)
        value.sSendContent = ios.read(tarscore.string, 7, False)
        value.iItemCountByGroup = ios.read(tarscore.int32, 8, False)
        value.iItemGroup = ios.read(tarscore.int32, 9, False)
        value.iSuperPupleLevel = ios.read(tarscore.int32, 10, False)
        value.iComboScore = ios.read(tarscore.int32, 11, False)
        value.iDisplayInfo = ios.read(tarscore.int32, 12, False)
        value.iEffectType = ios.read(tarscore.int32, 13, False)
        value.iSenderIcon = ios.read(tarscore.string, 14, False)
        value.iPresenterIcon = ios.read(tarscore.string, 15, False)
        value.iTemplateType = ios.read(tarscore.int32, 16, False)
        value.sExpand = ios.read(tarscore.string, 17, False)
        value.bBusi = ios.read(tarscore.boolean, 18, False)
        value.iColorEffectType = ios.read(tarscore.int32, 19, False)
        value.sPropsName = ios.read(tarscore.string, 20, False)
        value.iAccpet = ios.read(tarscore.int16, 21, False)
        value.iEventType = ios.read(tarscore.int64, 22, False)
        value.userInfo = ios.read(HuyaUserIdentityInfo, 23, False)
        value.lRoomId = ios.read(tarscore.int64, 24, False)
        value.lHomeOwnerUid = ios.read(tarscore.int64, 25, False)
        value.streamerInfo = ios.read(HuyaStreamerNode, 26, False)
        value.iPayType = ios.read(tarscore.int32, 27, False)
        value.iNobleLevel = ios.read(tarscore.int32, 28, False)
        value.tNobleLevel = ios.read(HuyaNobleLevelInfo, 29, False)
        value.tEffectInfo = ios.read(HuyaItemEffectInfo, 30, False)
        value.vExUid = ios.read(HuyaSendItemSubBroadcastPacket.VctInt64, 31, False)
        value.iComboStatus = ios.read(tarscore.int32, 32, False)
        value.iPidColorType = ios.read(tarscore.int32, 33, False)
        value.iMultiSend = ios.read(tarscore.int32, 34, False)
        value.iVFanLevel = ios.read(tarscore.int32, 35, False)
        value.iUpgradeLevel = ios.read(tarscore.int32, 36, False)
        value.sCustomText = ios.read(tarscore.string, 37, False)
        value.tDIYEffect = ios.read(HuyaDIYBigGiftEffect, 38, False)
        value.lComboSeqId = ios.read(tarscore.int64, 39, False)
        value.lPayTotal = ios.read(tarscore.int64, 41, False)
        value.vBizData = ios.read(HuyaSendItemSubBroadcastPacket.VctHuyaItemEffectBizData, 42, False)
        return value
