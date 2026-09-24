# vvimp for connecting the api --- postgreSQL
from sqlalchemy import Column, Integer, String, Boolean,DateTime
from app.data.database import Base
from datetime import datetime , timezone
# for history


from sqlalchemy import Column, Integer, String, Boolean, DateTime
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    is_available = Column(Boolean, default=True)

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    
class Borrowing(Base):
    __tablename__= "borrowings"
    id=Column(Integer,primary_key=True, index=True)
    book_id=Column(Integer, nullable=False)
    member_id=Column(Integer, nullable=False)
    returned = Column(Boolean, default=False)
    borrowed_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))
    due_date = Column(DateTime(timezone=True), nullable=False)
    returned_at = Column(DateTime(timezone=True), nullable=True)
   
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="member", nullable=False)