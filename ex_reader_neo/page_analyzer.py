import collections
import re
import html
from bs4 import BeautifulSoup
from collections import namedtuple

class PageAnalyzer:
    def __init__(self, page: str):
        """Takes in an html page string and get the key elements."""
        self.soup = BeautifulSoup(page, 'html.parser')
        self.prev_url, self.next_url = "", ""
        self.generate_urls()


    def generate_urls(self): raise NotImplementedError
    def get_prev_url(self): raise NotImplementedError
    def get_next_url(self): raise NotImplementedError
    def new_soup(self, page): self.soup = BeautifulSoup(page, 'html.parser')



class GalleryAnalyzer(PageAnalyzer):
    def generate_urls(self):
        IMGPage = namedtuple('IMGPage', ['page_num', 'url'])
        self.img_pages = [IMGPage(int(img_page.find("img")["alt"]), img_page.find("a")["href"]) for img_page in self.soup.find_all("div", {"class": "gdtl"})]
        # print(self.img_pages)

        img_count_string = self.soup.find("p", {"class": "gpc"}).string.split()
        self.total_img_count = int("".join(img_count_string[-2].split(",")))

        buttons = self.soup.find("table", {"class": "ptt"}).find("tr").contents
        self.prev_url = buttons[0].find("a")["href"] if buttons[0].find("a") else ""
        self.next_url = buttons[-1].find("a")["href"] if buttons[-1].find("a") else ""
        self.total_gallery_page_count = int(buttons[-2].string)
        self.tags = self.get_tags()




    def get_tags(self):
        tags = collections.defaultdict(list)
        tag_rows = self.soup.find("div", {"id": "taglist"}).find_all("tr")
        for tag_row in tag_rows:
            key, values = tag_row.find_all("td")
            tags[key.string] = [item.string for item in values.find_all("div")]
        return tags


    def get_prev_url(self): return self.prev_url
    def get_next_url(self): return self.next_url
    def get_img_pages(self): return self.img_pages
    def get_total_img_count(self): return self.total_img_count
    def get_total_gallery_page_count(self): return self.total_gallery_page_count



class ImgPageAnalyzer(PageAnalyzer):
    def generate_urls(self):
        self.prev_url = self.soup.find("a", {"id": "prev"})["href"]
        self.next_url = self.soup.find("a", {"id": "next"})["href"]
        self.img_url = self.soup.find("img", {"id": "img"})["src"]


    def get_prev_url(self): return self.prev
    def get_next_url(self): return self.next
    def get_img_url(self): return self.img_url
