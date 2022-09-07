
font_list = ['휴먼명조', 'Dotum-03', 'hy헤드라인m', 'GNGT(견고딕)']
Dotum_range = [range(0x0), range(0xa0), range(0x115a, 0x1160), range(0x11a3, 0x11a7), range(0x3000), range(0x3164), range(0xfffc)]
GNGT_range = [range(0x0, 0x1f), range(0x7f, 0xff), range(0xa4d4, 0xa4fe), range(0x10000)]
hyheadline_range = [range(0x0, 0xff), range(0xa4d4, 0xa4fe), range(0x10000)]

# int(0xffff) -> 65535

import cv2
import numpy as np
import os
import time

EMPTY_IMG = {255}

def list_all_files(rootdir, extend):
    if os.path.isdir(rootdir):
        return [
            {
                "path": ''.join([rootdir, file]),
                "name": file.split(".")[0]
            }
            for file in os.listdir(rootdir) if file.endswith(extend)
        ]

def is_empty_char(img_path):
    with open(img_path, 'rb') as f:
        data = f.read()
    encoded_img = np.frombuffer(data, dtype = np.uint8)
    img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    reduced_set = set(img.flatten())
    return reduced_set == EMPTY_IMG

def remove_empty_img(img_path):
    if os.path.isfile(img_path) and is_empty_char(img_path):
        os.remove(img_path)

def get_empty_list(img_dir_path):
    file_list = list_all_files(img_dir_path, '.png')
    return [file['path'] for file in file_list if is_empty_char(file)]

def get_empty_list(img_dir_path):
    file_list = []
    if os.path.isdir(img_dir_path):
        for file in os.listdir(img_dir_path): 
            img_path = ''.join([img_dir_path, file])
            name = file.split('.')[0]
            if is_empty_char(img_path) and name != '32':
                file_list.append(img_path)
    return file_list

font_list = ['휴먼명조', 'Dotum-03', 'hy헤드라인m', 'GNGT(견고딕)']
root_dir = '/mnt/d/'
start = time.time()

for dir_name in font_list:
    img_dir_path = f'{root_dir}{dir_name}/'
    print(get_empty_list(img_dir_path))
print("spent:", time.time() - start)