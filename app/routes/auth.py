from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    TokenResponse
)

from app.services.auth_service import (
    register_user, 
    login_user)
from app.data.database import get_db


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse)
def register(
    user: RegisterRequest,
    db: Session = Depends(get_db)
):
    new_user, message = register_user(
        db,
        user.name,
        user.email,
        user.phone,
        user.password
    )

    if new_user is None:
        raise HTTPException(
            status_code=400,
            detail=message
        )

    return new_user

@router.post("/login", response_model=TokenResponse)
def login(
   username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    access_token, message = login_user(
        db,
        username,
        password
    )

    if access_token is None:
        raise HTTPException(
            status_code=401,
            detail=message
        )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

