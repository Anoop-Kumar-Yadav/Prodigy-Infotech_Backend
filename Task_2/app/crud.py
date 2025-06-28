# app/crud.py
from sqlalchemy.orm import Session
from uuid import uuid4
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
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
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        for key, value in data.dict().items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
