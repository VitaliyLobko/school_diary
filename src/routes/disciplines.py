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
from src.repository import disciplines as repository_disciplines
from src.schemas import DisciplineModel, DisciplineResponse

router = APIRouter(prefix="/disciplines", tags=["disciplines"])

templates = Jinja2Templates(directory="templates")


@router.post("/", status_code=HTTP_201_CREATED, name="Create discipline")
async def create_disciplines(body: DisciplineModel, db: Session = Depends(get_db)):
    group = await repository_disciplines.create_discipline(body, db)
    return group


@router.get(
    "/",
    response_model=List[DisciplineResponse],
    name="List of all disciplines",
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
