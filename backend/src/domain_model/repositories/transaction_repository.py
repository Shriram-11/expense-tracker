from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from .base_repository import BaseRepository
from src.domain_model.models.transaction import Transaction


class TransactionRepository(BaseRepository[Transaction]):

    def __init__(self):
        super().__init__(Transaction)

    # -------------------------
    # Basic Filters
    # -------------------------

    async def get_by_date_range(
        self,
        session: AsyncSession,
        start_date: date,
        end_date: date
    ) -> List[Transaction]:

        stmt = select(Transaction).where(
            Transaction.transaction_date.between(start_date, end_date)
        ).order_by(Transaction.transaction_date)

        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_by_month(
        self,
        session: AsyncSession,
        year: int,
        month: int
    ) -> List[Transaction]:

        stmt = select(Transaction).where(
            func.extract("year", Transaction.transaction_date) == year,
            func.extract("month", Transaction.transaction_date) == month
        )

        result = await session.execute(stmt)
        return result.scalars().all()

    # -------------------------
    # Aggregations
    # -------------------------

    async def get_total_by_type_in_range(
        self,
        session: AsyncSession,
        start_date: date,
        end_date: date,
        txn_type: str
    ) -> float:

        stmt = select(
            func.coalesce(func.sum(Transaction.amount), 0)
        ).where(
            and_(
                Transaction.transaction_date.between(start_date, end_date),
                Transaction.type == txn_type
            )
        )

        result = await session.execute(stmt)
        return result.scalar_one()

    async def get_category_breakdown(
        self,
        session: AsyncSession,
        start_date: date,
        end_date: date,
        txn_type: str = "expense"
    ):

        stmt = select(
            Transaction.category,
            func.sum(Transaction.amount).label("total")
        ).where(
            and_(
                Transaction.transaction_date.between(start_date, end_date),
                Transaction.type == txn_type
            )
        ).group_by(Transaction.category)

        result = await session.execute(stmt)
        return result.all()

    async def get_daily_totals_for_month(
        self,
        session: AsyncSession,
        year: int,
        month: int
    ):

        stmt = select(
            Transaction.transaction_date,
            func.sum(Transaction.amount).label("total")
        ).where(
            func.extract("year", Transaction.transaction_date) == year,
            func.extract("month", Transaction.transaction_date) == month,
            Transaction.type == "expense"
        ).group_by(Transaction.transaction_date).order_by(Transaction.transaction_date)

        result = await session.execute(stmt)
        return result.all()

    # -------------------------
    # Recurring Support
    # -------------------------

    async def recurring_exists_for_month(
        self,
        session: AsyncSession,
        category: str,
        amount: float,
        year: int,
        month: int
    ) -> bool:

        stmt = select(Transaction.id).where(
            and_(
                Transaction.category == category,
                Transaction.amount == amount,
                func.extract("year", Transaction.transaction_date) == year,
                func.extract("month", Transaction.transaction_date) == month,
                Transaction.is_recurring_generated == True
            )
        )

        result = await session.execute(stmt)
        return result.scalar_one_or_none() is not None
