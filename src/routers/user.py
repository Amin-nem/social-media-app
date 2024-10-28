from fastapi import status, HTTPException, Depends, APIRouter
from .. import models,schema,utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix="/users",
    tags=['users']
)

@router.get('/',response_model=List[schema.UserOut])
def get_all_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.post('/',response_model=schema.UserOut)
def create_users(user:schema.UserCreate, db:Session = Depends(get_db)):


    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}',response_model=schema.UserOut)
def get_user(id:int,db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"user with id {id} doesn't exist")
    return user