from datetime import datetime
from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, Field, EmailStr
from src.database.models import Role


class ContactModel(BaseModel):
    contact_type: str
    contact_value: str


class ContactResponse(ContactModel):
    pass
