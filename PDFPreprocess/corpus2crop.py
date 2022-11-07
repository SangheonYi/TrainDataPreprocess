from generate_pdf import batch_convert_co2pdf, get_corpus_list
from os import cpu_count
from util.util import create_directory, create_directories, get_file_list
from tqdm import tqdm 
from annotate_box import batch_convert_pdf2crop, write_labels
from itertools import product
import tempfile

if __name__ == '__main__':
    pool_count = cpu_count()
    font_sizes = [8, 10, 14, 20, 24]
    font_names = ['NanumMyeongjoExtraBold.ttf', 'Dotum.ttf', 'hy_headline_m.ttf', 'Gungsuh.ttf', 'Batang.ttf', 'Gulim.ttf', ]

    # split corpus
    corpus_name = 'wind'
    corpus_count = 25631
    # corpus_name = 'kor_tech'
    # corpus_count = 125
    corpus_list = get_corpus_list(f'corpus/{corpus_name}.txt', corpus_count)

    with tempfile.TemporaryDirectory() as tempDir:
        directories = {
            'pdf_converted_dir':tempDir,
            'boxed_dir': tempDir,
            'cropped_dir':'cropped',
            'label_dir': 'labels',
            'pdf_dir': tempDir,
            'font_dir': 'font'
        }

        # generate tmp pdfs
        for corpus_idx, text in tqdm(enumerate(corpus_list), total=len(corpus_list)):
            corpus = {
            'idx': corpus_idx,
            'text': text,
            'name': corpus_name
            }
            batch_convert_co2pdf(pool_count, corpus, product(font_names, font_sizes), directories=directories)

        ## convert and crop tmp pdfs
        
        # set output directories
        det_rec_label_dict = {
            'det':'',
            'rec':''
        }
        create_directories(directories.values())

        # get font, size pdf
        pdf_names = [corpus_pdf_path.replace(f"{directories['pdf_dir']}/", '').replace('.pdf', '') 
        for corpus_pdf_path in get_file_list(directories['pdf_dir'])]

        step = pool_count * 2
        for pdf_idx in range(0, len(pdf_names), step):
            det_label, rec_label = batch_convert_pdf2crop(pool_count, pdf_names[pdf_idx:pdf_idx + step], directories=directories)
            det_rec_label_dict['det'] = f"{det_rec_label_dict['det']}{det_label}"
            det_rec_label_dict['rec'] = f"{det_rec_label_dict['rec']}{rec_label}"
        write_labels(directories['label_dir'], det_rec_label_dict['det'], det_rec_label_dict['rec'])