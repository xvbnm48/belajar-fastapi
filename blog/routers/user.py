from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from .. import database,schemas,models
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter()
get_db = database.get_db

@router.post('/user', status_code=status.HTTP_200_OK, tags=['User'])
def create(request: schemas.User, db: Session = Depends(get_db)):
    # hashed_password = pwd_context.hash(request.password)
    new_user = models.User(
        name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/users', status_code=status.HTTP_200_OK, tags=['User'])
def all(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/user/{id}', status_code=200, response_model=schemas.ShowUser, tags=['User'])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user id {id} not available')
    return user
