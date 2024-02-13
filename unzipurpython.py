import os
import zipfile

def move_and_unzip(zipfile_path):
    foldername = os.path.splitext(zipfile_path)[0]
    if os.path.exists(foldername) and os.path.isdir(foldername):
        os.rename(zipfile_path, os.path.join(foldername, zipfile_path))

        os.chdir(foldername)

        with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
            zip_ref.extractall()

        os.chdir('..')
    else:
        print("Error: Folder '{}' does not exist.".format(foldername))

files = os.listdir('.')

for file in files:
    if file.endswith(".zip"):
        move_and_unzip(file)
