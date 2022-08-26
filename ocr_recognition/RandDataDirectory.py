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