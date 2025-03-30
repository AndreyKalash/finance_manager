from uuid import UUID
from pydantic import BaseModel, ConfigDict


class CategoryAddDTO(BaseModel):
    category_name: str
    category_color: str


class CategoryDTO(CategoryAddDTO):
    id: UUID
