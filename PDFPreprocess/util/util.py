import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_directories(paths):
    for path in paths:
        create_directory(path)

