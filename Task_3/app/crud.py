from sqlalchemy.orm import Session
from . import models, schemas
from uuid import uuid4
from fastapi import HTTPException
from .auth import hash_password

def create_user(db: Session, user: schemas.UserRegister):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    new_user = models.User(
        id=str(uuid4()),
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        age=user.age,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
