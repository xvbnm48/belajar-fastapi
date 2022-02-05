from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import  models
from .database import engine, get_db
from .routers import blog, user


app = FastAPI()

# migration database
models.Base.metadata.create_all(engine)

# router
app.include_router(blog.router, tags=['Blog'])
app.include_router(user.router, tags=['User'])


# def get_db():
#     """
#     Get database session
#     """
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#

