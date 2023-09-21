from multiprocessing import Queue
from tarfile import TarFile, TarInfo
from io import BytesIO

class DataCollector:
    def __init__(self, end_count, q):
        self.img_q = q
        self.end_count = end_count
    
    def write_data2tar(self, tar:TarFile, data:list):
        if len(data) > 2:
            # save img on disk directly
            img, img_path, save_path = data
            img.save(save_path)
        else:
            img, img_path = data
        f = BytesIO()
        img.save(f, "png")
        f.seek(0)
        info = TarInfo(img_path)
        info.size = len(f.getbuffer())
        tar.addfile(info, fileobj=f)

    def collect(self, tar_path, mode):
        with TarFile.open(tar_path, mode=mode) as tar:
            while self.end_count > 0:
                while not self.img_q.empty():
                    data = self.img_q.get()
                    if isinstance(data, list):
                        self.write_data2tar(tar, data)
                    elif data == 'end':
                        self.end_count -= 1
                    else:
                        raise Exception(f"data error: data collector got: {data}, remain child count: {self.end_count}")