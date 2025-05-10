from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_config import fastapi_auth
from src.database.core.db import get_async_session
from src.database.stats import categories_month_sum, categories_month_count
from src.models import User

from .schemas import CategoryMonthSumDTO, CategoryMonthCountDTO

stats_router = APIRouter(
    prefix="/stats",
    tags=["stats"],
)
current_user = fastapi_auth.current_user()

@stats_router.get("/categories-month-sum", response_model=list[CategoryMonthSumDTO])
async def get_categories_month_sum(
    month: Annotated[int, Query(ge=1, le=12)],
    year: Annotated[int, Query(ge=1900)],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):

    stat = await categories_month_sum(session, current_user.id, month, year)
    return [
        CategoryMonthSumDTO(
            category=category_name,
            sum=float(price_sum),
            color=color
        )
        for price_sum, category_name, color in stat
    ]
    
    
@stats_router.get("/categories-month-count")
async def get_records(
    month: Annotated[int, Query(ge=1, le=12)],
    year: Annotated[int, Query(ge=1900)],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):

    stat = await categories_month_count(session, current_user.id, month, year)
    return [
        CategoryMonthCountDTO(
            category=category_name,
            count=float(reciord_count),
            color=color
        )
        for reciord_count, category_name, color in stat
    ]