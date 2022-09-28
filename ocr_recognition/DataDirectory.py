import os

class OriginDirectory():
    def __init__(self) -> None:
        self.image_dir = f"origin/kor_rec/"
        self.label_dir = f"origin/labels/"
        self.label_list = self.list_all_files(self.label_dir, self.label_list, '.json')
        self.label_list_len = len(self.label_list)

    def list_all_files(self, rootdir, file_list, extend):
        extend_upper = extend.upper()
        for file in os.listdir(rootdir):
            joined_path = os.path.join(rootdir, file)
            if os.path.isdir(joined_path):
                self.list_all_files(joined_path, file_list, extend)
            elif file.endswith(extend) or file.endswith(extend_upper):
                file_list.append({
                    "path": joined_path,
                    "name": file.split(".")[0]
                })

class DoneDirectory():
    def __init__(self) -> None:
        self.image_dir = f"done/kor_rec/"
        self.createDirectory(self.image_dir)
    
    def createDirectory(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print("Error: Failed to create the directory.")