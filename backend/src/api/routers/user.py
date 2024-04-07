from fastapi import APIRouter, HTTPException, status, Depends
from ..schemas import schemas
from ...db.models import models
from ...db.db import get_db
from .. import utils
from ..middleware import middleware
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def register(user: schemas.UserBase, db: Session = Depends(get_db)):

    #Hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    db.delete(current_user)
    db.commit()

@router.put("/", response_model=schemas.UserResponse)
def update_user(user: schemas.UserChange, current_user: models.User = Depends(middleware.get_current_user), db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.id == current_user.id)
    existing_user = query.first()
    match = utils.verify_password(user.old_password, existing_user.password)
    if not match:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect credentials.")

    query.update({
        "email": user.email,
        "username": user.username,
        "password": user.new_password,
        "is_private": user.is_private
    }, synchronize_session=False) 
    db.commit()

    updated_user = query.first()
    return updated_user
