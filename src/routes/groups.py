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
from src.repository import groups as repository_group
from src.repository.dependencies import get_group_by_id
from src.database.models import Group
from src.schemas.groups import GroupModel, GroupResponse


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


@router.put("/{group_id}", name="Update group by id")
async def update_group(
    body: GroupModel,
    group: Group = Depends(get_group_by_id),
    db: Session = Depends(get_db),
):
    group = await repository_group.update_group(body, group, db)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id: {group} not found",
        )
    return group


@router.delete(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="Delete group by id",
)
async def delete_group(
    group: Group = Depends(get_group_by_id),
    db: Session = Depends(get_db),
) -> None:

    group = await repository_group.delete_group(group, db)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group not found",
        )
