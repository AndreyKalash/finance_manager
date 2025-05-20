import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

import src.database.core.mapped_types as mt
from src.database.core.db import Base
from src.schemas import TagDTO

if TYPE_CHECKING:
    from src.models import Record, User, RecordType


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
    record_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("record_type.id"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="tags")
    records: Mapped[list["Record"]] = relationship(
        "Record", secondary="record_tag", back_populates="tags"
    )
    record_type: Mapped["RecordType"] = relationship("RecordType", back_populates="tags", lazy="selectin")
    

    __table_args__ = (
        Index("idx_name_user", "name", "user_id", "record_type_id", unique=True),
        Index("idx_color_user", "color", "user_id"),
    )

    def to_dto(self):
        return TagDTO(id=self.id, name=self.name, color=self.color)


class RecordTag(Base):
    __tablename__ = "record_tag"
    record_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("record.id"), primary_key=True
    )
    tag_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("tag.id"), primary_key=True
    )
    created_at: Mapped[mt.CREATED_AT]    

    __table_args__ = (
        Index("uq_record_tag", "record_id", "tag_id", unique=True),
    )