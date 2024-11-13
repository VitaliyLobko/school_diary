from datetime import datetime

from pydantic import BaseModel, Field, EmailStr



class StudentModel(BaseModel):
    is_active: bool = True
    full_name: str  = Field('NoName', min_length=3, max_length=250)
    dob: datetime
    group_id: int
    created_at: datetime
    updated_at: datetime

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


class StudentsResponseWithAvgGrade(BaseModel):
    id: int
    is_active: bool = True
    full_name: str
    dob: datetime
    group_id: int
    avg_grade: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True




class GroupModel(BaseModel):
    id: int
    name: str


class GroupResponse(BaseModel):
    id: int
    name: str

class DisciplineModel(BaseModel):
    id: int
    name: str
    teacher_id: int
    full_name: str


class DisciplineResponse(BaseModel):
    id: int
    name: str
    teacher_id: int
    full_name: str


class GradeModel(BaseModel):
    id: int
    grade: str
    date_of: datetime
    student_fullname: str
    teacher_fullname: str



class GradeResponse(BaseModel):
    id: int
    grade: str
    date_of: datetime
    student_fullname: str
    teacher_fullname: str
