from typing import List
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from src.database.models import Student, Grade, Group, Teacher
from src.schemas.teachers import (
    TeacherModel,
    TeachersIsActiveModel,
)
from src.schemas.students import (
    StudentModel,
    StudentIsActiveModel,
)


async def create_teacher(body: StudentModel, db: Session):
    student = Student(**body.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


async def get_all(db: Session):
    total_teachers = db.query(Teacher).count()
    return total_teachers


async def get_teachers(limit, offset, db: Session) -> List[Teacher]:
    teachers = (
        db.query(Teacher).order_by(Teacher.full_name).limit(limit).offset(offset).all()
    )
    return teachers


async def update_teacher(body: TeacherModel, teacher, db: Session):
    for name, value in body:
        setattr(teacher, name, value)
    db.commit()
    return teacher


async def is_active_teacher(body: TeachersIsActiveModel, teacher, db: Session):
    teacher.is_active = body.is_active
    db.commit()
    return teacher


async def delete_teacher(teacher, db: Session):
    db.delete(teacher)
    db.commit()
    return teacher


# teacher = session.query(Teacher).first()
# contact = Contact(contact_type="email", contact_value="teacher@example.com", person_type="teacher", person_id=teacher.id)
# session.add(contact)
# session.commit()
#
# # Получение контактов учителя
# teacher_contacts = teacher.contacts
