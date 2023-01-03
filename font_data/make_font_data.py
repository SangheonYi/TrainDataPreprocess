from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
import os
import struct
from support_unicode_dict import *
import random

exclude_unicodes_list = []
for v in exclude_unicodes.values():
    exclude_unicodes_list += v
for conv_dict in similar_dict_list:
    exclude_unicodes_list += list(conv_dict.keys())
font_path_list = ['휴먼명조.ttf', 'Dotum.ttf', 'hy헤드라인m.ttf', 'GNGT(견고딕).ttf', 'Gungsuh.ttf', 'Batang.ttf', 'Gulim.ttf']
human_empty_glyph_list = [8361]
hyhead_empty_glyph_list = [96]
hyhead_wrong_glyph_list = r2l(162, 163) + r2l(165, 166) + r2l(162, 163) + r2l(162, 163) + r2l(162, 163)
gngt_empty_glyph_list = r2l(0, 31) + r2l(127, 255) + r2l(42196, 42238)
ttf_exclude_glyph = {
    "휴먼명조": human_empty_glyph_list,
    "Dotum": [],
    "hy헤드라인m": hyhead_empty_glyph_list + hyhead_wrong_glyph_list,
    "견고딕": gngt_empty_glyph_list,
    "Gungsuh": [],
    "Batang": [],
    "Gulim": []
}

won_dict = {
    "휴먼명조": {
        chr(0xffe6): chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
    "hy헤드라인m": {
        chr(0xffe6): chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
    "견고딕": {
        chr(0x5c): chr(0x20a9), # \ ₩ basic latin back slash
    },
    "Dotum": {
        chr(0x5c): chr(0x20a9), # \ ₩ basic latin back slash
        chr(0xffe6): chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
    "Gungsuh": {
        chr(0x5c): chr(0x20a9), # \ ₩ basic latin back slash
        chr(0xffe6): chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
    "Batang": {
        chr(0x5c): chr(0x20a9), # \ ₩ basic latin back slash
        chr(0xffe6): chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
    "Gulim": {
        chr(0x5c): chr(0x20a9), # \ ₩ basic latin back slash
        chr(0xffe6): chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
}

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except OSError:
        print("Error: Failed to create the directory.")
        return False

def make_font_data(text_to_draw, font_path, encoding, save_dir, font_size=10, idx=None):
    # Image size
    W = int(font_size * 1.2)
    H = W
    # font setting
    encode_type = 'unic' if encoding.startswith("utf") else 'wans'
    font = ImageFont.truetype(font_path, size=font_size, encoding=encode_type)
    image =Image.new('RGB', (W, H), color = 'white')
    draw = ImageDraw.Draw(image)
    # start position for text
    coor = (W - font_size) // 2
    position_xy = (coor, coor)
    # draw text_to_draw on image
    draw.text(position_xy, text_to_draw, font=font, fill="black")
    # save image
    if isinstance(idx, int):
        save_path = f'{save_dir}/{idx}_{ord(text_to_draw)}.jpg'
    else:
        save_path = f'{save_dir}/{ord(text_to_draw)}.jpg'
    image.save(save_path)
    return save_path

def make_fonts_dataset(font_path_list, font_sizes, mode):
    label_lines = []
    korean_dict = set()
    for font_path in font_path_list:
        support_chars, encoding = get_ttf_support_chars(font_path)
        font_name = font_path[:-4]
        print("support size: ", len(support_chars))
        if encoding.startswith("utf"):
            korean_dict = korean_dict.union(support_chars)
            print("dict_size: ", len(korean_dict))
        if support_chars:
            for font_size in font_sizes:
                save_dir = f'kor_rec/{mode}{font_name}_{font_size}_data'
                if createDirectory(save_dir):
                    for idx, support_char in enumerate(support_chars):
                        image_path = make_font_data(support_char, font_path, encoding, save_dir, font_size=font_size, idx=idx)
                        unicode_label = get_encoded_chr(ord(support_char), encoding)
                        if unicode_label in won_dict[font_name].keys():
                            print(f"font: {font_name}, unicode: {unicode_label}, won_dict: {won_dict[font_name]}")
                            unicode_label = won_dict[font_name][unicode_label]
                        label_lines.append(f"{image_path}\t{support_char}\n")
        else:
            print(f"{font_path} is empty")
    with open("korean_dict.txt", "w", encoding="utf-8") as kor_dict_file:
        for e in sorted(korean_dict):
            kor_dict_file.write(f"{e}\n")
    return label_lines

def write_label_file(label_lines):
    with open('rec_font_train.txt', 'w', encoding="utf-8") as label_file:
        label_contents = ''.join(label_lines)
        label_file.write(label_contents)

def get_encoded_chr(i, encoding):
    if not encoding.startswith("utf") and i > 127:
        # euckr encoding
        # struct는 c언어에서 사용하는 타입의 binary 데이터와 호환할 때 사용한다.
        # H: unsigned short 2 bytes, >: big endian
        return struct.pack('>H', i).decode(encoding)
    return chr(i)

def is_valid_decimal(font_name, i):
    if "견고딕" in font_name:
        return i not in gngt_empty_glyph_list
    elif i in partial_include:
        return True
    elif not chr(i).isprintable() or i in exclude_unicodes_list:
        return False

    # check font glyph
    if font_name in ttf_exclude_glyph.keys():
        return i not in ttf_exclude_glyph[font_name]
    print(f"decimal is not valid, {font_name} is unknown font")
    return False

def get_ttf_support_chars(font_path):
    font = TTFont(font_path)   # specify the path to the font in question
    support_chars = []
    font_name = font_path[:-4]
    # print(dir(font))
    print(f"get support character list from {font_path}")
    for cmap in font['cmap'].tables:
        encoding = cmap.getEncoding()
        # print(dir(cmap))
        # print(cmap.isUnicode(), encoding)
        # print(encoding)
        # print(cmap.platformID)
        # print(cmap.platEncID)
        for i in cmap.cmap.keys():
            uni_chr = chr(i)
            if is_valid_decimal(font_name, i):
                try:                    
                    support_chars.append(uni_chr)
                except:
                    print(f"decimal {i} can't be encoded by {encoding}")
        if support_chars:
            return support_chars, encoding
    return False, ''

font_path_list = ['휴먼명조.ttf', 'Dotum.ttf', 'hy헤드라인m.ttf', '견고딕.ttf', 'Gungsuh.ttf', 'Batang.ttf', 'Gulim.ttf']
# font_path_list = ['Dotum.ttf']
font_sizes = [8, 14,]
# font_sizes = [24]
label_lines = make_fonts_dataset(font_path_list, font_sizes, 'train')
write_label_file(label_lines)