# Roadmap

진행상황의 단일 기준은 아래 문서들이다.

- 단계별 목표: `docs/PHASE_GOALS.md`
- 현재 진행상황: `docs/PROGRESS.md`
- 변경사항: `docs/CHANGELOG.md`

## Phase 0

프로젝트 skeleton, FastAPI, DB 연결, Docker Compose, 테스트 환경.

## Phase 1

Source/Article 저장, content hash, 중복 후보 탐지.

## Phase 2

본문 정제와 sentence evidence span.

## Phase 3

LLM provider abstraction, JSON parser, retry.

## Phase 4

Entity/Mention/Alias 모델, seed, mention extraction MVP.

## Phase 5

Entity linking MVP, alias/ticker/type 기반 점수와 ambiguous 상태 관리.
