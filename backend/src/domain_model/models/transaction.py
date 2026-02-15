from sqlalchemy import Column, Integer, Numeric, String, Date, Enum as SQLEnum
from datetime import date
from src.domain_model.models.base import BaseModel
from src.utils.constants import TransactionType, TransactionCategory


class Transaction(BaseModel):
    """Transaction model for the expense tracker."""

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(SQLEnum(TransactionType), nullable=False)
    category = Column(SQLEnum(TransactionCategory), nullable=False)
    description = Column(String(255), nullable=True)
    transaction_date = Column(
        Date, default=date.today, nullable=False)

    def __repr__(self):
        return (
            f"<Transaction(id={self.id}, amount={self.amount}, type={self.type}, "
            f"category={self.category}, transaction_date={self.transaction_date})>"
        )
