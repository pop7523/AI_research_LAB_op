from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import FactStatus
from app.models.fact import Fact


def verify_fact(db: Session, fact: Fact) -> Fact:
    matches = db.scalars(
        select(Fact).where(
            Fact.id != fact.id,
            Fact.subject_entity_id == fact.subject_entity_id,
            Fact.predicate == fact.predicate,
        )
    ).all()
    if not matches:
        fact.verification_status = FactStatus.UNVERIFIED.value
        db.flush()
        return fact

    value_matches = [match for match in matches if match.value == fact.value]
    value_conflicts = [
        match for match in matches if match.value is not None and match.value != fact.value
    ]
    if value_conflicts:
        fact.verification_status = FactStatus.NUMBER_MISMATCH.value
    elif value_matches:
        sources = [fact.article.source, *(match.article.source for match in value_matches)]
        fact.verification_status = (
            FactStatus.VERIFIED.value
            if any(source and source.is_official for source in sources)
            else FactStatus.PARTIALLY_VERIFIED.value
        )
    else:
        fact.verification_status = FactStatus.UNVERIFIED.value
    db.flush()
    return fact
