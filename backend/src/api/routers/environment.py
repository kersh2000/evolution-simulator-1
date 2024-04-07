from fastapi import APIRouter, HTTPException, status, Depends
from ..schemas import schemas
from ...db.models import models
from ...db.db import get_db
from ..middleware import middleware
from sqlalchemy.orm import Session

router = APIRouter(prefix="/environment", tags=['Environments'])

@router.get("/", response_model=list[schemas.EnvironmentResponse])
def get_environments(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    environments = db.query(models.Environment).filter(models.Environment.owner_id == current_user.id).all()
    return environments

@router.get("/public", response_model=list[schemas.EnvironmentResponse])
def get_public_environments(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    environments = db.query(models.Environment).filter(models.Environment.is_private == False).all()
    return environments

# Only works for admin account, fetches public and private simulations
@router.get("/all", response_model=list[schemas.EnvironmentResponse])
def get_all_environments(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    if (current_user.id != 1):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorised access, please contact admin/owner for further detail if access is needed.")
    environments = db.query(models.Environment).filter(models.Environment.owner_id == 1).all()
    return environments

@router.get("/{id}", response_model=schemas.EnvironmentResponse)
def get_environment(environment: models.Environment = Depends(middleware.get_current_environment)):
    return environment

@router.post("/", response_model=schemas.EnvironmentResponse)
def create_environment(environment: schemas.EnvironmentCreation ,db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    created_environment = models.Environment(**environment.model_dump())
    created_environment.owner_id = current_user.id
    db.add(created_environment)
    db.commit()
    db.refresh()
    return created_environment

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_environment(environment: models.Environment = Depends(middleware.get_current_environment), db: Session = Depends(get_db)):
    db.delete(environment)
    db.commit()

@router.put("/{id}", response_model=schemas.EnvironmentResponse)
def update_environment(environment: schemas.EnvironmentCreation, old_environment: models.Environment = Depends(middleware.get_current_environment), db: Session = Depends(get_db)):
    query = db.query(models.Environment).filter(models.Environment.id == old_environment.id)
    query.update(environment.model_dump(), synchronize_session=False)
    db.commit()

    updated_environment = query.first()
    return updated_environment

@router.patch("/{id}", response_model=schemas.EnvironmentResponse)
def patch_environment(id: int, environment_data: schemas.EnvironmentUpdate, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    query = db.query(models.Environment).filter(models.Environment.id == id)
    old_environment = query.first()

    if not old_environment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Environment was not found.")

    if old_environment.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "No corresponding environment were found.")
    
    updated_data = environment_data.model_dump(exclude_unset=True)
    if not updated_data:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No fields provided.")

    query.update(updated_data, synchronize_session=False)
    db.commit()

    updated_environment = query.first()
    return updated_environment
