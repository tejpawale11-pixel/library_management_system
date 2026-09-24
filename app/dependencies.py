from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.security import verify_token
from sqlalchemy.orm import Session
from app.security import verify_token
from app.data.database import get_db
from app.data.models import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_admin_email(
    token: str = Depends(oauth2_scheme)
):
    email = verify_token(token)

    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return email

def get_current_admin(
    current_user: str = Depends(get_current_admin_email),
    db: Session = Depends(get_db)
):
    admin = (
        db.query(admin)
        .filter(admin.email == current_admin)
        .first()
    )

    if admin is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    if admin.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can access this resource"
        )

    return admin