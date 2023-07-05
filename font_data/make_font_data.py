from PIL import Image, ImageDraw, ImageFont
import os
import sys
sys.path.append("..")
from OCRUnicodeRange import total_exclude_unicodes_list, won_dict, get_ttf_support_chars, write_font_label_file, is_cjk_ideographs
from multiprocessing import Pool
import random
import time
import numpy as np
from scipy.stats import loguniform

def font_init(font_path, encoding, font_size=10):
    encode_type = 'unic' if encoding.startswith("utf") else 'wans'
    return ImageFont.truetype(font_path, size=font_size, encoding=encode_type)

def make_font_data(draw_list, font):
    for text_to_draw, save_path in draw_list:
        # Image size
        left, top, right, bottom = font.getbbox(text_to_draw) # warning, char code 32 space's top and bottom are same
        W = int(font.getlength(text_to_draw))
        text_coord = (0, 0)
        if font.size < 10:
            text_coord = (0, 1)
            W += 1
        H = int((bottom - top) * 1.1) if text_to_draw != ' ' else font.size
        # draw text_to_draw on image
        image =Image.new('RGB', (W, H), color = 'white')
        draw = ImageDraw.Draw(image)
        draw.text(text_coord, text_to_draw, font=font, fill="black")
        # save image
        image.save(save_path)

def update_dict(support_chars, encoding, korean_dict):
    if encoding.startswith("utf"):
        korean_dict = korean_dict.union(support_chars)
    print("support size: ", len(support_chars))
    print("dict_size: ", len(korean_dict))
    return korean_dict

def sample_size(start_point, step_size, boundary):
    a, b = boundary
    rv = loguniform(a, b)
    drawn = (rv.rvs(1) - a) * step_size + start_point
    return int(drawn[0])

def get_random_gt(target_char, support_chars, font_name, ramdom_glyph_concat):
    random_chars = ''
    if ramdom_glyph_concat:
        random_chars = random.choices(support_chars, k=random.randint(15,23))
    joined = ''.join(random_chars)
    random_chars = f"{target_char}{joined}"
    random_gt = random_chars.translate(won_dict[font_name])
    is_fault = won_dict[font_name].get(target_char, False)
    if is_fault and is_fault in random_gt:
        print(f"found fault at {font_name} in ❓{random_gt}❓")
    return f"{target_char}{joined}", random_gt

def make_draw_list(support_chars, save_dir, font, font_name, ramdom_glyph_concat):
    draw_list = []
    sub_label_lines = []
    for idx, target_char in enumerate(support_chars):
        char_code = ord(target_char)
        random_chars, random_gt = get_random_gt(target_char, support_chars, font_name, ramdom_glyph_concat)
        if font.size < 11 and is_cjk_ideographs(char_code):
            continue
        save_path = f'{save_dir}/{idx}_{char_code}_{font.size}size.jpg'
        sub_label_lines.append(f"{save_path}\t{random_gt}\n")
        draw_list.append((random_chars, save_path))
    return draw_list, sub_label_lines

def make_fonts_dataset(font_name, font_sizes, storage_dir, ramdom_glyph_concat=False):
    label_lines = []
    korean_dict = set()
    
    font_path = f"fonts/{font_name}.ttf"
    support_chars, encoding = get_ttf_support_chars(font_path, total_exclude_unicodes_list)
    korean_dict = update_dict(support_chars, encoding, korean_dict)
    start = time.time()
    if support_chars:
        for font_size in font_sizes:
            font = font_init(font_path, encoding, font_size=font_size)
            save_dir = f'{storage_dir}/{font_name}_{font_size}_data'
            os.makedirs(save_dir, exist_ok=True)
            draw_list, sub_label_lines = make_draw_list(support_chars, save_dir, font, font_name, ramdom_glyph_concat)
            label_lines += sub_label_lines

            # generate font data
            make_font_data(draw_list, font)
            print(f"font: {font_name}, font size: {font_size} done, spent: {time.time() - start}")
    else:
        print(f"{font_path} is empty")
    return label_lines, korean_dict

from itertools import zip_longest

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

if __name__ == '__main__':
    storage_dir = "/home/sayi/workspace/OCR/PaddleOCR/train_data/font_data"
    font_label_list = []
    font_dict_set = set()

    font_name_list = ['휴먼명조', 'Dotum', 'hy헤드라인m', 'Gungsuh', 'Batang', 'Gulim', 'HY견고딕']
    font_name_list = ['hy헤드라인m']
    font_sizes = [10, 15, 20] # eval to small font
    font_sizes = [27, 47, 66] # 8, 14, 20 pt in 200dpi
    # 8, 10, 24 fix sizes, 11, 22, 33, 44, 55 interval random sizes

    step_size = 11
    font_sizes = [8, 10, 24] + [sample_size(start_point, step_size, (4, 5)) for start_point in range(11, 56, step_size)] 
    font_sizes = [8]
    ramdom_glyph_concat = True

    pool_count = os.cpu_count() // 2
    pool_count = pool_count if pool_count > 1 else 1 
    for font_name_sub_list in grouper(font_name_list, pool_count, fillvalue=None):
        font_name_sub_list = [font_name for font_name in font_name_sub_list if font_name is not None]
        pool_count = min(pool_count, len(font_name_sub_list))
        print(f"pool_count: {pool_count}")
        pool = Pool(pool_count)
        results = {font_name:pool.apply_async(make_fonts_dataset, args=
                                              (font_name, font_sizes, storage_dir, ramdom_glyph_concat)) 
                                              for font_name in font_name_sub_list }
        pool.close()
        pool.join()
        for font_name in font_name_sub_list:
            label_lines, korean_dict = results[font_name].get()
            font_label_list += label_lines
            font_dict_set = font_dict_set.union(korean_dict)

    write_font_label_file('rec_font_train.txt', font_label_list)
    with open("korean_dict.txt", "w", encoding="utf-8") as kor_dict_file:
        for e in sorted(font_dict_set):
            kor_dict_file.write(f"{e}\n")