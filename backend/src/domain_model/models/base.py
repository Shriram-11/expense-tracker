from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime
from datetime import datetime, timezone


def utc_now():
    """Return current UTC datetime with timezone awareness."""
    return datetime.now(timezone.utc)


# Create the base class for all models
Base = declarative_base()


class BaseModel(Base):
    """Base model with common fields for all models."""

    __abstract__ = True

    created_at = Column(DateTime(timezone=True),
                        default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True),
                        default=utc_now, onupdate=utc_now, nullable=False)
