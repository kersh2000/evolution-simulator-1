from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...db.db import get_db
from ...db.models import models
from .. import utils
from ..middleware.middleware import create_access_token


router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid Credentials")
    
    match = utils.verify_password(user_credentials.password, user.password)

    if not match:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid Credentials")
    
    access_token = create_access_token({"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}