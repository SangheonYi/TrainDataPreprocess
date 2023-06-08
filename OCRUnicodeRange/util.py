import struct

def r2l(a, b):
    # list of range from a to b include both a and b
    return list(range(a, b + 1))

def encode_int2unicode_chr(i:int, encoding: str):
    if not encoding.startswith("utf") and i > 127:
        return i.to_bytes(2, byteorder='big').decode(encoding)
        # euckr encoding
        # struct는 c언어에서 사용하는 타입의 binary 데이터와 호환할 때 사용한다.
        # H: unsigned short 2 bytes, >: big endian
        return struct.pack('>H', i).decode(encoding)
    return chr(i)

def enc_src2unicode_str(src, encoding: str):
    if not encoding.startswith("utf"):
        unic_str = ''
        for euckr_chr in src:
            unic_str = f"{unic_str}{encode_int2unicode_chr(ord(euckr_chr), encoding)}"
        return unic_str
    return src

def write_font_label_file(label_file_name, label_lines):
    with open(label_file_name, 'w', encoding="utf-8") as label_file:
        label_contents = ''.join(label_lines)
        label_file.write(label_contents)