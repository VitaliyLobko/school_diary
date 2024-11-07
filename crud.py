from sqlalchemy import func, desc

from models import Teacher, Student, Discipline, Grade, Group
from db import session


def top_5_students():
    """
    Топ 5 студентів із найбільшим середнім балом з усіх предметів.
    :return: list[dict]
    """
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade'), \
                           Group.name).select_from(Grade).join(Student).join(Group).group_by(Student.id).order_by(
        desc(func.avg(Grade.grade))).limit(5).all()

    print(result)


def top_5_students_by_discipline_id(discipline_id: int):
    """
        Топ 5 студентів із найбільшим середнім балом з визначеного предмета.
        :return: list[dict]
    """

    result = session.query(Student.fullname, Discipline.name, func.round(func.avg(Grade.grade), 2).label('avg_grade'), \
                           Teacher.fullname) \
        .select_from(Grade).join(Student).join(Discipline).join(Teacher).group_by(Student.id, Discipline.id) \
        .filter(Discipline.id == discipline_id).order_by(desc(func.avg(Grade.grade))).limit(5).all()
    print(result)


def top_5_students_by_group_id(group_id: int):
    """
        Топ 5 студентів визначеної групи.
        :return: list[dict]
    """

    result = session.query(Student.fullname, Group.name,
                           func.round(func.avg(Grade.grade), 2).label('avg_grade')).select_from(Grade) \
        .join(Student).join(Group) \
        .filter(Group.id == group_id).group_by(Group.id, Student.id).order_by(desc(func.avg(Grade.grade))).limit(
        5).all()
    print(result)


def students_by_group_id(group_id):
    """
        Студенти з визначеної  групи.
        :return: list[dict]
    """
    result = session.query(Student.fullname, Group.name).select_from(Group) \
        .join(Student).filter(Group.id == group_id).order_by(Student.fullname).all()
    print(result)

    total = session.query(func.count()).select_from(Student).join(Group) \
        .filter(Group.id == group_id).group_by(Group.id).all()

    print(total)


def all_grades_by_student_id(students_id):
    result = session.query(Student.fullname, Grade.date_of, Grade.grade, Discipline.name, Teacher.fullname) \
        .select_from(Grade) \
        .join(Student).join(Discipline).join(Teacher)\
        .filter(Student.id == students_id)\
        .group_by(Grade.id)\
        .order_by(desc(Grade.date_of)).all()

    print(result)

    row_count = session.query(func.count(Grade.id)).join(Student).filter(Student.id == students_id).all()
    print(row_count)

if __name__ == '__main__':
    # top_5_students()
    # top_5_students_by_group_id(3)
    # top_5_students_by_discipline_id(2)
    # students_by_group_id(3)
    all_grades_by_student_id(3)
