import secrets
import random

from flask import Flask, render_template, flash, url_for, make_response
from forms import ToggleRead, SearchForm
from bson.objectid import ObjectId

from db_handler import GalleryDB

# WARNING!!!! THIS IS ONLY FOR DEVELOPMENT!!!!
# NO SECURITY PRACTICE!!!!
# Run this before starting the main.py program.
# <directory to mongodb>/mongodb/bin/mongod --config <directory to mongodb>/mongodb/mongod.conf --fork

port = 12345
hostdb="localhost"
portdb = 23456


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(16)

galleryDB = GalleryDB(host=hostdb, port=portdb)


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


@app.route("/gallery", methods=["GET", "POST"])
def gallery():
    return render_gallery(1, "None", 1, 0)


@app.route("/gallery/p<int:page>.<int:allbooks>.<int:read>.<string:tag>", methods=["GET", "POST"])
def render_gallery(page, tag, allbooks, read):
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
    total_pages = (len(books) - 1) // 25 + 1 if len(books) else 1
    if 0 <= (page - 1) * 25 < len(books):
        books = books[-1-(page-1)*25:-1-page*25:-1]
    else:
        books = []
    return render_template("gallery.html", 
                           title="Gallery", 
                           page=page, 
                           total_pages=total_pages,
                           books=books, 
                           tags=tagdict,
                           maxcount=maxcount,
                           allbooks=allbooks,
                           read=read
                        )


def build_key_phraseset(phrase):
    symbol_set = {"[", "]", "(", ")", ",", 
                  "?", ";", "{", "}", "-", 
                  "!", "@", "*", "$", "&", 
                  ":", "'", "\"", ".", "=", 
                  "<", ">", "/", "\\", "|",
                  "+", "`"," "}
    phraseset, curr_chars = set(), []
    for c in phrase:
        if curr_chars and c in symbol_set:
            phraseset.add("".join(curr_chars))
            curr_chars = []
        elif c not in symbol_set:
            curr_chars.append(c)
    if curr_chars:
        phraseset.add("".join(curr_chars))
    return phraseset


def title_found(book_title, search_phrases):
    if not search_phrases:
        return False
    title_phrases = build_key_phraseset(book_title)
    return not bool(search_phrases - title_phrases)


@app.route("/search", methods=["GET", "POST"])
def search_title():
    all_books = galleryDB.get_all_books()
    books = []
    form = SearchForm(csrf_enabled=False)
    if form.validate_on_submit():
        for book in all_books:
            if title_found(book["title"], build_key_phraseset(form.key_phrases.data)):
                books.append(book)
    # if form.errors:
    #     flash(form.errors, "danger")
    return render_template("search.html",
                            title="Book",
                            books=books,
                            form=form
                          )


@app.route("/book-<string:book_id>", methods=["GET", "POST"])
def bookpage(book_id):
    book = galleryDB.get_book_byid(ObjectId(book_id))
    form = ToggleRead(csrf_enabled=False)
    read = book["read"]
    if form.validate_on_submit():
        galleryDB.update_read(book, read)
        read = not read
    # if form.errors:
    #     flash(form.errors, "danger")
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
    app.run(debug=True, port=port)
    # app.run(port=port)