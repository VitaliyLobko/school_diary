from datetime import datetime
from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel



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
