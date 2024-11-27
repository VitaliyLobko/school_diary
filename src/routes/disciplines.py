from typing import List
from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter,
    Query,
    Request,
)
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_201_CREATED
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import Discipline, Role
from src.repository import disciplines as repository_disciplines
from src.services.roles import RoleAccess
from src.schemas.disciplines import DisciplineModel, DisciplineResponse
from src.repository.dependencies import get_discipline_by_id

router = APIRouter(prefix="/disciplines", tags=["disciplines"])
templates = Jinja2Templates(directory="templates")

allowed_operation_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_create = RoleAccess([Role.admin, Role.moderator])
allowed_operation_update = RoleAccess([Role.admin, Role.moderator])
allowed_operation_remove = RoleAccess([Role.admin])


@router.post(
    "/",
    status_code=HTTP_201_CREATED,
    name="Create discipline",
    dependencies=[Depends(allowed_operation_create)],
)
async def create_discipline(body: DisciplineModel, db: Session = Depends(get_db)):
    discipline = await repository_disciplines.create_discipline(body, db)
    return discipline


@router.get(
    "/",
    response_model=List[DisciplineResponse],
    name="List of all disciplines",
    dependencies=[Depends(allowed_operation_get)],
)
async def get_disciplines(
    request: Request,
    limit: int = Query(20, le=500),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    disciplines = await repository_disciplines.get_disciplines(limit, offset, db)
    total_count = await repository_disciplines.get_all_dicsiplines(db)

    if disciplines is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")

    return templates.TemplateResponse(
        "disciplines.html",
        {
            "request": request,
            "disciplines": disciplines,
            "limit": limit,
            "offset": offset,
            "total_count": total_count,
            "title": "Disciplines List",
        },
    )


@router.put(
    "/{discipline_id}",
    name="Update discipline by id",
    dependencies=[Depends(allowed_operation_update)],
)
async def update_discipline(
    body: DisciplineModel,
    discipline: Discipline = Depends(get_discipline_by_id),
    db: Session = Depends(get_db),
):
    discipline = await repository_disciplines.update_discipline(body, discipline, db)
    if discipline is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id: {discipline} not found",
        )
    return discipline


@router.delete(
    "/{discipline_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="Delete discipline by id",
    dependencies=[Depends(allowed_operation_remove)],
)
async def delete_discipline(
    discipline: Discipline = Depends(get_discipline_by_id),
    db: Session = Depends(get_db),
) -> None:

    discipline = await repository_disciplines.delete_discipline(discipline, db)
    if discipline is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Discipline not found",
        )
