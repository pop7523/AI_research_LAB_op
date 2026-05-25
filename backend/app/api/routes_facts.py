from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.article import Article
from app.models.enums import FactStatus
from app.models.fact import Fact
from app.schemas.extraction_schema import ExtractionResult, FactRead
from app.services.extraction.fact_claim_extractor import extract_facts_claims_for_article
from app.services.review.review_service import ensure_review_item
from app.services.verification.fact_checker import verify_fact

router = APIRouter(tags=["facts"])


@router.post("/articles/{article_id}/extract-facts-claims", response_model=ExtractionResult)
def extract_article_facts_claims(
    article_id: str,
    db: Session = Depends(get_db),
) -> ExtractionResult:
    article = db.get(Article, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")
    facts, claims = extract_facts_claims_for_article(db, article)
    for fact in facts:
        if fact.needs_review:
            ensure_review_item(
                db,
                target_type="fact",
                target_id=fact.id,
                reason="subject_entity_unresolved",
                confidence=fact.confidence,
            )
    db.commit()
    return ExtractionResult(facts=facts, claims=claims)


@router.get("/facts", response_model=list[FactRead])
def list_facts(db: Session = Depends(get_db)) -> list[Fact]:
    return list(db.scalars(select(Fact).order_by(Fact.created_at.desc())).all())


@router.get("/facts/{fact_id}", response_model=FactRead)
def get_fact(fact_id: str, db: Session = Depends(get_db)) -> Fact:
    fact = db.get(Fact, fact_id)
    if fact is None:
        raise HTTPException(status_code=404, detail="fact not found")
    return fact


@router.post("/facts/{fact_id}/verify", response_model=FactRead)
def verify_fact_endpoint(fact_id: str, db: Session = Depends(get_db)) -> Fact:
    fact = db.get(Fact, fact_id)
    if fact is None:
        raise HTTPException(status_code=404, detail="fact not found")
    fact = verify_fact(db, fact)
    if fact.verification_status in {
        FactStatus.NUMBER_MISMATCH.value,
        FactStatus.SOURCE_CONFLICT.value,
        FactStatus.TIMEFRAME_UNCLEAR.value,
    }:
        ensure_review_item(
            db,
            target_type="fact",
            target_id=fact.id,
            reason=fact.verification_status,
            confidence=fact.confidence,
        )
    db.commit()
    db.refresh(fact)
    return fact


@router.post("/facts/{fact_id}/mark-disputed", response_model=FactRead)
def mark_fact_disputed(fact_id: str, db: Session = Depends(get_db)) -> Fact:
    fact = db.get(Fact, fact_id)
    if fact is None:
        raise HTTPException(status_code=404, detail="fact not found")
    fact.verification_status = FactStatus.DISPUTED.value
    fact.needs_review = True
    ensure_review_item(
        db,
        target_type="fact",
        target_id=fact.id,
        reason=FactStatus.DISPUTED.value,
        confidence=fact.confidence,
    )
    db.commit()
    db.refresh(fact)
    return fact

