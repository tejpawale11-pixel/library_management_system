# now for api---postersql
from sqlalchemy.orm import Session
from app.data.models import Book
from app.utils.file_handler import log_admin_activity

def get_all_books(db: Session, page: int = 1, limit: int = 10):
    offset = (page - 1) * limit # formula of pagination
    return db.query(Book).offset(offset).limit(limit).all() # Get only the required records
# limit --> how many records to return
# offset → how many records to skip

def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def search_books(db: Session, title: str):
    return db.query(Book).filter(
        Book.title.ilike(f"%{title}%")
    ).all()


def add_book(db: Session, title: str, author: str):
    new_book = Book(
        title=title,
        author=author,
        is_available=True
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    log_admin_activity(
    f"Admin added book: {new_book.title} (ID: {new_book.id})"
)
    return new_book


def issue_book(db: Session, book_id: int):

    book = get_book_by_id(db, book_id)

    if book is None:
        return None, "Book not found"

    if not book.is_available:
        return book, "Book is already issued"

    book.is_available = False

    db.commit()
    db.refresh(book)

    return book, "Book issued successfully"


def return_book(db: Session, book_id: int):

    book = get_book_by_id(db, book_id)

    if book is None:
        return None, "Book not found"

    if book.is_available:
        return book, "Book is already available"

    book.is_available = True

    db.commit()
    db.refresh(book)

    return book, "Book returned successfully"