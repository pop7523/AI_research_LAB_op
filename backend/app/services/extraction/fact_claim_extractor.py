import re
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.article import Article, ArticleSentence
from app.models.claim import Claim
from app.models.enums import ClaimStatus, FactStatus
from app.models.fact import Fact
from app.models.mention import Mention

CLAIM_HINTS = (
    "said",
    "says",
    "according to",
    "analyst",
    "expects",
    "forecast",
    "may",
    "could",
    "believes",
    "밝혔다",
    "말했다",
    "전망",
    "예상",
    "주장",
    "우려",
    "가능성",
)


def _money_value(text: str) -> tuple[Decimal | None, str | None, str | None]:
    dollar_match = re.search(r"\$([\d,.]+)\s*(billion|million)?", text, flags=re.IGNORECASE)
    if dollar_match:
        value = Decimal(dollar_match.group(1).replace(",", ""))
        scale = dollar_match.group(2)
        if scale and scale.lower() == "billion":
            value *= Decimal("1000000000")
        if scale and scale.lower() == "million":
            value *= Decimal("1000000")
        return value, "USD", "money"
    won_match = re.search(r"([\d,.]+)\s*(조|억)?\s*원", text)
    if won_match:
        value = Decimal(won_match.group(1).replace(",", ""))
        scale = won_match.group(2)
        if scale == "조":
            value *= Decimal("1000000000000")
        if scale == "억":
            value *= Decimal("100000000")
        return value, "KRW", "money"
    number_match = re.search(r"\b(\d+(?:\.\d+)?)\b", text)
    if number_match:
        return Decimal(number_match.group(1)), None, "number"
    return None, None, None


def _sentence_span(sentence: ArticleSentence) -> dict:
    return {
        "sentence_id": sentence.id,
        "paragraph_index": sentence.paragraph_index,
        "sentence_index": sentence.sentence_index,
        "start_offset": sentence.start_offset,
        "end_offset": sentence.end_offset,
    }


def _first_linked_mention(db: Session, article_id: str) -> Mention | None:
    return db.scalar(
        select(Mention)
        .where(Mention.article_id == article_id, Mention.linked_entity_id.is_not(None))
        .order_by(Mention.id)
    )


def extract_facts_claims_for_article(
    db: Session,
    article: Article,
) -> tuple[list[Fact], list[Claim]]:
    sentences = db.scalars(
        select(ArticleSentence).where(ArticleSentence.article_id == article.id)
    ).all()
    subject = _first_linked_mention(db, article.id)
    facts: list[Fact] = []
    claims: list[Claim] = []

    for sentence in sentences:
        text = sentence.text.strip()
        lower = text.lower()
        evidence_span = _sentence_span(sentence)
        value, currency, unit = _money_value(text)
        has_claim_hint = any(hint in lower for hint in CLAIM_HINTS)

        if value is not None and ("invest" in lower or "투자" in text or "매출" in text):
            fact = Fact(
                article_id=article.id,
                sentence_id=sentence.id,
                subject_entity_id=subject.linked_entity_id if subject else None,
                predicate="reported_numeric_development",
                object_text=text,
                value=value,
                unit=unit,
                currency=currency,
                evidence_text=text,
                evidence_span=evidence_span,
                confidence=0.78 if subject else 0.62,
                verification_status=FactStatus.EXTRACTED.value,
                evidence_level="article_sentence",
                needs_review=subject is None,
            )
            db.add(fact)
            facts.append(fact)

        if has_claim_hint:
            claim_type = (
                "attributed_statement"
                if ("said" in lower or "밝혔다" in text)
                else "interpretation"
            )
            related_ids = [subject.linked_entity_id] if subject and subject.linked_entity_id else []
            claim = Claim(
                article_id=article.id,
                sentence_id=sentence.id,
                speaker_text="article_source",
                speaker_type="source",
                claim_type=claim_type,
                content=text,
                related_entity_ids=related_ids,
                evidence_text=text,
                evidence_span=evidence_span,
                confidence=0.72,
                claim_status=ClaimStatus.ATTRIBUTED.value,
                needs_independent_verification=True,
                needs_review=False,
            )
            db.add(claim)
            claims.append(claim)

    db.flush()
    return facts, claims
