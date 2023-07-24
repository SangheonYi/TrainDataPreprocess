from tarfile import TarFile, TarInfo
from io import BytesIO
from typing import List

def imgs2tar(
    images: List,
    dest_path: str,
    format: str = "png",
):
    with TarFile.open(dest_path, mode="w:gz") as tar:
        for image, img_path in images:
            f = BytesIO()
            image.save(f, format)
            f.seek(0)
            info = TarInfo(img_path)
            info.size = len(f.getbuffer())
            tar.addfile(info, fileobj=f)