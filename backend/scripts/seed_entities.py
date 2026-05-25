from app.db.session import SessionLocal
from app.models.entity import Entity, EntityAlias
from sqlalchemy.orm import Session

SEED_ENTITIES = [
    {
        "canonical_name": "NVIDIA Corporation",
        "entity_type": "Company",
        "ticker": "NVDA",
        "aliases": ["Nvidia", "엔비디아", "NVDA"],
    },
    {
        "canonical_name": "Intel Corporation",
        "entity_type": "Company",
        "ticker": "INTC",
        "aliases": ["Intel", "인텔", "INTC"],
    },
    {
        "canonical_name": "Samsung Electronics",
        "entity_type": "Company",
        "ticker": "005930",
        "aliases": ["삼성", "삼성전자", "Samsung"],
    },
]


def seed(db: Session) -> None:
    for item in SEED_ENTITIES:
        aliases = item.pop("aliases")
        entity = Entity(**item)
        db.add(entity)
        db.flush()
        for alias in aliases:
            db.add(EntityAlias(entity_id=entity.id, alias=alias, language="ko", alias_type="name"))
    db.commit()


if __name__ == "__main__":
    with SessionLocal() as session:
        seed(session)

