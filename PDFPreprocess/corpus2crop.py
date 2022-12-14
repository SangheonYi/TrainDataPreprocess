from generate_pdf import batch_convert_co2pdf, get_corpus_list
from os import cpu_count
from util.util import create_directories, get_file_list, is_valid_rec_list
from tqdm import tqdm 
from annotate_box import batch_convert_pdf2crop, write_label
from itertools import product
import tempfile
from pathlib import Path

def cor2crop(font_config, corpus_name, corpus_list, directories={
    'pdf_converted_dir':'converted', 
    'boxed_dir':'boxed', 
    'cropped_dir':'cropped', 
    'label_dir': 'labels',
    'pdf_dir': 'corpus_pdf'
    },
    pool_count=cpu_count(),
    tmp_idx=None
    ):
    create_directories(directories.values())
    # generate tmp pdfs
    for corpus_idx, text in enumerate(corpus_list):
        # print(corpus_idx, text)
        corpus = {
        'idx': f"{tmp_idx}_{corpus_idx}",
        'text': text,
        'name': corpus_name
        }
        batch_convert_co2pdf(pool_count, corpus, font_config, directories=directories)

    ## convert and crop tmp pdfs
    
    # get font, size pdf
    pdf_names = [corpus_pdf_path.replace(f"{directories['pdf_dir']}/", '').replace('.pdf', '') 
    for corpus_pdf_path in get_file_list(directories['pdf_dir'])]

    # convert pdf -> images -> crop images & labels
    det_label_list = []
    rec_label_list = []
    step = pool_count
    for pdf_idx in range(0, len(pdf_names), step):
        det_label, rec_label = batch_convert_pdf2crop(pool_count, pdf_names[pdf_idx:pdf_idx + step], pdf2image_bool=True, directories=directories)
        rec_label_list.append(rec_label)
        det_label_list.append(det_label)
    write_label(directories['label_dir'], rec_label_list, 'rec_banila_train')
    write_label(directories['label_dir'], det_label_list, 'det_train')

    

if __name__ == '__main__':
    pool_count = cpu_count()
    font_sizes = [8, 10, 14, 20, 24]
    font_names = ['NanumMyeongjoExtraBold.ttf', 'Dotum.ttf', 'hy_headline_m.ttf', 'Gungsuh.ttf', 'Batang.ttf', 'Gulim.ttf', ]
    # font_names = ['Dotum.ttf']
    font_config = list(product(font_names, font_sizes))
    # split corpus
    corpus_name = 'wind' # total 1281505, split line size 50
    corpus_count = 25631
    
    corpus_name = 'kor_tech'
    corpus_count = 14
    corpus_list = get_corpus_list(f'corpus/{corpus_name}.txt', corpus_count)
    step_size = 125
    corpus_range = range(0, corpus_count, step_size)
    for tmp_idx, interval_start in tqdm(enumerate(corpus_range), total=len(corpus_range)):
        with tempfile.TemporaryDirectory() as pdf_tmp_dir, tempfile.TemporaryDirectory() as conv_tmp_dir:
            directories = {
                'pdf_converted_dir':conv_tmp_dir,
                'boxed_dir': None,
                'cropped_dir':'cropped',
                'label_dir': 'labels',
                'pdf_dir': pdf_tmp_dir,
                'font_dir': 'font'
            }
            cor2crop(font_config, corpus_name, corpus_list[interval_start:interval_start + step_size], directories=directories, tmp_idx=tmp_idx)
    if is_valid_rec_list(f"{directories['label_dir']}/rec_banila_train.txt"):
        print('???? label is valid!????')