import configparser
import pathlib
from datetime import datetime, timedelta
from typing import Optional

import redis
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from src.database.db import get_db
from src.repository import users as repository_user
from src.database.models import User
import pickle

from src.repository.users import get_user_by_email

config = configparser.ConfigParser()
file_config = pathlib.Path(__file__).parent.parent.joinpath("conf/config.ini")
config.read(file_config)

SECRET_KEY = config.get("AUTH", "SECRET_KEY")
ALGORITHM = config.get("AUTH", "ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

r = redis.Redis(host="localhost", port=6379, db=0)


class Hash:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)


hash_handler = Hash()


async def create_access_token(data: dict, expires_delta: Optional[float] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
    encoded_access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_access_token


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("scope") == "access_token":
            email = payload.get("sub")
            if email is None:
                raise credentials_exception
        else:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    # user = await repository_user.get_user_by_email(email, db)
    user = r.get(f"user:{email}")
    if user is None:
        user = await repository_user.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        r.set(f"user:{email}", pickle.dumps(user))
        r.expire(f"user:{email}", 900)
    else:
        user = pickle.loads(user)

    if user is None:
        raise credentials_exception
    return user


def create_email_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "email_token"})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_email_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["scope"] == "email_token":
            email = payload["sub"]
            return email
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid scope for token"
        )
    except JWTError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid token for email verification",
        )
