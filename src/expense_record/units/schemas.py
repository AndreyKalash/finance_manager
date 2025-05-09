from uuid import UUID
from pydantic import BaseModel, ConfigDict


class UnitAddDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    default_value: float


class UnitDTO(UnitAddDTO):
    id: UUID
