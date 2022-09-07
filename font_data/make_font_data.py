from PIL import Image, ImageDraw, ImageFont
import fontTools
from fontTools.ttLib import TTFont
import os
from collections.abc import Iterable
import struct

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def make_image(text_to_draw, font_path, encoding, font_size=10, mode=''):
    # Image size
    W = int(font_size * 1)
    H = W
    # font setting
    if encoding == 'utf-8':
        encoding = 'unic'
    else:
        encoding = 'wans'
    print(f"{font_path} encoding {encoding}")
    font = ImageFont.truetype(font_path, size=font_size, encoding=encoding)
    image =Image.new('RGB', (W, H), color = 'white')
    draw = ImageDraw.Draw(image)
    # start position for text
    x_text = 1
    y_text = 1
    # 각 줄의 내용을 적음
    draw.text((x_text, y_text), text_to_draw, font=font, fill="black")
    # 안에 적은 내용을 파일 이름으로 저장
    font_name = font_path[:-4]
    save_dir = f'{mode}{font_name}_{font_size}_data'
    createDirectory(save_dir)
    save_path = f'{save_dir}/{ord(text_to_draw)}.jpg'
    image.save(save_path)
    return save_path

def make_dataset(font_path_list, font_sizes, mode):
    label_lines = []
    for font_path in font_path_list:
        support_chars, encoding = get_support_chars(font_path)
        if support_chars:
            for c, label in support_chars:
                for font_size in font_sizes:
                    image_path = make_image(c, font_path, encoding, font_size=font_size, mode=mode)
                    label_lines.append(f"{image_path}\t{label}\n")
        else:
            print(f"{font_path} is empty")
    with open('train_label.txt', 'w', encoding="utf-8") as label_file:
        label_content = ''.join(label_lines)
        label_file.write(label_content)

def encode_not_utf8(i, encoding):
    return struct.pack('>H', i).decode(encoding)

def get_encoded_chr(i, encoding):
    if encoding != "utf-8" and i > 127:
        return encode_not_utf8(i, encoding)   
    return chr(i)

def is_valid_points(c):
    i = ord(c)
    return c.isprintable() and not (12643 < i < 12687 or 42196 < i < 42239)

def get_support_chars(font_path):
    font = TTFont(font_path)   # specify the path to the font in question
    support_chars = []
    for cmap in font['cmap'].tables:
        encoding = cmap.getEncoding()
        for i in cmap.cmap.keys():
            uni_chr = chr(i)
            if is_valid_points(uni_chr):
                try:
                    support_char = (uni_chr, get_encoded_chr(i, encoding))
                    support_chars.append(support_char)
                except:
                    print(f"{i} can't encode by {encoding}")
        if support_chars:
            return support_chars, encoding
    return False, ''

font_path_list = ['휴먼명조.ttf', 'Dotum-03.ttf', 'hy헤드라인m.ttf']
# font_path_list = ['GNGT(견고딕).ttf']
# old = get_support_chars_old(font_path_list[0])
# print(old)
# new = get_support_chars(font_path_list[0])
# print(new)
# different = set(old) - set(new)
# print(len(old), len(new))
# print(different)

font_sizes = [100]
# , 10, 11, 13, 16]
# make_dataset(font_path_list, font_sizes, 'old')
make_dataset(font_path_list, font_sizes, 'train')