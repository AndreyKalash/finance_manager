from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, relationship
from src.database.core.db import Base
import src.database.core.mapped_types as mt
from sqlalchemy import Index

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.models import Unit, Category, Tag, Record


class User(SQLAlchemyBaseUserTableUUID, Base):
    id: Mapped[mt.UUID_PK]

    username: Mapped[str]
    created_at: Mapped[mt.CREATED_AT]
    updated_at: Mapped[mt.UPDATED_AT]

    units: Mapped[list["Unit"]] = relationship("Unit", back_populates="user")
    categories: Mapped[list["Category"]] = relationship(
        "Category", back_populates="user"
    )
    tags: Mapped[list["Tag"]] = relationship("Tag", back_populates="user")
    records: Mapped[list["Record"]] = relationship("Record", back_populates="user")

    repr_col_num = 2
    repr_extra_cols = ("username",)

    __table_args__ = (Index("idx_username", "username", unique=True),)
