from string import ascii_letters, digits, printable
from pprint import pprint

alpha_set = set(ascii_letters)
digit_set = set(digits)
punc_mark = set(printable) - alpha_set - digit_set

eng_gts = []
kor_gts = []
num_gts = []
alnum_gts = []
partial_alpha_gts = []

# with open('rec_corpus_train.txt', 'r', encoding='utf-8') as label_file:
with open('/mnt/d/train_data/pdf/labels/low_res_train.txt', 'r', encoding='utf-8') as label_file:

    for line_idx, line in enumerate(label_file):
        if 'font_data' in line:
            continue
        gt = line[:-1].split('\t')[1]
        gt_set = set(gt) - punc_mark
        if not gt_set - alpha_set:
            eng_gts.append(gt)
        elif not gt_set - digit_set:
            num_gts.append(gt)
        elif not (gt_set - alpha_set) - digit_set:
            alnum_gts.append(gt)
        elif gt_set & alpha_set:
            partial_alpha_gts.append(gt)
        else :
            kor_gts.append(gt)

    # pprint(eng_gts)
    # pprint(kor_gts)
    pprint(num_gts)
    tot_len = len(eng_gts) + len(num_gts) + len(alnum_gts) + len(partial_alpha_gts) + len(kor_gts)
    print(len(eng_gts), len(num_gts), len(alnum_gts), len(partial_alpha_gts), len(kor_gts))
    
    print(f"eng_gts: {len(eng_gts) / tot_len * 100}, num_gts: {len(num_gts) / tot_len * 100}, alnum_gts: {len(alnum_gts) / tot_len * 100}, partial_alpha_gts: {len(partial_alpha_gts) / tot_len * 100}, kor_gts: {len(kor_gts) / tot_len * 100}")