from datetime import date
from typing import List, Optional, Any

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain_model.repositories.base_repository import BaseRepository
from src.domain_model.models.transaction import Transaction
from src.utils.constants import TransactionType


class TransactionRepository(BaseRepository[Transaction]):

    def __init__(self):
        super().__init__(Transaction)

    # =========================================================
    # Generic Filtering
    # =========================================================

    async def filter_transactions(
        self,
        session: AsyncSession,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        year: Optional[int] = None,
        month: Optional[int] = None,
        txn_type: Optional[TransactionType] = None,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 30
    ) -> List[Transaction]:

        filters = []

        if start_date and end_date:
            filters.append(
                Transaction.transaction_date.between(start_date, end_date)
            )

        if year and month:
            filters.append(func.extract(
                "year", Transaction.transaction_date) == year)
            filters.append(func.extract(
                "month", Transaction.transaction_date) == month)

        if txn_type:
            filters.append(Transaction.type == txn_type)

        if category:
            filters.append(Transaction.category == category)

        stmt = select(Transaction)

        if filters:
            stmt = stmt.where(and_(*filters))

        stmt = stmt.order_by(Transaction.transaction_date.desc())
        stmt = stmt.offset(skip).limit(limit)

        result = await session.execute(stmt)
        return result.scalars().all()

    # =========================================================
    # Count
    # =========================================================

    async def count_transactions(
        self,
        session: AsyncSession,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        year: Optional[int] = None,
        month: Optional[int] = None,
        txn_type: Optional[TransactionType] = None,
        category: Optional[str] = None
    ) -> int:

        filters = []

        if start_date and end_date:
            filters.append(
                Transaction.transaction_date.between(start_date, end_date)
            )

        if year and month:
            filters.append(func.extract(
                "year", Transaction.transaction_date) == year)
            filters.append(func.extract(
                "month", Transaction.transaction_date) == month)

        if txn_type:
            filters.append(Transaction.type == txn_type)

        if category:
            filters.append(Transaction.category == category)

        stmt = select(func.count(Transaction.id))

        if filters:
            stmt = stmt.where(and_(*filters))

        result = await session.execute(stmt)
        return result.scalar_one()

    # =========================================================
    # Aggregations
    # =========================================================

    async def sum_amount(
        self,
        session: AsyncSession,
        start_date: date,
        end_date: date,
        txn_type: Optional[TransactionType] = None
    ) -> float:

        filters = [
            Transaction.transaction_date.between(start_date, end_date)
        ]

        if txn_type:
            filters.append(Transaction.type == txn_type)

        stmt = select(
            func.coalesce(func.sum(Transaction.amount), 0)
        ).where(and_(*filters))

        result = await session.execute(stmt)
        return result.scalar_one()

    async def group_sum_by_field(
        self,
        session: AsyncSession,
        field: Any,
        start_date: date,
        end_date: date,
        txn_type: Optional[TransactionType] = None
    ):

        filters = [
            Transaction.transaction_date.between(start_date, end_date)
        ]

        if txn_type:
            filters.append(Transaction.type == txn_type)

        stmt = (
            select(
                field,
                func.sum(Transaction.amount).label("total")
            )
            .where(and_(*filters))
            .group_by(field)
        )

        result = await session.execute(stmt)
        return result.all()

    # =========================================================
    # Recurring Support
    # =========================================================

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
