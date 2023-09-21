from tarfile import TarFile, TarInfo
from io import BytesIO
from typing import List
from itertools import zip_longest
import argparse
from pathlib import Path
import os

def posix_path_to_str(path_arg):
    return str(Path(path_arg))

def get_args():
    parser = argparse.ArgumentParser()
    storage_dir = "/mnt/d/train_data/font_data/"
    os.makedirs(storage_dir, exist_ok=True)
    parser.add_argument("--storage_dir", type=posix_path_to_str, default=storage_dir)
    parser.add_argument("--tar_path", type=posix_path_to_str, default=f"{storage_dir}/font_data.tar.gz")

    # font config
    parser.add_argument("--font_name_list", type=list, default=['휴먼명조', 'Dotum', 'hy헤드라인m', 'Gungsuh', 'Batang', 'Gulim', 'HY견고딕'])
    # parser.add_argument("--font_name_list", type=list, default=['휴먼명조', 'Dotum'])
    # 8, 10, 24 fix sizes, 11, 22, 33, 44, 55 interval random sizes
    parser.add_argument("--font_sizes", type=list, default=reversed([8, 10, 24, 11, 22, 33, 44, 55]))
    # parser.add_argument("--font_sizes", type=list, default=[44, 55])
    # parser.add_argument("--font_sizes", type=list, default=[8, ])

    # option
    parser.add_argument("--is_corpus_draw", type=bool, default=False)
    parser.add_argument("--fix_font_size", type=bool, default=False)
    parser.add_argument("--ramdom_glyph_concat", type=bool, default=True)
    parser.add_argument("--word_count", type=int, default=180000)
    parser.add_argument("--pool_count", type=int, default=os.cpu_count())
    parser.add_argument("--save_img", type=bool, default=False)

    return parser.parse_args()

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def write_imgs2tar(
    images: List,
    dest_path: str,
):
    with TarFile.open(dest_path, mode="w:gz") as tar:
        for image, img_path in images:
            f = BytesIO()
            image.save(f, "png")
            f.seek(0)
            info = TarInfo(img_path)
            info.size = len(f.getbuffer())
            tar.addfile(info, fileobj=f)