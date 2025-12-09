from live_platform.common.tars import tarscore

class HuyaPropView(tarscore.struct):
    __tars_class__ = "Huya.PropView"
    MapInt64Int16 = tarscore.mapclass(tarscore.int64, tarscore.int16)

    def __init__(self):
        
        self.id = 0
        self.name = ""
        self.uids = HuyaPropView.MapInt64Int16()
        self.tips = ""
        self.gameids = HuyaPropView.MapInt64Int16()

    @staticmethod
    def writeTo(oos: tarscore.TarsOutputStream, value: "HuyaPropView"):
        oos.write(tarscore.int32, 0, value.id)
        oos.write(tarscore.string, 1, value.name)
        oos.write(HuyaPropView.MapInt64Int16, 2, value.uids)
        oos.write(tarscore.string, 3, value.tips)
        oos.write(HuyaPropView.MapInt64Int16, 4, value.gameids)

    @staticmethod
    def readFrom(ios: tarscore.TarsInputStream):
        value = HuyaPropView()
        value.id = ios.read(tarscore.int32, 0, False)
        value.name = ios.read(tarscore.string, 1, False)
        value.uids = ios.read(HuyaPropView.MapInt64Int16, 2, False)
        value.tips = ios.read(tarscore.string, 3, False)
        value.gameids = ios.read(HuyaPropView.MapInt64Int16, 4, False)
        return value
