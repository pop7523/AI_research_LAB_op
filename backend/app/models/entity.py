from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import JSON, Float, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin
from app.models.enums import EntityStatus

if TYPE_CHECKING:
    from app.models.mention import Mention


class Entity(IdMixin, TimestampMixin, Base):
    __tablename__ = "entities"

    canonical_name: Mapped[str] = mapped_column(Text, nullable=False)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    country: Mapped[str | None] = mapped_column(String(64))
    industry: Mapped[str | None] = mapped_column(String(128))
    ticker: Mapped[str | None] = mapped_column(String(32), index=True)
    external_ids: Mapped[dict | None] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(
        String(64),
        default=EntityStatus.ACTIVE.value,
        nullable=False,
    )

    aliases: Mapped[list[EntityAlias]] = relationship(
        back_populates="entity",
        cascade="all, delete-orphan",
    )
    mentions: Mapped[list[Mention]] = relationship(back_populates="linked_entity")


class EntityAlias(IdMixin, Base):
    __tablename__ = "entity_aliases"
    __table_args__ = (UniqueConstraint("entity_id", "alias", "language"),)

    entity_id: Mapped[str] = mapped_column(ForeignKey("entities.id"), nullable=False, index=True)
    alias: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    language: Mapped[str | None] = mapped_column(String(16))
    alias_type: Mapped[str | None] = mapped_column(String(64))
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    entity: Mapped[Entity] = relationship(back_populates="aliases")
