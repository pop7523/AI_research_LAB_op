import json
from pathlib import Path


def test_golden_article_fixtures_are_structured():
    fixture_dir = Path("tests/golden_articles")
    fixtures = [
        fixture
        for fixture in sorted(fixture_dir.glob("*.json"))
        if fixture.name != "rss_collected.json"
    ]

    assert fixtures
    for fixture in fixtures:
        data = json.loads(fixture.read_text(encoding="utf-8"))
        assert data["title"]
        assert data["raw_text"]
        assert "expected_mentions" in data
        assert "expected_facts" in data
        assert "expected_claims" in data


def test_collected_rss_fixture_shape_when_present():
    fixture = Path("tests/golden_articles/rss_collected.json")
    if not fixture.exists():
        return
    data = json.loads(fixture.read_text(encoding="utf-8"))
    assert data["articles"]
    assert all("raw_text" in article for article in data["articles"])
