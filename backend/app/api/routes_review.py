from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.enums import ReviewStatus
from app.models.review import ReviewItem
from app.schemas.research_schema import ReviewActionRequest, ReviewItemRead
from app.services.audit.audit_logger import log_action

router = APIRouter(tags=["review"])


@router.get("/review-queue", response_model=list[ReviewItemRead])
def list_review_queue(db: Session = Depends(get_db)) -> list[ReviewItem]:
    return list(
        db.scalars(
            select(ReviewItem)
            .where(ReviewItem.status == ReviewStatus.PENDING.value)
            .order_by(ReviewItem.created_at.asc())
        ).all()
    )


def _review_action(
    db: Session,
    review_item_id: str,
    status: ReviewStatus,
    payload: ReviewActionRequest,
) -> ReviewItem:
    item = db.get(ReviewItem, review_item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="review item not found")
    item.status = status.value
    item.reviewer_note = payload.reviewer_note
    if payload.confidence is not None:
        item.confidence = payload.confidence
    log_action(
        db,
        actor_type="human",
        actor_name="reviewer",
        action=f"review_{status.value.lower()}",
        target_type=item.target_type,
        target_id=item.target_id,
        input_refs={"review_item_id": item.id},
        output_summary={"review_status": item.status},
        confidence=item.confidence,
        reason=item.reviewer_note,
    )
    db.commit()
    db.refresh(item)
    return item


@router.post("/review-items/{review_item_id}/approve", response_model=ReviewItemRead)
def approve_review_item(
    review_item_id: str,
    payload: ReviewActionRequest,
    db: Session = Depends(get_db),
) -> ReviewItem:
    return _review_action(db, review_item_id, ReviewStatus.APPROVED, payload)


@router.post("/review-items/{review_item_id}/reject", response_model=ReviewItemRead)
def reject_review_item(
    review_item_id: str,
    payload: ReviewActionRequest,
    db: Session = Depends(get_db),
) -> ReviewItem:
    return _review_action(db, review_item_id, ReviewStatus.REJECTED, payload)


@router.post("/review-items/{review_item_id}/request-revision", response_model=ReviewItemRead)
def request_review_revision(
    review_item_id: str,
    payload: ReviewActionRequest,
    db: Session = Depends(get_db),
) -> ReviewItem:
    return _review_action(db, review_item_id, ReviewStatus.REVISION_REQUESTED, payload)

