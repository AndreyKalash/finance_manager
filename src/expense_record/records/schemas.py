from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel
from pydantic.fields import Field

from src.expense_record.categories.schemas import CategoryDTO
from src.expense_record.tags.schemas import TagDTO
from src.expense_record.units.schemas import UnitDTO


class RecordBaseDTO(BaseModel):
    record_date: date = Field(default=date.today())
    name: str
    price: Decimal = Field(ge=0)
    unit_quantity: Decimal = Field(default=1, gt=0)
    product_quantity: int = Field(default=1, gt=0)


class RecordAddDTO(RecordBaseDTO):
    unit_id: UUID
    category_id: UUID
    tags: list[UUID]


class RecordDTO(RecordBaseDTO):
    id: UUID
    
    unit: UnitDTO
    category: CategoryDTO
    tags: list[TagDTO]
