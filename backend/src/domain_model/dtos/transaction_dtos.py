from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from decimal import Decimal
from utils.constants import TransactionType, TransactionCategory


@dataclass
class TransactionBaseDto:
    """
    Base Transaction DTO containing common fields for all transaction DTOs.
    Maps to Transaction SQLAlchemy model fields.
    """
    amount: Decimal
    type: TransactionType
    category: TransactionCategory
    description: Optional[str] = None
    transaction_date: Optional[datetime] = None


@dataclass
class TransactionCreateDto(TransactionBaseDto):
    """
    DTO for creating a new transaction.
    Extends TransactionBaseDto - requires amount, type, category, and transaction_date.
    """
    pass


@dataclass
class TransactionUpdateDto(TransactionBaseDto):
    """
    DTO for updating an existing transaction.
    Extends TransactionBaseDto - all fields are optional for updates.
    """
    amount: Optional[Decimal] = None
    type: Optional[TransactionType] = None
    category: Optional[TransactionCategory] = None
    transaction_date: Optional[datetime] = None


@dataclass
class TransactionResponseDto(TransactionBaseDto):
    """
    DTO for transaction responses.
    Extends TransactionBaseDto with response-specific fields like id and timestamps.
    Includes database-generated timestamps.
    """
    id: int
    created_at: datetime
    updated_at: datetime
