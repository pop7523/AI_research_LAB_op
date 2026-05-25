from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import JSON, CheckConstraint, DateTime, Float, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin
from app.models.enums import FactStatus

if TYPE_CHECKING:
    from app.models.article import Article, ArticleSentence
    from app.models.entity import Entity


class Fact(IdMixin, TimestampMixin, Base):
    __tablename__ = "facts"
    __table_args__ = (CheckConstraint("length(trim(evidence_text)) > 0"),)

    article_id: Mapped[str] = mapped_column(ForeignKey("articles.id"), nullable=False, index=True)
    sentence_id: Mapped[str | None] = mapped_column(ForeignKey("article_sentences.id"))
    subject_entity_id: Mapped[str | None] = mapped_column(ForeignKey("entities.id"))
    predicate: Mapped[str] = mapped_column(Text, nullable=False)
    object_entity_id: Mapped[str | None] = mapped_column(ForeignKey("entities.id"))
    object_text: Mapped[str | None] = mapped_column(Text)
    value: Mapped[Decimal | None] = mapped_column(Numeric)
    unit: Mapped[str | None] = mapped_column(String(64))
    currency: Mapped[str | None] = mapped_column(String(16))
    time_scope: Mapped[str | None] = mapped_column(Text)
    normalized_time_start: Mapped[datetime | None] = mapped_column(DateTime)
    normalized_time_end: Mapped[datetime | None] = mapped_column(DateTime)
    evidence_text: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_span: Mapped[dict | None] = mapped_column(JSON)
    confidence: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)
    verification_status: Mapped[str] = mapped_column(
        String(64),
        default=FactStatus.EXTRACTED.value,
        nullable=False,
    )
    evidence_level: Mapped[str | None] = mapped_column(String(64))
    needs_review: Mapped[bool] = mapped_column(default=False, nullable=False)

    article: Mapped[Article] = relationship()
    sentence: Mapped[ArticleSentence | None] = relationship()
    subject_entity: Mapped[Entity | None] = relationship(foreign_keys=[subject_entity_id])
    object_entity: Mapped[Entity | None] = relationship(foreign_keys=[object_entity_id])

