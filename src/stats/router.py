from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_config import fastapi_auth
from src.database.core.db import get_async_session
from src.database.stats import categories_month_stats
from src.database.crud import select_data
from src.models import User
from src.records.records.models import RecordType

from src.schemas import CategoryMonthStatsDTO

stats_router = APIRouter(
    prefix="/stats",
    tags=["stats"],
)
current_user = fastapi_auth.current_user()

def create_stat_endpoint(stat_type: str):
    async def endpoint(
        record_type_name: Annotated[str, Path()],
        month: Annotated[int, Query(ge=1, le=12)],
        year: Annotated[int, Query(ge=1900)],
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_user),
    ):
        record_type = await select_data(
            session, 
            RecordType, 
            [RecordType.name == record_type_name]
        )
        
        stat_results = await categories_month_stats(
            session,
            current_user.id,
            record_type[0].id,
            stat_type,
            month,
            year
        )

        return [
            CategoryMonthStatsDTO(
                category=category_name,
                stats=float(stats),
                color=color
            )
            for stats, category_name, color in stat_results
        ]
    
    endpoint.__name__ = f"get_categories_month_{stat_type}"
    return endpoint

stats_router.get(
    "/{record_type_name}/categories-month-sum",
    response_model=list[CategoryMonthStatsDTO]
)(create_stat_endpoint("sum"))

stats_router.get(
    "/{record_type_name}/categories-month-count",
    response_model=list[CategoryMonthStatsDTO]
)(create_stat_endpoint("count"))