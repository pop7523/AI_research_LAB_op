import json
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel, ValidationError

from app.llm.provider import LLMMessage, LLMProvider


class LLMJSONParseError(ValueError):
    pass


def parse_json_response(raw: str) -> dict[str, Any]:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise LLMJSONParseError(str(exc)) from exc
    if not isinstance(parsed, dict):
        raise LLMJSONParseError("LLM response must be a JSON object")
    return parsed


def complete_with_json_retry(
    provider: LLMProvider,
    messages: list[LLMMessage],
    schema_model: type[BaseModel],
    repair_message_factory: Callable[[str], LLMMessage] | None = None,
    max_attempts: int = 2,
) -> BaseModel:
    schema = schema_model.model_json_schema()
    current_messages = list(messages)
    last_error = "unknown parse error"
    for _ in range(max_attempts):
        raw = provider.complete_json(current_messages, schema)
        try:
            return schema_model.model_validate(parse_json_response(raw))
        except (LLMJSONParseError, ValidationError) as exc:
            last_error = str(exc)
            repair = repair_message_factory or (
                lambda error: LLMMessage("user", f"Return valid JSON only. Error: {error}")
            )
            current_messages.append(repair(last_error))
    raise LLMJSONParseError(last_error)

