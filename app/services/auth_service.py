from sqlalchemy.orm import Session

from app.data.models import User
from app.security import hash_password, verify_password , create_access_token


def register_user(
    db: Session,
    name: str,
    email: str,
    phone: str,
    password: str
):
    # Check whether email already exists
    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        return None, "Email already registered"

    # Hash the password
    hashed_password = hash_password(password)

    # Create new user
    new_user = User(
        name=name,
        email=email,
        phone=phone,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user, "User registered successfully"

def login_user(
    db: Session,
    email: str,
    password: str
):
    # Find user by email
    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        return None, "Invalid email or password"

    # Verify entered password with stored hashed password
    if not verify_password(password, user.password):
        return None, "Invalid email or password"
    
     # Create JWT token
    access_token = create_access_token({
        "sub": user.email
    })


    return access_token, "Login successful"