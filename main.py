import argparse
import os
import requests

from decoder import Decoder
from layers import ImageLayer
from PIL import Image
from io import BytesIO


def main(filepath, respath: str):
    if filepath is not None:
        data, name = parse_file(filepath)
    elif respath is not None:
        name = respath.split('/')[len(respath.split('/')) - 1]
        r = requests.get(f'http://game.havenandhearth.com/res/{respath}.res', stream=True)
        if r.status_code != 200:
            raise Exception(f'Resource {respath} not found')
        data = r.raw.data
    else:
        raise Exception('filepath or URL required')

    if not data or not name:
        raise Exception('Error fetching data')

    layer = ImageLayer()

    decoder = Decoder(data)
    sig = 'Haven Resource 1'.encode('utf-8')
    if sig != decoder.get_bytes(len(sig)):
        raise Exception('Signature mismatch')
    ver = decoder.get_uint16()
    # TODO: figure out if I care about the version
    # seen 1 and 2 so far, both work
    # if ver != 1:
    #     raise Exception('Version mismatch', ver)

    while not decoder.eom():
        typ = decoder.get_string()
        l = decoder.get_int32()
        if typ != 'image':
            decoder.skip(l)
            continue
        layer.load(decoder.get_bytes(l))
    if layer.raw_image is not None:
        img = Image.open(BytesIO(layer.raw_image))
        img.save(f'{name}.png')
        print(f'saved image as {name}.png')
    print('done')


def parse_file(fp: str):
    if not os.path.exists(fp):
        raise Exception(f'Cannot find file {fp}')
    else:
        name = os.path.basename(fp)
        with open(fp, 'rb') as f:
            data = f.read()
        return data, name


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Resource tool')
    parser.add_argument('-f', dest='filepath', required=False, type=str)
    parser.add_argument('-u', dest='respath', required=False, type=str)
    args = parser.parse_args()
    main(args.filepath, args.respath)
