

#
from sqlalchemy.orm import Session
from app.data.models import Member
from app.utils.file_handler import log_admin_activity

def get_all_members(db: Session, page:int =1, limit: int=10):
    offset = (page - 1)*limit
    return db.query(Member).offset(offset).limit(limit).all()


def get_member_by_id(db: Session, member_id: int):
    return db.query(Member).filter(Member.id == member_id).first()


def add_member(db: Session, name: str, email: str):
    new_member = Member(
        name=name,
        email=email
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    log_admin_activity(
    f"Admin added member: {new_member.name} (ID: {new_member.id})"
    )

    return new_member