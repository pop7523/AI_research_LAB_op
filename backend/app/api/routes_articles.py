import feedparser
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import utc_now
from app.db.session import get_db
from app.models.article import Article, ArticleSentence
from app.models.enums import ArticleStatus
from app.schemas.article_schema import (
    ArticleCleanResult,
    ArticleCreate,
    ArticleRead,
    RssIngestRequest,
)
from app.services.cleaning.article_cleaner import clean_article_text, split_sentences
from app.services.ingest.hashing import content_hash

router = APIRouter(tags=["articles"])


def _store_article(db: Session, payload: ArticleCreate) -> Article:
    digest = content_hash(payload.raw_text)
    duplicate = db.scalar(select(Article).where(Article.content_hash == digest).limit(1))
    article = Article(
        **payload.model_dump(),
        collected_at=utc_now(),
        content_hash=digest,
        status=(
            ArticleStatus.DUPLICATE_CANDIDATE.value
            if duplicate
            else ArticleStatus.COLLECTED.value
        ),
        duplicate_of=duplicate.id if duplicate else None,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


@router.post("/articles", response_model=ArticleRead)
def create_article(payload: ArticleCreate, db: Session = Depends(get_db)) -> Article:
    return _store_article(db, payload)


@router.get("/articles", response_model=list[ArticleRead])
def list_articles(db: Session = Depends(get_db)) -> list[Article]:
    return list(db.scalars(select(Article).order_by(Article.created_at.desc())).all())


@router.get("/articles/{article_id}", response_model=ArticleRead)
def get_article(article_id: str, db: Session = Depends(get_db)) -> Article:
    article = db.get(Article, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")
    return article


@router.post("/articles/{article_id}/clean", response_model=ArticleCleanResult)
def clean_article(article_id: str, db: Session = Depends(get_db)) -> ArticleCleanResult:
    article = db.get(Article, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")
    article.clean_text = clean_article_text(article.raw_text or "")
    article.status = ArticleStatus.CLEANED.value
    article.sentences.clear()
    db.flush()
    for span in split_sentences(article.clean_text):
        db.add(ArticleSentence(article_id=article.id, **span.__dict__))
    db.commit()
    db.refresh(article)
    return ArticleCleanResult(article=article, sentences=article.sentences)


@router.post("/ingest/rss", response_model=list[ArticleRead])
def ingest_rss(payload: RssIngestRequest, db: Session = Depends(get_db)) -> list[Article]:
    parsed = feedparser.parse(payload.feed_url)
    articles: list[Article] = []
    for entry in parsed.entries[: payload.limit]:
        title = getattr(entry, "title", "Untitled")
        link = getattr(entry, "link", None)
        text = getattr(entry, "summary", title)
        articles.append(
            _store_article(
                db,
                ArticleCreate(source_id=payload.source_id, title=title, url=link, raw_text=text),
            )
        )
    return articles
