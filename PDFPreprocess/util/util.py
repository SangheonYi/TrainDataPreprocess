import os
import time
from pathlib import Path

def create_directory(path):
    os.makedirs(path, exist_ok=True)
    
def create_directories(paths):
    for path in paths:
        os.makedirs(path, exist_ok=True)

def get_file_list(path):
    for root, dir, file_list in os.walk(path):
        return [Path(root) / file for file in file_list]
    print(f"check {path} directory. its empty.")

def logging_time(original_fn):
    def wrapper_fn(*args, **kwargs):
        start_time = time.time()
        result = original_fn(*args, **kwargs)
        end_time = time.time()
        print("WorkingTime[{}]: {} sec".format(original_fn.__name__, end_time-start_time))
        return result
    return wrapper_fn

def is_valid_rec_list(file_name):
    with open(file_name, 'r', encoding='utf-8') as data_file:
        for line in data_file:
            path, GT = line.split('\t')
            if not os.path.exists(path):
                print("not exist:", path)
                return False
    return True

def write_label(label_dir, label_list, label_name):
    os.makedirs(label_dir, exist_ok=True)
    label = ''.join(label_list)
    label_path = f'{label_dir}/{label_name}.txt'
    with open(label_path, 'w', encoding='utf-8') as label_file:
        label_file.write(label)