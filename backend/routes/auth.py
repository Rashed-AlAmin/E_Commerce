from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.core.auth import hash_password, verify_password, create_access_token
from backend.core.dependencies import get_db
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        is_admin=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}




@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"user_id": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}
