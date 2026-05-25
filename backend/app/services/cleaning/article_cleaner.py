import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SentenceSpan:
    paragraph_index: int
    sentence_index: int
    text: str
    start_offset: int
    end_offset: int


def clean_article_text(raw_text: str) -> str:
    lines = [re.sub(r"\s+", " ", line).strip() for line in (raw_text or "").splitlines()]
    paragraphs = [line for line in lines if line]
    return "\n\n".join(paragraphs)


def split_sentences(clean_text: str) -> list[SentenceSpan]:
    spans: list[SentenceSpan] = []
    search_offset = 0
    for paragraph_index, paragraph in enumerate(clean_text.split("\n\n")):
        paragraph_start = clean_text.find(paragraph, search_offset)
        search_offset = paragraph_start + len(paragraph) + 2
        sentence_index = 0
        for match in re.finditer(r".+?(?:[.!?。]|다\.|요\.|니다\.|$)(?=\s|$)", paragraph):
            text = match.group(0).strip()
            if not text:
                continue
            start = paragraph_start + match.start()
            end = paragraph_start + match.end()
            spans.append(
                SentenceSpan(
                    paragraph_index=paragraph_index,
                    sentence_index=sentence_index,
                    text=text,
                    start_offset=start,
                    end_offset=end,
                )
            )
            sentence_index += 1
    return spans
