from fastapi import Depends, HTTPException, status
from .auth import verify_access_token
from ...db.db import get_db
from ...db.models import models
from ..schemas import schemas
from ..schemas.schemas import UserResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status.HTTP_403_FORBIDDEN, "Invalid Credentials", {"WWW-Authenticate": "Bearer"}
    )
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if user is None:
        raise credentials_exception
    return UserResponse.model_validate(user)

def get_current_simulation(id: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(get_current_user)) -> models.Simulation:
    simulation = db.query(models.Simulation).filter(models.Simulation.id == id).first()

    if not simulation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Simulation not found.")
    
    if simulation.is_private and simulation.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this simulation.")

    return simulation

def get_current_block(id: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(get_current_user)) -> models.Block:
    block = db.query(models.Block).filter(models.Block.id == id).first()

    if not block:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Block not found.")
    
    if block.is_private and block.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this block.")

    return block