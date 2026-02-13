from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.core.auth import decode_access_token
from backend.db.session import SessionLocal
from backend.models.user import User
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def get_current_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user
