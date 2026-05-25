import argparse
import json
from pathlib import Path

import feedparser

FALLBACK_ARTICLES = [
    {
        "title": "AI chip investment test article",
        "url": "https://example.com/golden/ai-capex-001",
        "source": "Synthetic Golden News",
        "raw_text": (
            "Nvidia said it will invest $5 billion in Intel. "
            "Analysts expect this may reshape AI chip competition."
        ),
        "expected_mentions": ["Nvidia", "Intel"],
        "expected_facts": [
            {
                "predicate": "reported_numeric_development",
                "value": 5000000000,
                "currency": "USD",
            }
        ],
        "expected_claims": [
            {"claim_type": "attributed_statement", "evidence_contains": "said"},
            {"claim_type": "interpretation", "evidence_contains": "expect"},
        ],
        "expected_entity_links": [],
    }
]


def collect_feed(feed_url: str, limit: int) -> list[dict]:
    parsed = feedparser.parse(feed_url)
    articles = []
    for entry in parsed.entries[:limit]:
        title = getattr(entry, "title", "").strip()
        summary = getattr(entry, "summary", "").strip()
        link = getattr(entry, "link", "").strip()
        if not title:
            continue
        articles.append(
            {
                "title": title,
                "url": link,
                "source": parsed.feed.get("title", "RSS Feed"),
                "raw_text": summary or title,
                "expected_mentions": [],
                "expected_facts": [],
                "expected_claims": [],
                "expected_entity_links": [],
            }
        )
    return articles


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feed", default="https://news.google.com/rss/search?q=AI%20chips")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--output", default="tests/golden_articles/rss_collected.json")
    args = parser.parse_args()

    articles = collect_feed(args.feed, args.limit)
    if not articles:
        articles = FALLBACK_ARTICLES

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps({"articles": articles}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"wrote {len(articles)} article(s) to {output_path}")


if __name__ == "__main__":
    main()

