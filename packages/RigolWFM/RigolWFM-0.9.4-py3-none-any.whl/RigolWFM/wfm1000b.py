# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Wfm1000b(KaitaiStruct):
    """This was put together based on an excel header list of unknown provenance.
    It has been tested with a handful of different files.  The offset to the
    data seems correct and the channel coupling is untested.
    """

    class TriggerSourceEnum(Enum):
        ch1 = 0
        ch2 = 1
        ext = 2
        ext5 = 3
        ac_line = 5
        dig_ch = 7

    class TriggerModeEnum(Enum):
        edge = 0
        pulse = 1
        slope = 2
        video = 3
        alt = 4
        pattern = 5
        duration = 6

    class MachineModeEnum(Enum):
        ds1000b = 0
        ds1000c = 1
        ds1000e = 2
        ds1000z = 3
        ds2000 = 4
        ds4000 = 5
        ds6000 = 6

    class UnitEnum(Enum):
        w = 0
        a = 1
        v = 2
        u = 3
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        pass

    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\xA5\xA5\xA4\x01":
                raise kaitaistruct.ValidationNotEqualError(b"\xA5\xA5\xA4\x01", self.magic, self._io, u"/types/header/seq/0")
            self.scopetype = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 0, False)).decode(u"UTF-8")
            self.unknown_1 = self._io.read_bytes(44)
            self.adcmode = self._io.read_u1()
            self.unknown_2 = self._io.read_bytes(3)
            self.points = self._io.read_u4le()
            self.active_channel = self._io.read_u1()
            self.unknown_3 = self._io.read_bytes(3)
            self.ch = [None] * (4)
            for i in range(4):
                self.ch[i] = Wfm1000b.ChannelHeader(self._io, self, self._root)

            self.time_scale = self._io.read_u8le()
            self.time_offset = self._io.read_s8le()
            self.sample_rate_hz = self._io.read_f4le()
            self.time_scale_stop = self._io.read_u8le()
            self.time_scale_offset = self._io.read_s8le()
            self.unknown_4 = [None] * (4)
            for i in range(4):
                self.unknown_4[i] = self._io.read_u4le()

            self.coupling_ch12 = self._io.read_u1()
            self.coupling_ch34 = self._io.read_u1()
            self.unknown_5 = self._io.read_bytes(4)
            self.trigger_mode = KaitaiStream.resolve_enum(Wfm1000b.TriggerModeEnum, self._io.read_u1())
            self.unknown_6 = self._io.read_u1()
            self.trigger_source = KaitaiStream.resolve_enum(Wfm1000b.TriggerSourceEnum, self._io.read_u1())

        @property
        def ch2(self):
            if hasattr(self, '_m_ch2'):
                return self._m_ch2 if hasattr(self, '_m_ch2') else None

            if self.ch[1].enabled:
                io = self._root._io
                _pos = io.pos()
                io.seek((420 + self._root.header.points))
                self._m_ch2 = io.read_bytes(self.points)
                io.seek(_pos)

            return self._m_ch2 if hasattr(self, '_m_ch2') else None

        @property
        def ch1(self):
            if hasattr(self, '_m_ch1'):
                return self._m_ch1 if hasattr(self, '_m_ch1') else None

            if self.ch[0].enabled:
                io = self._root._io
                _pos = io.pos()
                io.seek(420)
                self._m_ch1 = io.read_bytes(self.points)
                io.seek(_pos)

            return self._m_ch1 if hasattr(self, '_m_ch1') else None

        @property
        def ch4(self):
            if hasattr(self, '_m_ch4'):
                return self._m_ch4 if hasattr(self, '_m_ch4') else None

            if self.ch[3].enabled:
                io = self._root._io
                _pos = io.pos()
                io.seek((420 + (self._root.header.points * 3)))
                self._m_ch4 = io.read_bytes(self.points)
                io.seek(_pos)

            return self._m_ch4 if hasattr(self, '_m_ch4') else None

        @property
        def seconds_per_point(self):
            if hasattr(self, '_m_seconds_per_point'):
                return self._m_seconds_per_point if hasattr(self, '_m_seconds_per_point') else None

            self._m_seconds_per_point = (1.0 / self.sample_rate_hz)
            return self._m_seconds_per_point if hasattr(self, '_m_seconds_per_point') else None

        @property
        def ch3(self):
            if hasattr(self, '_m_ch3'):
                return self._m_ch3 if hasattr(self, '_m_ch3') else None

            if self.ch[2].enabled:
                io = self._root._io
                _pos = io.pos()
                io.seek((420 + (self._root.header.points * 2)))
                self._m_ch3 = io.read_bytes(self.points)
                io.seek(_pos)

            return self._m_ch3 if hasattr(self, '_m_ch3') else None


    class ChannelHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.scale_display = self._io.read_s4le()
            self.shift_display = self._io.read_s2le()
            self.unknown1 = self._io.read_bytes(2)
            self.probe_value = self._io.read_f4le()
            self.probe_type = self._io.read_s1()
            self.invert_disp_val = self._io.read_u1()
            self.enabled_val = self._io.read_u1()
            self.invert_m_val = self._io.read_u1()
            self.scale_measured = self._io.read_s4le()
            self.shift_measured = self._io.read_s2le()
            self.time_delayed = self._io.read_u1()
            self.unknown2 = self._io.read_bytes(1)

        @property
        def unit(self):
            if hasattr(self, '_m_unit'):
                return self._m_unit if hasattr(self, '_m_unit') else None

            self._m_unit = Wfm1000b.UnitEnum.v
            return self._m_unit if hasattr(self, '_m_unit') else None

        @property
        def time_offset(self):
            if hasattr(self, '_m_time_offset'):
                return self._m_time_offset if hasattr(self, '_m_time_offset') else None

            self._m_time_offset = self._root.header.time_offset
            return self._m_time_offset if hasattr(self, '_m_time_offset') else None

        @property
        def inverted(self):
            if hasattr(self, '_m_inverted'):
                return self._m_inverted if hasattr(self, '_m_inverted') else None

            self._m_inverted = (True if self.invert_m_val != 0 else False)
            return self._m_inverted if hasattr(self, '_m_inverted') else None

        @property
        def time_scale(self):
            if hasattr(self, '_m_time_scale'):
                return self._m_time_scale if hasattr(self, '_m_time_scale') else None

            self._m_time_scale = self._root.header.time_scale
            return self._m_time_scale if hasattr(self, '_m_time_scale') else None

        @property
        def volt_offset(self):
            if hasattr(self, '_m_volt_offset'):
                return self._m_volt_offset if hasattr(self, '_m_volt_offset') else None

            self._m_volt_offset = (self.shift_measured * self.volt_scale)
            return self._m_volt_offset if hasattr(self, '_m_volt_offset') else None

        @property
        def volt_per_division(self):
            if hasattr(self, '_m_volt_per_division'):
                return self._m_volt_per_division if hasattr(self, '_m_volt_per_division') else None

            self._m_volt_per_division = (((-0.0000010 * self.scale_measured) * self.probe_value) if self.inverted else ((0.0000010 * self.scale_measured) * self.probe_value))
            return self._m_volt_per_division if hasattr(self, '_m_volt_per_division') else None

        @property
        def volt_scale(self):
            if hasattr(self, '_m_volt_scale'):
                return self._m_volt_scale if hasattr(self, '_m_volt_scale') else None

            self._m_volt_scale = (self.volt_per_division / 25.0)
            return self._m_volt_scale if hasattr(self, '_m_volt_scale') else None

        @property
        def enabled(self):
            if hasattr(self, '_m_enabled'):
                return self._m_enabled if hasattr(self, '_m_enabled') else None

            self._m_enabled = (True if self.enabled_val != 0 else False)
            return self._m_enabled if hasattr(self, '_m_enabled') else None


    @property
    def header(self):
        if hasattr(self, '_m_header'):
            return self._m_header if hasattr(self, '_m_header') else None

        _pos = self._io.pos()
        self._io.seek(0)
        self._m_header = Wfm1000b.Header(self._io, self, self._root)
        self._io.seek(_pos)
        return self._m_header if hasattr(self, '_m_header') else None


