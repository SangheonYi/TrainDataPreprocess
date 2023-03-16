import struct

def r2l(a, b):
    # list of range from a to b include both a and b
    return list(range(a, b + 1))

def encode_int2unicode_chr(i, encoding):
    if not encoding.startswith("utf") and i > 127:
        # euckr encoding
        # struct는 c언어에서 사용하는 타입의 binary 데이터와 호환할 때 사용한다.
        # H: unsigned short 2 bytes, >: big endian
        return struct.pack('>H', i).decode(encoding)
    return chr(i)

def write_label_file(label_file_name, label_lines):
    with open(label_file_name, 'w', encoding="utf-8") as label_file:
        label_contents = ''.join(label_lines)
        label_file.write(label_contents)