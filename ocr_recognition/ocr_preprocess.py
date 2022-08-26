import json
from RandDataDirectory import RandDataDirectory
from OriginData import OriginData
import time
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

# open json label and image. preprocess the opened image
def recognition_data_preprocess(origin_image_dir: str, done_image_dir: str, origin_label_path: str):
       with open(origin_label_path, "r") as origin_label_file:
        origin_label_json = json.load(origin_label_file)
        origin_data = OriginData(origin_label_json, origin_image_dir)
        if not origin_data.image:
            return
        # count = 0
        done_label_contents = []
        for annot_index, annotation in enumerate(origin_data.label_annotations):
            cropped_name = f"{origin_data.name}-{annot_index}.jpg"
            text, bbox = origin_data.parse_annotation(annotation)
            try:
                # crop image
                origin_data.image.crop(bbox).save(done_image_dir + cropped_name)
                # append new label
                done_label_contents.append(f"{done_image_dir.split('/')[1]}/{cropped_name}\t{text}\n")
            except Exception as e:
                print(e)
                print(f"fault {origin_data.name} at {text} for {cropped_name}")
                print(f"img save {done_image_dir}")
        #     if count > 10:
        #         break
        return done_label_contents

if __name__ == "__main__":
    task = "train" # val or train
    start = time.time()
    origin = RandDataDirectory("origin")
    done = RandDataDirectory("done")
    print("list time:", time.time() - start)
    start = time.time()
    with open(done.label_dir + "val_list.txt", "w") as done_label:
        new_label = []
        for i, origin_label in enumerate(origin.label_list):
            origin_label_path = origin_label["path"]
            new_label += recognition_data_preprocess(origin.image_dir[task], done.image_dir[task], origin_label_path)
            print_progress(i, len(origin.label_list))
            if i == 10:
                break
        done_label.write(''.join(new_label))
    print("process time", time.time() - start)