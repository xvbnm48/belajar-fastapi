from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta
from .. import schemas, database, models , Token
from sqlalchemy.orm import Session
from ..hashing import Hash



router = APIRouter(
    tags=["Authentication"]
)


@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect email or password")
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
    # generate jwt token

    access_token = Token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}