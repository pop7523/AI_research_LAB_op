from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import utc_now
from app.models.enums import ReportStatus
from app.models.issue import Issue
from app.models.perspective import Perspective
from app.models.report import Report


def generate_report_for_issue(db: Session, issue: Issue) -> Report:
    perspectives = db.scalars(select(Perspective).where(Perspective.issue_id == issue.id)).all()
    lines = [
        f"# {issue.title}",
        "",
        "## 3줄 요약",
        f"- {issue.summary or '이슈 요약이 아직 제한적입니다.'}",
        "- 확인된 사실과 주장을 분리해 추가 검증이 필요합니다.",
        "- 반론과 불확실성을 함께 추적해야 합니다.",
        "",
        "## 확인된 사실",
        "- 현재 MVP에서는 evidence reference가 있는 fact만 이 섹션에 들어갈 수 있습니다.",
        "",
        "## 관점별 해석",
    ]
    for perspective in perspectives:
        lines.extend(
            [
                f"### {perspective.title}",
                perspective.content or "",
                f"- 근거: {', '.join(perspective.evidence_refs or []) or '없음'}",
                f"- 약점: {', '.join(perspective.weaknesses or []) or '없음'}",
            ]
        )
    lines.extend(
        [
            "",
            "## 리스크와 불확실성",
            f"- {issue.uncertainty_note or '추가 검증 필요'}",
            "",
            "## 검증 필요 사항",
            "- 공식자료 확인",
            "- 수치와 기간 재검증",
            "- 이해관계자별 유인 검토",
            "",
            "## 업데이트 이력",
            f"- {utc_now().date()}: draft generated",
        ]
    )
    report = Report(
        issue_id=issue.id,
        report_type="issue_brief",
        title=issue.title,
        summary=issue.summary,
        body_markdown="\n".join(lines),
        status=ReportStatus.DRAFT.value,
    )
    db.add(report)
    db.flush()
    return report

