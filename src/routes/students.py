from typing import List, Annotated
from fastapi import Depends, HTTPException, status, Path, APIRouter, Query, Request
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_201_CREATED
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import Student
from src.schemas import (
    StudentModel,
    StudentsResponse,
    StudentIsActiveModel,
    StudentsResponseWithAvgGrade,
)
from src.repository import students as repository_students
from src.repository.dependencies import get_student_by_id

router = APIRouter(prefix="/students", tags=["students"])

templates = Jinja2Templates(directory="templates")


@router.post(
    "/",
    status_code=HTTP_201_CREATED,
    response_model=StudentsResponse,
    name="Create student",
)
async def create_student(body: StudentModel, db: Session = Depends(get_db)):
    student = await repository_students.create_student(body, db)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="something wrong"
        )

    return student


@router.get(
    "/",
    response_model=List[StudentsResponse],
    name="List of all students",
)
async def get_students(
    request: Request,
    search_by: str = "",
    limit: int = Query(20, le=500),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    students = await repository_students.get_students(search_by, limit, offset, db)
    total_count = await repository_students.get_all(db)
    if students is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="data not found"
        )

    return templates.TemplateResponse(
        "students.html",
        {
            "request": request,
            "students": students,
            "limit": limit,
            "offset": offset,
            "total_count": total_count,
            "title": "Students List",
        },
    )


@router.get(
    "/top_10_students",
    response_model=List[StudentsResponseWithAvgGrade],
    tags=["students"],
)
async def top_10_students(request: Request, db: Session = Depends(get_db)):
    students = await repository_students.get_top_10_students(db)
    if students is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="data not found"
        )
    return templates.TemplateResponse(
        "top_10_students.html",
        {"request": request, "students": students, "title": "Top 10 students"},
    )


@router.get(
    "/avg_grade",
    response_model=List[StudentsResponseWithAvgGrade],
    name="List of all students sorting by avg grade",
)
async def get_students_avg_grade(
    request: Request,
    limit: int = Query(20, le=500),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    students = await repository_students.get_students_avg_grade(limit, offset, db)
    total_count = await repository_students.get_all_avg_grade(db)
    if students is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="data not found"
        )

    return templates.TemplateResponse(
        "students_with_grades.html",
        {
            "request": request,
            "students": students,
            "limit": limit,
            "offset": offset,
            "total_count": total_count,
            "title": "Avg grades",
        },
    )


@router.get("/{student_id}", name="Get student by id")
async def get_student(
    request: Request,
    student_id: Annotated[int, Path(ge=1, lt=10_000)],
    db: Session = Depends(get_db),
):
    student = await repository_students.get_student_by_id(student_id, db)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id: {student_id} not found",
        )
    return templates.TemplateResponse(
        "student.html", {"request": request, "student": student, "title": "Student"}
    )


@router.put("/{student_id}", name="Update student by id")
async def update_student(
    body: StudentModel,
    student: Student = Depends(get_student_by_id),
    db: Session = Depends(get_db),
):
    student = await repository_students.update_student(body, student, db)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id: {student} not found",
        )
    return student


@router.patch("/{student_id}/is_active", name="Set status is_active by student id")
async def is_active_student(
    body: StudentIsActiveModel,
    student: Student = Depends(get_student_by_id),
    db: Session = Depends(get_db),
):
    student = await repository_students.is_active_student(body, student, db)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student {student} not found",
        )
    return student


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="Delete student by id",
)
async def delete_student(
    student: Student = Depends(get_student_by_id), db: Session = Depends(get_db)
) -> None:

    student = await repository_students.delete_student(student, db)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student not found",
        )
