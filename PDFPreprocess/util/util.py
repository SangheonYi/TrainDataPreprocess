import os
import time

def create_directory(path):
    if path:
        if not os.path.exists(path):
            os.makedirs(path)

def create_directories(paths):
    for path in paths:
        create_directory(path)
            

def get_file_list(path):
    for root, dir, file_list in os.walk(path):
        return [os.path.join(root, file) for file in file_list]

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