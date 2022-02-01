
from telnetlib import STATUS
from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from pydantic import BaseModel
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .hashing import Hash

app = FastAPI()

# migration database
models.Base.metadata.create_all(engine)


def get_db():
    """
    Get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_200_OK, tags=['Blog'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    # return {'title': request.title, 'body': request.body}
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}', status_code=status.HTTP_200_OK,  tags=['Blog'])
def destroy(id, db: Session = Depends(get_db)):
    # blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # if blog is None:
    #     raise HTTPException(status_code=404, detail="Blog not found")
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=404, detail=f"Blog with id {id} not found")
    # db.delete(blog)
    blog.delete(synchronize_session=False)
    db.commit()
    return 'deleted'


@app.put('/blog/{id}', status_code=status.HTTP_200_OK, tags=['Blog'])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    # blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # if blog is None:
    #     raise HTTPException(status_code=404, detail="Blog not found")
    # blog.title = request.title
    # blog.body = request.body
    # db.commit()
    # return blog
    # db.query(models.Blog).filter(models.Blog.id == id).update(
    #     {'title': request.title, 'body': request.body})
    # db.commit()
    # return 'updated'
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=404, detail=f"Blog with id {id} not found")
    blog.update(request.dict())
    db.commit()
    return 'updated'


@app.get('/blog', response_model=List[schemas.ShowBlog], tags=['Blog'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['Blog'])
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=404, detail=f"Blog with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f'blog with id {id} not found'}
    return blog


@app.post('/user', status_code=status.HTTP_200_OK, tags=['User'])
def create(request: schemas.User, db: Session = Depends(get_db)):
    # hashed_password = pwd_context.hash(request.password)
    new_user = models.User(
        name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/users', status_code=status.HTTP_200_OK, tags=['User'])
def all(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get('/user/{id}', status_code=200, response_model=schemas.ShowUser, tags=['User'])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user id {id} not available')
    return user
