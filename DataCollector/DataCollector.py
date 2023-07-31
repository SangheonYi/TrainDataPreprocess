from multiprocessing import Queue
from tarfile import TarFile, TarInfo
from io import BytesIO

class DataCollector:
    def __init__(self, target_processes):
        self.img_q = Queue()
        self.target_processes = set(target_processes)
    
    def write_data2tar(self, tar:TarFile, data:tuple):
        img, img_path = data
        f = BytesIO()
        img.save(f, "png")
        f.seek(0)
        info = TarInfo(img_path)
        info.size = len(f.getbuffer())
        tar.addfile(info, fileobj=f)

    def collect(self, tar:TarFile):
        while self.target_processes:
            while not self.img_q.empty():
                img = self.img_q.get()
                if isinstance(img, tuple):
                    self.write_data2tar(tar, img)
                else:
                    try :
                        self.target_processes.remove(img)
                        print(f"remain target: {self.target_processes}")
                    except:
                        print(f"data error: data collector got: {img}, remain target: {self.target_processes}")
                        exit()