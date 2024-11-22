from typing import List, Annotated
from fastapi import Depends, HTTPException, status, Path, APIRouter, Query, Request
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_201_CREATED
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import Student, Teacher
from src.schemas.teachers import (
    TeacherModel,
    TeachersResponse,
    TeachersIsActiveModel,
)
from src.repository import teachers as repository_teachers
from src.repository.dependencies import get_teacher_by_id

router = APIRouter(prefix="/teachers", tags=["teachers"])

templates = Jinja2Templates(directory="templates")


@router.post(
    "/",
    status_code=HTTP_201_CREATED,
    response_model=TeachersResponse,
    name="Create teacher",
)
async def create_teacher(body: TeacherModel, db: Session = Depends(get_db)):
    teacher = await repository_teachers.create_teacher(body, db)
    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="something wrong"
        )

    return teacher


@router.get(
    "/",
    response_model=List[TeachersResponse],
    name="List of all teachers",
)
async def get_teachers(
    request: Request,
    limit: int = Query(20, le=500),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    teachers = await repository_teachers.get_teachers(limit, offset, db)
    total_count = await repository_teachers.get_all(db)
    if teachers is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="data not found"
        )

    return templates.TemplateResponse(
        "teachers.html",
        {
            "request": request,
            "teachers": teachers,
            "limit": limit,
            "offset": offset,
            "total_count": total_count,
            "title": "Teacher List",
        },
    )


@router.get("/{teacher_id}", name="Get teacher by id")
async def get_teacher(
    request: Request,
    teacher: Teacher = Depends(get_teacher_by_id),
    db: Session = Depends(get_db),
):
    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Teacher {teacher} not found",
        )
    return templates.TemplateResponse(
        "teacher.html", {"request": request, "teacher": teacher, "title": "Student"}
    )


@router.put("/{teacher_id}", name="Update teacher by id")
async def update_teacher(
    body: TeacherModel,
    teacher: Teacher = Depends(get_teacher_by_id),
    db: Session = Depends(get_db),
):
    teacher = await repository_teachers.update_teacher(body, teacher, db)
    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Teacher {teacher} not found",
        )
    return teacher


@router.patch(
    "/{teacher_id}/is_active",
    response_model=TeachersResponse,
    name="Set status is_active by teacher id",
)
async def is_active_teacher(
    body: TeachersIsActiveModel,
    teacher: Student = Depends(get_teacher_by_id),
    db: Session = Depends(get_db),
):
    teacher = await repository_teachers.is_active_teacher(body, teacher, db)
    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Teacher {teacher} not found",
        )
    return teacher


@router.delete(
    "/{teacher_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="Delete student by id",
)
async def delete_student(
    teacher: Student = Depends(get_teacher_by_id), db: Session = Depends(get_db)
) -> None:

    teacher = await repository_teachers.delete_teacher(teacher, db)
    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student not found",
        )
