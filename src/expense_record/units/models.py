import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

import src.database.core.mapped_types as mt
from src.database.core.db import Base
from src.schemas import UnitDTO

if TYPE_CHECKING:
    from src.models import Record, User


class Unit(Base):
    __tablename__ = "unit"
    id: Mapped[mt.UUID_PK]
    name: Mapped[str]
    default_value: Mapped[float]

    created_at: Mapped[mt.CREATED_AT]
    updated_at: Mapped[mt.UPDATED_AT]

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("user.id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship("User", back_populates="units")
    records: Mapped[list["Record"]] = relationship("Record", back_populates="unit")

    repr_col_num = 2

    __table_args__ = (
        Index("idx_unit_name_user", "name", "user_id", unique=True),
        Index("idx_unit_default_value_user", "default_value", "user_id"),
    )

    def to_dto(self):
        return UnitDTO(id=self.id, name=self.name, default_value=self.default_value)
