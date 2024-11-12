from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, func, DateTime, event
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, declarative_base
from src.database.db import engine

Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True)
    first_name = Column(String(120), default='None')
    last_name = Column(String(120), default='None')
    dob = Column(Date, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @hybrid_property
    def full_name(self):
        return self.first_name + ' ' + self.last_name


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True)
    first_name = Column(String(120), default='None')
    last_name = Column(String(120), default='None')
    dob = Column(Date, nullable=True)
    group_id = Column('group_id', ForeignKey('groups.id', ondelete='CASCADE'))
    group = relationship('Group', backref='students')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @hybrid_property
    def full_name(self):
        return self.first_name + ' ' + self.last_name


class Discipline(Base):
    __tablename__ = 'disciplines'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    teacher_id = Column('teacher_id', ForeignKey('teachers.id', ondelete='CASCADE'))
    teacher = relationship('Teacher', backref='disciplines')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    date_of = Column('date_of', Date, nullable=True)
    student_id = Column('student_id', ForeignKey('students.id', ondelete='CASCADE'))
    discipline_id = Column('discipline_id', ForeignKey('disciplines.id', ondelete='CASCADE'))
    student = relationship('Student', backref='grade')
    discipline = relationship('Discipline', backref='grade')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

#
# @event.listens_for(Teacher, 'before_update')
# def update_is_active(mapper, conn, target):
#     if target.teacher_id == 1:
#         target.is_active = False
#
#
# @event.listens_for(Teacher, 'before_insert')
# def update_is_active(mapper, conn, target):
#     if target.teacher_id == 1:
#         target.is_active = False