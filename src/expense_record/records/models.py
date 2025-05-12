import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import UUID, CheckConstraint, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

import src.database.core.mapped_types as mt
from src.database.core.db import Base
from src.schemas import RecordDTO

if TYPE_CHECKING:
    from src.models import Category, Tag, Unit, User


class Record(Base):
    __tablename__ = "record"
    id: Mapped[mt.UUID_PK]

    record_date: Mapped[date]
    name: Mapped[str]
    unit_quantity: Mapped[float]
    product_quantity: Mapped[int | None] 
    price: Mapped[float]

    created_at: Mapped[mt.CREATED_AT]
    updated_at: Mapped[mt.UPDATED_AT]

    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("category.id"), nullable=True
    )
    unit_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("unit.id"), nullable=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("user.id"), nullable=True
    )

    user: Mapped["User"] = relationship("User", back_populates="records", lazy="selectin")
    unit: Mapped["Unit"] = relationship("Unit", back_populates="records", lazy="selectin")
    category: Mapped["Category"] = relationship("Category", back_populates="records", lazy="selectin")
    tags: Mapped[list["Tag"]] = relationship(
        "Tag", 
        secondary="record_tag",
        back_populates="records",
        cascade="save-update, merge, delete",
        passive_deletes=True,
        lazy="selectin"
    )

    repr_col_num = 5

    __table_args__ = (
        Index("idx_record_date", "record_date"),
        Index("idx_product_name", "name"),
        CheckConstraint("unit_quantity > 0", name="check_unit_quantity"),
        CheckConstraint("quantity > 0", name="check_product_quantity"),
        CheckConstraint("price >= 0", name="check_product_price"),
    )

    def to_dto(self):
        return RecordDTO(
            id=self.id,
            record_date=self.record_date,
            name=self.name,
            unit_quantity=self.unit_quantity,
            product_quantity=self.product_quantity,
            price=self.price,
            unit=self.unit.to_dto() if self.unit else None,
            category=self.category.to_dto() if self.category else None,
            tags=[tag.to_dto() for tag in self.tags] if self.tags else []
        )

