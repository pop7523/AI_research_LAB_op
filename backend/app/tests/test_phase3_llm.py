from app.llm.provider import FakeLLMProvider, LLMMessage
from app.llm.response_parser import complete_with_json_retry, parse_json_response
from pydantic import BaseModel


class OkResult(BaseModel):
    ok: bool


def test_parse_json_response_accepts_objects():
    assert parse_json_response('{"ok": true}') == {"ok": True}


def test_complete_with_json_retry_repairs_invalid_json():
    provider = FakeLLMProvider(["not json", '{"ok": true}'])

    result = complete_with_json_retry(
        provider,
        [LLMMessage(role="system", content="Return JSON")],
        OkResult,
        max_attempts=2,
    )

    assert result.ok is True
    assert provider.calls == 2

