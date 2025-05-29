from uuid import UUID

from sqlalchemy import and_, exists, select, func, cast, text, Date
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Record, Category, RecordType, RecordTag
from datetime import date


async def categories_month_stats(
    session: AsyncSession,
    current_user_uuid: UUID,
    record_type_name: str,
    stats_type: str,
    month: int,
    year: int,
):
    # Определение временного диапазона для статистики (весь указанный месяц)
    start_date = date(year, month, 1)
    end_date = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    # Выбор агрегатной функции в зависимости от типа статистики
    if stats_type == "sum":
        aggregate = (
            func.sum(Record.amount)
            if record_type_name == "income"
            else func.sum(
                Record.amount * Record.product_quantity * Record.unit_quantity
            )
        )
    elif stats_type == "count":
        aggregate = func.count(Record.id)
    else:
        raise Exception("неверный тип")
    # Формирование базового запроса с джойнами и фильтрами
    stmt = (
        select(aggregate.label("stats"), Category.name, Category.color)
        .join(Category, Record.category_id == Category.id)
        .join(RecordType, Record.record_type_id == RecordType.id)
        .where(
            Record.user_id == current_user_uuid,
            RecordType.name == record_type_name,
            Record.record_date >= start_date,
            Record.record_date < end_date,
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
    steps: int = 10,
):
    # Расчет временных интервалов для группировки данных
    total_days = (filters.end_date - filters.start_date).days
    step_days = ((total_days + steps - 1) // steps) if steps > 0 else 1
    # Генерация временных меток начала интервалов через generate_series
    date_series = select(
        func.generate_series(
            filters.start_date,
            filters.end_date,
            cast(text(f"'{step_days} day'"), INTERVAL),
        ).label("window_start")
    ).cte("start_dates")
    # Определение оконных интервалов (начало и конец)
    date_windows = select(
        date_series.c.window_start,
        (
            date_series.c.window_start + cast(text(f"'{step_days-1} day'"), INTERVAL)
        ).label("window_end"),
    ).cte("date_windows")
    # Выбор формулы расчета суммы в зависимости от типа записи
    if record_type_name == "income":
        amount_expr = func.coalesce(func.sum(Record.amount), 0)
    elif record_type_name == "expense":
        amount_expr = func.coalesce(
            func.sum(Record.amount * Record.product_quantity * Record.unit_quantity), 0
        )
    # Базовые условия соединения записей с временными окнами
    join_conditions = [
        Record.record_date >= date_windows.c.window_start,
        Record.record_date <= date_windows.c.window_end,
        Record.user_id == current_user_uuid,
        Record.record_type_id == (
            select(RecordType.id)
            .where(RecordType.name == record_type_name)
            .scalar_subquery()
        )
    ]
    # Добавление дополнительных фильтров при наличии
    if filters.categories:
        join_conditions.append(Record.category_id.in_(filters.categories))
    if filters.tags:
        join_conditions.append(exists(
            select(RecordTag.record_id).where(
                RecordTag.tag_id.in_(filters.tags)
            ).correlate(Record)
        ))
    if filters.units:
        join_conditions.append(Record.unit_id.in_(filters.units))
    # Основной запрос с OUTER JOIN для сохранения всех временных интервалов
    query = (
        select(
            func.cast(date_windows.c.window_start, Date).label("date"),
            amount_expr.label("amount_sum"),
        )
        .select_from(
            date_windows.outerjoin(
                Record,
                and_(*join_conditions),
            )
        )
        .group_by(date_windows.c.window_start)
        .order_by(date_windows.c.window_start)
    )
    return await session.execute(query)
