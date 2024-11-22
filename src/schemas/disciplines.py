from pydantic import BaseModel


class DisciplineModel(BaseModel):
    id: int
    name: str
    teacher_id: int
    full_name: str


class DisciplineResponse(DisciplineModel):
    pass
