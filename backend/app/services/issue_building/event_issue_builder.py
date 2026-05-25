from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import utc_now
from app.models.article import Article
from app.models.claim import Claim
from app.models.enums import EventStatus, IssueStatus
from app.models.event import Event, EventLink
from app.models.fact import Fact
from app.models.issue import Issue, IssueLink


def build_event_and_issue_for_article(db: Session, article: Article) -> tuple[Event, Issue]:
    facts = db.scalars(select(Fact).where(Fact.article_id == article.id)).all()
    claims = db.scalars(select(Claim).where(Claim.article_id == article.id)).all()
    first_fact = facts[0] if facts else None
    title_seed = (
        first_fact.object_text[:80] if first_fact and first_fact.object_text else article.title
    )
    event_title = f"Article development: {title_seed}"
    event = db.scalar(select(Event).where(Event.title == event_title))
    if event is None:
        event = Event(
            event_type="article_development",
            title=event_title,
            summary=article.clean_text[:240] if article.clean_text else article.raw_text[:240],
            status=EventStatus.CANDIDATE.value,
            confidence=0.64,
            event_metadata={"article_id": article.id},
        )
        db.add(event)
        db.flush()

    for fact in facts:
        db.add(
            EventLink(
                event_id=event.id,
                fact_id=fact.id,
                article_id=article.id,
                relation_type="supported_by_fact",
                confidence=0.72,
            )
        )
    for claim in claims:
        db.add(
            EventLink(
                event_id=event.id,
                claim_id=claim.id,
                article_id=article.id,
                relation_type="contextual_claim",
                confidence=0.58,
            )
        )

    issue_title = "AI investment and market evidence review"
    if "규제" in (article.clean_text or article.raw_text or ""):
        issue_title = "Policy and regulation evidence review"
    issue = db.scalar(select(Issue).where(Issue.title == issue_title))
    if issue is None:
        issue = Issue(
            title=issue_title,
            summary="A developing issue assembled from article facts, claims, and events.",
            issue_type="market_research",
            status=IssueStatus.CANDIDATE.value,
            priority="normal",
            first_seen_at=utc_now(),
            last_updated_at=utc_now(),
            editorial_reason="Article contains structured facts or attributed claims.",
            uncertainty_note="Early issue candidate; requires verification and editorial review.",
            issue_metadata={"source_article_ids": [article.id]},
        )
        db.add(issue)
        db.flush()
    else:
        issue.last_updated_at = utc_now()

    db.add(
        IssueLink(
            issue_id=issue.id,
            article_id=article.id,
            event_id=event.id,
            link_type="article_event_assignment",
            confidence=0.66,
            reason="Article facts and claims match the issue theme.",
        )
    )
    db.flush()
    return event, issue
