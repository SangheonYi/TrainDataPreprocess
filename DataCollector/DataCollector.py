from multiprocessing import Queue
from tarfile import TarFile, TarInfo
from io import BytesIO

class DataCollector:
    def __init__(self, q:Queue, target_processes:set):
        self.q = q
        self.target_processes = target_processes
    
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
            while not self.q.empty():
                data = self.q.get()
                if isinstance(data, tuple):
                    self.write_data2tar(tar, data)
                else:
                    try :
                        self.target_processes.remove(data)
                        print(f"remain target: {self.target_processes}")
                    except:
                        print(f"error: data collector got: {data}, remain target: {self.target_processes}")
                        exit()