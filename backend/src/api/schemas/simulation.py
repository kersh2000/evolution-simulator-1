import datetime
from typing import Optional
from pydantic import BaseModel, Field
from .environment import EnvironmentBase
from .dogma import DogmaBase

class SimulationBase(BaseModel):
    name: str
    is_private: bool
    environment_id: int
    dogma_id: int

    class Config:
        from_attributes = True

class SimulationCreation(SimulationBase):
    owner_id: int

class SimulationResponse(SimulationBase):
    created_at: datetime.datetime
    edited_at: datetime.datetime

class SimulationFullResponse(SimulationResponse):
    environment: EnvironmentBase
    dogma: DogmaBase

class SimulationUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    is_private: Optional[bool] = Field(default=None)
    environment_id: Optional[int] = Field(default=None)
    dogma_id: Optional[int] = Field(default=None)

    class Config:
        from_attributes = True