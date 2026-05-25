from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin
from app.models.enums import IssueStatus

if TYPE_CHECKING:
    from app.models.article import Article
    from app.models.claim import Claim
    from app.models.event import Event
    from app.models.fact import Fact


class Issue(IdMixin, TimestampMixin, Base):
    __tablename__ = "issues"

    title: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    issue_type: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(
        String(64),
        default=IssueStatus.CANDIDATE.value,
        nullable=False,
    )
    priority: Mapped[str | None] = mapped_column(String(64))
    first_seen_at: Mapped[datetime | None] = mapped_column(DateTime)
    last_updated_at: Mapped[datetime | None] = mapped_column(DateTime)
    editorial_reason: Mapped[str | None] = mapped_column(Text)
    uncertainty_note: Mapped[str | None] = mapped_column(Text)
    issue_metadata: Mapped[dict | None] = mapped_column("metadata", JSON)

    links: Mapped[list[IssueLink]] = relationship(
        back_populates="issue",
        cascade="all, delete-orphan",
    )


class IssueLink(IdMixin, Base):
    __tablename__ = "issue_links"

    issue_id: Mapped[str] = mapped_column(ForeignKey("issues.id"), nullable=False, index=True)
    article_id: Mapped[str | None] = mapped_column(ForeignKey("articles.id"))
    event_id: Mapped[str | None] = mapped_column(ForeignKey("events.id"))
    fact_id: Mapped[str | None] = mapped_column(ForeignKey("facts.id"))
    claim_id: Mapped[str | None] = mapped_column(ForeignKey("claims.id"))
    link_type: Mapped[str] = mapped_column(String(64), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)

    issue: Mapped[Issue] = relationship(back_populates="links")
    article: Mapped[Article | None] = relationship()
    event: Mapped[Event | None] = relationship()
    fact: Mapped[Fact | None] = relationship()
    claim: Mapped[Claim | None] = relationship()
