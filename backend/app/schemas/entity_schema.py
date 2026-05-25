from pydantic import BaseModel, ConfigDict, Field


class EntityCreate(BaseModel):
    canonical_name: str
    entity_type: str
    description: str | None = None
    country: str | None = None
    industry: str | None = None
    ticker: str | None = None
    aliases: list[str] = Field(default_factory=list)


class EntityRead(BaseModel):
    id: str
    canonical_name: str
    entity_type: str
    description: str | None
    country: str | None
    industry: str | None
    ticker: str | None
    status: str

    model_config = ConfigDict(from_attributes=True)


class EntityAliasCreate(BaseModel):
    alias: str
    language: str | None = "ko"
    alias_type: str | None = "name"
    confidence: float = Field(default=1.0, ge=0, le=1)


class EntityAliasRead(EntityAliasCreate):
    id: str
    entity_id: str

    model_config = ConfigDict(from_attributes=True)


class MentionRead(BaseModel):
    id: str
    article_id: str
    sentence_id: str | None
    mention_text: str
    mention_type: str | None
    sentence: str | None
    linked_entity_id: str | None
    linking_status: str
    linking_confidence: float | None
    linking_reason: str | None
    needs_review: bool

    model_config = ConfigDict(from_attributes=True)


class MentionResolveRequest(BaseModel):
    entity_id: str
    confidence: float = Field(default=1.0, ge=0, le=1)
    reason: str = "manual_review"

