import requests
import time
from random import random
import json


class PageNavigator:
    def __init__(self, headers_filename="headers.json"):
        self.current_url, self.headers = "", {}
        # self.delay, self.random_scale = 0.2, 0.2 # time.sleep(self.delay + random()*self.random_scale)
        with open(headers_filename) as f:
            self.headers = json.load(f)
    
    
    def follow_url(self, url, get_content=False):
        """ returns target page text """
        # time.sleep(self.delay + random() * self.random_scale)
        if url:
            page = requests.get(url, headers=self.headers)
            if page.status_code == 200:
                if get_content:
                    return page.content
                self.current_url = url
                return page.text
        return ""