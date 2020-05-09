import os

from add_books.input_data_handler import InputDataHandler
from add_books.db_handler import DBHandler


if __name__ == "__main__":
    db_handler = DBHandler(port=23456)
    input_handler = InputDataHandler(
                        os.path.join(os.path.dirname(__file__), "books"),
                        "METADATA"
                    )
    for metadata_dir in input_handler.get_metadata_dirs():
        db_handler.add_book_one(
            os.path.join(metadata_dir, "metadata.json"),
            input_handler.get_contents_from_metadata_dir(metadata_dir)
        )