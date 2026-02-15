from dataclasses import dataclass
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')


@dataclass
class ApiResponseDto(Generic[T]):
    """
    Generic API Response DTO that can wrap any data type.
    """
    data: T
    success: bool
    message: Optional[str] = None


@dataclass
class PaginatedResponseDto(Generic[T]):
    """
    Generic Paginated Response DTO that wraps a list of items with pagination metadata.
    """
    data: List[T]
    total: int
    page_no: int
    max_per_page: int
    current_count: int
