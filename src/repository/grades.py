from sqlalchemy import desc
from sqlalchemy.orm import Session
from src.database.models import Group, Grade, Student, Teacher, Discipline
from src.schemas import GradeModel


async def create_grade(body: GradeModel, db: Session):
    grade = (Group(**body.model_dump()))
    db.add(grade)
    db.commit()
    db.refresh(grade)
    return grade


async def get_grades(limit, offset, db: Session):
    grades = (db.query(Grade.id,
                       Grade.grade,
                       Grade.date_of,
                       Student.full_name.label('student_fullname'),
                       Teacher.full_name.label('teacher_fullname'),
                       Discipline.name.label('discipline_name')).join(Student).join(Discipline).join(Teacher)
              .order_by(desc(Grade.date_of)).limit(limit).offset(offset).all())
    return grades
