from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def log_action(
    db: Session,
    *,
    actor_type: str,
    actor_name: str,
    action: str,
    target_type: str,
    target_id: str,
    input_refs: dict | list | None = None,
    output_summary: dict | list | None = None,
    confidence: float | None = None,
    reason: str | None = None,
) -> AuditLog:
    entry = AuditLog(
        actor_type=actor_type,
        actor_name=actor_name,
        action=action,
        target_type=target_type,
        target_id=target_id,
        input_refs=input_refs,
        output_summary=output_summary,
        confidence=confidence,
        reason=reason,
    )
    db.add(entry)
    db.flush()
    return entry

