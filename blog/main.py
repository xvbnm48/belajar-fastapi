
from fastapi import FastAPI, Depends, status, Response, HTTPException
from pydantic import BaseModel
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

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


@app.post('/blog', status_code=status.HTTP_200_OK)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    # return {'title': request.title, 'body': request.body}
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code=status.HTTP_200_OK)
def destroy(id, db: Session  = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog)
    db.commit()
    return Response(status_code=204)

@app.get('/blog')
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=200)
def show(id: int,response: Response ,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f'blog with id {id} not found'}


    return blog
