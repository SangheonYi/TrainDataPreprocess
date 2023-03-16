from pathlib import Path

cropped = Path('cropped')
for dir_path in cropped.iterdir():
    if len([img for img in dir_path.iterdir()]) == 0:
        print(dir_path)
