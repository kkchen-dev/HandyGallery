from datetime import datetime
import secrets

from flask import Flask, render_template, url_for, make_response
from forms import ToggleRead
from bson.objectid import ObjectId

from db_handler import GalleryDB

# WARNING!!!! THIS IS ONLY FOR DEVELOPMENT!!!!
# NO SECURITY PRACTICE!!!!
# Run this before starting the main.py program.
# <directory to mongodb>/mongodb/bin/mongod --config <directory to mongodb>/mongodb/mongod.conf --fork

port = 9937
portdb = 27127


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(16)

galleryDB = GalleryDB(host="localhost", port=portdb)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home Page")


@app.route("/gallery")
def gallery():
    books = galleryDB.get_all_books()
    return render_template("gallery.html", 
                           title="Gallery", 
                           books=books, 
                           tags=galleryDB.get_all_tags(),
                           allbooks=True,
                           read=False
                        )


@app.route("/gallery-read")
def gallery_read():
    books = galleryDB.get_read_books()
    return render_template("gallery.html", 
                           title="Gallery", 
                           books=books, 
                           tags=galleryDB.get_all_tags(books),
                           allbooks=False,
                           read=True
                        )


@app.route("/gallery-unread")
def gallery_unread():
    books = galleryDB.get_unread_books()
    return render_template("gallery.html", 
                           title="Gallery", 
                           books=books, 
                           tags=galleryDB.get_all_tags(books),
                           allbooks=False,
                           read=False
                        )


@app.route("/gallery-<string:tag>/<int:allbooks><int:read>")
def tagged_gallery(tag, allbooks, read):
    # print(f"{tag=}, {allbooks=}, {read=}")
    if allbooks:
        books = galleryDB.get_books_bytag(tag)
    else:
        books = galleryDB.get_books_bytag(tag, bool(read))
    return render_template("gallery.html", 
                           title="Gallery", 
                           books=books, 
                           tags=galleryDB.get_all_tags(),
                           allbooks=allbooks,
                           read=read
                        )


@app.route("/book-<string:book_id>", methods=["GET", "POST"])
def bookpage(book_id):
    book = galleryDB.get_book_byid(ObjectId(book_id))
    form = ToggleRead(csrf_enabled=False)
    read = book["read"]
    if form.validate_on_submit():
        galleryDB.update_read(book, read)
        read = not read
    # print(form.errors)
    return render_template("book.html",
                            title="Book",
                            imgs=book["contents"],
                            tags=book["tags"],
                            read=read,
                            form=form
                          )


@app.route('/images/<string:pid>.jpg')
def get_image(pid):
    response = make_response(galleryDB.get_img(pid))
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename=f'{pid}.jpg')
    return response


if __name__ == "__main__":
    # app.run(debug=True, port=port)
    app.run(port=port)