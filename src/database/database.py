from typing import Any
from uuid import UUID
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import MappedClassProtocol, DeclarativeBase, selectinload
from sqlalchemy.ext.asyncio import AsyncSession


async def select_data(
    session: AsyncSession,
    model: type[DeclarativeBase],
    current_user_uuid: UUID,
    limit: int = 1000,
    skip: int = 0,
):
    query = (
        select(model)
        .filter_by(user_id=current_user_uuid)
        .options(selectinload("*"))
        .limit(limit)
        .offset(skip)
        .order_by(model.created_at)
    )
    result = await session.execute(query)
    items_orm = result.scalars().all()
    return items_orm


async def upload_data(
    session: AsyncSession,
    model: MappedClassProtocol,
):
    session.add(model)
    await session.commit()
    await session.refresh(model)


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
