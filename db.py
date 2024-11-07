from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

url = 'sqlite:///./sqlalchemy_example.db'
engine = create_engine(url, connect_args={"check_same_thread": False}, echo=False)
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = DBSession()

