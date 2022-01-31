from sqlalchemy import Column, Integer, String
from .database import Base

# create models for database


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    body = Column(String)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))