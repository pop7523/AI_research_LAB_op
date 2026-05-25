from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin
from app.models.enums import EventStatus

if TYPE_CHECKING:
    from app.models.article import Article
    from app.models.claim import Claim
    from app.models.fact import Fact


class Event(IdMixin, TimestampMixin, Base):
    __tablename__ = "events"

    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str | None] = mapped_column(Text)
    summary: Mapped[str | None] = mapped_column(Text)
    event_time: Mapped[datetime | None] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(
        String(64),
        default=EventStatus.CANDIDATE.value,
        nullable=False,
    )
    confidence: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)
    event_metadata: Mapped[dict | None] = mapped_column("metadata", JSON)

    links: Mapped[list[EventLink]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
    )


class EventLink(IdMixin, Base):
    __tablename__ = "event_links"

    event_id: Mapped[str] = mapped_column(ForeignKey("events.id"), nullable=False, index=True)
    fact_id: Mapped[str | None] = mapped_column(ForeignKey("facts.id"))
    claim_id: Mapped[str | None] = mapped_column(ForeignKey("claims.id"))
    article_id: Mapped[str] = mapped_column(ForeignKey("articles.id"), nullable=False, index=True)
    relation_type: Mapped[str] = mapped_column(String(64), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)

    event: Mapped[Event] = relationship(back_populates="links")
    fact: Mapped[Fact | None] = relationship()
    claim: Mapped[Claim | None] = relationship()
    article: Mapped[Article] = relationship()
