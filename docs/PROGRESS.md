# 현재 진행상황

이 문서는 현재 phase, 완료된 phase, 검증 결과, 다음 작업을 추적한다. phase가 완료되거나 다음 phase로 넘어갈 때 반드시 갱신한다.

## 현재 상태

- 현재 기준 phase: Phase 5 완료
- 다음 예정 phase: Phase 6. Fact / Claim 추출 MVP
- 마지막 갱신: 2026-05-26

## 완료된 Phase

| Phase | 상태 | 요약 |
| --- | --- | --- |
| Phase 0 | 완료 | FastAPI skeleton, 설정, DB 세션, Alembic, pytest/ruff 환경 구성 |
| Phase 1 | 완료 | Source/Article API, content hash, duplicate candidate 탐지 |
| Phase 2 | 완료 | article cleaner, sentence evidence span, clean endpoint |
| Phase 3 | 완료 | LLM provider interface, fake provider, JSON parser/retry, guardrail prompt |
| Phase 4 | 완료 | Entity/EntityAlias/Mention 모델, entity API, mention extraction |
| Phase 5 | 완료 | alias/type/ticker 기반 entity linking, ambiguous review 처리 |

## 최근 검증 결과

- `pytest`: 11 passed
- `ruff check .`: All checks passed
- `alembic upgrade head`: 성공
- `docker compose config`: 성공
- Uvicorn HTTP smoke test: `GET /health` -> `200 {"status":"ok","app":"ai-newsroom"}`

참고:
- Docker Compose 검증 중 `C:\Users\kkn92\.docker\config.json` 접근 경고가 있었지만 command exit code는 0이었다.
- PowerShell 백그라운드 서버 실행은 현재 환경의 `Path/PATH` 중복 문제로 안정적이지 않았다. foreground 실행과 Uvicorn in-process smoke test로 API 기동 가능성을 확인했다.

## 다음 작업

Phase 6에서 진행할 일:
- Fact 모델 구현
- Claim 모델 구현
- evidence reference 필수 제약 구현
- Fact/Claim extraction schema 구현
- fake extraction service와 테스트 구현
- Fact/Claim 저장 API 또는 article extraction pipeline 확장

## 운영 규칙

- phase 시작 전 `docs/PHASE_GOALS.md`에서 목표와 완료 기준을 확인한다.
- phase 진행 중 중요한 결정은 이 문서의 진행상황에 반영한다.
- phase 완료 시 검증 결과를 이 문서에 기록한다.
- 구현 변경사항은 `docs/CHANGELOG.md`에 별도로 기록한다.

