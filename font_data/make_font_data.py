import os
import sys
sys.path.append("..")
from PIL import Image, ImageDraw, ImageFont
from multiprocessing import Pool, Process, Manager
from scipy.stats import loguniform
import random
import time
import traceback
from pathlib import Path

from util import get_valid_n_pair, get_corpus_words, get_args
from DataCollector import DataCollector
from OCRUnicodeRange import total_exclude_unicodes_list, won_dict, get_ttf_support_chars, write_font_label_file, exclude_range, convert_dict_list

def font_init(font_path, encoding, fix_font_size, font_size=10):
    if font_size not in [8, 10, 24] and not fix_font_size:
        font_size = sample_size(font_size, 11, (4, 5))
    encode_type = 'unic' if encoding.startswith("utf") else 'wans'
    font = ImageFont.truetype(font_path, size=font_size, encoding=encode_type)
    return font, font_size

def make_font_data(draw_list, font, img_q):
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

        # save image directly
        if (image, training_path) == None:
            print("😀", save_path, text_to_draw)
        img_data = [image, training_path]
        if config_args.save_img :
            img_data += save_path
        img_q.put(img_data)

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
        random_chars = random.choices(support_chars, k=random.randint(1,2))
    joined = ''.join(random_chars)
    to_draw_str = f"{target_char}{joined}"
    random_gt = to_draw_str.translate(won_dict[font_name])
    is_fault = won_dict[font_name].get(target_char, False)
    if is_fault and is_fault in random_gt:
        print(f"found fault at {font_name} in ❓{random_gt}❓")
    return to_draw_str, random_gt

def append_drawlist(draw_list, sub_label_lines, valid_gt, to_draw_str, save_path):
    global config_args
    save_path_posix = str(Path(save_path).as_posix())
    train_data_dir_idx = save_path_posix.find('train_data')
    training_path = save_path_posix[train_data_dir_idx:]
    sub_label_lines.append(f"{training_path}\t{valid_gt}\n")
    draw_list.append((to_draw_str, save_path, training_path))

def get_corpus_draw_list(valid_words, save_dir, font_name, label_lines):
    draw_list = []
    for idx, word in enumerate(valid_words):
        save_path = f'{save_dir}/{idx}.jpg'
        valid_gt = word.translate(won_dict[font_name])
        append_drawlist(draw_list, label_lines, valid_gt, word, save_path)
    return draw_list

def get_font_draw_list(support_chars, save_dir, font_name, label_lines):
    global config_args

    draw_list = []
    if config_args.save_img:
        os.makedirs(save_dir, exist_ok=True)
    for idx, target_char in enumerate(support_chars):
        char_code = ord(target_char)
        to_draw_str, random_gt = get_random_gt(target_char, support_chars, font_name, config_args.ramdom_glyph_concat)
        save_path = f'{save_dir}/{idx}_{char_code}.jpg'
        append_drawlist(draw_list, label_lines, random_gt, to_draw_str, save_path)
    return draw_list

def make_fonts_dataset(config_args, font_name, img_q):
    label_lines = []
    font_path = f"fonts/{font_name}.ttf"
    error_font_size = 0
    try:
        support_chars, encoding = get_ttf_support_chars(font_path, total_exclude_unicodes_list)
        print(f"{font_name} support size: {len(support_chars)}")
        if support_chars:
            if config_args.is_corpus_draw:
                start = time.time()
                global corpus_words
                tmp_support_chars = support_chars.copy()
                valid_words = get_valid_n_pair(corpus_words['kor'], config_args.word_count, tmp_support_chars)
                valid_words += get_valid_n_pair(corpus_words['eng'], config_args.word_count, tmp_support_chars)
                print(f"{font_name} get valid words spent:{time.time() - start}")

            for font_size in config_args.font_sizes:
                tmp_support_chars = support_chars.copy()
                font, init_font_size = font_init(font_path, encoding, config_args.fix_font_size, font_size=font_size)
                error_font_size = init_font_size
                if font.size < 11:
                    # exclude small cjk ideograph
                    tmp_support_chars = exclude_range(tmp_support_chars, 0x3300, 0x9FFF )
                save_dir = f"{config_args.storage_dir}/{font_name}_{init_font_size}_data"
                if config_args.is_corpus_draw:
                    save_dir = f'{save_dir}_corpus'
                if config_args.is_corpus_draw:
                    draw_list = get_corpus_draw_list(valid_words, save_dir, font_name, label_lines)
                else:
                    draw_list = get_font_draw_list(tmp_support_chars, save_dir, font_name, label_lines)
                start = time.time()
                # generate font data
                make_font_data(draw_list, font, img_q)
                print(f"draw spent: {time.time() - start}")
                print(f"font: {font_name}, font size: {init_font_size} done, q size: {img_q.qsize()}")
        else:
            print(f"{font_path} is empty")
    except Exception as e:
        print(f"{traceback.format_exc()}\nmake {font_name}_{error_font_size} dataset error: {e}")
    return label_lines, update_dict(support_chars, encoding)

def run_pool(config_args, pool_count, img_q, font_label_list, font_dict_set):
    results = dict()
    with Pool(pool_count) as pool:
        results = pool.starmap(make_fonts_dataset, [(config_args, font_name, img_q) for font_name in font_name_sub_list]) 
        for result in results:
            label_lines, korean_dict = result
            font_label_list += label_lines
            font_dict_set.update(korean_dict)

if __name__ == '__main__':
    config_args = get_args()
    dict_path = "korean_dict.txt"
    valid_char_set = set()
    if config_args.is_corpus_draw:
        corpus_words = get_corpus_words("../CorpusPreprocess/corpus/raw_text.txt")
        config_args.tar_path = config_args.tar_path[:-7] + '_corpus.tar.gz'

    font_label_list = []
    font_dict_set = set()
    pool_count = min(config_args.pool_count, len(config_args.font_name_list))
    if pool_count == os.cpu_count():
        pool_count -= 1 

    with Manager() as manager:
        img_q = manager.Queue(5000)
        sub_group_count = len(config_args.font_name_list) // pool_count
        if len(config_args.font_name_list) % pool_count > 0:
            sub_group_count += 1
        collector = DataCollector(sub_group_count, img_q)
        wirter_process = Process(target=collector.collect, args=(config_args.tar_path, 'w:gz'))
        wirter_process.start()
        print(f"pool count: {pool_count}")
        for sub_group_idx in range(sub_group_count):
            start_font_idx = sub_group_idx * pool_count
            font_name_sub_list = config_args.font_name_list[start_font_idx:start_font_idx + pool_count]
            pool_count = min(pool_count, len(font_name_sub_list))
            run_pool(config_args, pool_count, img_q, font_label_list, font_dict_set)
            img_q.put('end')
        print(f"dataset size: {len(font_label_list)}")
        print("data zipping")
        wirter_process.join()
    label_name = 'rec_corpus_train.txt' if config_args.is_corpus_draw else 'rec_font_train_8_15_range.txt'
    write_font_label_file(label_name, font_label_list)
    print(f"label saved: {label_name}")
    print(f"tar saved: {config_args.tar_path}")
    if not config_args.is_corpus_draw:
        with open(dict_path, "w", encoding="utf-8") as kor_dict_file:
            for inv_char_table in convert_dict_list:
                font_dict_set |= set(inv_char_table.values())
            kor_dict_file.write('\n'.join(sorted(list(font_dict_set))))