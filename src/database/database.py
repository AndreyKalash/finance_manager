from typing import Any
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedClassProtocol, selectinload


async def select_data(
    session: AsyncSession,
    model: type[DeclarativeBase],
    current_user_uuid: UUID | None = None,
    check_user: bool = True,
    limit: int = 1000,
    skip: int = 0,
    filters: list = [],
    selectload: list = []
):
    load_options = [selectinload(rel) for rel in selectload]
    query = (
        select(model)
        .options(*load_options)
        .limit(limit)
        .offset(skip)
        .order_by(model.created_at)
        .where(*filters)
    )
    if check_user:
        query = query.where(model.user_id==current_user_uuid)
    
    result = await session.execute(query)
    return result.scalars().all()


async def insert_data(
    session: AsyncSession,
    model: MappedClassProtocol,
    values: list[dict],
    commit: bool = True
):
    stmt = insert(model).values(values)
    await session.execute(stmt)
    if commit:
        await session.commit()


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
    filters: list,
    commit: bool = True
) -> DeclarativeBase | None:
    stmt = update(model).where(*filters).values(**update_data).returning(model)

    result = await session.execute(stmt)
    if commit:
        await session.commit()

    return result.scalar_one_or_none()


async def delete_data(
    session: AsyncSession, 
    model: type[DeclarativeBase],
    filters: list,
    commit: bool = True
):
    stmt = delete(model).where(*filters)

    result = await session.execute(stmt)
    if commit:
        await session.commit()

    return result.rowcount
