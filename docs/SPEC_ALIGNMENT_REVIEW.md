# SPEC 부합성 및 구조 점검 보고

마지막 점검일: 2026-05-26

## 요약 판단

현재 프로젝트는 Phase 0-5 범위에서는 대체로 SPEC에 부합한다. FastAPI skeleton, Source/Article, cleaner/evidence span, LLM abstraction, Entity/Mention, Entity Linking MVP는 실제 코드와 테스트로 구현되어 있다.

다만 전체 SPEC 기준으로는 아직 초기 골격이며, Fact/Claim/Verification 단계로 넘어가기 전에 몇 가지 침식 위험을 정리해야 한다.

## 검증 결과

- `pytest`: 11 passed
- `ruff check .`: All checks passed
- Git 상태: `main...origin/main`, clean

## 부합하는 부분

- 핵심 원칙이 `PROJECT_SPEC.md`와 `CODEX_INSTRUCTIONS.md`에 반영되어 있다.
- phase 문서 관리 체계가 `docs/PHASE_GOALS.md`, `docs/PROGRESS.md`, `docs/CHANGELOG.md`로 분리되어 있다.
- Article 상태 enum이 존재한다.
- sentence evidence span 구조가 존재한다.
- LLM provider와 response parser가 서비스 로직과 분리되어 있다.
- ambiguous linking에 대한 테스트가 존재한다.

## 침식 위험

### 1. Ambiguous entity가 linked_entity_id에 저장됨

`AMBIGUOUS` 상태에서도 top candidate가 `linked_entity_id`에 저장된다. 이는 "애매한 엔티티는 억지로 연결하지 않는다"는 원칙과 충돌할 수 있다.

권장:
- `AMBIGUOUS` 상태에서는 `linked_entity_id`를 `null`로 둔다.
- 후보 목록은 별도 candidate 구조로 저장한다.

### 2. Evidence offset이 반복 문단에서 틀릴 수 있음

sentence splitter가 `clean_text.find(paragraph)`를 사용한다. 같은 문단 텍스트가 반복되면 두 번째 문단의 offset도 첫 번째 문단 위치로 계산될 수 있다.

권장:
- paragraph 위치를 누적 offset 방식으로 계산한다.
- 반복 문단 케이스를 테스트에 추가한다.

### 3. Manual resolve에 audit/review 기록이 없음

`/mentions/{id}/resolve`는 사람이 직접 entity를 확정하는 중요한 행위지만 현재 audit log가 없다.

권장:
- Phase 13까지 기다리지 말고 manual review action부터 audit log 기준을 세운다.
- resolve action에 actor, target, reason, confidence를 남긴다.

### 4. 전체 SPEC 원문이 보존되어 있지 않음

현재 `PROJECT_SPEC.md`는 핵심 원칙 요약본이다. 사용자가 제공한 전체 18장짜리 SPEC은 repo에 그대로 보존되어 있지 않다.

권장:
- 전체 원문을 `PROJECT_SPEC.md` 또는 `docs/FULL_PROJECT_SPEC.md`로 보존한다.
- `PROJECT_SPEC.md`는 전체 기준 문서로, `ROADMAP.md`와 phase 문서는 실행 관리 문서로 유지한다.

### 5. `/articles/{id}/extract`의 의미가 넓어질 위험

현재 extract endpoint는 mention만 추출한다. Phase 6부터 Fact/Claim extraction이 추가되면 endpoint 의미가 혼동될 수 있다.

권장:
- mention 전용 endpoint와 Fact/Claim 전용 endpoint를 분리한다.
- 예: `/articles/{id}/extract-mentions`, `/articles/{id}/extract-facts-claims`, `/articles/{id}/run-structure-pipeline`

## 현재 실제 흐름

```text
source/article 생성
  -> duplicate 후보 탐지
  -> clean_text 생성
  -> sentence evidence span 생성
  -> alias 기반 mention 추출
  -> entity linking
  -> ambiguous review flag
```

이 흐름은 Phase 0-5 MVP로 적절하다.

아직 구현 전인 흐름:

```text
Fact/Claim
  -> Verification
  -> Event/Issue
  -> Analysis
  -> Integrity Review
  -> Report
  -> Human Review
  -> Audit/Evaluation
```

이는 현재 phase 기준 정상적인 미구현이다.

## 다음 우선순위

Phase 6으로 넘어가기 전 선행 수정:

1. `AMBIGUOUS` 상태에서는 `linked_entity_id`를 저장하지 않도록 수정
2. sentence offset 계산을 누적 offset 방식으로 수정
3. 전체 SPEC 원문을 repo 문서로 보존

그 다음 Phase 6에서 진행:

1. Fact 모델
2. Claim 모델
3. evidence reference 필수 제약
4. extraction schema
5. fake extraction service
6. Fact/Claim 저장 API 또는 pipeline 확장

