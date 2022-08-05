import os

class DataDirectory():
    def __init__(self, category) -> None:
        self.category = category
        self.image_dir = category + "/images/"
        self.label_dir = category + "/labels/"
        self.image_list = self.get_file_list(self.image_dir)
        self.label_list = self.get_file_list(self.label_dir)

    def get_file_list(self, dir_path):
        file_list = os.listdir(dir_path)
        file_list.sort()
        return file_list