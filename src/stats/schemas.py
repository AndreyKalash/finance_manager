from pydantic import BaseModel

class CategoryMonthSumDTO(BaseModel):
    category: str
    sum: float
    color: str
    
    
class CategoryMonthCountDTO(BaseModel):
    category: str
    count: float
    color: str
