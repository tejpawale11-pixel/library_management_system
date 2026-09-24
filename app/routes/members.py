
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_current_admin_email
from app.schemas.member import MemberCreat, MemberResponse
from app.services.member_service import (
    get_all_members,
    get_member_by_id,
    add_member
)
from app.data.database import get_db


router = APIRouter(
    prefix="/members",
    tags=["Members"]
)


@router.get("/", response_model=list[MemberResponse])
def get_members(
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 10,
    current_admin: str = Depends(get_current_admin_email)  
):
    borrowings = get_all_members(db, page, limit)
    if not borrowings:
        raise HTTPException(
            status_code=404,
            detail="No more members records available."
        )
    return borrowings


@router.get("/{member_id}", response_model=MemberResponse)
def get_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin_email)  
):
    member = get_member_by_id(db, member_id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return member


@router.post("/", response_model=MemberResponse)
def create_member(
    member: MemberCreat,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin_email)  
):
    return add_member(
        db,
        member.name,
        member.email
    )

    