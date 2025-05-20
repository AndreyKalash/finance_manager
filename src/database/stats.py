from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Record, Category
from datetime import date

async def categories_month_stats(
    session: AsyncSession,
    current_user_uuid: UUID,
    record_type_id: int,
    stats_type: str,
    month: int,
    year: int,
):
    start_date = date(year, month, 1)
    end_date = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    
    if stats_type == 'sum':
        aggregate = (
            func.sum(Record.amount)
            if record_type_id == 2
            else 
            func.sum(Record.amount * Record.product_quantity * Record.unit_quantity)
        )
    elif stats_type == 'count':
        aggregate = (
            func.count(Record.id)
        )
    else:
        raise Exception('неверный тип')
    
    stmt = (
        select(
            aggregate.label('stats'),
            Category.name,
            Category.color
        )
        .join(Category, Record.category_id == Category.id)
        .where(
            Record.user_id == current_user_uuid,
            Record.record_type_id == record_type_id,
            Record.record_date >= start_date,
            Record.record_date < end_date
        )
        .group_by(Category.color, Category.name)
        .having(aggregate > 0)
    )
    print(stmt)
    
    result = await session.execute(stmt)
    return result.all()