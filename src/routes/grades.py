from typing import List
from fastapi import Depends, HTTPException, status, Path, APIRouter, Query, Request, FastAPI
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_201_CREATED
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas import GradeModel, GradeResponse
from src.repository import grades as repository_grade

router = APIRouter(prefix="/grades", tags=['grades'])

templates = Jinja2Templates(directory='templates')


@router.post("/", status_code=HTTP_201_CREATED, name="Create grade")
async def create_grade(body: GradeModel, db: Session = Depends(get_db)):
    group = await  repository_grade.create_grade(body, db)
    return group


@router.get("/", response_model=List[GradeResponse], name="List of all grades", )
async def get_grades(request: Request, limit: int = Query(20, le=500), offset: int = 0,
                     db: Session = Depends(get_db)):
    grades = await repository_grade.get_grades(limit, offset, db)
    total_count = await repository_grade.get_all(db)
    if grades is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')

    return templates.TemplateResponse("grades.html", {
        "request": request,
        "grades": grades,
        "limit": limit,
        "offset": offset,
        "total_count": total_count,
        "title": "Grades",
    })
