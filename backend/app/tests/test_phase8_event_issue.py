def _article_with_fact_claim(client):
    client.post(
        "/entities",
        json={
            "canonical_name": "NVIDIA Corporation",
            "entity_type": "Company",
            "aliases": ["Nvidia"],
        },
    )
    article = client.post(
        "/articles",
        json={
            "title": "Nvidia investment",
            "raw_text": "Nvidia said it will invest $5 billion in Intel.",
        },
    ).json()
    client.post(f"/articles/{article['id']}/clean")
    client.post(f"/articles/{article['id']}/extract")
    client.post(f"/articles/{article['id']}/link")
    client.post(f"/articles/{article['id']}/extract-facts-claims")
    return article


def test_build_event_and_issue_from_article(client):
    article = _article_with_fact_claim(client)

    response = client.post(f"/articles/{article['id']}/build-event-issue")

    assert response.status_code == 200
    body = response.json()
    assert body["event"]["status"] == "CANDIDATE"
    assert body["issue"]["title"]
    assert client.get("/events").json()[0]["id"] == body["event"]["id"]
    assert client.get("/issues").json()[0]["id"] == body["issue"]["id"]

