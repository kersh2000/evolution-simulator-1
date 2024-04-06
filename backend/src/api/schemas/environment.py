import datetime
from pydantic import BaseModel

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