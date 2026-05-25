def test_extract_mentions_from_seeded_aliases(client):
    nvidia = client.post(
        "/entities",
        json={
            "canonical_name": "NVIDIA Corporation",
            "entity_type": "Company",
            "ticker": "NVDA",
            "aliases": ["엔비디아", "Nvidia"],
        },
    ).json()
    article = client.post(
        "/articles",
        json={"title": "AI chip", "raw_text": "엔비디아는 AI 칩 수요가 강하다고 밝혔다."},
    ).json()
    client.post(f"/articles/{article['id']}/clean")

    response = client.post(f"/articles/{article['id']}/extract")

    assert response.status_code == 200
    mentions = response.json()
    assert mentions[0]["mention_text"] == "엔비디아"
    assert mentions[0]["mention_type"] == "Company"
    assert mentions[0]["linked_entity_id"] is None
    assert nvidia["canonical_name"] == "NVIDIA Corporation"

