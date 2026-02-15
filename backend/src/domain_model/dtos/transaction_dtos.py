from pydantic import BaseModel
from typing import Optional, Union, List
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


class MonthlySummaryDto(BaseModel):
    total_expense: Decimal
    total_income: Decimal
    net_savings: Decimal


class WeeklySummaryDto(BaseModel):
    week_start: date
    week_end: date
    total_expense: Decimal
    total_income: Decimal
    net_savings: Decimal


class CategoryBreakdownItemDto(BaseModel):
    category: TransactionCategory
    total: Decimal


class CategoryBreakdownDto(BaseModel):
    year: int
    month: int
    total_expense: Decimal
    items: List[CategoryBreakdownItemDto]


class ProjectionSummaryDto(BaseModel):
    spent_so_far: Decimal
    projected_month_end: Decimal
    days_passed: int
    total_days: int
