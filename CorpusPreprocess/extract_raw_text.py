import json
from tqdm import tqdm

with open("tech_kor_en_train_set.json", 'r', encoding='utf-8') as ori_file:
# with open("sample.json", 'r', encoding='utf-8') as ori_file:
    print('loading')
    json_obj = json.load(ori_file)
    data_list = json_obj['data']
    print('extracting')
    with open(f'raw_text.txt', 'w', encoding='utf-8') as raw_text_file:
        for data in tqdm(data_list):
            raw_text_file.write(f"{data['ko_original']}\n{data['en']}\n")