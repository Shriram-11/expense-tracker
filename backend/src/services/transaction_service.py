from datetime import datetime, date, timedelta, timezone
from calendar import monthrange
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain_model.models.transaction import Transaction
from src.domain_model.models.base import utc_now
from src.domain_model.repositories.transaction_repository import TransactionRepository
from src.domain_model.dtos.transaction_dtos import (
    TransactionCreateDto,
    TransactionUpdateDto,
    TransactionResponseDto
)
from src.domain_model.dtos.base_dtos import ApiResponseDto, PaginatedResponseDto


class TransactionService:

    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    # =========================================================
    # CREATE
    # =========================================================

    async def create_transaction(self, session: AsyncSession, dto: TransactionCreateDto):

        try:
            if dto.amount <= 0:
                return ApiResponseDto(
                    data=None,
                    success=False,
                    message="Amount must be greater than zero"
                )

            # Extract date from transaction_date (handles both datetime and date objects)
            if dto.transaction_date:
                if isinstance(dto.transaction_date, datetime):
                    txn_date = dto.transaction_date.date()
                else:
                    txn_date = dto.transaction_date
            else:
                txn_date = date.today()

            transaction = Transaction(
                amount=dto.amount,
                type=dto.type,
                category=dto.category,
                description=dto.description,
                transaction_date=txn_date
            )

            created = await self.repository.create(session, transaction)

            return ApiResponseDto(
                data=TransactionResponseDto.model_validate(created),
                success=True,
                message="Transaction created successfully"
            )

        except Exception as e:
            return ApiResponseDto(
                data=None,
                success=False,
                message=f"Error creating transaction: {str(e)}"
            )

    # =========================================================
    # PAGINATION
    # =========================================================

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
                data=[TransactionResponseDto.model_validate(t) for t in items],
                total=total,
                page_no=page_no,
                max_per_page=max_per_page,
                current_count=len(items)
            )

        except Exception as e:
            return ApiResponseDto(
                data=None,
                success=False,
                message=f"Error fetching transactions: {str(e)}"
            )

    # =========================================================
    # GET BY ID
    # =========================================================

    async def get_by_id(self, session: AsyncSession, txn_id: int):

        try:
            transaction = await self.repository.get_by_id(session, txn_id)

            if not transaction:
                return ApiResponseDto(
                    data=None,
                    success=False,
                    message="Transaction not found"
                )

            return ApiResponseDto(
                data=TransactionResponseDto.model_validate(transaction),
                success=True
            )

        except Exception as e:
            return ApiResponseDto(
                data=None,
                success=False,
                message=f"Error retrieving transaction: {str(e)}"
            )

    # =========================================================
    # UPDATE
    # =========================================================

    async def update_transaction(
        self,
        session: AsyncSession,
        txn_id: int,
        dto: TransactionUpdateDto
    ):
        try:
            data = dto.model_dump(exclude_unset=True)

            if "amount" in data and data["amount"] is not None and data["amount"] <= 0:
                return ApiResponseDto(
                    data=None,
                    success=False,
                    message="Amount must be greater than zero"
                )

            # Extract date from transaction_date if provided
            if "transaction_date" in data and data["transaction_date"] is not None:
                if isinstance(data["transaction_date"], datetime):
                    data["transaction_date"] = data["transaction_date"].date()

            updated = await self.repository.update(
                session=session,
                obj_id=txn_id,
                data=data
            )

            if not updated:
                return ApiResponseDto(
                    data=None,
                    success=False,
                    message="Transaction not found"
                )

            return ApiResponseDto(
                data=TransactionResponseDto.model_validate(updated),
                success=True,
                message="Transaction updated successfully"
            )

        except Exception as e:
            return ApiResponseDto(
                data=None,
                success=False,
                message=f"Error updating transaction: {str(e)}"
            )

    # =========================================================
    # DELETE
    # =========================================================

    async def delete_transaction(self, session: AsyncSession, txn_id: int):

        try:
            success = await self.repository.delete(session, txn_id)

            if not success:
                return ApiResponseDto(
                    data=None,
                    success=False,
                    message="Transaction not found"
                )

            return ApiResponseDto(
                data=None,
                success=True,
                message="Transaction deleted successfully"
            )

        except Exception as e:
            return ApiResponseDto(
                data=None,
                success=False,
                message=f"Error deleting transaction: {str(e)}"
            )

    # =========================================================
    # ANALYTICS
    # =========================================================

    async def get_monthly_summary(self, session: AsyncSession, year: int, month: int):

        try:
            start = date(year, month, 1)
            last_day = monthrange(year, month)[1]
            end = date(year, month, last_day)

            total_expense = await self.repository.sum_amount(
                session, start, end, "expense"
            )

            total_income = await self.repository.sum_amount(
                session, start, end, "income"
            )

            return {
                "total_expense": total_expense,
                "total_income": total_income,
                "net_savings": total_income - total_expense
            }

        except Exception as e:
            return {"error": str(e)}

    async def get_projection(self, session: AsyncSession, year: int, month: int):

        try:
            today = date.today()
            start = date(year, month, 1)

            total_days = monthrange(year, month)[1]
            days_passed = today.day

            spent_so_far = await self.repository.sum_amount(
                session, start, today, "expense"
            )

            if days_passed == 0:
                return 0

            avg_daily = spent_so_far / days_passed
            projected = avg_daily * total_days

            return {
                "spent_so_far": spent_so_far,
                "projected_month_end": projected
            }

        except Exception as e:
            return {"error": str(e)}
