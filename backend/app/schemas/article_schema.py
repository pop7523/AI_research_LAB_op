from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SourceCreate(BaseModel):
    name: str
    url: str | None = None
    source_type: str = "news"
    credibility_level: str | None = None
    credibility_score: float | None = Field(default=None, ge=0, le=1)
    is_official: bool = False


class SourceRead(SourceCreate):
    id: str

    model_config = ConfigDict(from_attributes=True)


class ArticleCreate(BaseModel):
    source_id: str | None = None
    title: str
    url: str | None = None
    author: str | None = None
    published_at: datetime | None = None
    raw_text: str
    language: str = "ko"


class ArticleRead(BaseModel):
    id: str
    source_id: str | None
    title: str
    url: str | None
    raw_text: str | None
    clean_text: str | None
    language: str | None
    content_hash: str | None
    status: str
    duplicate_of: str | None

    model_config = ConfigDict(from_attributes=True)


class ArticleSentenceRead(BaseModel):
    id: str
    article_id: str
    paragraph_index: int
    sentence_index: int
    text: str
    start_offset: int
    end_offset: int

    model_config = ConfigDict(from_attributes=True)


class ArticleCleanResult(BaseModel):
    article: ArticleRead
    sentences: list[ArticleSentenceRead]


class RssIngestRequest(BaseModel):
    source_id: str
    feed_url: str
    limit: int = Field(default=10, ge=1, le=100)

