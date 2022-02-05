from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status

def get_all(db: Session): 
    blogs = db.query(models.Blog).all()
    return blogs

def create(db: Session, request: schemas.Blog):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete(id:int,db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=404, detail=f"Blog with id {id} not found")
    # db.delete(blog)
    blog.delete(synchronize_session=False)
    db.commit()
    return 'deleted'

def update(id:int,request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=404, detail=f"Blog with id {id} not found")
    blog.update(request.dict())
    db.commit()
    return 'updated'

def show(id:int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=404, detail=f"Blog with id {id} not found")
    blog.update(request.dict())
    db.commit()
    return 'updated'