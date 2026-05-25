def _ready_issue(client):
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
    issue = client.post(f"/articles/{article['id']}/build-event-issue").json()["issue"]
    client.post(f"/issues/{issue['id']}/analyze")
    client.post(f"/issues/{issue['id']}/integrity-review")
    return issue


def test_report_generation_requires_approval_before_publish(client):
    issue = _ready_issue(client)
    report = client.post(f"/issues/{issue['id']}/generate-report").json()

    publish_response = client.post(f"/reports/{report['id']}/publish")

    assert report["status"] == "DRAFT"
    assert publish_response.status_code == 409
    assert "관점별 해석" in report["body_markdown"]


def test_report_review_approval_and_publish_flow(client):
    issue = _ready_issue(client)
    report = client.post(f"/issues/{issue['id']}/generate-report").json()

    submitted = client.post(f"/reports/{report['id']}/submit-review").json()
    queue = client.get("/review-queue").json()
    bad_approval = client.post(
        f"/reports/{report['id']}/approve",
        json={"evidence_checked": True, "balance_checked": False},
    )
    approved = client.post(
        f"/reports/{report['id']}/approve",
        json={"evidence_checked": True, "balance_checked": True},
    ).json()
    published = client.post(f"/reports/{report['id']}/publish").json()

    assert submitted["status"] == "EDITOR_REVIEW_PENDING"
    assert any(item["target_id"] == report["id"] for item in queue)
    assert bad_approval.status_code == 409
    assert approved["status"] == "APPROVED"
    assert published["status"] == "PUBLISHED"


def test_review_queue_actions_create_audit_log(client):
    issue = _ready_issue(client)
    report = client.post(f"/issues/{issue['id']}/generate-report").json()
    client.post(f"/reports/{report['id']}/submit-review")
    item = client.get("/review-queue").json()[0]

    response = client.post(
        f"/review-items/{item['id']}/approve",
        json={"reviewer_note": "Looks acceptable.", "confidence": 0.9},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "APPROVED"

