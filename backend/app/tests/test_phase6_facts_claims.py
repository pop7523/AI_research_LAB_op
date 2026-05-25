import pytest
from app.models.claim import Claim
from app.models.fact import Fact
from sqlalchemy.exc import IntegrityError


def _create_linked_article(client):
    client.post(
        "/entities",
        json={
            "canonical_name": "NVIDIA Corporation",
            "entity_type": "Company",
            "ticker": "NVDA",
            "aliases": ["Nvidia"],
        },
    )
    article = client.post(
        "/articles",
        json={
            "title": "Nvidia investment",
            "raw_text": (
                "Nvidia said it will invest $5 billion in Intel. "
                "Analysts expect this may reshape AI chip competition."
            ),
        },
    ).json()
    client.post(f"/articles/{article['id']}/clean")
    client.post(f"/articles/{article['id']}/extract")
    client.post(f"/articles/{article['id']}/link")
    return article


def test_extract_facts_and_claims_with_evidence(client):
    article = _create_linked_article(client)

    response = client.post(f"/articles/{article['id']}/extract-facts-claims")

    assert response.status_code == 200
    body = response.json()
    assert len(body["facts"]) == 1
    assert len(body["claims"]) >= 1
    fact = body["facts"][0]
    assert fact["evidence_text"]
    assert fact["evidence_span"]["sentence_id"]
    assert fact["value"] == "5000000000"
    assert body["claims"][0]["needs_independent_verification"] is True


def test_fact_and_claim_require_evidence(db_session):
    db_session.add(Fact(article_id="article", predicate="reported", evidence_text=""))
    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()

    db_session.add(
        Claim(article_id="article", claim_type="interpretation", content="x", evidence_text="")
    )
    with pytest.raises(IntegrityError):
        db_session.flush()
