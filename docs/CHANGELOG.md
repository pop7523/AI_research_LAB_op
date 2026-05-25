# 변경사항

이 문서는 실제 코드/문서 변경 내역을 phase 단위로 기록한다. phase가 끝날 때마다 새 항목을 추가한다.

## 2026-05-26. Phase 0-5 초기 구현

문서:
- `README.md` 추가
- `PROJECT_SPEC.md` 추가
- `CODEX_INSTRUCTIONS.md` 추가
- `ROADMAP.md` 추가
- `.env.example` 추가
- `.gitignore` 추가
- `docs/PHASE_GOALS.md` 추가
- `docs/PROGRESS.md` 추가
- `docs/CHANGELOG.md` 추가

개발환경:
- `pyproject.toml` 추가
- `.venv` 생성
- FastAPI, SQLAlchemy, Alembic, Pydantic, pytest, ruff 등 의존성 설치
- `Dockerfile` 추가
- `docker-compose.yml` 추가

Backend:
- FastAPI app factory와 `/health` endpoint 추가
- DB base/session 설정 추가
- Alembic 환경과 `0001_initial` migration 추가
- Source 모델 추가
- Article 모델 추가
- ArticleSentence 모델 추가
- Entity 모델 추가
- EntityAlias 모델 추가
- Mention 모델 추가
- article/source/entity/mention 관련 Pydantic schema 추가

API:
- `POST /sources`
- `GET /sources`
- `POST /articles`
- `GET /articles`
- `GET /articles/{id}`
- `POST /articles/{id}/clean`
- `POST /ingest/rss`
- `POST /entities`
- `GET /entities`
- `GET /entities/{id}`
- `POST /entities/{id}/aliases`
- `POST /articles/{id}/extract`
- `POST /articles/{id}/link`
- `POST /mentions/{id}/resolve`

Services:
- content normalization/hash 생성
- article text cleaner
- sentence splitter와 offset span 생성
- seeded alias 기반 mention extraction
- alias/type/ticker 기반 entity linking
- ambiguous candidate review 처리
- LLM provider interface
- fake LLM provider
- JSON response parser와 retry helper
- article text untrusted data guardrail prompt

Tests:
- health endpoint test
- source/article creation test
- duplicate article detection test
- cleaner/sentence span test
- clean endpoint test
- LLM JSON parser/retry test
- mention extraction test
- exact alias linking test
- ambiguous alias review test

검증:
- `pytest`: 11 passed
- `ruff check .`: All checks passed
- `alembic upgrade head`: 성공
- `docker compose config`: 성공
- Uvicorn HTTP smoke test 성공

## 2026-05-26. SPEC 부합성 점검 문서화

문서:
- `docs/SPEC_ALIGNMENT_REVIEW.md` 추가

내용:
- 현재 Phase 0-5 구현이 전체 SPEC에 부합하는지 점검
- AI 개발 과정에서 생길 수 있는 구조적 침식 위험 정리
- Phase 6 진입 전 선행 수정 권장사항 기록

## 2026-05-26. Phase 6-12 MVP 구현

Phase 6:
- `Fact`, `Claim` 모델 추가
- evidence text check constraint 추가
- `POST /articles/{id}/extract-facts-claims` 추가
- rule-based Fact/Claim extraction MVP 추가
- Fact/Claim evidence 필수 테스트 추가

Phase 7:
- Fact verification 상태 흐름 추가
- `POST /facts/{id}/verify`, `POST /facts/{id}/mark-disputed` 추가
- official source 기반 verified 판정과 number mismatch review queue 테스트 추가

Phase 8:
- `Event`, `EventLink`, `Issue`, `IssueLink` 모델 추가
- `POST /articles/{id}/build-event-issue` 추가
- article fact/claim 기반 event/issue builder MVP 추가

Phase 9:
- `Perspective` 모델 추가
- `POST /issues/{id}/analyze` 추가
- positive/negative/neutral perspective analysis MVP 추가

Phase 10:
- integrity review service 추가
- `POST /issues/{id}/integrity-review` 추가
- evidence assessment, counterarguments, assumptions, balance review 구조 추가

Phase 11:
- `Report` 모델 추가
- `POST /issues/{id}/generate-report` 추가
- `POST /reports/{id}/submit-review`, `approve`, `publish` 상태 guard 추가

Phase 12:
- `ReviewItem`, `AuditLog` 모델 추가
- `GET /review-queue`와 review action API 추가
- mention resolve와 review action audit logging 추가

Test data:
- `tests/golden_articles/*.json` golden article fixtures 추가
- `backend/scripts/collect_test_articles.py` RSS/fallback 수집 스크립트 추가
- `tests/golden_articles/rss_collected.json` fallback 수집 결과 추가

Quality fixes:
- ambiguous entity는 `linked_entity_id`를 저장하지 않도록 수정
- 반복 문단 sentence offset 계산 오류 방지

검증:
- `pytest`: 25 passed
- `ruff check .`: All checks passed
- SQLite `alembic upgrade head`: 성공
- Docker Compose config: 성공
- Uvicorn `/health` smoke test: 성공
