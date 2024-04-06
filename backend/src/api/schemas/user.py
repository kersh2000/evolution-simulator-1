import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class UserLoginBase(BaseModel):
    username: str
    password: str