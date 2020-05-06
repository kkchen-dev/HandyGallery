import json
import os
import datetime
from page_analyzer import *
from page_navigator import *
from file_io_handler import *


class ReaderGenerator:
    def __init__(self):
        self.tags = None
    
    def retrieve_img_pages(self, fileIOHandler):
        pageNavigator = PageNavigator()

        page, img_pages = fileIOHandler.get_start_page(), []
        start_page = int(fileIOHandler.get_first_page())
        final_page = int(fileIOHandler.get_final_page())

        process = ProcessBar(fileIOHandler.get_total_page(), "Gallery Pages")
        while len(img_pages) < fileIOHandler.get_total_page():
            galleryAnalyzer = GalleryAnalyzer(page)
            self.tags = galleryAnalyzer.tags
            for page_number, url in galleryAnalyzer.get_img_pages():
                if start_page <= page_number <= final_page: img_pages.append(url)
                elif page_number > final_page: break
            process.make_process_doc(len(img_pages))
            page = pageNavigator.follow_url(galleryAnalyzer.get_next_url())
            if not page: break
        return img_pages


    def generate_online_reader(self):
        fileIOHandler = FileIOHandler()
        fileIOHandler.online_file_output(self.retrieve_img_pages(fileIOHandler))


    def download_images(self, img_pages:list, file_path: str):
        pageNavigator = PageNavigator()
        if not os.path.exists(file_path): os.makedirs(file_path)
        process = ProcessBar(len(img_pages), "Image Pages")
        for i in range(len(img_pages)):
            page = pageNavigator.follow_url(img_pages[i])
            imgPageAnalyzer = ImgPageAnalyzer(page)
            imgDownloader = PageNavigator("headers_unenc.json")
            image = imgDownloader.follow_url(imgPageAnalyzer.get_img_url(), True)
            with open(f"{file_path}/{1+i}.jpg", 'wb') as f:
                f.write(image)
            process.make_process_doc(i+1)


    def generate_offline_reader(self):
        fileIOHandler = FileIOHandler()
        img_pages = self.retrieve_img_pages(fileIOHandler)
        file_path = fileIOHandler.get_output_path() + fileIOHandler.get_title()
        self.download_images(img_pages, file_path)
        fileIOHandler.offline_file_output(len(img_pages))


    def generate_data_folder(self):
        fileIOHandler = FileIOHandler()
        img_pages = self.retrieve_img_pages(fileIOHandler)
        file_path = fileIOHandler.get_output_path() + "METADATA " + fileIOHandler.get_title()
        self.download_images(img_pages, file_path)
        contents = []
        for i in range(len(img_pages)):
            with open(f"{file_path}/{1+i}.jpg", "rb") as f:
                contents.append(f.read())
        metadata = {
            "title": fileIOHandler.get_title(),
            "thumbnail": None,
            "tags": self.tags,
            "contents": [],
            "date_added": str(datetime.datetime.now()),
            "read": False
        }
        metadata_path = f"{file_path}/metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
        return metadata_path, contents





class ProcessBar:
    def __init__(self, total, title):
        self.process_bar_dir = ""
        with open("data.json") as f:
            self.process_bar_dir = os.path.expanduser(json.load(f)["process_bar"])
        self.total, self.current = total, 0
        self.prev_file, self.title = "", title


    def __del__(self):
        if self.prev_file and os.path.isfile(self.prev_file):
            os.remove(self.prev_file)


    def make_process_doc(self, curr):
        curr_file = self.process_bar_dir + f"{self.title} - {curr} out of {self.total} ({(curr * 100 / self.total):.2f}%).process"
        if not self.prev_file: open(curr_file, 'a')
        else: os.rename(self.prev_file, curr_file)
        self.current, self.prev_file = curr, curr_file