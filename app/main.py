from fastapi import FastAPI
from app.routes import books #2 after making router
from app.routes import members #
from app.routes import borrowings
from app.routes import auth
from app.data.database import engine, Base
from app.data import models
Base.metadata.create_all(bind=engine)#

app = FastAPI(
    title="LIBRARY MANAGEMENT SYSTEM",
    description = "Backend API for managing books and library",
    version="1.0.0"
)

app.include_router(books.router) #2 after making router and vvimp aIt connects your books API to the main FastAPI applications 
app.include_router(members.router) #
app.include_router(borrowings.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {
        "message":"LIBRARY MANAGEMENT SYSTEM API is running"
    }
