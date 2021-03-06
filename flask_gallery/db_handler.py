import collections
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs

class GalleryDB:
    def __init__(self, host="localhost", port=23456, maxSevSelDelay=10):
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
        return self.db["book_collection"].find_one({"_id": ObjectId(book_id)})


    def get_books_by_wether_read(self, read):
        return self.get_read_books() if read else self.get_unread_books()


    def get_unread_books(self):
        return [book for book in self.db["book_collection"].find({"read": False})]


    def get_read_books(self):
        return [book for book in self.db["book_collection"].find({"read": True})]

    
    def get_books_bytags(self, tags: list, read=None):
        book_ids = set()
        for tag in tags:
            temp_ids = set()
            for item in self.db["tag_collection"].find({"tag": tag}):
                temp_ids.add(item["book_id"])
            if not book_ids:
                book_ids.update(temp_ids)
            else:
                book_ids &= temp_ids
        
        books = []
        for book_id in book_ids:
            book = self.db["book_collection"].find_one(ObjectId(book_id))
            if book["read"] == read or read is None:
                books.append(self.db["book_collection"].find_one(ObjectId(book_id)))
        return books


    def delete_book(self, book_id):
        book = self.db["book_collection"].find_one(ObjectId(book_id))
        for page_id in book["contents"]:
            self.fs.delete(ObjectId(page_id))
        self.db["book_collection"].delete_one({"_id": ObjectId(book_id)})
        self.db["tag_collection"].delete_many({"book_id": book_id})


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


    def toggle_read(self, book, read):
        self.db["book_collection"].update_one(
            book, 
            {
                "$set": 
                {
                    "read": not read
                }
            }
        )