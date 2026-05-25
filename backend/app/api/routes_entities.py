from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.article import Article
from app.models.entity import Entity, EntityAlias
from app.models.enums import EntityLinkingStatus
from app.models.mention import Mention
from app.schemas.entity_schema import (
    EntityAliasCreate,
    EntityAliasRead,
    EntityCreate,
    EntityRead,
    MentionRead,
    MentionResolveRequest,
)
from app.services.audit.audit_logger import log_action
from app.services.extraction.mention_extractor import extract_mentions_for_article
from app.services.linking.entity_linker import link_mentions_for_article
from app.services.review.review_service import ensure_review_item

router = APIRouter(tags=["entities"])


@router.post("/entities", response_model=EntityRead)
def create_entity(payload: EntityCreate, db: Session = Depends(get_db)) -> Entity:
    aliases = payload.aliases or [payload.canonical_name]
    data = payload.model_dump(exclude={"aliases"})
    entity = Entity(**data)
    db.add(entity)
    db.flush()
    for alias in aliases:
        db.add(EntityAlias(entity_id=entity.id, alias=alias, language="ko", alias_type="name"))
    db.commit()
    db.refresh(entity)
    return entity


@router.get("/entities", response_model=list[EntityRead])
def list_entities(db: Session = Depends(get_db)) -> list[Entity]:
    return list(db.scalars(select(Entity).order_by(Entity.canonical_name)).all())


@router.get("/entities/{entity_id}", response_model=EntityRead)
def get_entity(entity_id: str, db: Session = Depends(get_db)) -> Entity:
    entity = db.get(Entity, entity_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="entity not found")
    return entity


@router.post("/entities/{entity_id}/aliases", response_model=EntityAliasRead)
def create_entity_alias(
    entity_id: str,
    payload: EntityAliasCreate,
    db: Session = Depends(get_db),
) -> EntityAlias:
    if db.get(Entity, entity_id) is None:
        raise HTTPException(status_code=404, detail="entity not found")
    alias = EntityAlias(entity_id=entity_id, **payload.model_dump())
    db.add(alias)
    db.commit()
    db.refresh(alias)
    return alias


@router.post("/articles/{article_id}/extract", response_model=list[MentionRead])
def extract_article_mentions(article_id: str, db: Session = Depends(get_db)) -> list[Mention]:
    article = db.get(Article, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")
    mentions = extract_mentions_for_article(db, article)
    db.commit()
    return mentions


@router.post("/articles/{article_id}/link", response_model=list[MentionRead])
def link_article_mentions(article_id: str, db: Session = Depends(get_db)) -> list[Mention]:
    if db.get(Article, article_id) is None:
        raise HTTPException(status_code=404, detail="article not found")
    mentions = link_mentions_for_article(db, article_id)
    for mention in mentions:
        if mention.needs_review:
            ensure_review_item(
                db,
                target_type="mention",
                target_id=mention.id,
                reason=mention.linking_status,
                confidence=mention.linking_confidence,
            )
    db.commit()
    return mentions


@router.post("/mentions/{mention_id}/resolve", response_model=MentionRead)
def resolve_mention(
    mention_id: str,
    payload: MentionResolveRequest,
    db: Session = Depends(get_db),
) -> Mention:
    mention = db.get(Mention, mention_id)
    entity = db.get(Entity, payload.entity_id)
    if mention is None:
        raise HTTPException(status_code=404, detail="mention not found")
    if entity is None:
        raise HTTPException(status_code=404, detail="entity not found")
    mention.linked_entity_id = entity.id
    mention.linking_status = EntityLinkingStatus.LINKED.value
    mention.linking_confidence = payload.confidence
    mention.linking_reason = payload.reason
    mention.needs_review = False
    log_action(
        db,
        actor_type="human",
        actor_name="reviewer",
        action="resolve_mention",
        target_type="mention",
        target_id=mention.id,
        input_refs={"entity_id": entity.id},
        output_summary={"linking_status": mention.linking_status},
        confidence=payload.confidence,
        reason=payload.reason,
    )
    db.commit()
    db.refresh(mention)
    return mention
