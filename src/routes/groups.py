from typing import List
from fastapi import (
    Depends,
    HTTPException,
    status,
    Path,
    APIRouter,
    Query,
    Request,
    FastAPI,
)
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_201_CREATED
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.repository import groups as repository_group
from src.schemas import GroupModel, GroupResponse

router = APIRouter(prefix="/groups", tags=["groups"])

templates = Jinja2Templates(directory="templates")


@router.post("/", status_code=HTTP_201_CREATED, name="Create group")
async def create_group(body: GroupModel, db: Session = Depends(get_db)):
    group = await repository_group.create_group(body, db)
    return group


@router.get(
    "/",
    response_model=List[GroupResponse],
    name="List of all groups",
)
async def get_groups(
    request: Request,
    limit: int = Query(20, le=500),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    groups = await repository_group.get_groups(limit, offset, db)
    total_count = await repository_group.get_all(db)

    if groups is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")

    return templates.TemplateResponse(
        "groups.html",
        {
            "request": request,
            "groups": groups,
            "limit": limit,
            "offset": offset,
            "total_count": total_count,
            "title": "Groups",
        },
    )
