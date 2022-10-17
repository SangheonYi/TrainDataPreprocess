import os

dir_path = "pdf"
print(os.walk(dir_path))
for (root, directories, files) in os.walk(dir_path):
    print((root, directories, files))
    for file in files:
        file_path = os.path.join(root, file)
        print(file_path, os.path.basename(file_path), os.path.splitext(file_path))