import os
from DataDirectory import list_all_files

class RandDataDirectory():
    def __init__(self, state) -> None:
        self.state = state
        self.image_dir = {}
        self.label_dir = {}
        self.label_list = []
        for key in ["val", "train"]:
            self.image_dir[key] = f"{state}/kor_rec_{key}/"
            self.label_dir[key] = f"{state}/labels_{key}/"
            self.createDirectory(self.image_dir[key])
            self.createDirectory(self.label_dir[key])
            list_all_files(self.label_dir[key], self.label_list, '.json')
    
    def createDirectory(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print("Error: Failed to create the directory.")