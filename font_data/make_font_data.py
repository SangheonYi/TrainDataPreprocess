from PIL import Image, ImageDraw, ImageFont
import os
import sys
sys.path.append("..")
from OCRUnicodeRange import *

def make_font_data(text_to_draw, font_path, encoding, save_path, font_size=10):
    # font setting
    encode_type = 'unic' if encoding.startswith("utf") else 'wans'
    font = ImageFont.truetype(font_path, size=font_size, encoding=encode_type)
    # Image size
    W = int(font.getlength(text_to_draw) * 1.2)
    H = int(font_size * 1.1)
    # draw text_to_draw on image
    image =Image.new('RGB', (W, H), color = 'white')
    draw = ImageDraw.Draw(image)
    draw.text((W * 0.1, 0), text_to_draw, font=font, fill="black")
    # save image
    image.save(save_path)

def make_fonts_dataset(font_path_list, font_sizes, mode):
    label_lines = []
    korean_dict = set()
    for font_path in font_path_list:
        font_path = f"fonts/{font_path}"
        support_chars, encoding = get_ttf_support_chars(font_path, total_exclude_unicodes_list)
        font_name = font_path.split('/')[-1][:-4]
        print("support size: ", len(support_chars))
        if encoding.startswith("utf"):
            korean_dict = korean_dict.union(support_chars)
            print("dict_size: ", len(korean_dict))
        if support_chars:
            for font_size in font_sizes:
                save_dir = f'kor_rec/{mode}{font_name}_{font_size}_data'
                os.makedirs(save_dir, exist_ok=True)
                for idx, support_char in enumerate(support_chars):
                    save_path = f'{save_dir}/{idx}_{ord(support_char)}.jpg'
                    make_font_data(support_char, font_path, encoding, save_path, font_size=font_size)
                    unicode_label = encode_int2unicode_chr(ord(support_char), encoding)
                    if unicode_label in won_dict[font_name].keys():
                        unicode_label = won_dict[font_name][unicode_label]
                    label_lines.append(f"{save_path}\t{support_char}\n")
                print(f"font: {font_name}, font size: {font_size} done")
        else:
            print(f"{font_path} is empty")
    return label_lines, korean_dict

font_path_list = ['Dotum.ttf']
font_sizes = [27, 47, 66] # 8, 14, 20 pt in 200dpi
font_sizes = [27]

label_lines, korean_dict = make_fonts_dataset(font_path_list, font_sizes, 'train')
write_label_file('rec_font_train.txt', label_lines)
with open("korean_dict.txt", "w", encoding="utf-8") as kor_dict_file:
    for e in sorted(korean_dict):
        kor_dict_file.write(f"{e}\n")