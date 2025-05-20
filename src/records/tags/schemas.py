from uuid import UUID

from pydantic import BaseModel


class TagAddDTO(BaseModel):
    name: str
    color: str


class TagDTO(TagAddDTO):
    id: UUID
