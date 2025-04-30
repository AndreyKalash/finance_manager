from typing import Any
from uuid import UUID
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import MappedClassProtocol, DeclarativeBase, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .core.db import execute_statement


async def insert_data_to_table(
    table: MappedClassProtocol, data_rows: list[dict], session: AsyncSession
):
    statement = insert(table).values(data_rows)
    await session.execute(statement)


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
    )
    result = await session.execute(query)
    items_orm = result.scalars().all()
    return items_orm


# async def select_records_data(
#     session: AsyncSession,
#     model: type[DeclarativeBase],
#     current_user_uuid: UUID,
#     limit: int,
#     skip: int,
# ):
#     query = select(model).filter_by(user_id=current_user_uuid).options(selectinload('*')).limit(limit).offset(skip)
#     result = await session.execute(query)
#     items_orm = result.scalars().all()
#     return items_orm


async def insert_user_data(
    session: AsyncSession,
    model: type[DeclarativeBase],
    values: dict[str, Any],
):
    statement = insert(model).values(values)
    return await execute_statement(session, statement)


async def update_user_data(
    session: AsyncSession,
    model: type[DeclarativeBase],
    values: dict[str, Any],
    filters: dict[str, Any],
):
    statement = update(model).values(values).filter_by(**filters)
    return await execute_statement(session, statement)


async def delete_user_data(
    session: AsyncSession, model: type[DeclarativeBase], filters: dict[str, Any]
):
    statement = delete(model).filter_by(**filters)
    return await execute_statement(session, statement)
