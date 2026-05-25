from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import JSON, Boolean, CheckConstraint, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin
from app.models.enums import ClaimStatus

if TYPE_CHECKING:
    from app.models.article import Article, ArticleSentence
    from app.models.entity import Entity


class Claim(IdMixin, TimestampMixin, Base):
    __tablename__ = "claims"
    __table_args__ = (CheckConstraint("length(trim(evidence_text)) > 0"),)

    article_id: Mapped[str] = mapped_column(ForeignKey("articles.id"), nullable=False, index=True)
    sentence_id: Mapped[str | None] = mapped_column(ForeignKey("article_sentences.id"))
    speaker_entity_id: Mapped[str | None] = mapped_column(ForeignKey("entities.id"))
    speaker_text: Mapped[str | None] = mapped_column(Text)
    speaker_type: Mapped[str | None] = mapped_column(String(64))
    claim_type: Mapped[str] = mapped_column(String(64), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    related_entity_ids: Mapped[list[str] | None] = mapped_column(JSON)
    evidence_text: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_span: Mapped[dict | None] = mapped_column(JSON)
    confidence: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)
    claim_status: Mapped[str] = mapped_column(
        String(64),
        default=ClaimStatus.EXTRACTED.value,
        nullable=False,
    )
    possible_incentive: Mapped[str | None] = mapped_column(Text)
    needs_independent_verification: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    needs_review: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    article: Mapped[Article] = relationship()
    sentence: Mapped[ArticleSentence | None] = relationship()
    speaker_entity: Mapped[Entity | None] = relationship()
