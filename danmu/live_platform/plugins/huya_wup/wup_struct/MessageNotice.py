from live_platform.plugins.huya_wup.wup_struct.UidNickName import HuyaUidNickName
from live_platform.plugins.huya_wup.wup_struct.DecorationInfo import HuyaDecorationInfo
from live_platform.plugins.huya_wup.wup_struct.BulletFormat import HuyaBulletFormat
from live_platform.plugins.huya_wup.wup_struct.ContentFormat import HuyaContentFormat
from live_platform.plugins.huya_wup.wup_struct.SenderInfo import HuyaSenderInfo
from live_platform.common.tars import tarscore

class HuyaMessageNotice(tarscore.struct):
    __tars_class__ = "Huya.MessageNotice"
    VctHuyaDecorationInfo = tarscore.vctclass(HuyaDecorationInfo)
    VctHuyaUidNickName = tarscore.vctclass(HuyaUidNickName)

    def __init__(self):
        self.tUserInfo = HuyaSenderInfo()
        self.lTid = 0
        self.lSid = 0
        self.sContent = ""
        self.iShowMode = 0
        self.tFormat = HuyaContentFormat()
        self.tBulletFormat = HuyaBulletFormat()
        self.iTermType = 0
        self.vDecorationPrefix = HuyaMessageNotice.VctHuyaDecorationInfo()
        self.vDecorationSuffix = HuyaMessageNotice.VctHuyaDecorationInfo()
        self.vAtSomeone = HuyaMessageNotice.VctHuyaUidNickName()
        self.lPid = 0
        self.vBulletPrefix = HuyaMessageNotice.VctHuyaDecorationInfo()
        self.sIconUrl = ""
        self.iType = 0
        self.vBulletSuffix = HuyaMessageNotice.VctHuyaDecorationInfo()

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaMessageNotice"): 
        oos.write(tarscore.struct, 0, value.tUserInfo)
        oos.write(tarscore.int64, 1, value.lTid)
        oos.write(tarscore.int64, 2, value.lSid)
        oos.write(tarscore.string, 3, value.sContent)
        oos.write(tarscore.int32, 4, value.iShowMode)
        oos.write(tarscore.struct, 5, value.tFormat)
        oos.write(tarscore.struct, 6, value.tBulletFormat)
        oos.write(tarscore.int32, 7, value.iTermType)
        oos.write(HuyaMessageNotice.VctHuyaDecorationInfo, 8, value.vDecorationPrefix)
        oos.write(HuyaMessageNotice.VctHuyaDecorationInfo, 9, value.vDecorationSuffix)
        oos.write(HuyaMessageNotice.VctHuyaUidNickName, 10, value.vAtSomeone)
        oos.write(tarscore.int64, 11, value.lPid)
        oos.write(HuyaMessageNotice.VctHuyaDecorationInfo, 12, value.vBulletPrefix)
        oos.write(tarscore.string, 13, value.sIconUrl)
        oos.write(tarscore.int32, 14, value.iType)
        oos.write(HuyaMessageNotice.VctHuyaDecorationInfo, 15, value.vBulletSuffix)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaMessageNotice()
        value.tUserInfo = ios.read(HuyaSenderInfo, 0, False)
        value.lTid = ios.read(tarscore.int64, 1, False)
        value.lSid = ios.read(tarscore.int64, 2, False)
        value.sContent = ios.read(tarscore.string, 3, False)
        value.iShowMode = ios.read(tarscore.int32, 4, False)
        value.tFormat = ios.read(HuyaContentFormat, 5, False)
        value.tBulletFormat = ios.read(HuyaBulletFormat, 6, False)
        value.iTermType = ios.read(tarscore.int32, 7, False)
        value.vDecorationPrefix = ios.read(HuyaMessageNotice.VctHuyaDecorationInfo, 8, False)
        value.vDecorationSuffix = ios.read(HuyaMessageNotice.VctHuyaDecorationInfo, 9, False)
        value.vAtSomeone = ios.read(HuyaMessageNotice.VctHuyaUidNickName, 10, False)
        value.lPid = ios.read(tarscore.int64, 11, False)
        value.vBulletPrefix = ios.read(HuyaMessageNotice.VctHuyaDecorationInfo, 12, False)
        value.sIconUrl = ios.read(tarscore.string, 13, False)
        value.iType = ios.read(tarscore.int32, 14, False)
        value.vBulletSuffix = ios.read(HuyaMessageNotice.VctHuyaDecorationInfo, 15, False)
        return value
