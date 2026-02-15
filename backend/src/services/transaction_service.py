from calendar import monthrange
from datetime import date, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain_model.models.transaction import Transaction
from src.domain_model.repositories.transaction_repository import TransactionRepository
from src.domain_model.dtos.transaction_dtos import (
    TransactionCreateDto,
    TransactionUpdateDto,
    TransactionResponseDto,
    MonthlySummaryDto,
    WeeklySummaryDto,
    CategoryBreakdownDto,
    CategoryBreakdownItemDto,
    ProjectionSummaryDto,
)
from src.domain_model.dtos.base_dtos import PaginatedResponseDto
from src.utils.constants import TransactionType
from src.utils.exceptions import ServiceException


class TransactionService:

    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    @staticmethod
    def _normalize_transaction_date(value):
        if value is None:
            return date.today()
        if isinstance(value, datetime):
            return value.date()
        return value

    @staticmethod
    def _get_month_window(year: int, month: int):
        start = date(year, month, 1)
        end = date(year, month, monthrange(year, month)[1])
        return start, end

    async def create_transaction(self, session: AsyncSession, dto: TransactionCreateDto):
        if dto.amount <= 0:
            raise ServiceException("Amount must be greater than zero", 400)

        transaction = Transaction(
            amount=dto.amount,
            type=dto.type,
            category=dto.category,
            description=dto.description,
            transaction_date=self._normalize_transaction_date(dto.transaction_date),
        )

        try:
            created = await self.repository.create(session, transaction)
            return TransactionResponseDto.model_validate(created)
        except Exception as exc:
            raise ServiceException(f"Error creating transaction: {str(exc)}", 500) from exc

    async def get_paginated(
        self,
        session: AsyncSession,
        page_no: int,
        max_per_page: int
    ):
        try:
            skip = (page_no - 1) * max_per_page
            items = await self.repository.filter_transactions(
                session=session,
                skip=skip,
                limit=max_per_page
            )
            total = await self.repository.count_transactions(session)

            return PaginatedResponseDto(
                data=[TransactionResponseDto.model_validate(item) for item in items],
                total=total,
                page_no=page_no,
                max_per_page=max_per_page,
                current_count=len(items),
            )
        except Exception as exc:
            raise ServiceException(f"Error fetching transactions: {str(exc)}", 500) from exc

    async def get_by_id(self, session: AsyncSession, txn_id: int):
        try:
            transaction = await self.repository.get_by_id(session, txn_id)
            if not transaction:
                raise ServiceException("Transaction not found", 404)

            return TransactionResponseDto.model_validate(transaction)
        except ServiceException:
            raise
        except Exception as exc:
            raise ServiceException(f"Error retrieving transaction: {str(exc)}", 500) from exc

    async def update_transaction(
        self,
        session: AsyncSession,
        txn_id: int,
        dto: TransactionUpdateDto
    ):
        data = dto.model_dump(exclude_unset=True)

        if "amount" in data and data["amount"] is not None and data["amount"] <= 0:
            raise ServiceException("Amount must be greater than zero", 400)

        if "transaction_date" in data:
            data["transaction_date"] = self._normalize_transaction_date(data["transaction_date"])

        try:
            updated = await self.repository.update(
                session=session,
                obj_id=txn_id,
                data=data
            )
            if not updated:
                raise ServiceException("Transaction not found", 404)

            return TransactionResponseDto.model_validate(updated)
        except ServiceException:
            raise
        except Exception as exc:
            raise ServiceException(f"Error updating transaction: {str(exc)}", 500) from exc

    async def delete_transaction(self, session: AsyncSession, txn_id: int):
        try:
            deleted = await self.repository.delete(session, txn_id)
            if not deleted:
                raise ServiceException("Transaction not found", 404)
            return True
        except ServiceException:
            raise
        except Exception as exc:
            raise ServiceException(f"Error deleting transaction: {str(exc)}", 500) from exc

    async def get_monthly_summary(self, session: AsyncSession, year: int, month: int):
        try:
            start, end = self._get_month_window(year, month)
            total_expense = await self.repository.sum_amount(
                session, start, end, TransactionType.EXPENSE
            )
            total_income = await self.repository.sum_amount(
                session, start, end, TransactionType.INCOME
            )
            return MonthlySummaryDto(
                total_expense=total_expense,
                total_income=total_income,
                net_savings=total_income - total_expense,
            )
        except Exception as exc:
            raise ServiceException(f"Error fetching monthly summary: {str(exc)}", 500) from exc

    async def get_weekly_summary(self, session: AsyncSession):
        try:
            today = date.today()
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)

            total_expense = await self.repository.sum_amount(
                session, week_start, week_end, TransactionType.EXPENSE
            )
            total_income = await self.repository.sum_amount(
                session, week_start, week_end, TransactionType.INCOME
            )
            return WeeklySummaryDto(
                week_start=week_start,
                week_end=week_end,
                total_expense=total_expense,
                total_income=total_income,
                net_savings=total_income - total_expense,
            )
        except Exception as exc:
            raise ServiceException(f"Error fetching weekly summary: {str(exc)}", 500) from exc

    async def get_category_breakdown(self, session: AsyncSession, year: int, month: int):
        try:
            start, end = self._get_month_window(year, month)
            grouped = await self.repository.group_sum_by_field(
                session=session,
                field=Transaction.category,
                start_date=start,
                end_date=end,
                txn_type=TransactionType.EXPENSE
            )

            items = [
                CategoryBreakdownItemDto(category=category, total=total)
                for category, total in grouped
            ]
            items.sort(key=lambda item: item.total, reverse=True)
            total_expense = sum(item.total for item in items)

            return CategoryBreakdownDto(
                year=year,
                month=month,
                total_expense=total_expense,
                items=items,
            )
        except Exception as exc:
            raise ServiceException(f"Error fetching category breakdown: {str(exc)}", 500) from exc

    async def get_projection(self, session: AsyncSession, year: int, month: int):
        try:
            today = date.today()
            start, end = self._get_month_window(year, month)
            total_days = end.day

            if today < start:
                days_passed = 0
                spent_so_far = 0
            elif today > end:
                days_passed = total_days
                spent_so_far = await self.repository.sum_amount(
                    session, start, end, TransactionType.EXPENSE
                )
            else:
                days_passed = today.day
                spent_so_far = await self.repository.sum_amount(
                    session, start, today, TransactionType.EXPENSE
                )

            projected = 0 if days_passed == 0 else (spent_so_far / days_passed) * total_days

            return ProjectionSummaryDto(
                spent_so_far=spent_so_far,
                projected_month_end=projected,
                days_passed=days_passed,
                total_days=total_days,
            )
        except Exception as exc:
            raise ServiceException(f"Error fetching projection: {str(exc)}", 500) from exc
