import json
import os

def write_raw_txt(corpus_name, list_part, i):
    print(f'writing {i}th')
    with open(f'raw/{corpus_name}_raw{i}.txt', 'w', encoding='utf-8') as raw_text_file:
        for data in list_part:
            raw_text_file.write(data)

def make_for_pdf_corpus(corpus_file_name):
    # with open("sample.json", 'r', encoding='utf-8') as ori_file:
    corpus_name, extend = corpus_file_name.split('.')
    with open(corpus_file_name, 'r', encoding='utf-8') as ori_file:
        print("loading")
        os.makedirs('raw', exist_ok=True)
        cnt_per_dir = 50
        if extend == 'json':
            json_obj = json.load(ori_file)
            data_list = [f"{data['ko_original']}\n{data['en']}\n" for data in json_obj['data']]
        elif extend == 'txt':
            data_list = [line for line in ori_file]
        for i in range((len(data_list) // cnt_per_dir) + 1):
            write_raw_txt(corpus_name, data_list[i * cnt_per_dir : (i + 1) * cnt_per_dir], i)

corpus_file_names = ["tech_kor_en_train_set.json"]

for corpus_file_name in corpus_file_names:
    make_for_pdf_corpus(corpus_file_name)