from dataclasses import dataclass
import struct


@dataclass
class Decoder:
    data: bytes

    def eom(self):
        return len(self.data) == 0

    def skip(self, l: int):
        self.data = self.data[l:]

    def get_string(self):
        l = 0
        while l < len(self.data) and self.data[l] != 0:
            l += 1
        s = self.data[:l].decode('utf-8')
        self.data = self.data[l + 1:]
        return s

    def get_bytes(self, l: int):
        if l > len(self.data) or l < 0:
            l = len(self.data)
        b = self.data[:l]
        self.data = self.data[l:]
        return b

    def get_uint8(self):
        u = self.data[0]
        self.data = self.data[1:]
        return u

    def get_int16(self):
        u = struct.unpack('<h', self.data[:2])[0]
        self.data = self.data[2:]
        return u

    def get_uint16(self):
        u = struct.unpack('<H', self.data[:2])[0]
        self.data = self.data[2:]
        return u

    def get_int32(self):
        u = struct.unpack('<i', self.data[:4])[0]
        self.data = self.data[4:]
        return u

    def get_uint32(self):
        u = struct.unpack('<I', self.data[:4])[0]
        self.data = self.data[4:]
        return u

    def get_int64(self):
        u = struct.unpack('<q', self.data[:8])[0]
        self.data = self.data[8:]
        return u

    def get_float32(self):
        u = struct.unpack('<f', self.data[:4])[0]
        self.data = self.data[4:]
        return u

    def get_float64(self):
        u = struct.unpack('<d', self.data[:8])[0]
        self.data = self.data[8:]
        return u
