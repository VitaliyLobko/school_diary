from datetime import datetime
from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel


class GroupModel(BaseModel):
    name: str


class GroupResponse(GroupModel):
    id: int
