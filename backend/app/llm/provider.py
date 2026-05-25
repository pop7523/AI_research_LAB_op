from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LLMMessage:
    role: str
    content: str


class LLMProvider(ABC):
    @abstractmethod
    def complete_json(self, messages: list[LLMMessage], schema: dict[str, Any]) -> str:
        raise NotImplementedError


class FakeLLMProvider(LLMProvider):
    def __init__(self, responses: list[str] | None = None):
        self.responses = responses or ['{"ok": true}']
        self.calls = 0

    def complete_json(self, messages: list[LLMMessage], schema: dict[str, Any]) -> str:
        response = self.responses[min(self.calls, len(self.responses) - 1)]
        self.calls += 1
        return response

