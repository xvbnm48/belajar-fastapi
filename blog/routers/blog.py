from fastapi import APIRouter, Depends, HTTPException, status
from .. import models, schemas
from typing import List
from .. import database
from sqlalchemy.orm import Session
from ..repository import blog

router = APIRouter(
    tags=["Blog"],
    prefix="/blog"
)

get_db = database.get_db

@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db)):
    return blog.get_all(db)

@router.post('/', status_code=status.HTTP_200_OK)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    # return {'title': request.title, 'body': request.body}
    return blog.create(db, request)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session = Depends(get_db)):
    # blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # if blog is None:
    #     raise HTTPException(status_code=404, detail="Blog not found")
   return blog.delete(id, db)


@router.put('/{id}', status_code=status.HTTP_200_OK)
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
    return blog.update(id, request, db)


# @router.get('/blog', response_model=List[schemas.ShowBlog])
# def all(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
    return blog.show(id,db)
