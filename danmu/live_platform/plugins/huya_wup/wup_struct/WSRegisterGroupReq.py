from live_platform.common.tars import tarscore
from live_platform.common.tars.__util import util

class HuyaWSRegisterGroupReq(tarscore.struct):
    __tars_class__ = "Huya.WSRegisterGroupReq"

    def __init__(self):
        self.vGroupId = tarscore.vctclass = tarscore.vctclass(tarscore.string)
        self.sToken = ""

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value):
        oos.write(tarscore.vctclass, 0, value.vGroupId)
        oos.write(tarscore.string, 1, value.sToken)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaWSRegisterGroupReq()
        value.vGroupId = ios.read(tarscore.vctclass, 0, False)
        value.sToken = ios.read(tarscore.string, 1, False)
