from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import PerspectiveStatus
from app.models.issue import Issue, IssueLink
from app.models.perspective import Perspective


def analyze_issue(db: Session, issue: Issue) -> list[Perspective]:
    existing = db.scalars(select(Perspective).where(Perspective.issue_id == issue.id)).all()
    if existing:
        return existing
    links = db.scalars(select(IssueLink).where(IssueLink.issue_id == issue.id)).all()
    evidence_refs = [
        ref
        for link in links
        for ref in (link.fact_id, link.claim_id, link.event_id, link.article_id)
        if ref
    ]
    perspectives = [
        Perspective(
            issue_id=issue.id,
            perspective_type="positive",
            title="Constructive interpretation",
            content="The available evidence may indicate a meaningful strategic development.",
            status=PerspectiveStatus.PLAUSIBLE_VIEW.value,
            evidence_refs=evidence_refs[:5],
            weaknesses=["Evidence is still article-level and may lack official confirmation."],
            affected_stakeholders=["companies", "investors", "customers"],
            confidence=0.58,
        ),
        Perspective(
            issue_id=issue.id,
            perspective_type="negative",
            title="Skeptical interpretation",
            content="The evidence may be overstated if claims are not independently verified.",
            status=PerspectiveStatus.PLAUSIBLE_VIEW.value,
            evidence_refs=evidence_refs[:5],
            weaknesses=["Counterevidence may not yet be collected."],
            affected_stakeholders=["investors", "policy makers"],
            confidence=0.54,
        ),
        Perspective(
            issue_id=issue.id,
            perspective_type="neutral",
            title="Wait-and-see interpretation",
            content=(
                "The issue should remain open until official data or repeated reporting arrives."
            ),
            status=PerspectiveStatus.SUPPORTED_VIEW.value,
            evidence_refs=evidence_refs[:5],
            weaknesses=["May understate early directional signals."],
            affected_stakeholders=["editors", "readers"],
            confidence=0.66,
        ),
    ]
    db.add_all(perspectives)
    issue.issue_metadata = {
        **(issue.issue_metadata or {}),
        "analysis": {
            "stakeholders": ["companies", "investors", "policy makers", "readers"],
            "key_debates": ["evidence strength", "financial impact", "timing"],
            "key_data_to_watch": ["official filings", "earnings commentary", "follow-up reporting"],
            "uncertainties": ["source independence", "timeframe", "numeric comparability"],
        },
    }
    db.flush()
    return perspectives
