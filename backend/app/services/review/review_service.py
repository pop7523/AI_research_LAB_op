from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import ReviewStatus
from app.models.review import ReviewItem


def ensure_review_item(
    db: Session,
    *,
    target_type: str,
    target_id: str,
    reason: str,
    confidence: float | None = None,
) -> ReviewItem:
    existing = db.scalar(
        select(ReviewItem).where(
            ReviewItem.target_type == target_type,
            ReviewItem.target_id == target_id,
            ReviewItem.status == ReviewStatus.PENDING.value,
        )
    )
    if existing:
        return existing
    item = ReviewItem(
        target_type=target_type,
        target_id=target_id,
        reason=reason,
        confidence=confidence,
    )
    db.add(item)
    db.flush()
    return item

