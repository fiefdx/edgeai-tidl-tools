# automatically generated by the FlatBuffers compiler, do not modify

# namespace: tflite

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class CosOptions(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsCosOptions(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = CosOptions()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def CosOptionsBufferHasIdentifier(cls, buf, offset, size_prefixed=False):
        return flatbuffers.util.BufferHasIdentifier(buf, offset, b"\x54\x46\x4C\x33", size_prefixed=size_prefixed)

    # CosOptions
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

def CosOptionsStart(builder): builder.StartObject(0)
def CosOptionsEnd(builder): return builder.EndObject()


class CosOptionsT(object):

    # CosOptionsT
    def __init__(self):
        pass

    @classmethod
    def InitFromBuf(cls, buf, pos):
        cosOptions = CosOptions()
        cosOptions.Init(buf, pos)
        return cls.InitFromObj(cosOptions)

    @classmethod
    def InitFromObj(cls, cosOptions):
        x = CosOptionsT()
        x._UnPack(cosOptions)
        return x

    # CosOptionsT
    def _UnPack(self, cosOptions):
        if cosOptions is None:
            return

    # CosOptionsT
    def Pack(self, builder):
        CosOptionsStart(builder)
        cosOptions = CosOptionsEnd(builder)
        return cosOptions
