import os

def is_valid_rec_list(file_name):
    with open(file_name, 'r', encoding='utf-8') as data_file:
        for line in data_file:
            path, GT = line.split('\t')
            if not os.path.exists(path):
                print("not exist:", path)

files = ['admi_font_banila_train.txt', 'admi_val.txt']

for file in files:
    is_valid_rec_list(file)
