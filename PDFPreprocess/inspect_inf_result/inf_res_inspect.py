from shutil import copyfile
from pathlib import Path
import sys
sys.path.append("..")
from util.util import create_directory

def source_copy(false_type, parent_path, file_name):
    create_directory(f"{false_type}/{parent_path}")
    copyfile(f"../{file_name}.png", f"{false_type}/{file_name}.png")

def print_log(idx, line_len, key, result, gt):
    print(f"progress: {idx}/{line_len} path: {key}.png")
    print(f"result len: {len(result)} gt len: {len(gt)}")
    print(f"result:\t{result}")
    print(f"gt:\t\t{gt}\n")

exclude_chr_list = ['/'] + list(map(chr, range(0x2160, 0x217F)))
with open('inf.log', 'r', encoding='utf-8') as log_file, open('rec_banila_train.txt', 'r', encoding='utf-8') as GT_file:
    lines = [line[:-1].split('.png:') for line in log_file.readlines()]
    gt_dict = dict()
    count_many_space = 0
    short_count = 0
    long_count = 0
    for gt_line in GT_file.readlines():
        k, v = gt_line.split('\t')
        gt_dict[k[:-4]] = v[:-1]
    for idx, line in enumerate(lines):
        key = line[0].split("Predicts of ")[1]
        result = line[1][2:].split(", 0.")[0][:-1]
        gt = gt_dict[key]
        if gt != result and gt not in exclude_chr_list:
            false_img_path = Path(key)
            if not false_img_path.parent.exists():
                create_directory(false_img_path.parent)
            copyfile(f"../{key}.png", f"{key}.png")
            print(f"progress: {idx}/{len(lines)} path: {key}.png")
            print(f"result len: {len(result)} gt len: {len(gt)}")
            print(f"result:\t{result}")
            print(f"gt:\t\t{gt}\n")

            if gt.count(' ') < result.count(' '):
                count_many_space += 1
                source_copy("space", false_img_path.parent, key)
            if len(gt) < len(result):
                long_count += 1
                source_copy("long", false_img_path.parent, key)
            if len(gt) > len(result):
                short_count += 1
                source_copy("short", false_img_path.parent, key)
                # print_log(idx, len(lines), key, result, gt)
    print(f"space many: {count_many_space}, long: {long_count}, short {short_count}")