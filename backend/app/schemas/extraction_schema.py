from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class FactCreate(BaseModel):
    article_id: str
    sentence_id: str | None = None
    subject_entity_id: str | None = None
    predicate: str
    object_entity_id: str | None = None
    object_text: str | None = None
    value: Decimal | None = None
    unit: str | None = None
    currency: str | None = None
    time_scope: str | None = None
    evidence_text: str = Field(min_length=1)
    evidence_span: dict | None = None
    confidence: float = Field(default=0.5, ge=0, le=1)
    evidence_level: str | None = None


class FactRead(FactCreate):
    id: str
    verification_status: str
    needs_review: bool

    model_config = ConfigDict(from_attributes=True)


class ClaimCreate(BaseModel):
    article_id: str
    sentence_id: str | None = None
    speaker_entity_id: str | None = None
    speaker_text: str | None = None
    speaker_type: str | None = None
    claim_type: str
    content: str
    related_entity_ids: list[str] | None = None
    evidence_text: str = Field(min_length=1)
    evidence_span: dict | None = None
    confidence: float = Field(default=0.5, ge=0, le=1)
    possible_incentive: str | None = None
    needs_independent_verification: bool = False


class ClaimRead(ClaimCreate):
    id: str
    claim_status: str
    needs_review: bool

    model_config = ConfigDict(from_attributes=True)


class ExtractionResult(BaseModel):
    facts: list[FactRead]
    claims: list[ClaimRead]

