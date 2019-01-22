import os
import requests

from flask import Flask, render_template, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
 
app = Flask(__name__)
 
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    """Searches database for author or title matching given string"""
    terms = request.form.get("search").capitalize()
    # search a join table
    authors = db.execute("SELECT author, id FROM authors WHERE author LIKE :terms",
                          {"terms": '%'+terms+'%'}).fetchall()
    books = db.execute("SELECT title, isbn FROM books WHERE title LIKE :terms",
                          {"terms": '%'+terms+'%'}).fetchall()
    return render_template("index.html", authors=authors, books=books)


@app.route("/book/<string:isbn>")
def book(isbn):
    """Returns information for particular book"""
    book = db.execute("SELECT title, author, id, year, isbn FROM books INNER JOIN authors ON books.author_id = authors.id WHERE isbn = :isbn", 
                      {"isbn": isbn}).fetchone()
    # from https://openlibrary.org/dev/docs/api/covers
    cover = f"http://covers.openlibrary.org/b/isbn/{book['isbn']}-M.jpg?default=false"
    if requests.get(cover).status_code != 200:
        cover = None
    return render_template("book.html", book=book, cover=cover)


@app.route("/author/<string:id>")
def author(id):
    """Returns all books by particular author"""
    author = db.execute("SELECT author FROM authors WHERE id=:id", 
                        {"id":id}).fetchone()
    books = db.execute("SELECT title, isbn FROM books WHERE author_id=:id", 
                       {"id":id}).fetchall()
    return render_template("author.html", author=author, books=books)