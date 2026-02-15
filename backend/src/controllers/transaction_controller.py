from fastapi import APIRouter, Depends, Query, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.dependencies import (
    get_transaction_service,
    get_db_session
)

from src.services.transaction_service import TransactionService
from src.domain_model.dtos.transaction_dtos import (
    TransactionCreateDto,
    TransactionUpdateDto,
    TransactionResponseDto
)
from src.domain_model.dtos.base_dtos import ApiResponseDto, PaginatedResponseDto


router = APIRouter(
    prefix="/api/v1/transactions",
    tags=["Transactions"]
)


@router.post(
    "/",
    response_model=ApiResponseDto[TransactionResponseDto],
    status_code=status.HTTP_201_CREATED
)
async def create_transaction(
    dto: TransactionCreateDto,
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    return await service.create_transaction(session, dto)


@router.get(
    "/",
    response_model=PaginatedResponseDto[TransactionResponseDto]
)
async def get_transactions(
    page_no: int = Query(1, ge=1),
    max_per_page: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    return await service.get_paginated(session, page_no, max_per_page)


@router.get(
    "/{txn_id}",
    response_model=ApiResponseDto[TransactionResponseDto]
)
async def get_transaction_by_id(
    txn_id: int = Path(..., gt=0),
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    return await service.get_by_id(session, txn_id)


@router.put(
    "/{txn_id}",
    response_model=ApiResponseDto[TransactionResponseDto]
)
async def update_transaction(
    txn_id: int = Path(..., gt=0),
    dto: TransactionUpdateDto = ...,
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    return await service.update_transaction(session, txn_id, dto)


@router.delete(
    "/{txn_id}",
    response_model=ApiResponseDto[bool]
)
async def delete_transaction(
    txn_id: int = Path(..., gt=0),
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    return await service.delete_transaction(session, txn_id)


@router.get("/summary/monthly")
async def get_monthly_summary(
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    return await service.get_monthly_summary(session, year, month)


@router.get("/summary/weekly")
async def get_weekly_summary(
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    return await service.get_weekly_summary(session)


@router.get("/summary/category")
async def get_category_breakdown(
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    return await service.get_category_breakdown(session, year, month)


@router.get("/summary/projection")
async def get_projection(
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    return await service.get_projection(session, year, month)
