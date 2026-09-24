from sqlalchemy.orm import Session

from app.data.models import Borrowing, Book, Member
from datetime import datetime, timedelta , timezone
from app.utils.file_handler import log_admin_activity
def get_all_borrowings(db: Session,page: int =1, limit: int = 10):
    offset = (page -1) * limit
    return db.query(Borrowing).offset(offset).limit(limit).all()


def borrow_book(db: Session, book_id: int, member_id: int):

    # Check whether book exists
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        return None, "Book not found"

    member = db.query(Member).filter(Member.id == member_id).first()


    if member is None:
        return None, "Member not found"

    # Check book availability
    if not book.is_available:
        return None, "Book is already issued"
    
    # check how many books member has borrowed
    borrowed_count=(
        db.query(Borrowing)
        .filter(
            Borrowing.member_id==member_id,
            Borrowing.returned == False
        )
        .count()
    )

    # max 2 books
    if borrowed_count>=2:
        return None, "You can borrow maximum 2 books"
    
    borrowed_at = datetime.now(timezone.utc)
    due_date = borrowed_at + timedelta(days=30)
    # Create borrowing record
    borrowing= Borrowing(
        book_id=book_id,
        member_id = member_id,
        borrowed_at=borrowed_at,
        due_date=due_date,
        returned=False
    )
    db.add(borrowing)
    
    # mark book as unavailabel
    book.is_available=False
    db.commit()
    db.refresh(borrowing)
    log_admin_activity(
    f"Admin issued book ID: {book_id} to member ID: {member_id}"
)
    
    return borrowing, "Book borrowed successfully"

def return_book(db: Session, book_id: int):
    # check whether book exists
    book = (
        db.query(Book).
        filter(Book.id == book_id).
        first()
    )
    
    if book is None:
        return None, "Book not found"
    # find active borrowing record
    borrowing = (
        db.query(Borrowing)
        .filter(
            Borrowing.book_id == book_id,
            
            Borrowing.returned == False
        )
        .first()
    )
    
    if borrowing is None:
        return None, "This book is not currently issued"
    
    # mark borrowing as returned
    borrowing.returned = True
    borrowing.returned_at = datetime.now(timezone.utc)
    #make book available again
    book.is_available = True
    db.commit()
    db.refresh(borrowing)
    log_admin_activity(
    f"Admin returned book ID: {book_id} from member ID: {borrowing.member_id}"
)
    
    return borrowing, "Book returned successfully"
    
    
    
    