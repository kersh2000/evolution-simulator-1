from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import ARRAY
from ..db import Base
from sqlalchemy.sql import func

class Block(Base):
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    is_private = Column(Boolean, nullable=False, default=True)
    # Additional columns
    genome = Column(String, nullable=False)
    proteome = Column(ARRAY(String))
    colour = Column(String, nullable=False)
    energy = Column(Integer, nullable=False, default=1000000)
    x = Column(Integer)
    y = Column(Integer)
    # Default columns
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    edited_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())