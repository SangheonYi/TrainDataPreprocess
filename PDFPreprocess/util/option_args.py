import argparse
import os
import platform
from pprint import pprint
from pathlib import Path

def posix_path_to_str(path_arg):
    return str(Path(path_arg))

def init_args():
    
    if platform.system() == 'Linux':
        storage_dir = "/home/sayi/workspace/OCR/PaddleOCR/train_data/pdf/"
        storage_dir = "/mnt/d/train_data/pdf/"
        pdf_root = "/mnt/c/Exception/"
    else:
        storage_dir = "C:/train_data/test/"
        storage_dir = "D:/train_data/pdf/"
        pdf_root = "C:/Exception/"
    parser = argparse.ArgumentParser()

    # paths
    parser.add_argument("--label_dir", type=posix_path_to_str, default=f"{storage_dir}labels")
    parser.add_argument("--font_dir", type=posix_path_to_str, default="../font_data/fonts")
    parser.add_argument("--tar_path", type=posix_path_to_str, default=f"{storage_dir}eng_pdf.tar.gz")

    # debug paths
    # parser.add_argument("--boxed_dir", type=posix_path_to_str, default=f"{storage_dir}/issue/boxed")
    # parser.add_argument("--pdf_converted_dir", type=posix_path_to_str, default=f"{storage_dir}/issue/converted")
    # parser.add_argument("--cropped_dir", type=posix_path_to_str, default=f"{storage_dir}/issue/cropped")
    # parser.add_argument("--pdf_dir", type=posix_path_to_str, default=f"{pdf_root}det_clean_file/issue")

    # debug paths
    # parser.add_argument("--boxed_dir", type=posix_path_to_str, default=f"{storage_dir}/boxed")
    # parser.add_argument("--pdf_converted_dir", type=posix_path_to_str, default=f"{storage_dir}/converted")
    # parser.add_argument("--cropped_dir", type=posix_path_to_str, default=f"{storage_dir}/cropped")
    # parser.add_argument("--pdf_dir", type=posix_path_to_str, default=f"{pdf_root}det_clean_file/pdf_files")

    # crawling pdf paths
    # parser.add_argument("--boxed_dir", type=posix_path_to_str, default=f"{storage_dir}/2l_boxed")
    # parser.add_argument("--pdf_converted_dir", type=posix_path_to_str, default=f"{storage_dir}/2l_converted")
    # parser.add_argument("--cropped_dir", type=posix_path_to_str, default=f"{storage_dir}/2l_cropped")
    # parser.add_argument("--pdf_dir", type=posix_path_to_str, default=f"{pdf_root}det_clean_file/pdf_files")

    # eng pdf paths
    # parser.add_argument("--boxed_dir", type=bool, default=False)
    # parser.add_argument("--pdf_converted_dir", type=posix_path_to_str, default=f"{storage_dir}eng_pdf_converted")
    # parser.add_argument("--cropped_dir", type=posix_path_to_str, default=f"{storage_dir}eng_pdf_cropped")
    # parser.add_argument("--pdf_dir", type=posix_path_to_str, default=f"{pdf_root}det_clean_file/eng_pdf")

    # eng eval paths
    # parser.add_argument("--boxed_dir", type=bool, default=False)
    # parser.add_argument("--pdf_converted_dir", type=posix_path_to_str, default=f"{storage_dir}eng_eval_converted")
    # parser.add_argument("--cropped_dir", type=posix_path_to_str, default=f"{storage_dir}eng_eval_cropped")
    # parser.add_argument("--pdf_dir", type=posix_path_to_str, default=f"{pdf_root}det_clean_file/issue")

    # kor eval paths
    # parser.add_argument("--boxed_dir", type=bool, default=False)
    # parser.add_argument("--pdf_converted_dir", type=posix_path_to_str, default=f"{storage_dir}kor_eval_converted")
    # parser.add_argument("--cropped_dir", type=posix_path_to_str, default=f"{storage_dir}kor_eval_cropped")
    # parser.add_argument("--pdf_dir", type=posix_path_to_str, default=f"{pdf_root}det_clean_file/issue")

    # space eval
    parser.add_argument("--boxed_dir", type=bool, default=False)
    parser.add_argument("--pdf_converted_dir", type=posix_path_to_str, default=f"{storage_dir}space_eval_converted")
    parser.add_argument("--cropped_dir", type=posix_path_to_str, default=f"{storage_dir}space_eval_cropped")
    parser.add_argument("--pdf_dir", type=posix_path_to_str, default=f"{pdf_root}det_clean_file/space_eval")

    # pdf2img_option
    parser.add_argument("--fmt", type=str, default="png")
    parser.add_argument("--paths_only", type=bool, default=True)
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument("--thread_count", type=int, default=4)
    parser.add_argument("--dpi", type=int, default=200)
    # page 옵션은 되도록 지양할 것, 이미지 생성 장수랑 pdf page 동기화 안되서 터질 수 있다.
    # 수정했으면 이전 생성 데이터 싹 지우고 다시 생성할 것.
    # parser.add_argument("--first_page", type=int, default=3) 
    parser.add_argument("--last_page", type=int, default=1)

    # convert and crop option
    parser.add_argument("--pdf2image_bool", type=bool, default=True)
    parser.add_argument("--crop_image_save", type=bool, default=True) # write_tarball must be true to work.
    parser.add_argument("--bbox_image_save", type=bool, default=False)
    parser.add_argument("--write_tarball", type=bool, default=True)
    parser.add_argument("--dpi_random", type=bool, default=False)
    parser.add_argument("--crop_line_bool", type=bool, default=True)
    parser.add_argument("--merge_bbox", type=bool, default=False)
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
        # "first_page" : args.first_page,
        # "last_page" : args.last_page,
    }

if __name__ == '__main__':
    args = parse_args()
    pprint(dir(args))
    print(args['use_pdftocairo'])
    pprint(args.use_pdftocairo)