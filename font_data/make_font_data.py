from PIL import Image, ImageDraw, ImageFont
import os
import sys
sys.path.append("..")
from OCRUnicodeRange import total_exclude_unicodes_list, won_dict, get_ttf_support_chars, write_font_label_file, is_cjk_ideographs
from multiprocessing import Pool
from scipy.stats import loguniform
import random
import time
import string
from util import get_random_words, corpus_lines, imgs2tar

def font_init(font_path, encoding, font_size=10):
    encode_type = 'unic' if encoding.startswith("utf") else 'wans'
    return ImageFont.truetype(font_path, size=font_size, encoding=encode_type)

def is_ascii_lower(target):
    if set(target).difference(range(string.ascii_lowercase)):
        return False
    return True

def make_font_data(draw_list, font, generated_imgs):
    for text_to_draw, save_path, training_path in draw_list:
        W = int(font.getlength(text_to_draw) + 2)
        text_coord = (1, 0)
        if font.size <= 10:
            text_coord = (1, 1)
            W += 1
        H = int(font.size * 1.1) + 2
        # draw text_to_draw on image
        image =Image.new('RGB', (W, H), color = 'white')
        draw = ImageDraw.Draw(image)
        draw.text(text_coord, text_to_draw, font=font, fill="black")
        # save image
        # image.save(save_path)
        generated_imgs.append((image, training_path))

def update_dict(support_chars, encoding):
    print("support size: ", len(support_chars))
    return support_chars if encoding.startswith("utf") else set()

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
    to_draw_str = f"{target_char}{joined}"
    random_gt = to_draw_str.translate(won_dict[font_name])
    is_fault = won_dict[font_name].get(target_char, False)
    if is_fault and is_fault in random_gt:
        print(f"found fault at {font_name} in ❓{random_gt}❓")
    return to_draw_str, random_gt

def append_drawlist(draw_list, sub_label_lines, valid_gt, to_draw_str, save_path):
    global storage_dir

    training_path = save_path.replace(storage_dir, "")
    sub_label_lines.append(f"{training_path}\t{valid_gt}\n")
    draw_list.append((to_draw_str, save_path, training_path))

def get_draw_list(support_chars, save_dir, font, font_name, options):
    draw_list = []
    sub_label_lines = []
    os.makedirs(save_dir, exist_ok=True)
    if options["is_corpus_draw"]:
        for idx, word in enumerate(get_random_words(corpus_lines, options["k_size"])):
            save_path = f'{save_dir}/{idx}.jpg'
            valid_gt = word.translate(won_dict[font_name])
            append_drawlist(draw_list, sub_label_lines, valid_gt, word, save_path)
    else:
        for idx, target_char in enumerate(support_chars):
            char_code = ord(target_char)
            if font.size < 11 and is_cjk_ideographs(char_code):
                continue
            to_draw_str, random_gt = get_random_gt(target_char, support_chars, font_name, options["ramdom_glyph_concat"])
            save_path = f'{save_dir}/{idx}_{char_code}.jpg'
            append_drawlist(draw_list, sub_label_lines, random_gt, to_draw_str, save_path)
    return draw_list, sub_label_lines

def make_fonts_dataset(font_name, font_sizes, storage_dir, options):
    label_lines = []
    generated_imgs = []
    font_path = f"fonts/{font_name}.ttf"
    support_chars, encoding = get_ttf_support_chars(font_path, total_exclude_unicodes_list)
    if support_chars:
        for font_size in font_sizes:
            start = time.time()
            if font_size not in [8, 10, 24] and not options["fix_font_size"]:
                font_size = sample_size(font_size, 11, (4, 5))
            font = font_init(font_path, encoding, font_size=font_size)
            save_dir = f'{storage_dir}font_data_72/{font_name}_{font_size}_data'
            if options["is_corpus_draw"]:
                save_dir = f'{save_dir}_corpus'
            draw_list, sub_label_lines = get_draw_list(support_chars, save_dir, font, font_name, options)
            label_lines += sub_label_lines

            # generate font data
            make_font_data(draw_list, font, generated_imgs)
            print(f"font: {font_name}, font size: {font_size} done, spent: {time.time() - start}")
    else:
        print(f"{font_path} is empty")
    return label_lines, update_dict(support_chars, encoding), generated_imgs

from itertools import zip_longest

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

if __name__ == '__main__':
    options = {
        "is_corpus_draw": False,
        "k_size": 200,
        "fix_font_size": True,
        "ramdom_glyph_concat": True,
    }

    storage_dir = "/mnt/c/exception/ocr_tmp/test"
    storage_dir = "/home/sayi/workspace/OCR/PaddleOCR/train_data/test/"
    font_label_list = []
    font_dict_set = set()

    font_name_list = ['hy헤드라인m']
    font_name_list = ['휴먼명조', 'Dotum', 'hy헤드라인m', 'Gungsuh', 'Batang', 'Gulim', 'HY견고딕']
    font_name_list = ['휴먼명조', 'Dotum']

    step_size = 11
    # 8, 10, 24 fix sizes, 11, 22, 33, 44, 55 interval random sizes
    font_sizes = [34]
    font_sizes = [8, 10, 24] + [start_point for start_point in range(11, 56, step_size)] 
    font_sizes = list(range(8, 22, 2))
    font_sizes = [8, 10, 24]

    pool_count = os.cpu_count() // 2
    pool_count = pool_count if pool_count > 1 else 1 
    total_img_list = []
    for font_name_sub_list in grouper(font_name_list, pool_count, fillvalue=None):
        font_name_sub_list = [font_name for font_name in font_name_sub_list if font_name is not None]
        pool_count = min(pool_count, len(font_name_sub_list))
        print(f"pool_count: {pool_count}")
        pool = Pool(pool_count)
        results = {font_name:pool.apply_async(make_fonts_dataset, args=
                                              (font_name, font_sizes, storage_dir, options)) 
                                              for font_name in font_name_sub_list }
        pool.close()
        pool.join()
        for font_name in font_name_sub_list:
            label_lines, korean_dict, font_img_list = results[font_name].get()
            font_label_list += label_lines
            font_dict_set = font_dict_set.union(korean_dict)
            total_img_list += font_img_list

    print("dataset size: ", len(font_label_list))
    print("save tar")
    tar_start = time.time()
    imgs2tar(total_img_list, 'font_data.tar.gz')
    print(f"tar save spent: {time.time() - tar_start}")
    label_name = 'rec_corpus_train.txt' if options["is_corpus_draw"] else 'rec_font_train.txt'

    write_font_label_file(label_name, font_label_list)

    with open("korean_dict.txt", "w", encoding="utf-8") as kor_dict_file:
        for e in sorted(font_dict_set):
            kor_dict_file.write(f"{e}\n")