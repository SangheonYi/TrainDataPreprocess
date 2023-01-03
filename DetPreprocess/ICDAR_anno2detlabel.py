import json
import cv2
from pathlib import Path
import numpy as np


datasets = 'datasets/total_text'
data_dir = Path('icdar2019')
train_image_dir = 'train_images'

def draw_polygons():
    count = 0
    with open(data_dir / "art_labels.json", "r") as ori_file, open(f"{datasets}/train.txt", "w") as det_file, open(f"{datasets}/train_list.txt", "w") as det_file_list:
        ori_json = json.load(ori_file)
        for k, gts in ori_json.items():
            img_path = data_dir / f'{train_image_dir}/{k}.jpg' 
            # print(img_path, img_path.exists())
            train_img_name = f"lined_{k}.jpg"
            img = cv2.imread(str(img_path), cv2.IMREAD_COLOR).astype('float32')
            with open(f"{datasets}/train_gts/{train_img_name}.txt", "w") as img_label_gt, open(f"{datasets}/train_gts/lined_{k}.gt", "w") as img_label_txt:
                for gt in gts:
                    if gt['transcription'] != '###':
                        point =  np.array(gt["points"])
                        img = cv2.polylines(img, [point], True, (0, 255, 0), 2) 
                        det_file.write(f'{train_img_name}\n')
                        det_file_list.write(f'{train_img_name}\n')
                        converted_gt = ''
                        for coor in point:
                            converted_gt += f"{coor[0]},{coor[1]},"
                        img_label_gt.write(f"{converted_gt}0\n")
                        img_label_txt.write(f"{converted_gt}0\n")
            cv2.imwrite(f'{datasets}/{train_image_dir}/{train_img_name}', img)
            # count += 1
            # if count > 10:
            #     return

draw_polygons()