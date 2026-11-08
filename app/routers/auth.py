from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, hash_password, verify_password
from app.core.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(User).where(User.email == data.email.lower()))
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(email=data.email.lower(), hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == form.username.lower()))
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account disabled")
    return {"access_token": create_access_token(str(user.id)), "token_type": "bearer"}
@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)):
    return current_user