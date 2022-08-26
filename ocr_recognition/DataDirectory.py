import os
def list_all_files(rootdir, file_list, extend):
    extend_upper = extend.upper()
    for file in os.listdir(rootdir):
        joined_path = os.path.join(rootdir, file)
        if os.path.isdir(joined_path):
            list_all_files(joined_path, file_list, extend)
        elif file.endswith(extend) or file.endswith(extend_upper):
            file_list.append({
                "path": joined_path,
                "name": file.split(".")[0]
            })
            

class DataDirectory():
    def __init__(self, category, task) -> None:
        self.category = category
        self.image_dir = f"{category}/kor_rec_{task}/"
        self.label_dir = f"{category}/labels_{task}/"
        self.image_list = []
        self.label_list = []
        list_all_files(self.image_dir, self.image_list, '.jpg') # self.get_file_list(self.image_dir)
        list_all_files(self.label_dir, self.label_list, '.json') # self.get_file_list(self.label_dir)
