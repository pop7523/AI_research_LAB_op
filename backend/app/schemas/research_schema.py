from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EventRead(BaseModel):
    id: str
    event_type: str
    title: str | None
    summary: str | None
    event_time: datetime | None
    status: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)


class IssueRead(BaseModel):
    id: str
    title: str
    summary: str | None
    issue_type: str | None
    status: str
    priority: str | None
    uncertainty_note: str | None

    model_config = ConfigDict(from_attributes=True)


class EventIssueResult(BaseModel):
    event: EventRead
    issue: IssueRead


class PerspectiveRead(BaseModel):
    id: str
    issue_id: str
    perspective_type: str | None
    title: str | None
    content: str | None
    status: str
    evidence_refs: list[str] | None
    weaknesses: list[str] | None
    affected_stakeholders: list[str] | None
    confidence: float

    model_config = ConfigDict(from_attributes=True)


class IntegrityReviewRead(BaseModel):
    issue_id: str
    evidence_assessment: list[dict]
    counterarguments: list[str]
    speaker_incentives: list[str]
    assumptions: list[str]
    break_conditions: list[str]
    balance_review: dict


class ReportRead(BaseModel):
    id: str
    issue_id: str
    report_type: str | None
    title: str | None
    body_markdown: str | None
    summary: str | None
    status: str
    evidence_checked: bool
    balance_checked: bool
    editor_approved: bool
    published_at: datetime | None
    version: int

    model_config = ConfigDict(from_attributes=True)


class ReportApprovalRequest(BaseModel):
    evidence_checked: bool = True
    balance_checked: bool = True
    reviewer_note: str | None = None


class ReviewItemRead(BaseModel):
    id: str
    target_type: str
    target_id: str
    reason: str
    status: str
    confidence: float | None
    reviewer_note: str | None

    model_config = ConfigDict(from_attributes=True)


class ReviewActionRequest(BaseModel):
    reviewer_note: str | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)

