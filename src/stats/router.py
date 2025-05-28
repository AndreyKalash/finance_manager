from fastapi import APIRouter
from .endpoints import create_stat_endpoint, create_trend_endpont

from src.schemas import CategoryMonthStatsDTO, TrendDTO

stats_router = APIRouter(
    prefix="/stats",
    tags=["stats"],
)

stats_router.get(
    "/{record_type_name}/categories-month-sum",
    response_model=list[CategoryMonthStatsDTO],
)(create_stat_endpoint("sum"))

stats_router.get(
    "/{record_type_name}/categories-month-count",
    response_model=list[CategoryMonthStatsDTO],
)(create_stat_endpoint("count"))

stats_router.post("/{record_type_name}/trend", response_model=list[TrendDTO])(
    create_trend_endpont()
)
