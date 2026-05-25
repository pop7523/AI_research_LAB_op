import hashlib
import re


def normalize_content(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip().lower()


def content_hash(text: str) -> str:
    return hashlib.sha256(normalize_content(text).encode("utf-8")).hexdigest()

