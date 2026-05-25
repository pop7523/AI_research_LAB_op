from app.models.enums import ArticleStatus
from app.services.cleaning.article_cleaner import clean_article_text, split_sentences


def test_clean_article_text_normalizes_paragraphs():
    raw = " Nvidia   said it will invest. \n\n\n Intel responded. "

    clean = clean_article_text(raw)

    assert clean == "Nvidia said it will invest.\n\nIntel responded."


def test_split_sentences_keeps_evidence_offsets():
    clean = "Nvidia said it will invest. Intel responded."

    spans = split_sentences(clean)

    assert [span.text for span in spans] == [
        "Nvidia said it will invest.",
        "Intel responded.",
    ]
    assert clean[spans[0].start_offset : spans[0].end_offset] == spans[0].text


def test_split_sentences_handles_repeated_paragraph_offsets():
    clean = "Repeat sentence.\n\nRepeat sentence."

    spans = split_sentences(clean)

    assert len(spans) == 2
    assert spans[0].start_offset == 0
    assert spans[1].start_offset == len("Repeat sentence.\n\n")
    assert clean[spans[1].start_offset : spans[1].end_offset] == spans[1].text


def test_clean_endpoint_creates_sentence_evidence(client):
    article = client.post(
        "/articles",
        json={"title": "Clean me", "raw_text": "First sentence. Second sentence."},
    ).json()

    response = client.post(f"/articles/{article['id']}/clean")

    assert response.status_code == 200
    body = response.json()
    assert body["article"]["status"] == ArticleStatus.CLEANED
    assert len(body["sentences"]) == 2
    assert body["sentences"][0]["text"] == "First sentence."
