from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin
from app.models.enums import ArticleStatus

if TYPE_CHECKING:
    from app.models.mention import Mention
    from app.models.source import Source


class Article(IdMixin, TimestampMixin, Base):
    __tablename__ = "articles"

    source_id: Mapped[str | None] = mapped_column(ForeignKey("sources.id"))
    title: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str | None] = mapped_column(Text, unique=True)
    author: Mapped[str | None] = mapped_column(Text)
    published_at: Mapped[datetime | None] = mapped_column(DateTime)
    collected_at: Mapped[datetime | None] = mapped_column(DateTime)
    raw_html_path: Mapped[str | None] = mapped_column(Text)
    raw_text: Mapped[str | None] = mapped_column(Text)
    clean_text: Mapped[str | None] = mapped_column(Text)
    language: Mapped[str | None] = mapped_column(String(16))
    content_hash: Mapped[str | None] = mapped_column(String(64), index=True)
    status: Mapped[str] = mapped_column(
        String(64),
        default=ArticleStatus.COLLECTED.value,
        nullable=False,
    )
    duplicate_of: Mapped[str | None] = mapped_column(ForeignKey("articles.id"))
    article_metadata: Mapped[dict | None] = mapped_column("metadata", JSON)

    source: Mapped[Source | None] = relationship(back_populates="articles")
    sentences: Mapped[list[ArticleSentence]] = relationship(
        back_populates="article",
        cascade="all, delete-orphan",
    )
    mentions: Mapped[list[Mention]] = relationship(
        back_populates="article",
        cascade="all, delete-orphan",
    )


class ArticleSentence(IdMixin, Base):
    __tablename__ = "article_sentences"

    article_id: Mapped[str] = mapped_column(ForeignKey("articles.id"), nullable=False, index=True)
    paragraph_index: Mapped[int] = mapped_column(Integer, nullable=False)
    sentence_index: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    start_offset: Mapped[int] = mapped_column(Integer, nullable=False)
    end_offset: Mapped[int] = mapped_column(Integer, nullable=False)

    article: Mapped[Article] = relationship(back_populates="sentences")
