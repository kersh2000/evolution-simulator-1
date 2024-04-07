from fastapi import APIRouter, HTTPException, status, Depends
from ..schemas import schemas
from ...db.models import models
from ...db.db import get_db
from ..middleware import middleware
from sqlalchemy.orm import Session

router = APIRouter(prefix="/dogma", tags=['Dogma'])

@router.get("/", response_model=list[schemas.DogmaResponse])
def get_dogmas(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    dogmas = db.query(models.Dogma).filter(models.Dogma.owner_id == current_user.id).all()
    return dogmas

@router.get("/public", response_model=list[schemas.DogmaResponse])
def get_public_dogmas(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    dogmas = db.query(models.Dogma).filter(models.Dogma.is_private == False).all()
    return dogmas

# Only works for admin account, fetches public and private simulations
@router.get("/all", response_model=list[schemas.DogmaResponse])
def get_all_dogmas(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    if (current_user.id != 1):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorised access, please contact admin/owner for further detail if access is needed.")
    dogmas = db.query(models.Dogma).filter(models.Dogma.owner_id == 1).all()
    return dogmas

@router.get("/{id}", response_model=schemas.DogmaResponse)
def get_dogma(dogma: models.Dogma = Depends(middleware.get_current_dogma)):
    return dogma

@router.post("/", response_model=schemas.DogmaResponse)
def create_dogma(dogma: schemas.DogmaCreation ,db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    created_dogma = models.Dogma(**dogma.model_dump())
    created_dogma.owner_id = current_user.id
    db.add(created_dogma)
    db.commit()
    db.refresh()
    return created_dogma

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dogma(dogma: models.Dogma = Depends(middleware.get_current_dogma), db: Session = Depends(get_db)):
    db.delete(dogma)
    db.commit()

@router.put("/{id}", response_model=schemas.DogmaResponse)
def update_dogma(dogma: schemas.DogmaCreation, old_dogma: models.Dogma = Depends(middleware.get_current_dogma), db: Session = Depends(get_db)):
    query = db.query(models.Dogma).filter(models.Dogma.id == old_dogma.id)
    query.update(dogma.model_dump(), synchronize_session=False)
    db.commit()

    updated_dogma = query.first()
    return updated_dogma

@router.patch("/{id}", response_model=schemas.DogmaResponse)
def patch_dogma(id: int, dogma_data: schemas.DogmaUpdate, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    query = db.query(models.Dogma).filter(models.Dogma.id == id)
    old_dogma = query.first()

    if not old_dogma:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Dogma was not found.")

    if old_dogma.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "No corresponding dogma were found.")
    
    updated_data = dogma_data.model_dump(exclude_unset=True)
    if not updated_data:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No fields provided.")

    query.update(updated_data, synchronize_session=False)
    db.commit()

    updated_dogma = query.first()
    return updated_dogma
