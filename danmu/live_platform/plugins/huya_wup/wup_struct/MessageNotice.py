from live_platform.plugins.huya_wup.wup_struct.UidNickName import HuyaUidNickName
from live_platform.plugins.huya_wup.wup_struct.DecorationInfo import HuyaDecorationInfo
from live_platform.plugins.huya_wup.wup_struct.BulletFormat import HuyaBulletFormat
from live_platform.plugins.huya_wup.wup_struct.ContentFormat import HuyaContentFormat
from live_platform.plugins.huya_wup.wup_struct.SenderInfo import HuyaSenderInfo
from live_platform.common.tars import tarscore

class HuyaMessageNotice:
    __tars_class__ = "Huya.MessageNotice"
    VctHuyaDecorationInfo = tarscore.vctclass(HuyaDecorationInfo)
    VctHuyaUidNickName = tarscore.vctclass(HuyaUidNickName)

    def __init__(self):
        self.tUserInfo: tarscore.struct = HuyaSenderInfo()
        self.lTid: tarscore.int64 = 0
        self.lSid: tarscore.int64 = 0
        self.sContent: tarscore.string = ""
        self.iShowMode: tarscore.int32 = 0
        self.tFormat: tarscore.struct = HuyaContentFormat()
        self.tBulletFormat: tarscore.struct = HuyaBulletFormat()
        self.iTermType: tarscore.int32 = 0
        self.vDecorationPrefix = HuyaMessageNotice.VctHuyaDecorationInfo()
        self.vDecorationSuffix = HuyaMessageNotice.VctHuyaDecorationInfo()
        self.vAtSomeone = HuyaMessageNotice.VctHuyaUidNickName()
        self.lPid: tarscore.int64 = 0
        self.vBulletPrefix = HuyaMessageNotice.VctHuyaDecorationInfo()
        self.sIconUrl: tarscore.string = ""
        self.iType: tarscore.int32 = 0
        self.vBulletSuffix = HuyaMessageNotice.VctHuyaDecorationInfo()

    def writeTo(self, oos: tarscore.TarsOutputStream): 
        oos.write(tarscore.struct, 0, self.tUserInfo)
        oos.write(tarscore.int64, 1, self.lTid)
        oos.write(tarscore.int64, 2, self.lSid)
        oos.write(tarscore.string, 3, self.sContent)
        oos.write(tarscore.int32, 4, self.iShowMode)
        oos.write(tarscore.struct, 5, self.tFormat)
        oos.write(tarscore.struct, 6, self.tBulletFormat)
        oos.write(tarscore.int32, 7, self.iTermType)
        oos.write(HuyaMessageNotice.VctHuyaDecorationInfo, 8, self.vDecorationPrefix)
        oos.write(HuyaMessageNotice.VctHuyaDecorationInfo, 9, self.vDecorationSuffix)
        oos.write(HuyaMessageNotice.VctHuyaUidNickName, 10, self.vAtSomeone)
        oos.write(tarscore.int64, 11, self.lPid)
        oos.write(HuyaMessageNotice.VctHuyaDecorationInfo, 12, self.vBulletPrefix)
        oos.write(tarscore.string, 13, self.sIconUrl)
        oos.write(tarscore.int32, 14, self.iType)
        oos.write(HuyaMessageNotice.VctHuyaDecorationInfo, 15, self.vBulletSuffix)

    def readFrom(self, ios: tarscore.TarsInputStream):
        self.tUserInfo = ios.read(HuyaSenderInfo, 0, False)
        self.lTid = ios.read(tarscore.int64, 1, False)
        self.lSid = ios.read(tarscore.int64, 2, False)
        self.sContent = ios.read(tarscore.string, 3, False)
        self.iShowMode = ios.read(tarscore.int32, 4, False)
        self.tFormat = ios.read(HuyaContentFormat, 5, False)
        self.tBulletFormat = ios.read(HuyaBulletFormat, 6, False)
        self.iTermType = ios.read(tarscore.int32, 7, False)
        self.vDecorationPrefix = ios.read(HuyaMessageNotice.VctHuyaDecorationInfo, 8, False)
        self.vDecorationSuffix = ios.read(HuyaMessageNotice.VctHuyaDecorationInfo, 9, False)
        self.vAtSomeone = ios.read(HuyaMessageNotice.VctHuyaUidNickName, 10, False)
        self.lPid = ios.read(tarscore.int64, 11, False)
        self.vBulletPrefix = ios.read(HuyaMessageNotice.VctHuyaDecorationInfo, 12, False)
        self.sIconUrl = ios.read(tarscore.string, 13, False)
        self.iType = ios.read(tarscore.int32, 14, False)
        self.vBulletSuffix = ios.read(HuyaMessageNotice.VctHuyaDecorationInfo, 15, False)
