import secrets
import random

from flask import Flask, render_template, redirect, flash, url_for, make_response
from forms import SearchForm, BookDeletion

from db_handler import GalleryDB
import local_search

# WARNING!!!! THIS IS ONLY FOR DEVELOPMENT!!!!
# NO SECURITY PRACTICE!!!!
# Run this before starting the main.py program.
# <directory to mongodb>/mongodb/bin/mongod --config <directory to mongodb>/mongodb/mongod.conf --fork

db_host="localhost"
db_port = 23456
flask_port = 12345
debug = False


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(16)

galleryDB = GalleryDB(host=db_host, port=db_port)


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
    return render_gallery(1, "None", 1, 0)


@app.route("/gallery/p<int:page>.<int:allbooks>.<int:read>.<string:tag>")
def render_gallery(page, tag, allbooks, read):
    split_tag = tag.split("+")
    if len(set(split_tag)) < len(split_tag):
        tag = "+".join(list(set(split_tag)))
        return redirect(url_for("render_gallery", page=page, tag=tag, allbooks=allbooks, read=read))
    
    if tag == "None":
        tag = ""
        if allbooks:
            books = galleryDB.get_all_books()
        else:
            books = galleryDB.get_books_by_wether_read(read=read)
    else:
        if allbooks:
            books = galleryDB.get_books_bytags(split_tag)
        else:
            books = galleryDB.get_books_bytags(split_tag, bool(read))
    
    tagdict = galleryDB.get_all_tags(books)
    valcounts = sorted([b for value in tagdict.values() for a, b in value])
    maxcounts = [1, 1, 1, 1]
    maxcounts_length = len(maxcounts)
    valcounts_length = len(valcounts)
    if valcounts_length:
        for i in range(maxcounts_length):
            maxcounts[i] = valcounts[-1] * (i+1) // maxcounts_length
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
                           tagtypes=sorted(list(tagdict.keys())),
                           tagdict=tagdict,
                           selected_tag=tag,
                           maxcounts=maxcounts,
                           allbooks=allbooks,
                           read=read
                        )


@app.route("/search", methods=["GET", "POST"])
def search_title():
    all_books = galleryDB.get_all_books()
    books = []
    form = SearchForm(csrf_enabled=False)
    if form.validate_on_submit():
        for book in all_books:
            if local_search.title_found(book["title"], form.key_phrases.data):
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
    book = galleryDB.get_book_byid(book_id)
    read = book["read"]
    form = BookDeletion(csrf_enabled=False)
    if form.validate_on_submit():
        if form.confirm.data:
            galleryDB.delete_book(book_id)
            flash("Book Deleted", "success")
            return redirect(url_for("home"))
        flash("Book Not Deleted: Please confirm the deletion.", "danger")
    return render_template("book.html",
                            title=book["title"],
                            book_id=book_id,
                            imgs=book["contents"],
                            tags=book["tags"],
                            read=read,
                            form=form
                          )

@app.route("/book-<string:book_id>/toggle", methods=["GET", "POST"])
def bookpage_toggle_read(book_id):
    book = galleryDB.get_book_byid(book_id)
    read = book["read"]
    galleryDB.toggle_read(book, read)
    return redirect(url_for("bookpage", book_id=book_id))


@app.route('/images/<string:pid>.jpg')
def get_image(pid):
    response = make_response(galleryDB.get_img(pid))
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename=f'{pid}.jpg')
    return response


if __name__ == "__main__":
    app.run(debug=debug, port=flask_port)