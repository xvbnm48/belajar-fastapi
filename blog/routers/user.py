from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from .. import database,schemas,models
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..repository import user

router = APIRouter(
    tags=["User"],
    prefix="/user"
)
get_db = database.get_db

@router.post('/', status_code=status.HTTP_200_OK)
def create(request: schemas.User, db: Session = Depends(get_db)):
    # hashed_password = pwd_context.hash(request.password)
    return user.create(request, db)


# @router.get('/users', status_code=status.HTTP_200_OK)
# def all(db: Session = Depends(get_db)):
#     users = db.query(models.User).all()
#     return users


@router.get('/{id}', status_code=200, response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)
