from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.article import Article


class Source(IdMixin, TimestampMixin, Base):
    __tablename__ = "sources"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str | None] = mapped_column(Text)
    source_type: Mapped[str] = mapped_column(String(64), nullable=False)
    credibility_level: Mapped[str | None] = mapped_column(String(64))
    credibility_score: Mapped[float | None] = mapped_column(Float)
    political_bias_note: Mapped[str | None] = mapped_column(Text)
    business_incentive_note: Mapped[str | None] = mapped_column(Text)
    is_official: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    articles: Mapped[list[Article]] = relationship(back_populates="source")
