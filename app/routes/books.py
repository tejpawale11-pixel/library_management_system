

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.data.models import Book
from app.schemas.book import BookCreate, BookResponse
from app.data.database import get_db
from app.dependencies import get_current_admin_email

from app.services.book_service import (
    get_all_books,
    get_book_by_id,
    search_books,
    add_book,
    issue_book,
    return_book 
)


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.get("/get_all_books/", response_model=list[BookResponse])
def get_books(
    db: Session = Depends(get_db),
    page: int =1,
    limit: int =10,
    current_admin: str = Depends(get_current_admin_email)
):
    borrowings = get_all_books(db,page,limit)
    if not borrowings:
        raise HTTPException(
            status_code=404,
            detail="NO mor books record available."
        )
    return borrowings


@router.get("/search/", response_model=list[BookResponse])
def search_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin_email)
):
    return search_books(db,book.title)


@router.get("/{book_id}", response_model=BookResponse)
def get_book( 
    book: BookCreate,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin_email)
):
    book = get_book_by_id(db,book)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


@router.post("/", response_model=BookResponse)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin_email)
):
    
    return add_book(db, book.title, book.author)


@router.put("/{book_id}/issue", response_model=BookResponse)
def issue_book_endpoint(
    book_id: int,
    db: Session = Depends(get_db),
     current_admin: str = Depends(get_current_admin_email)
):
    book, message = issue_book(db, book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail=message
        )

    if message != "Book issued successfully":
        raise HTTPException(
            status_code=400,
            detail=message
        )

    return book


@router.put("/{book_id}/return", response_model=BookResponse)
def return_book_endpoint(
    book_id: int,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin_email)
):
    book, message = return_book(db, book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail=message
        )

    if message != "Book returned successfully":
        raise HTTPException(
            status_code=400,
            detail=message
        )

    return book

@router.post("/bulk")
def add_bulk_books(
    current_admin_email: str = Depends(get_current_admin_email),
     db: Session = Depends(get_db)
):
    books = [
        {"title": "The Alchemist", "author": "Paulo Coelho"},
        {"title": "Atomic Habits", "author": "James Clear"},
        {"title": "Rich Dad Poor Dad", "author": "Robert Kiyosaki"},
        {"title": "Think and Grow Rich", "author": "Napoleon Hill"},
        {"title": "The Power of Now", "author": "Eckhart Tolle"},
    ]
    
    for book in books:
        new_book = Book(
            title=book["title"],
            author=book["author"],
            is_available=True
        )
        db.add(new_book)
    db.commit()
    return {
        "message": "Books added successfully",
        "total_books_added": len(books)
    }

