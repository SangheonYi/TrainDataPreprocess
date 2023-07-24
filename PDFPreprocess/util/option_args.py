import argparse
import os
from pprint import pprint
from pathlib import Path

def posix_path_to_str(path_arg):
    return str(Path(path_arg))

def init_args():
    storage_dir = "/mnt/d/train_data/pdf/"
    storage_dir = "C:/train_data/test/"
    storage_dir = "D:/train_data/pdf/"
    parser = argparse.ArgumentParser()

    # directories
    parser.add_argument("--label_dir", type=posix_path_to_str, default=f"{storage_dir}labels")
    parser.add_argument("--font_dir", type=posix_path_to_str, default="../font_data/fonts")

    # debug directries
    parser.add_argument("--pdf_converted_dir", type=posix_path_to_str, default=f"{storage_dir}/converted")
    parser.add_argument("--cropped_dir", type=posix_path_to_str, default=f"{storage_dir}/cropped")
    parser.add_argument("--boxed_dir", type=posix_path_to_str, default=f"{storage_dir}/boxed")
    # parser.add_argument("--pdf_dir", type=posix_path_to_str, default="C:/Exception/det_clean_file/issue")

    # crawling pdf directories
    # parser.add_argument("--boxed_dir", type=bool, default=False)
    # parser.add_argument("--pdf_converted_dir", type=posix_path_to_str, default=f"{storage_dir}/converted")
    # parser.add_argument("--cropped_dir", type=posix_path_to_str, default=f"{storage_dir}/cropped")
    parser.add_argument("--pdf_dir", type=posix_path_to_str, default="C:/Exception/det_clean_file/new_pdf")

    # corpus directories
    # parser.add_argument("--boxed_dir", type=bool, default=False)
    # parser.add_argument("--pdf_converted_dir", type=posix_path_to_str, default=f"{storage_dir}corpus_converted")
    # parser.add_argument("--cropped_dir", type=posix_path_to_str, default=f"{storage_dir}corpus_cropped")
    # parser.add_argument("--pdf_dir", type=posix_path_to_str, default="C:/Exception/det_clean_file/corpus_pdf")

    # eng eval directories
    # parser.add_argument("--boxed_dir", type=bool, default=False)
    # parser.add_argument("--pdf_converted_dir", type=posix_path_to_str, default=f"{storage_dir}eng_eval_converted")
    # parser.add_argument("--cropped_dir", type=posix_path_to_str, default=f"{storage_dir}eng_eval_cropped")
    # parser.add_argument("--pdf_dir", type=posix_path_to_str, default="C:/Exception/det_clean_file/issue")

    # pdf2img_option
    parser.add_argument("--fmt", type=str, default="png")
    parser.add_argument("--paths_only", type=bool, default=True)
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument("--thread_count", type=int, default=4)
    parser.add_argument("--dpi", type=int, default=200)
    parser.add_argument("--last_page", type=int, default=1)

    # convert and crop option
    parser.add_argument("--pdf2image_bool", type=bool, default=False)
    parser.add_argument("--dpi_random", type=bool, default=False)
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
        "timeout" : args.timeout,
        "thread_count" : args.thread_count,
        "dpi" : args.dpi,
        # "last_page" : args.last_page,
    }

if __name__ == '__main__':
    args = parse_args()
    pprint(dir(args))
    print(args['use_pdftocairo'])
    pprint(args.use_pdftocairo)