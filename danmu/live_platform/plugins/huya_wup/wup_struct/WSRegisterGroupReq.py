from live_platform.common.tars import tarscore

class HuyaWSRegisterGroupReq:
    __tars_class__ = "Huya.WSRegisterGroupReq"

    def __init__(self):
        VecStr = tarscore.vctclass(tarscore.string)
        self.vGroupId = VecStr()
        self.sToken: tarscore.string = ""

    def writeTo(self, oos: tarscore.TarsOutputStream):
        VecStr = tarscore.vctclass(tarscore.string)
        oos.write(VecStr(), 0, self.vGroupId)
        oos.write(tarscore.string, 1, self.sToken)

    def readFrom(self, ios: tarscore.TarsInputStream):
        VecStr = tarscore.vctclass(tarscore.string)
        self.vGroupId = ios.read(VecStr(), 0, False)
        self.sToken = ios.read(tarscore.string, 1, False)
