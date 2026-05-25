# 현재 진행상황

이 문서는 현재 phase, 완료된 phase, 검증 결과, 다음 작업을 추적한다. phase가 완료되거나 다음 phase로 넘어갈 때 반드시 갱신한다.

## 현재 상태

- 현재 기준 phase: Phase 12 완료
- 다음 예정 phase: Phase 13. Audit / Evaluation 고도화
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
| Phase 6 | 완료 | Fact/Claim 모델, evidence 필수 제약, rule-based extraction MVP |
| Phase 7 | 완료 | Fact verification 상태 흐름, matching/number mismatch/review queue |
| Phase 8 | 완료 | Event/Issue 모델, article 기반 event/issue builder MVP |
| Phase 9 | 완료 | Issue 기반 perspective analysis MVP |
| Phase 10 | 완료 | Integrity review, counterargument, balance review MVP |
| Phase 11 | 완료 | Report draft generation, approve/publish guard |
| Phase 12 | 완료 | Review queue, approve/reject/revision action, audit log |

## 최근 검증 결과

- `pytest`: 25 passed
- `ruff check .`: All checks passed
- `alembic upgrade head`: 성공
- `docker compose config`: 성공
- Uvicorn HTTP smoke test: `GET /health` -> `200 {"status":"ok","app":"ai-newsroom"}`

참고:
- Docker Compose 검증 중 `C:\Users\kkn92\.docker\config.json` 접근 경고가 있었지만 command exit code는 0이었다.
- PowerShell 백그라운드 서버 실행은 현재 환경의 `Path/PATH` 중복 문제로 안정적이지 않았다. foreground 실행과 Uvicorn in-process smoke test로 API 기동 가능성을 확인했다.

## 다음 작업

Phase 13에서 진행할 일:
- audit log 커버리지 확대
- task execution log와 prompt version 저장
- extraction/linking/report evaluation fixture 확장
- regression evaluation command 추가
- quality metrics 산출

운영 참고:
- `backend/scripts/collect_test_articles.py`는 RSS 수집을 시도하고, 네트워크/피드 실패 시 deterministic fallback fixture를 생성한다.
- 현재 `tests/golden_articles/rss_collected.json`은 fallback test article로 생성되었다.

## 운영 규칙

- phase 시작 전 `docs/PHASE_GOALS.md`에서 목표와 완료 기준을 확인한다.
- phase 진행 중 중요한 결정은 이 문서의 진행상황에 반영한다.
- phase 완료 시 검증 결과를 이 문서에 기록한다.
- 구현 변경사항은 `docs/CHANGELOG.md`에 별도로 기록한다.
