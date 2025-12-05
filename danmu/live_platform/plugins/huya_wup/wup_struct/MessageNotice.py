from live_platform.plugins.huya_wup.wup_struct.UidNickName import HuyaUidNickName
from live_platform.plugins.huya_wup.wup_struct.DecorationInfo import HuyaDecorationInfo
from live_platform.plugins.huya_wup.wup_struct.BulletFormat import HuyaBulletFormat
from live_platform.plugins.huya_wup.wup_struct.ContentFormat import HuyaContentFormat
from live_platform.plugins.huya_wup.wup_struct.SenderInfo import HuyaSenderInfo
from live_platform.common.tars import tarscore

class HuyaMessageNotice(tarscore.struct):
    __tars_class__ = "Huya.MessageNotice"

    def __init__(self):
        self.tUserInfo: tarscore.struct = HuyaSenderInfo()
        self.lTid: tarscore.int64 = 0
        self.lSid: tarscore.int64 = 0
        self.sContent: tarscore.string = ""
        self.iShowMode: tarscore.int32 = 0
        self.tFormat: tarscore.struct = HuyaContentFormat()
        self.tBulletFormat: tarscore.struct = HuyaBulletFormat
        self.iTermType: tarscore.int32 = 0
        self.vDecorationPrefix: tarscore.vctclass = tarscore.vctclass(HuyaDecorationInfo)
        self.vDecorationSuffix: tarscore.vctclass = tarscore.vctclass(HuyaDecorationInfo)
        self.vAtSomeone: tarscore.vctclass = tarscore.vctclass(HuyaUidNickName)
        self.lPid: tarscore.int64 = 0
        self.vBulletPrefix: tarscore.vctclass = tarscore.vctclass(HuyaDecorationInfo)
        self.sIconUrl: tarscore.string = ""
        self.iType: tarscore.int32 = 0
        self.vBulletSuffix: tarscore.vctclass = tarscore.vctclass(HuyaDecorationInfo)

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value):
        oos.write(tarscore.struct, 0, value.tUserInfo)
        oos.write(tarscore.int64, 1, value.lTid)
        oos.write(tarscore.int64, 2, value.lSid)
        oos.write(tarscore.string, 3, value.sContent)
        oos.write(tarscore.int32, 4, value.iShowMode)
        oos.write(tarscore.struct, 5, value.tFormat)
        oos.write(tarscore.struct, 6, value.tBulletFormat)
        oos.write(tarscore.int32, 7, value.iTermType)
        oos.write(tarscore.vctclass, 8, value.vDecorationPrefix)
        oos.write(tarscore.vctclass, 9, value.vDecorationSuffix)
        oos.write(tarscore.vctclass, 10, value.vAtSomeone)
        oos.write(tarscore.int64, 11, value.lPid)
        oos.write(tarscore.vctclass, 12, value.vBulletPrefix)
        oos.write(tarscore.string, 13, value.sIconUrl)
        oos.write(tarscore.int32, 14, value.iType)
        oos.write(tarscore.vctclass, 15, value.vBulletSuffix)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaMessageNotice()
        value.tUserInfo = ios.read(tarscore.struct, 0, False)
        value.lTid = ios.read(tarscore.int64, 1, False)
        value.lSid = ios.read(tarscore.int64, 2, False)
        value.sContent = ios.read(tarscore.string, 3, False)
        value.iShowMode = ios.read(tarscore.int32, 4, False)
        value.tFormat = ios.read(tarscore.struct, 5, False)
        value.tBulletFormat = ios.read(tarscore.struct, 6, False)
        value.iTermType = ios.read(tarscore.int32, 7, False)
        value.vDecorationPrefix = ios.read(tarscore.vctclass, 8, False)
        value.vDecorationSuffix = ios.read(tarscore.vctclass, 9, False)
        value.vAtSomeone = ios.read(tarscore.vctclass, 10, False)
        value.lPid = ios.read(tarscore.int64, 11, False)
        value.vBulletPrefix = ios.read(tarscore.vctclass, 12, False)
        value.sIconUrl = ios.read(tarscore.string, 13, False)
        value.iType = ios.read(tarscore.int32, 14, False)
        value.vBulletSuffix = ios.read(tarscore.vctclass, 15, False)
