from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import DeclarativeBase
from uuid import UUID

ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, session: AsyncSession, obj: ModelType) -> ModelType:
        session.add(obj)
        await session.flush()
        await session.refresh(obj)
        return obj

    async def get_by_id(
        self,
        session: AsyncSession,
        obj_id: UUID
    ) -> Optional[ModelType]:

        stmt = select(self.model).where(self.model.id == obj_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        session: AsyncSession
    ) -> List[ModelType]:

        stmt = select(self.model)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def delete(
        self,
        session: AsyncSession,
        obj_id: UUID
    ) -> bool:

        stmt = delete(self.model).where(self.model.id == obj_id)
        result = await session.execute(stmt)
        return result.rowcount > 0

    async def update(
        self,
        session: AsyncSession,
        obj_id: UUID,
        data: dict
    ) -> Optional[ModelType]:

        stmt = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**data)
            .returning(self.model)
        )

        result = await session.execute(stmt)
        return result.scalar_one_or_none()
