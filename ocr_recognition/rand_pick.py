import json
from RandDataDirectory import RandDataDirectory
from OriginData import OriginData
import time
import random
import os

current_progress = 0
def print_progress(i, list_len):
    global current_progress
    progress = round(i / list_len, 2) * 100
    if i % 100 == 0:
        print(f'{i} done')
    if progress % 5 == 0 and current_progress < progress: 
        current_progress = progress
        print(f'{progress}%')

def rand_key():
    rand_int = random.randint(1, 10)
    train_val = "train"
    if rand_int < 3:
        train_val = "val"
    return train_val

def image_preprocess(done_image_dirs: dict, origin_data: OriginData, label_contents_dict:dict):
    # count = 0
    for annot_index, annotation in enumerate(origin_data.label_annotations):
        key = rand_key()
        done_image_dir = done_image_dirs["train"]
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
    #     if count > 10:
    #         break

# open json label and image. preprocess the opened image
def recognition_data_preprocess(origin: RandDataDirectory, done_image_dirs: dict, origin_label_path: str, label_files: dict):
    with open(origin_label_path, "r") as origin_label_file:
        label_contents_dict = {
            "train":[],
            "val":[]
        }
        origin_label_json = json.load(origin_label_file)
        origin_data = OriginData(origin_label_json, origin.image_dir['val'])
        if not origin_data.image:
            return
        image_preprocess(done_image_dirs, origin_data, label_contents_dict)
        for key in label_files.keys():
            label_files[key].write("".join(label_contents_dict[key]))
            # print(len(label_contents_dict[key]))

if __name__ == "__main__":
    start = time.time()
    origin = RandDataDirectory("origin")
    done = RandDataDirectory("done")
    print("list time:", time.time() - start)
    start = time.time()
    with open(done.label_dir["train"] + "train_list.txt", "w") as train_label, open(done.label_dir["val"] + "val_list.txt", "w") as val_label:
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
            print_progress(i, len(origin.label_list))
            # if i == 0:
            #     break
    print("process time", time.time() - start)