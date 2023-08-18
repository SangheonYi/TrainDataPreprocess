from multiprocessing import Queue
from tarfile import TarFile, TarInfo
from io import BytesIO

class DataCollector:
    def __init__(self, end_count, q):
        self.img_q = q
        self.end_count = end_count
    
    def write_data2tar(self, tar:TarFile, data:tuple):
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
                    img = self.img_q.get()
                    if isinstance(img, tuple):
                        self.write_data2tar(tar, img)
                    elif img == 'end':
                        self.end_count -= 1
                    else:
                        raise Exception(f"data error: data collector got: {img}, remain child count: {self.end_count}")