from app.models.enums import ArticleStatus
from app.services.ingest.hashing import content_hash


def test_create_source_and_article(client):
    source_response = client.post("/sources", json={"name": "Test News", "source_type": "news"})
    assert source_response.status_code == 200
    source_id = source_response.json()["id"]

    article_response = client.post(
        "/articles",
        json={
            "source_id": source_id,
            "title": "Nvidia invests in Intel",
            "url": "https://example.com/a",
            "raw_text": "Nvidia said it will invest $5 billion in Intel.",
        },
    )

    assert article_response.status_code == 200
    article = article_response.json()
    assert article["status"] == ArticleStatus.COLLECTED
    expected_hash = content_hash("Nvidia said it will invest $5 billion in Intel.")
    assert article["content_hash"] == expected_hash


def test_duplicate_article_is_candidate(client):
    payload = {
        "title": "Same article",
        "raw_text": "Same text.\n\nSame text.",
    }
    first = client.post("/articles", json=payload).json()
    second = client.post("/articles", json={**payload, "title": "Same article copy"}).json()

    assert first["status"] == ArticleStatus.COLLECTED
    assert second["status"] == ArticleStatus.DUPLICATE_CANDIDATE
    assert second["duplicate_of"] == first["id"]
