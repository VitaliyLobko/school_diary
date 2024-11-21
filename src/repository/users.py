from typing import List

from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import StudentModel, StudentIsActiveModel, UserModel


async def create_user(body: UserModel, password, db: Session):
    new_user = User(email=body.email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def get_user_by_email(email, db: Session) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    return user


async def delete_student(student, db: Session):
    db.delete(student)
    db.commit()
    return student
