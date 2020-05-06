import collections
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs

class GalleryDB:
    def __init__(self, host="localhost", port=27127, maxSevSelDelay=10):
        try:
            client = pymongo.MongoClient(host, 
                                         port=port,
                                         serverSelectionTimeoutMS=maxSevSelDelay
                                        )
            client.server_info()
        except:
            pass
        else:
            print("Connection Succeeded.")
        self.db = client["reader_database"]
        self.fs = gridfs.GridFS(self.db)


    def get_all_books(self):
        return [book for book in self.db["book_collection"].find()]


    def get_book_byid(self, book_id):
        return self.db["book_collection"].find_one({"_id": book_id})


    def get_unread_books(self):
        return [book for book in self.db["book_collection"].find({"read": False})]


    def get_read_books(self):
        return [book for book in self.db["book_collection"].find({"read": True})]


    def get_books_bytag(self, tag: str, read=None):
        books = []
        for item in self.db["tag_collection"].find({"tag": tag}):
            book = self.db["book_collection"].find_one(ObjectId(item["book_id"]))
            if book["read"] == read or read is None:
                books.append(self.db["book_collection"].find_one(ObjectId(item["book_id"])))
        return books


    def get_img(self, content_id):
        return self.fs.get(ObjectId(content_id)).read()


    def get_book_contents(self, content_ids: str):
        return [get_img(content_id) for content_id in content_ids]

    
    def get_all_tags(self, books=None):
        if books == None:
            tagset = set(tag["tag"] for tag in self.db["tag_collection"].find())
            tagcounter = collections.Counter(tag["tag"] for tag in self.db["tag_collection"].find())
        else:
            book_ids = set([str(book["_id"]) for book in books])
            tagset = set()
            tagcounter = collections.Counter()
            for tag in self.db["tag_collection"].find():
                if tag["book_id"] in book_ids:
                    tagset.add(tag["tag"])
                    tagcounter[tag["tag"]] += 1
        tagdict = collections.defaultdict(list)
        for tag in tagset:
            tagtype, tagvalue = tag.split(":")
            tagdict[tagtype].append((tagvalue, tagcounter[tag]))
        for key in tagdict:
            tagdict[key].sort()
        return tagdict


    def update_read(self, book, read):
        self.db["book_collection"].update_one(
            book, 
            {
                "$set": 
                {
                    "read": not read
                }
            }
        )