import json
import os
from page_analyzer import *


class FileIOHandler:
    def __init__(self):
        self.first_gallery_page, filename, self.data, self.settings, download_path = "", "data.json", {}, {}, ""
        self.max_imgs_per_page = 160
        with open(filename) as f:
            self.data = json.load(f)
        self.settings_path = os.path.expanduser(self.data["settings"])
        with open(self.settings_path) as f:
            self.settings = json.load(f)
        
        self.first_img_page = self.settings["page_start"]
        download_path = os.path.expanduser(self.data["download_path"])
        self.first_file = download_path + str((int(self.first_img_page) - 1) // int(self.settings["imgs_per_page"]) + 1) + ".html"
        with open(self.first_file) as f:
            self.first_gallery_page = f.read()
        self.galleryAnalyzer = GalleryAnalyzer(self.first_gallery_page)

        self.last_img_page = self.galleryAnalyzer.get_total_img_count()
        if 0 < self.settings["page_end"] <= self.galleryAnalyzer.get_total_img_count():
            self.last_img_page = self.settings["page_end"]
        self.total_img_page = self.set_total_page(self.first_img_page, self.last_img_page)
        self.title = self.set_title()


    def __del__(self):
        os.remove(self.first_file)
        with open("default_settings.json") as default_settings_file:
            with open(self.settings_path, 'w') as settings_file:
                json.dump(json.load(default_settings_file), settings_file, indent=4)


    def set_total_page(self, first_img_page, last_img_page):
        total = last_img_page - first_img_page + 1
        return (total > 0) * total


    def set_title(self):
        if self.settings["title"]:
            title = html.unescape(self.settings["title"])
        else:
            jp_title = self.galleryAnalyzer.soup.find("h1", {"id": "gj"}).string
            en_title = self.galleryAnalyzer.soup.find("h1", {"id": "gn"}).string
            title = html.unescape(jp_title if jp_title else en_title)
        filename_restriction = set("/\\\:*?\"<>|")
        return "".join([c for c in title if c not in filename_restriction])


    def calculate_output_file_count(self, imgs_per_page, output_file_count):
        total_img_count = imgs_per_page
        while imgs_per_page > self.max_imgs_per_page:
            output_file_count += 1
            imgs_per_page = total_img_count // output_file_count
        return (imgs_per_page, output_file_count)



    def online_file_output(self, urls):
        output_html = []
        with open("output_html.json") as f:
            output_html = json.load(f)

        imgs_per_page, output_file_count = self.calculate_output_file_count(len(urls), 1)
        for i in range(output_file_count):
            curr_urls = urls[i*imgs_per_page:(i+1)*imgs_per_page]

            output_string = output_html[0]
            for j in range(len(curr_urls)):
                output_string += f"<a id=\"a{j}\" href=\"{curr_urls[j]}\"></a>"
            output_string += output_html[1] + str(len(curr_urls)) + output_html[2]
            filename = self.get_title() + " " + (output_file_count > 1) * chr(ord('A')+i)
            with open(os.path.expanduser(self.data["output_path"]) + filename + self.data["output_file_type"], 'w') as f:
                f.write(output_string)


    def offline_file_output(self, len_images):
        with open("reader.json") as f:
            output_html = json.load(f)
        
        imgs_per_page, output_file_count = self.calculate_output_file_count(len_images, 1)
        for i in range(output_file_count):
            output_string = output_html[0]
            for j in range(i*imgs_per_page, min((i+1)*imgs_per_page, len_images)):
                output_string += output_html[1] + str(j+1) + ".jpg" + output_html[2]
            output_string += output_html[3]
            with open(f"{self.get_output_path()}{self.get_title()}/{chr(ord('A')+i)}.htmll", 'w') as f:
                f.write(output_string)


    def get_start_page(self): return self.first_gallery_page
    def get_first_page(self): return self.first_img_page
    def get_final_page(self): return self.last_img_page
    def get_total_page(self): return self.total_img_page
    def get_output_path(self): return os.path.expanduser(self.data["output_path"])
    def get_title(self): return self.title