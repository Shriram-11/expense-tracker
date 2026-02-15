from fastapi import Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain_model.dtos.base_dtos import ApiResponseDto
from src.utils.exceptions import ServiceException


class ControllerExceptionHandler:
    """Converts service exceptions into consistent API responses."""

    @staticmethod
    async def handle_service_exception(
        response: Response,
        session: AsyncSession,
        exc: ServiceException
    ):
        response.status_code = exc.status_code
        await session.rollback()
        return ApiResponseDto(
            data=None,
            success=False,
            message=exc.message
        )

    @staticmethod
    async def handle_unexpected_exception(
        response: Response,
        session: AsyncSession
    ):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        await session.rollback()
        return ApiResponseDto(
            data=None,
            success=False,
            message="An unexpected error occurred"
        )
