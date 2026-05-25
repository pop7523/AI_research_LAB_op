from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.claim import Claim
from app.models.enums import ClaimStatus
from app.schemas.extraction_schema import ClaimRead

router = APIRouter(tags=["claims"])


@router.get("/claims", response_model=list[ClaimRead])
def list_claims(db: Session = Depends(get_db)) -> list[Claim]:
    return list(db.scalars(select(Claim).order_by(Claim.created_at.desc())).all())


@router.get("/claims/{claim_id}", response_model=ClaimRead)
def get_claim(claim_id: str, db: Session = Depends(get_db)) -> Claim:
    claim = db.get(Claim, claim_id)
    if claim is None:
        raise HTTPException(status_code=404, detail="claim not found")
    return claim


@router.post("/claims/{claim_id}/analyze-incentive", response_model=ClaimRead)
def analyze_claim_incentive(claim_id: str, db: Session = Depends(get_db)) -> Claim:
    claim = db.get(Claim, claim_id)
    if claim is None:
        raise HTTPException(status_code=404, detail="claim not found")
    claim.possible_incentive = "Speaker or source may benefit from shaping interpretation."
    claim.claim_status = ClaimStatus.INCENTIVE_ANALYZED.value
    db.commit()
    db.refresh(claim)
    return claim
