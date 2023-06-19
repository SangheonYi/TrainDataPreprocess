from PIL import Image, ImageDraw, ImageFont
import os
import sys
sys.path.append("..")
from OCRUnicodeRange import *
import random
import time

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

def update_dict(support_chars, encoding, korean_dict):
    if encoding.startswith("utf"):
        korean_dict = korean_dict.union(support_chars)
    print("support size: ", len(support_chars))
    print("dict_size: ", len(korean_dict))
    return korean_dict

def get_unicode_label(random_chars, encoding, font_name):
    for idx, target_char in enumerate(random_chars):
        char_code = ord(target_char)
        unicode_char = encode_int2unicode_chr(char_code, encoding)
        random_chars[idx:] = won_dict[font_name].get(unicode_char, unicode_char)
    return 

def make_fonts_dataset(font_name_list, font_sizes, storage_dir):
    label_lines = []
    korean_dict = set()
    
    for font_name in font_name_list:
        font_path = f"fonts/{font_name}.ttf"
        support_chars, encoding = get_ttf_support_chars(font_path, total_exclude_unicodes_list)
        korean_dict = update_dict(support_chars, encoding, korean_dict)
        start = time.time()
        font_won_table = str.maketrans(won_dict[font_name].keys(), '12345')
        if support_chars:
            for font_size in font_sizes:
                save_dir = f'{storage_dir}/{font_name}_{font_size}_data'
                os.makedirs(save_dir, exist_ok=True)
                for idx, support_char in enumerate(support_chars):
                    char_code = ord(support_char)
                    save_path = f'{save_dir}/{idx}_{char_code}.jpg'
                    random_chars = f"{support_char}{random.choices(support_chars, k=random.randint(8,15))}"
                    make_font_data(random_chars, font_path, encoding, save_path, font_size=font_size)
                    unicode_label = get_unicode_label(random_chars, encoding, font_name)
                    label_lines.append(f"{save_path}\t{unicode_label}\n")
                print(f"font: {font_name}, font size: {font_size} done, spent: {time.time() - start}")
        else:
            print(f"{font_path} is empty")
    return label_lines, korean_dict


storage_dir = "/home/sayi/workspace/OCR/PaddleOCR/train_data/font_data"

font_name_list = ['Dotum']
font_sizes = [27, 47, 66] # 8, 14, 20 pt in 200dpi
font_sizes = [10, 15, 20] # eval to small font

label_lines, korean_dict = make_fonts_dataset(font_name_list, font_sizes, storage_dir)
write_font_label_file('rec_font_train.txt', label_lines)
with open("korean_dict.txt", "w", encoding="utf-8") as kor_dict_file:
    for e in sorted(korean_dict):
        kor_dict_file.write(f"{e}\n")