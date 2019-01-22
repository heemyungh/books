import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
 
app = Flask(__name__)
 
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html", searches=False)


@app.route("/search", methods=["POST"])
def search():
    terms = request.form.get("search")
    # search a join table
    searches = db.execute("SELECT title, author, year, isbn FROM authors INNER JOIN books ON authors.id = books.author_id WHERE title LIKE :terms OR author LIKE :terms",
                          {"terms": '%'+terms+'%'}).fetchall()
    return render_template("index.html", searches=searches)