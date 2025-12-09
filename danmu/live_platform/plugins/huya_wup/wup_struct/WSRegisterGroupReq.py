from live_platform.common.tars import tarscore

class HuyaWSRegisterGroupReq(tarscore.struct):
    __tars_class__ = "Huya.WSRegisterGroupReq"

    def __init__(self):
        self.VecStr = tarscore.vctclass(tarscore.string)
        self.vGroupId = self.VecStr()
        self.sToken: tarscore.string = ""

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaWSRegisterGroupReq"):
        oos.write(value.VecStr, 0, value.vGroupId)
        oos.write(tarscore.string, 1, value.sToken)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaWSRegisterGroupReq()
        value.vGroupId = ios.read(value.VecStr, 0, False)
        value.sToken = ios.read(tarscore.string, 1, False)

    def debug(self):
        print("------- HuyaWSRegisterGroupReq DEBUG -------")

        print("vGroupId:")
        if isinstance(self.vGroupId, list):
            for i, item in enumerate(self.vGroupId):
                print(f"  [{i}] {item!r}")
        else:
            print("  <invalid type>", self.vGroupId)

        print(f"sToken: {self.sToken!r}")

        print("--------------------------------------------")
