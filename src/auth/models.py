from typing import TYPE_CHECKING

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Index
from sqlalchemy.orm import Mapped, relationship

import src.database.core.mapped_types as mt
from src.database.core.db import Base

if TYPE_CHECKING:
    from src.models import Category, Record, Tag, Unit


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
