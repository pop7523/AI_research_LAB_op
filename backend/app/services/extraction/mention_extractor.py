from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.article import Article, ArticleSentence
from app.models.entity import EntityAlias
from app.models.mention import Mention


def extract_mentions_for_article(db: Session, article: Article) -> list[Mention]:
    sentences = db.scalars(
        select(ArticleSentence).where(ArticleSentence.article_id == article.id)
    ).all()
    if not sentences:
        return []

    aliases = db.scalars(select(EntityAlias)).all()
    existing = {
        (m.sentence_id, m.mention_text)
        for m in db.scalars(select(Mention).where(Mention.article_id == article.id)).all()
    }
    mentions: list[Mention] = []

    for sentence in sentences:
        for alias in aliases:
            start = sentence.text.lower().find(alias.alias.lower())
            if start < 0 or (sentence.id, alias.alias) in existing:
                continue
            mention = Mention(
                article_id=article.id,
                sentence_id=sentence.id,
                mention_text=alias.alias,
                mention_type=alias.entity.entity_type,
                sentence=sentence.text,
                paragraph_index=sentence.paragraph_index,
                start_offset=sentence.start_offset + start,
                end_offset=sentence.start_offset + start + len(alias.alias),
            )
            db.add(mention)
            mentions.append(mention)
    db.flush()
    return mentions

