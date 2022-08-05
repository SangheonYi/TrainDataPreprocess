from io import TextIOWrapper
from itertools import product
import json
from PIL import Image
from DataDirectory import DataDirectory
# import PIL

# im1 = Image.open(f"flower1.jpg")
# im1 = im1.save("geeks.jpg")
    
def json_to_label(origin: DataDirectory, label_file: str, output_file: TextIOWrapper):
    with open(origin.label_dir + label_file, "r") as file:
        json_data = json.load(file)
        annotation_list = json_data["annotations"]
        for label in annotation_list:
            id = label["id"]
            text = label["annotation.text"]
            output_file.write(f"{label_file}-{id}.jpg\t{text}\n")

if __name__ == "__main__":
    origin = DataDirectory("origin")
    done = DataDirectory("done")
    with open(done.label_dir + "label.txt", "w") as done_label:
        for origin_label in origin.label_list:
            json_to_label(origin, origin_label, done_label)