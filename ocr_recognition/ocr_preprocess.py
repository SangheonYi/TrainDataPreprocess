import json
from PIL import Image
from DataDirectory import DataDirectory

def get_bbox(area: list):
    return (area[0], area[1], area[0] + area[2], area[1] + area[3])

def recognition_data_preprocess(origin: DataDirectory, file_name: str):
    new_labels = []
    with open(origin.get_origin_label(file_name), "r") as file:
        json_data = json.load(file)
        image = Image.open(origin.get_origin_image(file_name))
        for label in json_data["annotations"]:
            # crop image
            id = label["id"]
            cropped_name = f"{file_name}-{id}.jpg"
            bbox = get_bbox(label["annotation.bbox"])
            image.crop(bbox).save(done.image_dir + cropped_name)
            # append new label
            text = label["annotation.text"]
            new_labels.append(f"{cropped_name}\t{text}\n")
    return new_labels

if __name__ == "__main__":
    origin = DataDirectory("origin")
    done = DataDirectory("done")
    with open(done.label_dir + "label.txt", "w") as done_label:
        new_label = []
        for origin_label in origin.label_list:
            file_name = origin_label.split(".")[0]
            new_label += recognition_data_preprocess(origin, file_name)
        done_label.write(''.join(new_label))