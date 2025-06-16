import datetime
from typing import Optional
from pydantic import BaseModel, Field

class EnvironmentBase(BaseModel):
    name: str
    is_private: bool
    base_mutation_rate: int
    width: int
    height: int
    food_spawn_rate: int
    food_spawn_amount: int
    concentration_limit: int
    diffusion_rate: int
    default_num_of_blocks: int

    class Config:
        from_attributes = True

class EnvironmentResponse(EnvironmentBase):
    created_at: datetime.datetime
    edited_at: datetime.datetime

class EnvironmentCreation(EnvironmentBase):
    owner_id: int

class EnvironmentUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    is_private: Optional[bool] = Field(default=None)
    base_mutation_rate: Optional[float] = Field(default=None)
    width: Optional[int] = Field(default=None)
    height: Optional[int] = Field(default=None)
    food_spawn_rate: Optional[int] = Field(default=None)
    food_spawn_amount: Optional[int] = Field(default=None)
    concentration_limit: Optional[int] = Field(default=None)
    diffusion_rate: Optional[int] = Field(default=None)
    default_num_of_blocks: Optional[int] = Field(default=None)