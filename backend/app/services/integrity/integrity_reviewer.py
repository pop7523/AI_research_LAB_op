from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.issue import Issue
from app.models.perspective import Perspective


def review_issue_integrity(db: Session, issue: Issue) -> dict:
    perspectives = db.scalars(select(Perspective).where(Perspective.issue_id == issue.id)).all()
    perspective_types = {p.perspective_type for p in perspectives if p.perspective_type}
    missing_views = [
        view for view in ("positive", "negative", "neutral") if view not in perspective_types
    ]
    evidence_refs = [ref for p in perspectives for ref in (p.evidence_refs or [])]
    result = {
        "issue_id": issue.id,
        "evidence_assessment": [
            {
                "evidence_ref_count": len(set(evidence_refs)),
                "assessment": "limited" if len(set(evidence_refs)) < 2 else "developing",
            }
        ],
        "counterarguments": [
            "The reported development may be temporary or commercially framed.",
            "Official documents may later narrow or contradict the article-level framing.",
        ],
        "speaker_incentives": [
            "Companies may emphasize strategic benefits.",
            "Analysts may emphasize market-moving interpretations.",
        ],
        "assumptions": [
            "Article evidence is accurately extracted.",
            "Linked entities refer to the intended canonical organizations.",
        ],
        "break_conditions": [
            "Official filing contradicts the reported number.",
            "Follow-up reporting changes the timeframe or subject.",
        ],
        "balance_review": {
            "missing_views": missing_views,
            "overstated_claims": [],
            "needs_revision": bool(missing_views),
        },
    }
    issue.issue_metadata = {**(issue.issue_metadata or {}), "integrity_review": result}
    db.flush()
    return result

