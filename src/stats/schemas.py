from uuid import UUID
from pydantic import BaseModel
from datetime import date

class CategoryMonthStatsDTO(BaseModel):
    category: str
    stats: float
    color: str
    
class TrendBodyDTO(BaseModel):
    start_date: date
    end_date: date
    categories: list[UUID] = []
    tags: list[UUID] = []
    units: list[UUID] = []
    
class TrendDTO(BaseModel):
    date: date
    amount_sum: float