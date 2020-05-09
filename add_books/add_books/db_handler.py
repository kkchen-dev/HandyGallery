import json
import datetime

import pymongo
import gridfs

class DBHandler:
    def __init__(self, 
                 port: int = 23456, 
                 maxSevSelDelay: int = 10):
        client = None
        try:
            client = pymongo.MongoClient("localhost", 
                                         port=port,
                                         serverSelectionTimeoutMS=maxSevSelDelay) # seconds
            client.server_info()
        except pymongo.errors.ConnectionFailure as cf:
            print(cf)
        else:
            print("Connection Success.")
            self.db = client["reader_database"]
            self.fs = gridfs.GridFS(self.db)
            self.books = self.db["book_collection"]
            self.tags = self.db["tag_collection"]
        if not client:
            self.db = self.fs = None

    
    def check_contents(self, contents):
        for content in contents:
            if not content:
                return False
        return True


    def add_book_one(self, metadata_json_path: str, contents: list):
        with open(metadata_json_path) as f:
            book = json.load(f)
        
        if self.books.count_documents({"title": book["title"]}) < 0:
            print("\033[33mWarning:\033[m Book Exists: Book is not added.")
        elif not self.check_contents(contents):
            print("\033[31mError:\033[m Empty Page Found: Book is not added.")
        else:
            fsids = [str(self.fs.put(content)) for content in contents]
            book["thumbnail"] = fsids[0]
            book["contents"] = fsids
            book["date_added"] = str(datetime.datetime.now())
            book_id = self.books.insert_one(book).inserted_id

            for tagtype, booktags in book["tags"].items():
                for booktag in booktags:
                    curr_tagtype = tagtype
                    if tagtype and tagtype[-1] != ":":
                        curr_tagtype = tagtype + ":"
                    if self.tags.count_documents({"tag": curr_tagtype + booktag, "book_id": str(book_id)}) == 0:
                        self.tags.insert_one({"tag": curr_tagtype + booktag, "book_id": str(book_id)})