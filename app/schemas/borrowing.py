from pydantic import BaseModel


class BorrowingCreate(BaseModel):
    book_id: int
    member_id: int


class BorrowingResponse(BaseModel):
    id: int
    book_id: int
   