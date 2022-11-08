from generate_pdf import batch_convert_co2pdf, get_corpus_list
from os import cpu_count
from util.util import create_directories, get_file_list
from tqdm import tqdm 
from annotate_box import batch_convert_pdf2crop, write_labels
from itertools import product
import tempfile

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
    
    # set output directories
    det_rec_label_dict = {
        'det':'',
        'rec':''
    }

    # get font, size pdf
    pdf_names = [corpus_pdf_path.replace(f"{directories['pdf_dir']}/", '').replace('.pdf', '') 
    for corpus_pdf_path in get_file_list(directories['pdf_dir'])]

    # convert pdf -> images -> crop images & labels
    step = pool_count
    for pdf_idx in range(0, len(pdf_names), step):
        det_label, rec_label = batch_convert_pdf2crop(pool_count, pdf_names[pdf_idx:pdf_idx + step], pdf2image_bool=True, directories=directories)
        det_rec_label_dict['det'] = f"{det_rec_label_dict['det']}{det_label}"
        det_rec_label_dict['rec'] = f"{det_rec_label_dict['rec']}{rec_label}"
    write_labels(directories['label_dir'], det_rec_label_dict['det'], det_rec_label_dict['rec'], det_label_name='../det_train', rec_label_name='../rec_banila_train')

if __name__ == '__main__':
    pool_count = cpu_count()
    font_sizes = [8, 10, 14, 20, 24]
    font_names = ['NanumMyeongjoExtraBold.ttf', 'Dotum.ttf', 'hy_headline_m.ttf', 'Gungsuh.ttf', 'Batang.ttf', 'Gulim.ttf', ]
    font_config = list(product(font_names, font_sizes))
    # split corpus
    corpus_name = 'wind' # total 1281505, split line size 50
    corpus_count = 25631
    
    # corpus_name = 'kor_tech'
    # corpus_count = 125
    corpus_list = get_corpus_list(f'corpus/{corpus_name}.txt', corpus_count)
    step_size = 125
    corpus_range = range(0, corpus_count, step_size)
    for tmp_idx, interval_start in tqdm(enumerate(corpus_range), total=len(corpus_range)):
        with tempfile.TemporaryDirectory() as tempDir:
            directories = {
                'pdf_converted_dir':'converted',
                'boxed_dir': None,
                'cropped_dir':'cropped',
                'label_dir': 'labels',
                'pdf_dir': tempDir,
                'font_dir': 'font'
            }
            cor2crop(font_config, corpus_name, corpus_list[interval_start:interval_start + step_size], directories=directories, tmp_idx=tmp_idx)