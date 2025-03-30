from datetime import date
import uuid
from sqlalchemy import CheckConstraint, ForeignKey, Index, UUID, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.core.db import Base
import src.database.core.mapped_types as mt
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.models import User, Unit, Category, Tag


class Record(Base):
    __tablename__ = "record"
    id: Mapped[mt.UUID_PK]

    record_date: Mapped[date]
    product_name: Mapped[str]
    unit_quantity: Mapped[float]
    product_quantity: Mapped[int]
    product_price: Mapped[float]

    created_at: Mapped[mt.CREATED_AT]
    updated_at: Mapped[mt.UPDATED_AT]

    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("category.id", ondelete="CASCADE")
    )
    unit_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("unit.id", ondelete="CASCADE")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("user.id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship("User", back_populates="records")
    unit: Mapped["Unit"] = relationship("Unit", back_populates="records")
    category: Mapped["Category"] = relationship("Category", back_populates="records")
    tags: Mapped[list["Tag"]] = relationship(
        "Tag", secondary="record_tag", back_populates="records"
    )

    repr_col_num = 5

    __table_args__ = (
        Index("idx_record_date", "record_date"),
        Index("idx_product_name", "product_name"),
        CheckConstraint("unit_quantity > 0", name="check_unit_quantity"),
        CheckConstraint("product_quantity > 0", name="check_product_quantity"),
        CheckConstraint("product_price >= 0", name="check_product_price"),
    )
