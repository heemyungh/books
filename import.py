import csv
import os
 
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
 
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
 
def main():
    f = open("books.csv")
    reader = csv.DictReader(f)
    for row in reader:
        # check if author is already in database
        check = db.execute("SELECT id FROM authors WHERE author = :author",
                           {"author": row.get("author")}).fetchone()
        if not check:
            db.execute("INSERT INTO authors (author) VALUES (:author)",
                       {"author": row.get("author")})
        author_id = db.execute("SELECT id FROM authors WHERE author = :author",
                   {"author": row.get("author")}).fetchone()[0]
        db.execute("INSERT INTO books (isbn, title, author_id, year) VALUES (:isbn, :title, :author_id, :year)",
                   {"isbn": row.get("isbn"), "title": row.get("title"), "author_id": author_id, "year": row.get("year")})
        print(row.get("title"), row.get("author"))
    db.commit()
 
if __name__ == "__main__":
    main()