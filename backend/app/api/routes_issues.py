from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.issue import Issue
from app.models.perspective import Perspective
from app.schemas.research_schema import IntegrityReviewRead, IssueRead, PerspectiveRead
from app.services.analysis.analyst import analyze_issue
from app.services.integrity.integrity_reviewer import review_issue_integrity

router = APIRouter(tags=["issues"])


@router.get("/issues", response_model=list[IssueRead])
def list_issues(db: Session = Depends(get_db)) -> list[Issue]:
    return list(db.scalars(select(Issue).order_by(Issue.created_at.desc())).all())


@router.get("/issues/{issue_id}", response_model=IssueRead)
def get_issue(issue_id: str, db: Session = Depends(get_db)) -> Issue:
    issue = db.get(Issue, issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="issue not found")
    return issue


@router.post("/issues/{issue_id}/analyze", response_model=list[PerspectiveRead])
def analyze_issue_endpoint(issue_id: str, db: Session = Depends(get_db)) -> list[Perspective]:
    issue = db.get(Issue, issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="issue not found")
    perspectives = analyze_issue(db, issue)
    db.commit()
    return perspectives


@router.post("/issues/{issue_id}/integrity-review", response_model=IntegrityReviewRead)
def review_issue_integrity_endpoint(
    issue_id: str,
    db: Session = Depends(get_db),
) -> dict:
    issue = db.get(Issue, issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="issue not found")
    result = review_issue_integrity(db, issue)
    db.commit()
    return result

