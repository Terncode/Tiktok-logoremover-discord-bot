import os
import shutil

FOLDER_NAME = "temp"
ACTUAL_DIR = "." + os.sep + FOLDER_NAME

def ensure_temp():
    if os.path.exists(ACTUAL_DIR) is False:
        os.mkdir(ACTUAL_DIR)

def create_temp_directory(name, clear):
    folder_name = ACTUAL_DIR + os.sep + name
    if clear is True and os.path.exists(folder_name):
        shutil.rmtree(folder_name)
    
    if os.path.exists(folder_name) is False:
        os.mkdir(folder_name)
    return folder_name

def remove_temp(name):
    folder_name = ACTUAL_DIR + os.sep + name
    if os.path.exists(folder_name) is False:
       shutil.rmtree(folder_name)


ensure_temp()


