
from live_platform.huya.plugins.huya_wup.wup_struct.PropsItem import HuyaPropsItem
from live_platform.huya.common.tars import tarscore

class HuyaGetPropsListRsp(tarscore.struct):
    __tars_class__ = "Huya.GetPropsListRsp"
    VctHuyaPropsItem = tarscore.vctclass(HuyaPropsItem)

    def __init__(self):
        self.vPropsItemList = HuyaGetPropsListRsp.VctHuyaPropsItem()
        self.sMd5 = ""
        self.iNewEffectSwitch = 0
        self.iMirrorRoomShowNum = 0
        self.iGameRoomShowNum = 0

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaGetPropsListRsp"):
        oos.write(HuyaGetPropsListRsp.VctHuyaPropsItem, 1, value.vPropsItemList)
        oos.write(tarscore.string, 2, value.sMd5)
        oos.write(tarscore.int16, 3, value.iNewEffectSwitch)
        oos.write(tarscore.int16, 4, value.iMirrorRoomShowNum)
        oos.write(tarscore.int16, 5, value.iGameRoomShowNum)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaGetPropsListRsp()
        value.vPropsItemList = ios.read(HuyaGetPropsListRsp.VctHuyaPropsItem, 1, False)
        value.sMd5 = ios.read(tarscore.string, 2, False)
        value.iNewEffectSwitch = ios.read(tarscore.int16, 3, False)
        value.iMirrorRoomShowNum = ios.read(tarscore.int16, 4, False)
        value.iGameRoomShowNum = ios.read(tarscore.int16, 5, False)
        return value

