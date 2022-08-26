import os
from PIL import Image

class OriginData():
    def __init__(self, label_json, image_dir) -> None:
        self.label = label_json
        self.label_annotations = label_json["annotations"]
        self.image_meta = label_json["images"][0]
        self.name = self.image_meta["image.file.name"][:-4]
        self.image = self.open_image(image_dir)
        pass

    def open_image(self, image_dir):
        key_list = ['image.category', 'image.make.code', 'image.make.year', 'image.file.name']
        path_parts = list(map(lambda key: self.image_meta[key], key_list))
        image_path = image_dir + '/'.join(path_parts)
        if not os.path.isfile(image_path):
            print('not exist image:', image_path)
            return False
        return Image.open(image_path)

    def parse_annotation(self, annotation):
        area = annotation["annotation.bbox"]
        text = annotation["annotation.text"]
        return text, (area[0], area[1], area[0] + area[2], area[1] + area[3])
