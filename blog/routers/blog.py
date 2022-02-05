from fastapi import APIRouter, Depends, HTTPException, status
from .. import models, schemas
from typing import List
from .. import database
from sqlalchemy.orm import Session

router = APIRouter()

get_db = database.get_db

@router.get('/blog', response_model=List[schemas.ShowBlog], tags=['Blog'])
def all(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/blog', status_code=status.HTTP_200_OK, tags=['Blog'])
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    # return {'title': request.title, 'body': request.body}
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete('/blog/{id}', status_code=status.HTTP_200_OK,  tags=['Blog'])
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


@router.put('/blog/{id}', status_code=status.HTTP_200_OK, tags=['Blog'])
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


# @router.get('/blog', response_model=List[schemas.ShowBlog], tags=['Blog'])
# def all(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs


@router.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['Blog'])
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=404, detail=f"Blog with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f'blog with id {id} not found'}
    return blog
