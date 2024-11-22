from datetime import datetime
from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel


class GradeModel(BaseModel):
    grade: str
    date_of: datetime
    student_fullname: str
    teacher_fullname: str


class GradeResponse(GradeModel):
    id: int
