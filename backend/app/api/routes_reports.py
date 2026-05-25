from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import utc_now
from app.db.session import get_db
from app.models.enums import ReportStatus
from app.models.issue import Issue
from app.models.report import Report
from app.schemas.research_schema import ReportApprovalRequest, ReportRead
from app.services.publishing.report_generator import generate_report_for_issue
from app.services.review.review_service import ensure_review_item

router = APIRouter(tags=["reports"])


@router.post("/issues/{issue_id}/generate-report", response_model=ReportRead)
def generate_issue_report(issue_id: str, db: Session = Depends(get_db)) -> Report:
    issue = db.get(Issue, issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="issue not found")
    report = generate_report_for_issue(db, issue)
    db.commit()
    db.refresh(report)
    return report


@router.get("/reports", response_model=list[ReportRead])
def list_reports(db: Session = Depends(get_db)) -> list[Report]:
    return list(db.scalars(select(Report).order_by(Report.created_at.desc())).all())


@router.get("/reports/{report_id}", response_model=ReportRead)
def get_report(report_id: str, db: Session = Depends(get_db)) -> Report:
    report = db.get(Report, report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="report not found")
    return report


@router.post("/reports/{report_id}/submit-review", response_model=ReportRead)
def submit_report_review(report_id: str, db: Session = Depends(get_db)) -> Report:
    report = db.get(Report, report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="report not found")
    report.status = ReportStatus.EDITOR_REVIEW_PENDING.value
    ensure_review_item(
        db,
        target_type="report",
        target_id=report.id,
        reason="final_report_requires_human_review",
    )
    db.commit()
    db.refresh(report)
    return report


@router.post("/reports/{report_id}/approve", response_model=ReportRead)
def approve_report(
    report_id: str,
    payload: ReportApprovalRequest,
    db: Session = Depends(get_db),
) -> Report:
    report = db.get(Report, report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="report not found")
    if not payload.evidence_checked or not payload.balance_checked:
        raise HTTPException(status_code=409, detail="evidence and balance checks are required")
    report.evidence_checked = True
    report.balance_checked = True
    report.editor_approved = True
    report.status = ReportStatus.APPROVED.value
    db.commit()
    db.refresh(report)
    return report


@router.post("/reports/{report_id}/publish", response_model=ReportRead)
def publish_report(report_id: str, db: Session = Depends(get_db)) -> Report:
    report = db.get(Report, report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="report not found")
    if report.status != ReportStatus.APPROVED.value:
        raise HTTPException(status_code=409, detail="report must be approved before publish")
    report.status = ReportStatus.PUBLISHED.value
    report.published_at = utc_now()
    db.commit()
    db.refresh(report)
    return report

