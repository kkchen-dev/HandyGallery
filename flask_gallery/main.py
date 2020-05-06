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

port = 12345
portdb = 23456


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(16)

galleryDB = GalleryDB(host="localhost", port=portdb)


@app.route("/")
@app.route("/home")
def home():
    books = galleryDB.get_all_books()
    unread_books = galleryDB.get_books_by_wether_read(read=False)
    random.shuffle(unread_books)
    return render_template("home.html", 
                           title="Home Page",
                           books=unread_books[:5], 
                           total_length=len(books),
                           unread_length=len(unread_books),
                           allbooks=True,
                           read=False
                          )


@app.route("/gallery")
def gallery():
    return render_gallery("None", 1, 0)


@app.route("/gallery/<int:allbooks>.<int:read>.<string:tag>")
def render_gallery(tag, allbooks, read):
    if tag == "None":
        if allbooks:
            books = galleryDB.get_all_books()
        else:
            books = galleryDB.get_books_by_wether_read(read=read)
    else:
        if allbooks:
            books = galleryDB.get_books_bytag(tag)
        else:
            books = galleryDB.get_books_bytag(tag, bool(read))
    
    tagdict = galleryDB.get_all_tags(books)
    valcounts = [b for value in tagdict.values() for a, b in value]
    maxcount = max(valcounts) if len(valcounts) else 1
    return render_template("gallery.html", 
                           title="Gallery", 
                           books=books, 
                           tags=tagdict,
                           maxcount=maxcount,
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