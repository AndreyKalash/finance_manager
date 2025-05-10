from typing import Any
from uuid import UUID

from sqlalchemy import select, func, extract
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Record, Category
from datetime import date

async def categories_month_sum(
    session: AsyncSession,
    current_user_uuid: UUID,
    month: int,
    year: int,
):
    start_date = date(year, month, 1)
    end_date = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    
    stmt = (
        select(
            func.sum(Record.price * Record.product_quantity).label('price_sum'),
            Category.name,
            Category.color
        )
        .join(Category, Record.category_id == Category.id)
        .where(
            Record.user_id == current_user_uuid,
            Record.record_date >= start_date,
            Record.record_date < end_date
        )
        .group_by(Category.id, Category.name)
        .having(func.sum(Record.price * Record.product_quantity) > 0)
    )
    result = await session.execute(stmt)
    return result.all()


async def categories_month_count(
    session: AsyncSession,
    current_user_uuid: UUID,
    month: int,
    year: int,
):
    start_date = date(year, month, 1)
    end_date = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    
    stmt = (
        select(
            func.count(Record.id).label('record_count'),
            Category.name,
            Category.color
        )
        .join(Category, Record.category_id == Category.id)
        .where(
            Record.user_id == current_user_uuid,
            Record.record_date >= start_date,
            Record.record_date < end_date
        )
        .group_by(Category.id, Category.name)
        .having(func.count(Record.id) > 0)
    )
    result = await session.execute(stmt)
    return result.all()
