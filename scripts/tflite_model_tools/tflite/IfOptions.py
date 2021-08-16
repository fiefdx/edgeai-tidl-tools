# automatically generated by the FlatBuffers compiler, do not modify

# namespace: tflite

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class IfOptions(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsIfOptions(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = IfOptions()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def IfOptionsBufferHasIdentifier(cls, buf, offset, size_prefixed=False):
        return flatbuffers.util.BufferHasIdentifier(buf, offset, b"\x54\x46\x4C\x33", size_prefixed=size_prefixed)

    # IfOptions
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # IfOptions
    def ThenSubgraphIndex(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # IfOptions
    def ElseSubgraphIndex(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

def IfOptionsStart(builder): builder.StartObject(2)
def IfOptionsAddThenSubgraphIndex(builder, thenSubgraphIndex): builder.PrependInt32Slot(0, thenSubgraphIndex, 0)
def IfOptionsAddElseSubgraphIndex(builder, elseSubgraphIndex): builder.PrependInt32Slot(1, elseSubgraphIndex, 0)
def IfOptionsEnd(builder): return builder.EndObject()


class IfOptionsT(object):

    # IfOptionsT
    def __init__(self):
        self.thenSubgraphIndex = 0  # type: int
        self.elseSubgraphIndex = 0  # type: int

    @classmethod
    def InitFromBuf(cls, buf, pos):
        ifOptions = IfOptions()
        ifOptions.Init(buf, pos)
        return cls.InitFromObj(ifOptions)

    @classmethod
    def InitFromObj(cls, ifOptions):
        x = IfOptionsT()
        x._UnPack(ifOptions)
        return x

    # IfOptionsT
    def _UnPack(self, ifOptions):
        if ifOptions is None:
            return
        self.thenSubgraphIndex = ifOptions.ThenSubgraphIndex()
        self.elseSubgraphIndex = ifOptions.ElseSubgraphIndex()

    # IfOptionsT
    def Pack(self, builder):
        IfOptionsStart(builder)
        IfOptionsAddThenSubgraphIndex(builder, self.thenSubgraphIndex)
        IfOptionsAddElseSubgraphIndex(builder, self.elseSubgraphIndex)
        ifOptions = IfOptionsEnd(builder)
        return ifOptions
