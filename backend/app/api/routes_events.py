from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.article import Article
from app.models.event import Event
from app.schemas.research_schema import EventIssueResult, EventRead
from app.services.issue_building.event_issue_builder import build_event_and_issue_for_article

router = APIRouter(tags=["events"])


@router.post("/articles/{article_id}/build-event-issue", response_model=EventIssueResult)
def build_article_event_issue(article_id: str, db: Session = Depends(get_db)) -> EventIssueResult:
    article = db.get(Article, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")
    event, issue = build_event_and_issue_for_article(db, article)
    db.commit()
    return EventIssueResult(event=event, issue=issue)


@router.get("/events", response_model=list[EventRead])
def list_events(db: Session = Depends(get_db)) -> list[Event]:
    return list(db.scalars(select(Event).order_by(Event.created_at.desc())).all())

