from __future__ import annotations

from sqlalchemy import Float, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdMixin, TimestampMixin
from app.models.enums import ReviewStatus


class ReviewItem(IdMixin, TimestampMixin, Base):
    __tablename__ = "review_items"
    __table_args__ = (UniqueConstraint("target_type", "target_id", "status"),)

    target_type: Mapped[str] = mapped_column(String(64), nullable=False)
    target_id: Mapped[str] = mapped_column(String(36), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(64),
        default=ReviewStatus.PENDING.value,
        nullable=False,
    )
    confidence: Mapped[float | None] = mapped_column(Float)
    reviewer_note: Mapped[str | None] = mapped_column(Text)

