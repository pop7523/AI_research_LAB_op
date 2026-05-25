from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin
from app.models.enums import ReportStatus

if TYPE_CHECKING:
    from app.models.issue import Issue


class Report(IdMixin, TimestampMixin, Base):
    __tablename__ = "reports"

    issue_id: Mapped[str] = mapped_column(ForeignKey("issues.id"), nullable=False, index=True)
    report_type: Mapped[str | None] = mapped_column(String(64))
    title: Mapped[str | None] = mapped_column(Text)
    body_markdown: Mapped[str | None] = mapped_column(Text)
    summary: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(64),
        default=ReportStatus.DRAFT.value,
        nullable=False,
    )
    evidence_checked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    balance_checked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    editor_approved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    issue: Mapped[Issue] = relationship()

