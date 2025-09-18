from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models

def get_user_by_email(db: Session, email: str):
    return db.query(models.UserDB).filter(models.UserDB.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserDB).offset(skip).limit(limit).all()

def create_user(db: Session, user: models.UserCreate):
    try:
        db_user = models.UserDB(
            full_name=user.full_name,
            email=user.email,
            phone=user.phone
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        return None  # User already exists