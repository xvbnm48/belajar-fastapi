from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# create engine path: blog/database.py
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# create engine with SQLALCHEMY_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

# make session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# make connection to database
Base = declarative_base()
