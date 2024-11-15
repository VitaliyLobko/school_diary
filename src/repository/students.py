from typing import List

from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from src.database.models import Student, Grade, Group
from src.schemas import StudentModel, StudentIsActiveModel


async def create_student(body: StudentModel, db: Session):
    student = Student(**body.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


async def get_all(db: Session):
    total_students = db.query(Student).count()
    return total_students


async def get_students(search_by, limit, offset, db: Session) -> List[Student]:
    if search_by:
        students = (
            db.query(Student)
            .order_by(Student.full_name)
            .filter(Student.full_name.ilike(f"%{search_by}%"))
            .limit(limit)
            .offset(offset)
            .all()
        )
    else:
        students = (
            db.query(Student)
            .order_by(Student.full_name)
            .limit(limit)
            .offset(offset)
            .all()
        )
    return students


async def get_top_10_students(db: Session) -> List[Student]:
    students = (
        db.query(
            Student.id,
            Student.full_name,
            Student.dob,
            Student.created_at,
            Student.updated_at,
            Student.is_active,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
            Group.id.label("group_id"),
            Group.name.label("group_name"),
        )
        .select_from(Student)
        .join(Group)
        .join(Grade)
        .group_by(Student.id, Group.id)
        .order_by(desc(func.avg(Grade.grade)), Student.full_name)
        .limit(10)
        .all()
    )
    return students


async def get_all_avg_grade(db: Session) -> List[Student]:
    total_avg_grade = (
        db.query(
            Student.id,
            Student.full_name,
            Student.dob,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
            Group.id.label("group_id"),
            Group.name.label("group_name"),
            Student.created_at,
            Student.updated_at,
            Student.is_active,
        )
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .group_by(Student.id, Group.id)
        .order_by(desc(func.avg(Grade.grade)), Student.full_name)
        .count()
    )
    return total_avg_grade


async def get_students_avg_grade(limit, offset, db: Session) -> List[Student]:
    students = (
        db.query(
            Student.id,
            Student.full_name,
            Student.dob,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
            Group.id.label("group_id"),
            Group.name.label("group_name"),
            Student.created_at,
            Student.updated_at,
            Student.is_active,
        )
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .group_by(Student.id, Group.id)
        .order_by(desc(func.avg(Grade.grade)), Student.full_name)
        .limit(limit)
        .offset(offset)
        .all()
    )
    return students


async def get_student_by_id(student_id: int, db: Session) -> Student | None:
    student = (
        db.query(
            Student.id,
            Student.full_name,
            Student.dob,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
            Group.id.label("group_id"),
            Group.name.label("group_name"),
            Student.created_at,
            Student.updated_at,
            Student.is_active,
        )
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .group_by(Student.id, Group.id)
        .order_by(desc(func.avg(Grade.grade)), Student.full_name)
        .where(Student.id == student_id)
        .first()
    )

    return student


async def update_student(body: StudentModel, student: int, db: Session):
    for name, value in body:
        setattr(student, name, value)
    db.commit()
    return student


async def is_active_student(body: StudentIsActiveModel, student, db: Session):
    student.is_active = body.is_active
    db.commit()
    return student


async def delete_student(student, db: Session):
    db.delete(student)
    db.commit()
    return student
