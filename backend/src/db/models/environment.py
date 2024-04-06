from sqlalchemy import Column, Float, ForeignKey, Integer, String, Boolean, TIMESTAMP
from ..db import Base
from sqlalchemy.sql import func

class Environment(Base):
    __tablename__ = "environments"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    is_private = Column(Boolean, nullable=False, default=True)
    # Additional columns
    base_mutation_rate = Column(Float, default=0.025)
    width = Column(Integer, nullable=False, default=50)
    height = Column(Integer, nullable=False, default=50)
    food_spawn_rate = Column(Float, nullable=False, default=0.03)
    food_spawn_amount = Column(Float, nullable=False, default=531441)
    concentration_limit = Column(Float, nullable=False, default=0.0001)
    diffusion_rate = Column(Float, nullable=False, default=1)
    default_num_of_blocks = Column(Integer, nullable=False, default=200)
    # Default columns
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    edited_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())