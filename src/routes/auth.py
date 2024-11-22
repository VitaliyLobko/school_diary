from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter,
    Request,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.auth import create_access_token, hash_handler
from src.database.db import get_db
from src.repository import users as repository_user
from fastapi.templating import Jinja2Templates
from src.schemas.users import UserModel

router = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="templates")


@router.post("/signup")
async def signup(body: UserModel, db: Session = Depends(get_db)):
    exist_user = await repository_user.get_user_by_email(body.username, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    password = hash_handler.get_password_hash(body.password)
    new_user = await repository_user.create_user(body, password, db)
    return {"new_user": new_user.email}


@router.post("/login")
async def login(
    request: Request,
    body: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = await repository_user.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )
    if not hash_handler.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    access_token = await create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
    # return templates.TemplateResponse(
    #     "index.html",
    #     {
    #         "request": request,
    #         "title": "Home App",
    #         "access_token": access_token,
    #         "token_type": "bearer",
    #     },
    # )