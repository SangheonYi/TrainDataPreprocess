import argparse
import os
from pprint import pprint

def init_args():
    storage_dir = "/home/sayi/workspace/OCR/PaddleOCR/train_data/"
    parser = argparse.ArgumentParser()

    # directories
    parser.add_argument("--pdf_converted_dir", type=str, default=f'{storage_dir}converted')
    parser.add_argument("--label_dir", type=str, default=f'{storage_dir}labels')
    parser.add_argument("--cropped_dir", type=str, default=f'{storage_dir}cropped')
    # parser.add_argument("--boxed_dir", type=bool, default=False) # if False not save boxed image
    parser.add_argument("--boxed_dir", type=str, default=f'{storage_dir}boxed')
    # parser.add_argument("--pdf_dir", type=str, default=f'{storage_dir}pdf/papers')
    # parser.add_argument("--pdf_dir", type=str, default=f'{storage_dir}pdf/det_clean_pdf')
    parser.add_argument("--pdf_dir", type=str, default=f'{storage_dir}pdf/issue')

    # pdf2img_option
    parser.add_argument("--fmt", type=str, default="png")
    parser.add_argument("--paths_only", type=bool, default=True)
    parser.add_argument("--use_pdftocairo", type=bool, default=True)
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument("--thread_count", type=int, default=4)
    parser.add_argument("--last_page", type=int, default=1)

    # convert and crop option
    parser.add_argument("--pdf2image_bool", type=bool, default=True)
    parser.add_argument("--crop_line_bool", type=bool, default=False)
    parser.add_argument("--pool_count", type=int, default=os.cpu_count())
    
    return parser

def parse_args():
    parser = init_args()
    return parser.parse_args()

def get_pdf2img_option(args):
    return {
        "fmt" : args.fmt,
        "paths_only" : args.paths_only,
        "use_pdftocairo" : args.use_pdftocairo,
        "timeout" : args.timeout,
        "thread_count" : args.thread_count,
        # "last_page" : args.last_page,
    }

if __name__ == '__main__':
    args = parse_args()
    pprint(dir(args))
    print(args['use_pdftocairo'])
    pprint(args.use_pdftocairo)