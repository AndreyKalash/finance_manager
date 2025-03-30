import uuid
from sqlalchemy import ForeignKey, UUID, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.core.db import Base
import src.database.core.mapped_types as mt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import User, Record


class Category(Base):
    __tablename__ = "category"
    id: Mapped[mt.UUID_PK]
    category_name: Mapped[str]
    category_color: Mapped[str]

    created_at: Mapped[mt.CREATED_AT]
    updated_at: Mapped[mt.UPDATED_AT]

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("user.id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship("User", back_populates="categories")
    records: Mapped[list["Record"]] = relationship("Record", back_populates="category")

    __table_args__ = (
        Index("idx_category_name_user", "category_name", "user_id", unique=True),
    )
