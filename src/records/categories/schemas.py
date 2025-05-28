from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CategoryAddDTO(BaseModel):
    name: str
    color: str

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, arbitrary_types_allowed=True
    )


class CategoryDTO(CategoryAddDTO):
    id: UUID
