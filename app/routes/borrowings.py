from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_current_admin_email
from app.data.models import Book, Member, Borrowing # for condn of 5 membrers
from app.schemas.borrowing import (
    BorrowingCreate,
    BorrowingResponse
)

from app.services.borrowing_service import (
    get_all_borrowings,
    borrow_book,
    return_book
)

from app.data.database import get_db


router = APIRouter(
    prefix="/borrowings",
    tags=["Borrowings"]
)


@router.get("/", response_model=list[BorrowingResponse])
def get_borrowings(
    db: Session = Depends(get_db),
    page: int =1,
    limit: int = 10,
    current_admin: str = Depends(get_current_admin_email)              
):
    borrowings= get_all_borrowings(db, page, limit)
    if not borrowings:
        raise HTTPException(
            status_code=404,
            detail="NO more borrowing records available."
        )
    return borrowings


@router.post("/", response_model=BorrowingResponse)
def create_borrowing(
    borrowing: BorrowingCreate,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin_email)  
):
    print("CURRENT admin FROM JWT:", current_admin)

    result, message = borrow_book(
        db,
        borrowing.book_id,
        borrowing.member_id
    )

    if result is None:

        if message in ["Book not found", "Member not found"]:
            raise HTTPException(
                status_code=404,
                detail=message
            )

        raise HTTPException(
            status_code=400,
            detail=message
        )

    return result

@router .put("/return/{book_id}")
def return_book_endpoint(
    book_id: int,
    
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin_email)
):
    result, message = return_book(
        db,
        book_id
        
    )
    
    if result is None:
        if message == "Book not found":
            raise HTTPException(
               status_code=404, 
               detail=message
            )
        raise HTTPException(
            status_code=400,
            detail=message
        )
    return {
        "message": message,
        "borrowing_id":result.id,
        "book_id": result.book_id,
        "member_id": result.member_id,
        "returned": result.returned
    }
    
@router.get("/summary")
def library_summary(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_email)
):
    total_books = db.query(Book).count()

    available_books = (
        db.query(Book)
        .filter(Book.is_available == True)
        .count()
    )

    issued_books = (
        db.query(Book)
        .filter(Book.is_available == False)
        .count()
    )

    total_members = db.query(Member).count()

    active_borrowings = (
        db.query(Borrowing)
        .filter(Borrowing.returned == False)
        .count()
    )

    return {
        "total_books": total_books,
        "available_books": available_books,
        "issued_books": issued_books,
        "total_members": total_members,
        "active_borrowings": active_borrowings
    }