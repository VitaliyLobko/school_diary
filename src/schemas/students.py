from datetime import datetime
from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel
from src.schemas.contacts import ContactModel


class StudentModel(BaseModel):
    is_active: bool = True
    first_name: Annotated[str, MinLen(2), MaxLen(250)]
    last_name: Annotated[str, MinLen(2), MaxLen(250)]
    dob: datetime
    group_id: int
    contacts: ContactModel


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


class StudentsResponseWithAvgGrade(StudentsResponse):
    avg_grade: float
    group_name: str
