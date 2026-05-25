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

