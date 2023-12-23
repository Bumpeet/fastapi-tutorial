from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models
from .. import schemas
from ..database import get_db
from ..utils import hashing


router = APIRouter(tags=["Users"])

@router.post("/signup", 
          status_code=status.HTTP_201_CREATED,
         # response_model=schemas.UserCreateResponse
          )
def create_user(credentials:schemas.UserCreate,
                db: Session = Depends(get_db)):
    hashed_pwd = hashing(credentials.password)
    credentials.password = hashed_pwd
    new_credentials = models.User(**credentials.model_dump())
    db.add(new_credentials)
    db.commit()
    db.refresh(new_credentials)

    return f'New user with has been created with email as: {new_credentials.email} and id: {new_credentials.id}. Please check you email for verification'


@router.get('/getUser/{id}', response_model=schemas.GetUserResponse)
def get_user(id:int, db:Session=Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id==id).first() #.all()

    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail=f'User with id - {id} is not found')
        
    return user