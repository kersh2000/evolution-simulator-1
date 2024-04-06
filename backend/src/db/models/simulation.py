from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP
from ..db import Base
from sqlalchemy.sql import func

class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    is_private = Column(Boolean, nullable=False, default=True)
    # Additional columns
    environment_id = Column(Integer, ForeignKey("environments.id", ondelete="CASCADE"), nullable=False)
    dogma_id = Column(Integer, ForeignKey("dogmas.id", ondelete="CASCADE"), nullable=False)
    # Default columns
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    edited_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())