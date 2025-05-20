from pydantic import BaseModel

class CategoryMonthStatsDTO(BaseModel):
    category: str
    stats: float
    color: str
    
