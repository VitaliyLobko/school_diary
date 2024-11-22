from datetime import datetime
from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel


class GroupModel(BaseModel):
    id: int
    name: str


class GroupResponse(GroupModel):
    pass
