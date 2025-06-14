from typing import Any
from uuid import UUID
from src.database.core.db import Base
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import MappedClassProtocol, selectinload


async def select_data(
    session: AsyncSession,
    model: type[Base],
    filters: list = [],
    limit: int = 1000,
    skip: int = 0,
    selectload: list = [],
    no_limit: bool = False,
    order_by = None
):
    load_options = [selectinload(rel) for rel in selectload]
    query = (
        select(model).where(*filters).limit(limit).options(*load_options)
    )
    if not no_limit:
        query = query.offset(skip)
   
    if order_by is not None:
        query = query.order_by(order_by)
        

    result = await session.execute(query)
    return result.scalars().all()


async def insert_data(
    session: AsyncSession,
    model: MappedClassProtocol,
    values: list[dict],
    commit: bool = True,
):
    stmt = insert(model).values(values)
    await session.execute(stmt)
    if commit:
        await session.commit()


async def upload_data(
    session: AsyncSession, model: MappedClassProtocol, names: list = []
):
    session.add(model)
    await session.commit()
    await session.refresh(model, attribute_names=[*names])


async def update_data(
    session: AsyncSession,
    model: type[Base],
    update_data: dict[str, Any],
    filters: list,
    commit: bool = True,
) -> Base | None:
    stmt = update(model).where(*filters).values(**update_data).returning(model)

    result = await session.execute(stmt)
    if commit:
        await session.commit()

    return result.scalar_one_or_none()


async def delete_data(
    session: AsyncSession, model: type[Base], filters: list, commit: bool = True
):
    stmt = delete(model).where(*filters)

    result = await session.execute(stmt)
    if commit:
        await session.commit()

    return result.rowcount
