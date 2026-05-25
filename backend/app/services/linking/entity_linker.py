from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entity import Entity, EntityAlias
from app.models.enums import EntityLinkingStatus
from app.models.mention import Mention


@dataclass(frozen=True)
class LinkCandidate:
    entity: Entity
    score: float
    reason: str


def score_link_candidates(db: Session, mention: Mention) -> list[LinkCandidate]:
    text = mention.mention_text.strip().lower()
    aliases = db.scalars(
        select(EntityAlias).where(EntityAlias.alias.ilike(mention.mention_text))
    ).all()
    candidates: list[LinkCandidate] = []

    for alias in aliases:
        score = 0.80 * alias.confidence
        reasons = ["exact_alias"]
        if mention.mention_type and alias.entity.entity_type == mention.mention_type:
            score += 0.10
            reasons.append("type_match")
        if alias.entity.ticker and alias.entity.ticker.lower() == text:
            score += 0.10
            reasons.append("ticker_match")
        candidates.append(LinkCandidate(alias.entity, min(score, 1.0), "+".join(reasons)))

    return sorted(candidates, key=lambda candidate: candidate.score, reverse=True)


def classify_link(candidates: list[LinkCandidate]) -> tuple[str, LinkCandidate | None, bool]:
    if not candidates:
        return EntityLinkingStatus.UNRESOLVED.value, None, False
    if len(candidates) > 1 and candidates[0].score - candidates[1].score < 0.15:
        return EntityLinkingStatus.AMBIGUOUS.value, candidates[0], True
    top = candidates[0]
    if top.score >= 0.90:
        return EntityLinkingStatus.LINKED.value, top, False
    if top.score >= 0.70:
        return EntityLinkingStatus.PROVISIONAL_LINK.value, top, True
    if top.score >= 0.50:
        return EntityLinkingStatus.AMBIGUOUS.value, top, True
    return EntityLinkingStatus.UNRESOLVED.value, None, False


def link_mention(db: Session, mention: Mention) -> Mention:
    status, candidate, needs_review = classify_link(score_link_candidates(db, mention))
    mention.linking_status = status
    mention.needs_review = needs_review
    if candidate is not None and status != EntityLinkingStatus.AMBIGUOUS.value:
        mention.linked_entity_id = candidate.entity.id
        mention.linking_confidence = candidate.score
        mention.linking_reason = candidate.reason
    elif candidate is not None:
        mention.linked_entity_id = None
        mention.linking_confidence = candidate.score
        mention.linking_reason = f"ambiguous_candidate:{candidate.entity.id}:{candidate.reason}"
    else:
        mention.linked_entity_id = None
        mention.linking_confidence = None
        mention.linking_reason = "no_candidate"
    db.flush()
    return mention


def link_mentions_for_article(db: Session, article_id: str) -> list[Mention]:
    mentions = db.scalars(select(Mention).where(Mention.article_id == article_id)).all()
    return [link_mention(db, mention) for mention in mentions]
