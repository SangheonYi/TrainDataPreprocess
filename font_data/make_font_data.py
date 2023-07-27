import os
import sys
sys.path.append("..")
from PIL import Image, ImageDraw, ImageFont
from multiprocessing import Pool, Queue, Process
from scipy.stats import loguniform
import random
import time
from tarfile import TarFile, TarInfo
from io import BytesIO

from util import get_random_words, corpus_lines, write_imgs2tar, grouper, get_args
from DataCollector import DataCollector
from OCRUnicodeRange import total_exclude_unicodes_list, won_dict, get_ttf_support_chars, write_font_label_file, exclude_range

def font_init(font_path, encoding, fix_font_size, font_size=10):
    if font_size not in [8, 10, 24] and not fix_font_size:
        font_size = sample_size(font_size, 11, (4, 5))
    encode_type = 'unic' if encoding.startswith("utf") else 'wans'
    font = ImageFont.truetype(font_path, size=font_size, encoding=encode_type)
    return font, font_size

def make_font_data(draw_list, font):
    global data_que

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
        # data_que.put((image, training_path))

def update_dict(support_chars, encoding):
    return set(support_chars) if encoding.startswith("utf") else set()

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
    global config_args

    training_path = save_path.replace(config_args.storage_dir, "")
    sub_label_lines.append(f"{training_path}\t{valid_gt}\n")
    draw_list.append((to_draw_str, save_path, training_path))

def get_draw_list(support_chars, save_dir, font_name, label_lines):
    global config_args

    draw_list = []
    os.makedirs(save_dir, exist_ok=True)
    if config_args.is_corpus_draw:
        for idx, word in enumerate(get_random_words(corpus_lines, config_args.k_size)):
            save_path = f'{save_dir}/{idx}.jpg'
            valid_gt = word.translate(won_dict[font_name])
            append_drawlist(draw_list, label_lines, valid_gt, word, save_path)
    else:
        for idx, target_char in enumerate(support_chars):
            char_code = ord(target_char)
            to_draw_str, random_gt = get_random_gt(target_char, support_chars, font_name, config_args.ramdom_glyph_concat)
            save_path = f'{save_dir}/{idx}_{char_code}.jpg'
            append_drawlist(draw_list, label_lines, random_gt, to_draw_str, save_path)
    return draw_list

def make_fonts_dataset(font_name):
    global config_args

    label_lines = []
    font_path = f"fonts/{font_name}.ttf"
    support_chars, encoding = get_ttf_support_chars(font_path, total_exclude_unicodes_list)
    print(f"{font_name} support size: {len(support_chars)}")
    if support_chars:
        for font_size in config_args.font_sizes:
            tmp_support_chars = support_chars.copy()
            font, font_size = font_init(font_path, encoding, config_args.fix_font_size, font_size=font_size)
            if font.size < 11:
                # exclude small cjk ideograph
                tmp_support_chars = exclude_range(tmp_support_chars, 0x3300, 0x9FFF )
            save_dir = f"{config_args.storage_dir}font_data_72/{font_name}_{font_size}_data"
            if config_args.is_corpus_draw:
                save_dir = f'{save_dir}_corpus'
            draw_list = get_draw_list(tmp_support_chars, save_dir, font_name, label_lines)
            # generate font data
            make_font_data(draw_list, font)
            print(f"font: {font_name}, font size: {font_size} done, spent: {time.time() - start}")
    else:
        print(f"{font_path} is empty")
    # data_que.put(font_name)
    return label_lines, update_dict(support_chars, encoding)

def run_collector(data_que):
    global config_args
    start = time.time()

    with TarFile.open(config_args.tar_path, mode="w:gz") as tar:
        collector = DataCollector(data_que, set(config_args.font_name_list))
        collector.collect(tar)
    print("write spent:", time.time() - start)

def run_pool(pool_count):
    pool = Pool(pool_count)
    results = dict()
    for font_name in font_name_sub_list:
        results[font_name] = pool.apply_async(make_fonts_dataset, args=(font_name, )) 
    pool.close()
    pool.join()
    return results

if __name__ == '__main__':
    config_args = get_args()
    data_que = Queue()
    font_label_list = []
    font_dict_set = set()
    pool_count = min(config_args.pool_count, len(config_args.font_name_list))
    if pool_count == os.cpu_count():
        pool_count -= 1 
    wirter_process = Process(target=run_collector, args=(data_que,))
    wirter_process.start()
    print(f"pool count: {pool_count}")
    for font_name_sub_list in grouper(config_args.font_name_list, pool_count, fillvalue=None):
        font_name_sub_list = [font_name for font_name in font_name_sub_list if font_name is not None]
        pool_count = min(pool_count, len(font_name_sub_list))
        results = run_pool(pool_count)
        for font_name in font_name_sub_list:
            label_lines, korean_dict = results[font_name].get()
            font_label_list += label_lines
            font_dict_set = font_dict_set.union(korean_dict)
    wirter_process.join()
    print("dataset size: ", len(font_label_list))
    label_name = 'rec_corpus_train.txt' if config_args.is_corpus_draw else 'rec_font_train.txt'
    write_font_label_file(label_name, font_label_list)
    with open("korean_dict.txt", "w", encoding="utf-8") as kor_dict_file:
        for e in sorted(font_dict_set):
            kor_dict_file.write(f"{e}\n")