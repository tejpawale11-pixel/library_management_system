from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Create engine using the URL from config
engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Dependency to open/close DB sessions in API endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
