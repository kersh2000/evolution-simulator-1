import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class BlockBase(BaseModel):
    genome: str
    proteome: Optional[List[str]] = None
    colour: str
    energy: int
    x: Optional[int] = None
    y: Optional[int] = None

    class Config:
        from_attributes = True

class BlockCreation(BlockBase):
    name: str
    is_private: bool
    owner_id: int

class BlockResponse(BlockBase):
    id: int
    name: str
    is_private: bool
    created_at: datetime.datetime
    edited_at: datetime.datetime

class BlockUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    is_private: Optional[bool] = Field(default=None)
    genome: Optional[str] = Field(default=None)
    proteome: Optional[List[str]] = Field(default=None)
    colour: Optional[str] = Field(default=None)
    energy: Optional[int] = Field(default=None)
    x: Optional[int] = Field(default=None)
    y: Optional[int] = Field(default=None)