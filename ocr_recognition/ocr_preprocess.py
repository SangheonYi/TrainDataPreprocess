import json
from DataDirectory import OriginDirectory, DoneDirectory
from OriginData import OriginData
import time
import random
import os

KEYS = ["train", "val"]
current_progress = 0

def print_progress(i, list_len):
    global current_progress
    progress = round(i / list_len, 2) * 100
    if i % 100 == 0:
        print(f'{i} done')
    if progress % 5 == 0 and current_progress < progress: 
        current_progress = progress
        print(f'{progress}%')

# save crop image and record it's label in label_contents_dict
def image_preprocess(done_image_dir: str, origin_data: OriginData):
    label_contents_dict = { key:[] for key in KEYS}
    # count = 0
    for annot_index, annotation in enumerate(origin_data.label_annotations):
        key = random.choices(KEYS, weights=[0.3, 0.7])[0]
        cropped_name = f"{origin_data.name}-{annot_index}.jpg"
        text, bbox = origin_data.parse_annotation(annotation)
        try:
            # crop image
            origin_data.image.crop(bbox).save(done_image_dir + cropped_name)
            # append new label
            label_contents_dict[key].append(f"{done_image_dir.split('/')[1]}/{cropped_name}\t{text}\n")
        except Exception as e:
            print(e)
            print(f"fault {origin_data.name} at {text} for {cropped_name}")
            print(f"img save {done_image_dir}")
    return label_contents_dict
    #     if count > 10:
    #         break

# open json label and image. preprocess the opened image
def recognition_data_preprocess(origin: OriginDirectory, done_image_dir: str, origin_label_path: str, label_files: dict):
    with open(origin_label_path, "r") as origin_label_file:
        origin_label_json = json.load(origin_label_file)
        origin_data = OriginData(origin_label_json, origin.image_dir)
        if origin_data.image:
            label_contents_dict = image_preprocess(done_image_dir, origin_data)
            for key in KEYS:
                label_files[key].write("".join(label_contents_dict[key]))
                # print(len(label_contents_dict[key]))

if __name__ == "__main__":
    start = time.time()
    origin, done = OriginDirectory(), DoneDirectory()
    print("list time:", time.time() - start)
    start = time.time()
    with open("train_list.txt", "w") as train_label, open("val_list.txt", "w") as val_label:
        label_files = {
            "train":train_label,
            "val":val_label
        }
        for i, origin_label in enumerate(origin.label_list):
            # print(origin_label)
            origin_label_path = origin_label["path"]
            if not os.path.isfile(origin_label_path):
                print('not exist label:', origin_label_path)
                continue
            recognition_data_preprocess(origin, done.image_dir, origin_label_path, label_files)
            print_progress(i, origin.label_list_len)
            # if i == 0:
            #     break
    print("process time", time.time() - start)