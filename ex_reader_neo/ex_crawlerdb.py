import json

import pymongo
from pymongo import MongoClient
import gridfs

from reader_generator import ReaderGenerator


# Do the following steps in the terminal before executing this module.
# conda activate flask
# ../mongodb/bin/mongod --config ../mongodb/mongod.conf --fork


if __name__ == "__main__":
    readerGenerator = ReaderGenerator()
    metadata_path, contents = readerGenerator.generate_data_folder()
    try:
        maxSevSelDelay = 10 # seconds
        client = pymongo.MongoClient("localhost", port=27127,
                                    serverSelectionTimeoutMS=maxSevSelDelay)
        client.server_info()
    except:
        pass
    else:
        print("Connection Succeeded.")
        db = client["reader_database"]
        fs = gridfs.GridFS(db)

        books = db["book_collection"]
        tags = db["tag_collection"]
        with open(metadata_path) as f:
            book = json.load(f)
        
        if books.count_documents({"title": book["title"]}) > 0:
            print("Book Exists.")
        else:
            fsids = [str(fs.put(content)) for content in contents]
            book["thumbnail"] = fsids[0]
            book["contents"] = fsids
            book_id = books.insert_one(book).inserted_id

            for tagtype, booktags in book["tags"].items():
                for booktag in booktags:
                    if tags.count_documents({"tag": tagtype + booktag, "book_id": str(book_id)}) == 0:
                        tags.insert_one({"tag": tagtype + booktag, "book_id": str(book_id)})
        
