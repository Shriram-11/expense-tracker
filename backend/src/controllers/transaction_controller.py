from fastapi import APIRouter, Depends, Query, Path, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.dependencies import (
    get_transaction_service,
    get_db_session
)
from src.utils.exceptions import ServiceException
from src.utils.exception_handler import ControllerExceptionHandler
from src.services.transaction_service import TransactionService
from src.domain_model.dtos.transaction_dtos import (
    TransactionCreateDto,
    TransactionUpdateDto,
    TransactionResponseDto,
    MonthlySummaryDto,
    WeeklySummaryDto,
    CategoryBreakdownDto,
    ProjectionSummaryDto,
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
    response: Response,
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    try:
        data = await service.create_transaction(session, dto)
        return ApiResponseDto(
            data=data,
            success=True,
            message="Transaction created successfully"
        )
    except ServiceException as exc:
        return await ControllerExceptionHandler.handle_service_exception(response, session, exc)
    except Exception:
        return await ControllerExceptionHandler.handle_unexpected_exception(response, session)


@router.get(
    "/",
    response_model=ApiResponseDto[PaginatedResponseDto[TransactionResponseDto]]
)
async def get_transactions(
    response: Response,
    page_no: int = Query(1, ge=1),
    max_per_page: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    try:
        paginated_data = await service.get_paginated(session, page_no, max_per_page)
        return ApiResponseDto(
            data=paginated_data,
            success=True,
            message="Transactions fetched successfully"
        )
    except ServiceException as exc:
        return await ControllerExceptionHandler.handle_service_exception(response, session, exc)
    except Exception:
        return await ControllerExceptionHandler.handle_unexpected_exception(response, session)


@router.get(
    "/{txn_id}",
    response_model=ApiResponseDto[TransactionResponseDto]
)
async def get_transaction_by_id(
    response: Response,
    txn_id: int = Path(..., gt=0),
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    try:
        data = await service.get_by_id(session, txn_id)
        return ApiResponseDto(
            data=data,
            success=True,
            message="Transaction fetched successfully"
        )
    except ServiceException as exc:
        return await ControllerExceptionHandler.handle_service_exception(response, session, exc)
    except Exception:
        return await ControllerExceptionHandler.handle_unexpected_exception(response, session)


@router.put(
    "/{txn_id}",
    response_model=ApiResponseDto[TransactionResponseDto]
)
async def update_transaction(
    response: Response,
    txn_id: int = Path(..., gt=0),
    dto: TransactionUpdateDto = ...,
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    try:
        data = await service.update_transaction(session, txn_id, dto)
        return ApiResponseDto(
            data=data,
            success=True,
            message="Transaction updated successfully"
        )
    except ServiceException as exc:
        return await ControllerExceptionHandler.handle_service_exception(response, session, exc)
    except Exception:
        return await ControllerExceptionHandler.handle_unexpected_exception(response, session)


@router.delete(
    "/{txn_id}",
    response_model=ApiResponseDto[bool]
)
async def delete_transaction(
    response: Response,
    txn_id: int = Path(..., gt=0),
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    try:
        data = await service.delete_transaction(session, txn_id)
        return ApiResponseDto(
            data=data,
            success=True,
            message="Transaction deleted successfully"
        )
    except ServiceException as exc:
        return await ControllerExceptionHandler.handle_service_exception(response, session, exc)
    except Exception:
        return await ControllerExceptionHandler.handle_unexpected_exception(response, session)


@router.get(
    "/summary/monthly",
    response_model=ApiResponseDto[MonthlySummaryDto]
)
async def get_monthly_summary(
    response: Response,
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    try:
        data = await service.get_monthly_summary(session, year, month)
        return ApiResponseDto(
            data=data,
            success=True,
            message="Monthly summary fetched successfully"
        )
    except ServiceException as exc:
        return await ControllerExceptionHandler.handle_service_exception(response, session, exc)
    except Exception:
        return await ControllerExceptionHandler.handle_unexpected_exception(response, session)


@router.get(
    "/summary/weekly",
    response_model=ApiResponseDto[WeeklySummaryDto]
)
async def get_weekly_summary(
    response: Response,
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    try:
        data = await service.get_weekly_summary(session)
        return ApiResponseDto(
            data=data,
            success=True,
            message="Weekly summary fetched successfully"
        )
    except ServiceException as exc:
        return await ControllerExceptionHandler.handle_service_exception(response, session, exc)
    except Exception:
        return await ControllerExceptionHandler.handle_unexpected_exception(response, session)


@router.get(
    "/summary/category",
    response_model=ApiResponseDto[CategoryBreakdownDto]
)
async def get_category_breakdown(
    response: Response,
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    try:
        data = await service.get_category_breakdown(session, year, month)
        return ApiResponseDto(
            data=data,
            success=True,
            message="Category breakdown fetched successfully"
        )
    except ServiceException as exc:
        return await ControllerExceptionHandler.handle_service_exception(response, session, exc)
    except Exception:
        return await ControllerExceptionHandler.handle_unexpected_exception(response, session)


@router.get(
    "/summary/projection",
    response_model=ApiResponseDto[ProjectionSummaryDto]
)
async def get_projection(
    response: Response,
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    session: AsyncSession = Depends(get_db_session),
    service: TransactionService = Depends(get_transaction_service)
):
    try:
        data = await service.get_projection(session, year, month)
        return ApiResponseDto(
            data=data,
            success=True,
            message="Projection fetched successfully"
        )
    except ServiceException as exc:
        return await ControllerExceptionHandler.handle_service_exception(response, session, exc)
    except Exception:
        return await ControllerExceptionHandler.handle_unexpected_exception(response, session)
