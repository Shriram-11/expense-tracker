from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime, date
from decimal import Decimal
from src.utils.constants import TransactionType, TransactionCategory


class TransactionBaseDto(BaseModel):
    amount: Decimal
    type: TransactionType
    category: TransactionCategory
    description: Optional[str] = None
    transaction_date: Optional[Union[date, datetime]] = None


class TransactionCreateDto(TransactionBaseDto):
    pass


class TransactionUpdateDto(BaseModel):
    amount: Optional[Decimal] = None
    type: Optional[TransactionType] = None
    category: Optional[TransactionCategory] = None
    description: Optional[str] = None
    transaction_date: Optional[Union[date, datetime]] = None


class TransactionResponseDto(TransactionBaseDto):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
