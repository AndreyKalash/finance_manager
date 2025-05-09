from uuid import UUID

from pydantic import BaseModel


class CategoryAddDTO(BaseModel):
    name: str
    color: str


class CategoryDTO(CategoryAddDTO):
    id: UUID
