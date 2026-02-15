from typing import Generic, TypeVar, Optional, List

from pydantic import BaseModel

T = TypeVar('T')


class ApiResponseDto(BaseModel, Generic[T]):
    """Generic API response wrapper."""

    data: Optional[T] = None
    success: bool
    message: Optional[str] = None


class PaginatedResponseDto(BaseModel, Generic[T]):
    """Generic paginated payload."""

    data: List[T]
    total: int
    page_no: int
    max_per_page: int
    current_count: int
