from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import  models
from .database import engine, get_db
from .routers import blog, user, authentication


app = FastAPI(
    title="Blog API",
    description="A simple blog API",
)

# migration database
models.Base.metadata.create_all(engine)

# router
app.include_router(blog.router, tags=['Blog'])
app.include_router(user.router, tags=['User'])
app.include_router(authentication.router, tags=['Authentication'])


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

