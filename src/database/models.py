import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    Boolean,
    func,
    DateTime,
    event,
    Enum,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True)
    first_name = Column(String(120), default="None")
    last_name = Column(String(120), default="None")
    dob = Column(Date, nullable=True)
    # contacts = relationship(
    #     "Contact",
    #     primaryjoin="and_(foreign(Contact.person_id)==Teacher.id, Contact.person_type=='teacher')",
    #     backref="teacher",
    # )
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @hybrid_property
    def full_name(self):
        return self.first_name + " " + self.last_name


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True)
    first_name = Column(String(120), default="None")
    last_name = Column(String(120), default="None")
    dob = Column(Date, nullable=True)
    group_id = Column("group_id", ForeignKey("groups.id", ondelete="CASCADE"))
    group = relationship("Group", backref="students")
    # contacts = relationship(
    #     "Contact",
    #     primaryjoin="and_(foreign(Contact.person_id)==Student.id, Contact.person_type=='student')",
    #     # Используем foreign()
    #     backref="student",
    # )
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @hybrid_property
    def full_name(self):
        return self.first_name + " " + self.last_name


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    contact_type = Column(String(50), nullable=False)
    contact_value = Column(String(255), nullable=False)
    person_id = Column(Integer, nullable=False)
    person_type = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Discipline(Base):
    __tablename__ = "disciplines"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    teacher_id = Column("teacher_id", ForeignKey("teachers.id", ondelete="CASCADE"))
    teacher = relationship("Teacher", backref="disciplines")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    date_of = Column("date_of", Date, nullable=True)
    student_id = Column("student_id", ForeignKey("students.id", ondelete="CASCADE"))
    discipline_id = Column(
        "discipline_id", ForeignKey("disciplines.id", ondelete="CASCADE")
    )
    student = relationship("Student", backref="grade")
    discipline = relationship("Discipline", backref="grade")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    avatar = Column(String(255), nullable=True)
    username = Column(String(50), nullable=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    roles = Column("roles", Enum(Role), default=Role.user)
