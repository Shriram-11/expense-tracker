from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.database import get_async_session
from src.domain_model.repositories.transaction_repository import TransactionRepository
from src.services.transaction_service import TransactionService


def get_transaction_repository():
    return TransactionRepository()


def get_transaction_service(
    repo: TransactionRepository = Depends(get_transaction_repository)
):
    return TransactionService(repo)


async def get_db_session():
    async for session in get_async_session():
        yield session
