from generate_pdf import batch_convert_co2pdf, get_corpus_list
from util import get_file_list, is_valid_rec_list
from tqdm import tqdm 
from multi_level_bbox import batch_convert_pdf2crop, write_label
from itertools import product
import tempfile
from pathlib import Path
from option_args import parse_args

def cor2crop(args, font_config, corpus_name, corpus_list, tmp_idx=None):
    # generate tmp pdfs
    for corpus_idx, text in enumerate(corpus_list):
        # print(corpus_idx, text)
        corpus = {
        'idx': f"{tmp_idx}_{corpus_idx}",
        'text': text,
        'name': corpus_name
        }
        batch_convert_co2pdf(corpus, font_config, args)

    # get font, size pdf
    pdf_names = [Path(corpus_pdf_path).stem
    for corpus_pdf_path in get_file_list(args.pdf_dir)]

    # convert pdf -> images -> crop images & labels
    det_label_list = []
    rec_label_list = []
    step = args.pool_count
    for pdf_idx in range(0, len(pdf_names), step):
        pdf_names_sublist = pdf_names[pdf_idx:pdf_idx + step]
        det_label, det_section_label, rec_label = batch_convert_pdf2crop(pdf_names_sublist, args)
        rec_label_list.append(rec_label)
        det_label_list.append(det_label)
    write_label(args.label_dir, rec_label_list, 'rec_banila_train')
    write_label(args.label_dir, det_label_list, 'det_train')

if __name__ == '__main__':
    args = parse_args()
    font_sizes = [8, 10, 14, 20] # pt size
    font_sizes = [8]
    font_names = ['NanumMyeongjoExtraBold.ttf', 'Dotum.ttf', 'hy_headline_m.ttf', 'Gungsuh.ttf', 'Batang.ttf', 'Gulim.ttf', ]
    font_names = ['Dotum.ttf']
    font_names = ['Batang.ttf']
    font_config = list(product(font_names, font_sizes))
    print(font_config)
    # split corpus
    corpus_name = 'wind' # total 1281505, split line size 50
    corpus_count = 25631
    
    corpus_name = 'kor_tech'
    corpus_name = 'eng'
    corpus_count = 1
    corpus_list = get_corpus_list(f'corpus/{corpus_name}.txt', corpus_count)
    step_size = 125
    corpus_list = ["det test data"]
    corpus_range = range(0, corpus_count, step_size)
    for tmp_idx, interval_start in tqdm(enumerate(corpus_range), total=len(corpus_range)):
        with tempfile.TemporaryDirectory() as pdf_tmp_dir, tempfile.TemporaryDirectory() as conv_tmp_dir:
            cor2crop(args, font_config, corpus_name, corpus_list[interval_start:interval_start + step_size], tmp_idx=tmp_idx)
    if is_valid_rec_list(f"{args.label_dir}/rec_banila_train.txt"):
        print('😎 rec label is valid!💯')