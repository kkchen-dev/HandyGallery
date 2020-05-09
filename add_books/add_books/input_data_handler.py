import os
import json


class InputDataHandler:
    def __init__(self, path_to_books_folder: str, identifier: str):
        self.path_to_books_folder = path_to_books_folder
        self.metadata_dirs = []
        for fname in os.listdir(path_to_books_folder):
            full_path_to_f = os.path.join(path_to_books_folder, fname)
            split_fname = fname.split()
            if (fname[:len(identifier)] == identifier and 
                os.path.isdir(full_path_to_f) and
                len(split_fname) > 1 and
                split_fname[1].lower() != "template"
                ):
                self.metadata_dirs.append(full_path_to_f)
        print(f"Target Folders: {self.metadata_dirs}")


    def get_metadata_dirs(self):
        return self.metadata_dirs


    def check_jpgs(self, folder: str, jpgs: list):
        jpgsets = set(jpgs)
        max_jpg_num = 0
        for j in jpgs:
            jsplit = j.split(".")
            if len(jsplit) == 2 and jsplit[0].isdigit() and jsplit[1] == "jpg":
                jpgnum = int(jsplit[0])
                if jpgnum > max_jpg_num:
                    max_jpg_num = jpgnum

        missing_page_nums = []
        contents = []
        for i in range(1, max_jpg_num + 1):
            if f"{i}.jpg" in jpgsets:
                jpgsets.remove(f"{i}.jpg")
                with open(os.path.join(folder, f"{i}.jpg"), "rb") as f:
                    contents.append(f.read())
            else:
                missing_page_nums.append(f"{i}.jpg")
        if jpgsets:
            print(f"\033[33mUnused JPG Warning:\033[m Folder: \"{folder}\" has unused JPG files: {list(jpgsets)}")
        if missing_page_nums:
            print(f"\033[33mMissing JPG Warning:\033[m Folder: \"{folder}\" has potentially missing JPG files: {[f'{i}.jpg' for i in missing_page_nums]}")
        return contents


    def get_contents_from_metadata_dir(self, metadata_dir):
        files = os.listdir(metadata_dir)
        found_first_page = False
        found_metadata_json = False
        jpgs = []
        for f in files:
            if f[-4:] == ".jpg":
                jpgs.append(f)
                if f == "1.jpg":
                    found_first_page = True
            if f == "metadata.json":
                found_metadata_json = True
            if found_first_page and found_metadata_json:
                break
        else:
            if not found_first_page:
                print(f"\033[31mError:\033[m Folder: \"{metadata_dir}\" First jpg \"1.jpg\" is not found.")
            if not found_metadata_json:
                print(f"\033[31mError:\033[m Folder: \"{metadata_dir}\" The required file \"metadata.json\" is not found.")
            return []
        return self.check_jpgs(metadata_dir, jpgs)