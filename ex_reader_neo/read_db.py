from pprint import pprint
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs

if __name__ == "__main__":
    try:
        maxSevSelDelay = 10 # seconds
        client = pymongo.MongoClient("localhost", port=27127,
                                    serverSelectionTimeoutMS=maxSevSelDelay)
        client.server_info()
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print(err)
    else:
        print("Connection Succeeded.")
        db = client["reader_database"]
        fs = gridfs.GridFS(db)
        books = db["book_collection"]
        # print(books.count_documents({"title":""}))
        for book in books.find():
            print(book)
        # for tag in db["tag_collection"].find({"tag": "artist:takku"}):
        #     print(tag)
        # print(fs.get(ObjectId(books.find_one()["contents"][1])).read())