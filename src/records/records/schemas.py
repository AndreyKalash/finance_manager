from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel
from pydantic.fields import Field

from src.records.categories.schemas import CategoryDTO
from src.records.tags.schemas import TagDTO
from src.records.units.schemas import UnitDTO


class RecordBaseDTO(BaseModel):
    record_date: date = Field(default=date.today())
    name: str
    amount: Decimal = Field(ge=0)
    
    class Config:
        extra = 'ignore'


class ExpenseRecordBaseDTO(RecordBaseDTO):
    unit_quantity: Decimal | None = None
    product_quantity: int | None = None


class IncomeRecordAddDTO(RecordBaseDTO):
    category_id: UUID
    tags: list[UUID]


class IncomeRecordDTO(RecordBaseDTO):
    id: UUID
    
    category: CategoryDTO
    tags: list[TagDTO]


class ExpenseRecordAddDTO(ExpenseRecordBaseDTO):
    unit_id: UUID
    category_id: UUID
    tags: list[UUID]


class ExpenseRecordDTO(ExpenseRecordBaseDTO):
    id: UUID
    
    unit: UnitDTO | None
    category: CategoryDTO
    tags: list[TagDTO]
