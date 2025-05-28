from typing import Annotated

from fastapi import Body, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_config import fastapi_auth
from src.database.core.db import get_async_session
from src.stats.database import categories_month_stats, trend
from src.models import User

from src.schemas import CategoryMonthStatsDTO, TrendBodyDTO, TrendDTO

current_user = fastapi_auth.current_user()


def create_stat_endpoint(stat_type: str):
    async def endpoint(
        record_type_name: Annotated[str, Path()],
        month: Annotated[int, Query(ge=1, le=12)],
        year: Annotated[int, Query(ge=1900)],
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_user),
    ):
        stat_results = await categories_month_stats(
            session, current_user.id, record_type_name, stat_type, month, year
        )

        return [
            CategoryMonthStatsDTO(
                category=category_name, stats=float(stats), color=color
            )
            for stats, category_name, color in stat_results
        ]

    endpoint.__name__ = f"get_categories_month_{stat_type}"
    return endpoint


def create_trend_endpont():
    async def endpoint(
        record_type_name: Annotated[str, Path()],
        filters: Annotated[TrendBodyDTO, Body()],
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_user),
    ):
        result = await trend(session, current_user.id, record_type_name, filters)
        return [TrendDTO(date=d, amount_sum=a) for d, a in result]

    endpoint.__name__ = "get_income_expense_trend"
    return endpoint
