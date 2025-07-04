
from sqlalchemy.orm import Session
from uuid import uuid4
from . import models, schemas
from fastapi import HTTPException

def create_user(db: Session, user: schemas.UserCreate):

    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    user_obj = models.User(id=str(uuid4()), **user.dict())
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session):
    return db.query(models.User).all()

def update_user(db: Session, user_id: str, data: schemas.UserCreate):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in data.dict().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: str):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
