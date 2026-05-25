def _issue(client):
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
            "raw_text": (
                "Nvidia said it will invest $5 billion in Intel. "
                "Analysts expect this may reshape AI chip competition."
            ),
        },
    ).json()
    client.post(f"/articles/{article['id']}/clean")
    client.post(f"/articles/{article['id']}/extract")
    client.post(f"/articles/{article['id']}/link")
    client.post(f"/articles/{article['id']}/extract-facts-claims")
    return client.post(f"/articles/{article['id']}/build-event-issue").json()["issue"]


def test_issue_analysis_creates_balanced_perspectives(client):
    issue = _issue(client)

    response = client.post(f"/issues/{issue['id']}/analyze")

    assert response.status_code == 200
    perspectives = response.json()
    assert {p["perspective_type"] for p in perspectives} == {"positive", "negative", "neutral"}
    assert all(p["evidence_refs"] for p in perspectives)


def test_integrity_review_records_counterarguments_and_balance(client):
    issue = _issue(client)
    client.post(f"/issues/{issue['id']}/analyze")

    response = client.post(f"/issues/{issue['id']}/integrity-review")

    assert response.status_code == 200
    body = response.json()
    assert body["counterarguments"]
    assert body["balance_review"]["needs_revision"] is False

