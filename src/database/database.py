from typing import Any
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedClassProtocol, selectinload


async def select_data(
    session: AsyncSession,
    model: type[DeclarativeBase],
    current_user_uuid: UUID,
    limit: int = 1000,
    skip: int = 0,
    filters: list = [],
    selectload: list = ["*"]
):
    query = (
        select(model)
        .options(selectinload(*selectload))
        .limit(limit)
        .offset(skip)
        .order_by(model.created_at)
        .where(model.user_id==current_user_uuid, *filters)
    )
    result = await session.execute(query)
    return result.scalars().all()


async def upload_data(
    session: AsyncSession,
    model: MappedClassProtocol,
    names: list = []
):
    session.add(model)
    await session.commit()
    await session.refresh(model, attribute_names=[*names])


async def update_data(
    session: AsyncSession,
    model: type[DeclarativeBase],
    update_data: dict[str, Any],
    filters: dict[str, Any],
) -> DeclarativeBase | None:
    stmt = update(model).where(*filters).values(**update_data).returning(model)

    result = await session.execute(stmt)
    await session.commit()

    return result.scalar_one_or_none()


async def delete_data(
    session: AsyncSession, model: type[DeclarativeBase], filters: dict[str, Any]
):
    stmt = delete(model).where(*filters)

    result = await session.execute(stmt)
    await session.commit()

    return result.rowcount
