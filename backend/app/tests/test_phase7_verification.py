from app.models.enums import FactStatus


def _seed_entity(client):
    return client.post(
        "/entities",
        json={
            "canonical_name": "NVIDIA Corporation",
            "entity_type": "Company",
            "ticker": "NVDA",
            "aliases": ["Nvidia"],
        },
    ).json()


def _article_to_fact(client, raw_text, source_id=None):
    article = client.post(
        "/articles",
        json={"source_id": source_id, "title": "Fact article", "raw_text": raw_text},
    ).json()
    client.post(f"/articles/{article['id']}/clean")
    client.post(f"/articles/{article['id']}/extract")
    client.post(f"/articles/{article['id']}/link")
    extraction = client.post(f"/articles/{article['id']}/extract-facts-claims").json()
    return extraction["facts"][0]


def test_fact_without_match_is_unverified(client):
    _seed_entity(client)
    fact = _article_to_fact(client, "Nvidia said it will invest $5 billion in Intel.")

    response = client.post(f"/facts/{fact['id']}/verify")

    assert response.status_code == 200
    assert response.json()["verification_status"] == FactStatus.UNVERIFIED


def test_matching_official_fact_verifies(client):
    _seed_entity(client)
    official = client.post(
        "/sources",
        json={"name": "Official", "source_type": "official", "is_official": True},
    ).json()
    fact_a = _article_to_fact(
        client,
        "Nvidia said it will invest $5 billion in Intel.",
        source_id=official["id"],
    )
    fact_b = _article_to_fact(client, "Nvidia said it will invest $5 billion in Intel.")

    client.post(f"/facts/{fact_a['id']}/verify")
    response = client.post(f"/facts/{fact_b['id']}/verify")

    assert response.json()["verification_status"] == FactStatus.VERIFIED


def test_number_mismatch_creates_review_item(client):
    _seed_entity(client)
    _article_to_fact(client, "Nvidia said it will invest $5 billion in Intel.")
    fact_b = _article_to_fact(client, "Nvidia said it will invest $6 billion in Intel.")

    response = client.post(f"/facts/{fact_b['id']}/verify")
    queue = client.get("/review-queue").json()

    assert response.json()["verification_status"] == FactStatus.NUMBER_MISMATCH
    assert any(item["target_id"] == fact_b["id"] for item in queue)

