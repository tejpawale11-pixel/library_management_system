from app.data.database import SessionLocal #SessionLocal, It gives us a database session, which allows Python to communicate with PostgreSQL.
from app.data.models import Member
db = SessionLocal() # opens a connection/session through SQLAlchemy for it we use db
for i in range(16, 25): 
    member = Member(
        name=f"Member{i}",
        email=f"member{i}@gmail.com"
    )
    db.add(member) #I want to insert this Member into the database
db.commit() # Save everything
db.close()
print("9 dummy members added successfully!")
# for this we use the new terminal not of server
 
## books

from app.data.database import SessionLocal
from app.data.models import Book

db = SessionLocal()

existing_books = db.query(Book).count() #looks at the books table so that we can understand the count of book

print("Existing books:", existing_books)

db.close()
# here i have already 25 books so this structure

# therefore it will be
from app.data.database import SessionLocal
from app.data.models import Book

db = SessionLocal()

for i in range(26, 31):
    book = Book(
        title=f"Book {i}",
        author=f"Author {i}",
        is_available=True
    )

    db.add(book)

db.commit()
db.close()

print("5 dummy books added successfully!")

## borrowing 
from app.data.database import SessionLocal
from app.data.models import Borrowing

db = SessionLocal()

existing_borrowings = db.query(Borrowing).count()

print("Existing borrowings:", existing_borrowings)

db.close()

# therefore we will get member, book and borrowing 
from app.data.database import SessionLocal
from app.data.models import Member, Book, Borrowing

db = SessionLocal()

members = db.query(Member).all()
books = db.query(Book).all()
borrowings = db.query(Borrowing).all()

print("Members:", len(members))
print("Books:", len(books))
print("Borrowings:", len(borrowings))

db.close()