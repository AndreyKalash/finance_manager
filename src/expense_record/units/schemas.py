from uuid import UUID
from pydantic import BaseModel, ConfigDict


class UnitAddDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    unit_name: str


class UnitDTO(UnitAddDTO):
    id: UUID
