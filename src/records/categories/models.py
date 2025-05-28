import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

import src.database.core.mapped_types as mt
from src.database.core.db import Base
from src.schemas import CategoryDTO

if TYPE_CHECKING:
    from src.models import Record, User, RecordType


class Category(Base):
    __tablename__ = "category"
    id: Mapped[mt.UUID_PK]
    name: Mapped[str]
    color: Mapped[str]

    created_at: Mapped[mt.CREATED_AT]
    updated_at: Mapped[mt.UPDATED_AT]

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("user.id", ondelete="CASCADE")
    )
    record_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("record_type.id"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="categories")
    records: Mapped[list["Record"]] = relationship("Record", back_populates="category")
    record_type: Mapped["RecordType"] = relationship(
        "RecordType", back_populates="categories", lazy="selectin"
    )

    __table_args__ = (
        Index(
            "idx_category_name_user", "name", "user_id", "record_type_id", unique=True
        ),
        Index("idx_category_color_user", "color", "user_id"),
    )

    def to_dto(self):
        return CategoryDTO(id=self.id, name=self.name, color=self.color)
