from uuid import UUID

from sqlalchemy import and_, select, func, cast, text, true, Date
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Record, Category, RecordType, RecordTag
from datetime import date
from .utils import calculate_date_steps



async def categories_month_stats(
    session: AsyncSession,
    current_user_uuid: UUID,
    record_type_name: str,
    stats_type: str,
    month: int,
    year: int,
):
    start_date = date(year, month, 1)
    end_date = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)        
    
    if stats_type == 'sum':
        aggregate = (
            func.sum(Record.amount)
            if record_type_name == 'income'
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
        .join(RecordType, Record.record_type_id == RecordType.id)
        .where(
            Record.user_id == current_user_uuid,
            RecordType.name == record_type_name,
            Record.record_date >= start_date,
            Record.record_date < end_date
        )
        .group_by(Category.color, Category.name)
        .having(aggregate > 0)
    )
    
    result = await session.execute(stmt)
    return result.all()

async def trend(
    session: AsyncSession,
    current_user_uuid: UUID,
    record_type_name: str,
    filters,
    steps: int = 10
):
    total_days = (filters.end_date - filters.start_date).days
    step_days = ((total_days + steps - 1) // steps) if steps > 0 else 1
    
    date_series = select(
            func.generate_series(
            filters.start_date,
            filters.end_date,
            cast(text(f"'{step_days} day'"), INTERVAL)
        ).label('window_start')
    ).cte('start_dates')
    
    date_windows = (
        select(
            date_series.c.window_start,
            (date_series.c.window_start + cast(text(f"'{step_days-1} day'"), INTERVAL)).label('window_end')
        )
        .cte('date_windows')
    )
    
    if record_type_name == 'income':
        amount_expr = func.coalesce(func.sum(Record.amount), 0)
    elif record_type_name == 'expense':
        amount_expr = (
            func.coalesce(func.sum(Record.amount * Record.product_quantity * Record.unit_quantity), 0)
        )
    
    query = (
        select(
            func.cast(date_windows.c.window_start, Date).label('date'),
            amount_expr.label('amount_sum')
        )
        .select_from(
            date_windows.outerjoin(
                Record,
                and_(
                    Record.record_date >= date_windows.c.window_start,
                    Record.record_date <= date_windows.c.window_end,
                    Record.user_id == current_user_uuid,
                    Record.record_type_id == select(RecordType.id).where(RecordType.name == record_type_name).scalar_subquery()
                )
            )
        )
        .group_by(date_windows.c.window_start)
        .order_by(date_windows.c.window_start)
    )

    if filters.categories:
        query = query.where(Record.category_id.in_(filters.categories))
        
    if filters.tags:
        query = query.where(Record.id.in_(select(RecordTag.record_id).where).tag_id.in_(filters.tags)).scalar_subquery()
        
    if filters.units:
        query = query.where(Record.unit_id.in_(filters.units))

    return await session.execute(query)
