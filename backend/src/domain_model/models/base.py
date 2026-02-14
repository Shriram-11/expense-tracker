from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime
from datetime import datetime


# Create the base class for all models
Base = declarative_base()


class BaseModel(Base):
    """Base model with common fields for all models."""
    
    __abstract__ = True
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
