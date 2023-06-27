from PIL import Image, ImageDraw, ImageFont
import os
import sys
sys.path.append("..")
from OCRUnicodeRange import total_exclude_unicodes_list, won_dict, get_ttf_support_chars, write_font_label_file
from multiprocessing import Pool
import random
import time

def make_font_data(text_to_draw, font_path, encoding, save_path, font_size=10):
    # font setting
    encode_type = 'unic' if encoding.startswith("utf") else 'wans'
    font = ImageFont.truetype(font_path, size=font_size, encoding=encode_type)
    # Image size
    left, top, right, bottom = font.getbbox(text_to_draw) # warning, char code 32 space's top and bottom are same
    W = int(font.getlength(text_to_draw))
    text_coord = (0, 0)
    if font_size < 10:
        text_coord = (0, 1)
        W += 1
    H = int((bottom - top) * 1.1) if text_to_draw != ' ' else font_size
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

def get_random_arg(target_char, support_chars, font_name, ramdom_glyph_concat):
    random_chars = ''
    if ramdom_glyph_concat:
        random_chars = random.choices(support_chars, k=random.randint(15,23))
    joined = ''.join(random_chars)
    random_chars = f"{target_char}{joined}"
    random_gt = random_chars.translate(won_dict[font_name])
    random_size = random.randint(8, 56)
    return f"{target_char}{joined}", random_gt, random_size

def make_fonts_dataset(font_name, font_sizes, storage_dir, ramdom_font_size=False, ramdom_glyph_concat=False):
    label_lines = []
    korean_dict = set()
    
    font_path = f"fonts/{font_name}.ttf"
    support_chars, encoding = get_ttf_support_chars(font_path, total_exclude_unicodes_list)
    korean_dict = update_dict(support_chars, encoding, korean_dict)
    start = time.time()
    if support_chars:
        for font_size in font_sizes:
            if ramdom_font_size:
                save_dir = f'{storage_dir}/{font_name}_random_size_data'
            else:
                save_dir = f'{storage_dir}/{font_name}_{font_size}_data'
            os.makedirs(save_dir, exist_ok=True)
            for idx, target_char in enumerate(support_chars):
                char_code = ord(target_char)
                random_chars, random_gt, random_size = get_random_arg(target_char, support_chars, font_name, ramdom_glyph_concat)
                if ramdom_font_size:
                    font_size = random_size
                save_path = f'{save_dir}/{idx}_{char_code}_{font_size}size.jpg'
                make_font_data(random_chars, font_path, encoding, save_path, font_size=font_size)
                label_lines.append(f"{save_path}\t{random_gt}\n")
            if ramdom_font_size:
                print(f"font: {font_name}, random font size done, spent: {time.time() - start}")
            else:
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
    font_sizes = [10, 15, 20] # eval to small font
    font_sizes = [27, 47, 66] # 8, 14, 20 pt in 200dpi
    font_sizes = [8]
    ramdom_font_size = False
    ramdom_glyph_concat = False

    pool_count = os.cpu_count() // 4
    pool_count = pool_count if pool_count > 1 else 1 
    for font_name_sub_list in grouper(font_name_list, pool_count, fillvalue=None):
        font_name_sub_list = [font_name for font_name in font_name_sub_list if font_name is not None]
        pool_count = min(pool_count, len(font_name_sub_list))
        print(f"pool_count: {pool_count}")
        pool = Pool(pool_count)
        results = {font_name:pool.apply_async(make_fonts_dataset, args=
                                              (font_name, font_sizes, storage_dir, ramdom_font_size, ramdom_glyph_concat)) 
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