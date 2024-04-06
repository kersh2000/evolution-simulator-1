from datetime import datetime, timedelta
from jose import JWTError, jwt
from .config import jwt_secret, jwt_algorithm, jwt_expire_mins
from ..schemas import schemas

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=jwt_expire_mins)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_secret, algorithm=jwt_algorithm)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm])
        id: int = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
