from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import JSON, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin
from app.models.enums import PerspectiveStatus

if TYPE_CHECKING:
    from app.models.issue import Issue


class Perspective(IdMixin, TimestampMixin, Base):
    __tablename__ = "perspectives"

    issue_id: Mapped[str] = mapped_column(ForeignKey("issues.id"), nullable=False, index=True)
    perspective_type: Mapped[str | None] = mapped_column(String(64))
    title: Mapped[str | None] = mapped_column(Text)
    content: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(64),
        default=PerspectiveStatus.PLAUSIBLE_VIEW.value,
        nullable=False,
    )
    evidence_refs: Mapped[list[str] | None] = mapped_column(JSON)
    weaknesses: Mapped[list[str] | None] = mapped_column(JSON)
    affected_stakeholders: Mapped[list[str] | None] = mapped_column(JSON)
    confidence: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)

    issue: Mapped[Issue] = relationship()

