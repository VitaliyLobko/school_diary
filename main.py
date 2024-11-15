import pathlib
import time
from _pydatetime import date
from datetime import datetime, timedelta
from random import choice, randint
import uvicorn
from faker import Faker
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import text
from starlette.responses import JSONResponse, HTMLResponse

from src.database.models import Teacher, Student, Discipline, Grade, Group
from src.database.db import get_db
from src.routes import students, groups, disciplines, grades


def date_range(start: date, end: date) -> list:
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result


app = FastAPI()

BASE_DIR = pathlib.Path(__file__).parent

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(students.router)
app.include_router(groups.router)
app.include_router(disciplines.router)
app.include_router(grades.router)


@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    during = time.time() - start_time
    response.headers["performance"] = str(during)
    return response


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "Home App"}
    )


@app.get("/healthchecker")
async def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("Select 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="DB is not worked")
        return {"message": "Welcome to FastAPI"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to db")


@app.get("/seed", tags=["seed"])
async def seed(db: Session = Depends(get_db)):
    disciplines = [
        "Вища математика",
        "Хімія",
        "Економіка підприємства",
        "Обчислювальна математика",
        "Історія України",
        "Теоретична механіка",
        "Менеджмент організацій",
        "Системне програмування",
    ]

    groups = ["ВВ1", "ДД33", "АА5"]

    fake = Faker()
    number_of_teachers = 5
    number_of_students = 50

    def seed_teachers():
        for _ in range(number_of_teachers):
            teacher = Teacher(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                dob=fake.date_of_birth(None, 18, 60),
            )
            db.add(teacher)
        db.commit()

    def seed_disciplines():
        teacher_ids = db.scalars(select(Teacher.id)).all()
        for discipline in disciplines:
            db.add(Discipline(name=discipline, teacher_id=choice(teacher_ids)))
        db.commit()

    def seed_groups():
        for group in groups:
            db.add(Group(name=group))
        db.commit()

    def seed_students():
        group_ids = db.scalars(select(Group.id)).all()
        for _ in range(number_of_students):
            student = Student(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                group_id=choice(group_ids),
                dob=fake.date_of_birth(None, 18, 60),
            )
            db.add(student)
        db.commit()

    def seed_grades():
        # дата початку навчального процесу
        start_date = datetime.strptime("2020-09-01", "%Y-%m-%d")
        # дата закінчення навчального процесу
        end_date = datetime.strptime("2021-05-25", "%Y-%m-%d")
        d_range = date_range(start=start_date, end=end_date)
        discipline_ids = db.scalars(select(Discipline.id)).all()
        student_ids = db.scalars(select(Student.id)).all()

        for d in d_range:  # пройдемося по кожній даті
            random_id_discipline = choice(discipline_ids)
            random_ids_student = [choice(student_ids) for _ in range(5)]
            # проходимося списком "везучих" студентів, додаємо їх до результуючого списку
            # і генеруємо оцінку
            for student_id in random_ids_student:
                grade = Grade(
                    grade=randint(1, 12),
                    date_of=d,
                    student_id=student_id,
                    discipline_id=random_id_discipline,
                )
                db.add(grade)
        db.commit()

    seed_teachers()
    seed_disciplines()
    seed_groups()
    seed_students()
    seed_grades()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8005)
