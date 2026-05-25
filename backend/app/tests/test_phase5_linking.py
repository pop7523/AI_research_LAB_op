from app.models.enums import EntityLinkingStatus


def test_exact_alias_type_match_links_high_confidence(client):
    entity = client.post(
        "/entities",
        json={
            "canonical_name": "NVIDIA Corporation",
            "entity_type": "Company",
            "ticker": "NVDA",
            "aliases": ["엔비디아"],
        },
    ).json()
    article = client.post(
        "/articles",
        json={"title": "Investment", "raw_text": "엔비디아는 인텔에 투자한다고 밝혔다."},
    ).json()
    client.post(f"/articles/{article['id']}/clean")
    client.post(f"/articles/{article['id']}/extract")

    response = client.post(f"/articles/{article['id']}/link")

    mention = response.json()[0]
    assert mention["linked_entity_id"] == entity["id"]
    assert mention["linking_status"] == EntityLinkingStatus.LINKED
    assert mention["linking_confidence"] >= 0.9


def test_ambiguous_alias_requires_review(client):
    client.post(
        "/entities",
        json={
            "canonical_name": "Samsung Electronics",
            "entity_type": "Company",
            "aliases": ["삼성"],
        },
    )
    client.post(
        "/entities",
        json={
            "canonical_name": "Samsung C&T",
            "entity_type": "Company",
            "aliases": ["삼성"],
        },
    )
    article = client.post(
        "/articles",
        json={"title": "Samsung", "raw_text": "삼성은 대규모 투자를 검토 중이다."},
    ).json()
    client.post(f"/articles/{article['id']}/clean")
    client.post(f"/articles/{article['id']}/extract")

    response = client.post(f"/articles/{article['id']}/link")

    mention = response.json()[0]
    assert mention["linking_status"] == EntityLinkingStatus.AMBIGUOUS
    assert mention["linked_entity_id"] is None
    assert mention["needs_review"] is True
