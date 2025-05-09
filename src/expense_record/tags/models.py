import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

import src.database.core.mapped_types as mt
from src.database.core.db import Base
from src.schemas import TagDTO

if TYPE_CHECKING:
    from src.models import Record, User


class Tag(Base):
    __tablename__ = "tag"
    id: Mapped[mt.UUID_PK]
    name: Mapped[str]
    color: Mapped[str]

    created_at: Mapped[mt.CREATED_AT]
    updated_at: Mapped[mt.UPDATED_AT]

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("user.id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship("User", back_populates="tags")
    records: Mapped[list["Record"]] = relationship(
        "Record", secondary="record_tag", back_populates="tags"
    )

    __table_args__ = (
        Index("idx_name_user", "name", "user_id", unique=True),
        Index("idx_color_user", "color", "user_id"),
    )

    def to_dto(self):
        return TagDTO(id=self.id, name=self.name, color=self.color)


class RecordTag(Base):
    __tablename__ = "record_tag"
    record_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("record.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True
    )
