from datetime import datetime
from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, Field, EmailStr


class StudentModel(BaseModel):
    is_active: bool = True
    first_name: Annotated[str, MinLen(2), MaxLen(250)]
    last_name: Annotated[str, MinLen(2), MaxLen(250)]
    dob: datetime
    group_id: int


class StudentIsActiveModel(BaseModel):
    is_active: bool = True


class StudentsResponse(BaseModel):
    id: int
    is_active: bool = True
    full_name: str
    dob: datetime
    group_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StudentsResponseWithAvgGrade(StudentsResponse):
    avg_grade: float
    group_name: str

    class Config:
        from_attributes = True


class TeacherModel(BaseModel):
    is_active: bool = True
    first_name: Annotated[str, MinLen(2), MaxLen(250)]
    last_name: Annotated[str, MinLen(2), MaxLen(250)]
    dob: datetime


class TeachersResponse(BaseModel):
    id: int
    is_active: bool = True
    full_name: str
    dob: datetime
    created_at: datetime
    updated_at: datetime


class TeachersIsActiveModel(BaseModel):
    is_active: bool = True


class GroupModel(BaseModel):
    id: int
    name: str


class GroupResponse(GroupModel):
    pass


class DisciplineModel(BaseModel):
    id: int
    name: str
    teacher_id: int
    full_name: str


class DisciplineResponse(DisciplineModel):
    pass


class GradeModel(BaseModel):
    id: int
    grade: str
    date_of: datetime
    student_fullname: str
    teacher_fullname: str


class GradeResponse(GradeModel):
    pass


class UserModel(BaseModel):
    username: str
    password: str
