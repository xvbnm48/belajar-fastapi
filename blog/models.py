from sqlalchemy import Column, Integer, String
from .database import Base

# create models for database


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    body = Column(String)
