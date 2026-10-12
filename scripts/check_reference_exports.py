"""Check generated PNG transparency and SVG parsing, not visual quality or architecture approval."""
import json
from pathlib import Path
import struct
import xml.etree.ElementTree as ET
import zlib

ROOT = Path(__file__).resolve().parents[1]


def alpha_range(path):
    data = path.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    offset = 8
    compressed = b''
    while offset < len(data):
        length = struct.unpack('>I', data[offset:offset+4])[0]
        kind = data[offset+4:offset+8]
        block = data[offset+8:offset+8+length]
        if kind == b'IHDR':
            width, height, bits, color, compression, filtering, interlace = struct.unpack('>IIBBBBB', block)
            assert (bits, color, compression, filtering, interlace) == (8, 6, 0, 0, 0), 'Expected noninterlaced RGBA PNG'
        if kind == b'IDAT':
            compressed += block
        offset += length + 12
    raw = zlib.decompress(compressed)
    previous = [0] * width
    low, high = 255, 0
    stride = width * 4 + 1
    for y in range(height):
        row = raw[y*stride:(y+1)*stride]
        mode = row[0]
        alpha = list(row[4::4])
        for x, value in enumerate(alpha):
            left = alpha[x-1] if x else 0
            up = previous[x]
            diagonal = previous[x-1] if x else 0
            if mode == 1:
                value += left
            elif mode == 2:
                value += up
            elif mode == 3:
                value += (left + up) // 2
            elif mode == 4:
                prediction = left + up - diagonal
                distances = [abs(prediction-left), abs(prediction-up), abs(prediction-diagonal)]
                value += (left, up, diagonal)[distances.index(min(distances))]
            elif mode != 0:
                raise ValueError('Unexpected PNG filter')
            alpha[x] = value % 256
        low = min(low, min(alpha))
        high = max(high, max(alpha))
        previous = alpha
    assert low == 0 and high == 255, 'Missing transparent background or opaque diagram pixels'
    return {'width': width, 'height': height, 'alpha_min': low, 'alpha_max': high}


if __name__ == '__main__':
    results = []
    for path in sorted((ROOT/'docs/diagrams').glob('1[1-4]_*.png')):
        svg = ET.parse(path.with_suffix('.svg')).getroot()
        assert 'background:transparent' in svg.attrib['style']
        assert svg.find('{http://www.w3.org/2000/svg}title') is not None
        results.append({'view': path.stem, **alpha_range(path)})
    assert len(results) == 4
    report = {'scope': 'Four v0.4 exports; not a review of the thirteen historical views',
              'result': 'PASS', 'checks': results}
    (ROOT/'governance/evidence/reference-diagram-exports.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
