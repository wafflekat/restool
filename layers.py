from abc import abstractmethod
from dataclasses import dataclass

from decoder import Decoder


@dataclass
class Layer:

    @abstractmethod
    def load(self, data: bytes):
        pass


class ImageLayer(Layer):
    raw_image = None

    def load(self, data: bytes):
        decoder = Decoder(data)

        _ = decoder.get_int16()
        _ = decoder.get_int16()

        # obsolete flag?
        fl = decoder.get_uint8()

        _ = decoder.get_int16()

        # coords
        _ = decoder.get_int16()
        _ = decoder.get_int16()

        # image related key-value data
        kvdata = {}

        if fl & 4 != 0:
            while True:
                key = decoder.get_string()
                if not key:
                    break
                l = decoder.get_uint8()
                if l & 0x80 != 0:
                    l = decoder.get_int32()
                d = decoder.get_bytes(l)
                # val = Decoder(d)
                # if key == 'scale':
                #     kvdata[key] = val.get_float32()
                # else:
                kvdata[key] = d

        self.raw_image = decoder.get_bytes(-1)
