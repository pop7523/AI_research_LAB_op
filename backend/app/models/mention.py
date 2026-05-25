from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin
from app.models.enums import EntityLinkingStatus

if TYPE_CHECKING:
    from app.models.article import Article
    from app.models.entity import Entity


class Mention(IdMixin, Base):
    __tablename__ = "mentions"

    article_id: Mapped[str] = mapped_column(ForeignKey("articles.id"), nullable=False, index=True)
    sentence_id: Mapped[str | None] = mapped_column(ForeignKey("article_sentences.id"))
    mention_text: Mapped[str] = mapped_column(Text, nullable=False)
    mention_type: Mapped[str | None] = mapped_column(String(64))
    sentence: Mapped[str | None] = mapped_column(Text)
    paragraph_index: Mapped[int | None] = mapped_column(Integer)
    start_offset: Mapped[int | None] = mapped_column(Integer)
    end_offset: Mapped[int | None] = mapped_column(Integer)
    linked_entity_id: Mapped[str | None] = mapped_column(ForeignKey("entities.id"))
    linking_status: Mapped[str] = mapped_column(
        String(64),
        default=EntityLinkingStatus.UNRESOLVED.value,
        nullable=False,
    )
    linking_confidence: Mapped[float | None] = mapped_column(Float)
    linking_reason: Mapped[str | None] = mapped_column(Text)
    needs_review: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    article: Mapped[Article] = relationship(back_populates="mentions")
    linked_entity: Mapped[Entity | None] = relationship(back_populates="mentions")
