from pydantic import BaseModel  # pydantic = fastapi


class BookCreate(BaseModel):
    title: str
    author: str


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    is_available: bool
    
    class Config:
        from_attributes = True