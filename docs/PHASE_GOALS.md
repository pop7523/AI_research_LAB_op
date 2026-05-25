# 단계별 구현 목표

이 문서는 각 phase의 목표와 완료 기준을 관리한다. phase를 시작하거나 범위를 조정할 때 이 문서를 먼저 갱신한다.

## Phase 0. 프로젝트 부트스트랩

목표:
- 개발 가능한 최소 백엔드 구조를 만든다.
- FastAPI 앱, 설정 로딩, DB 세션, migration, 테스트 환경을 준비한다.

완료 기준:
- `GET /health`가 동작한다.
- DB migration이 적용된다.
- `pytest`가 통과한다.
- `ruff check`가 통과한다.
- Docker Compose 구성이 유효하다.

## Phase 1. Article 수집/저장 MVP

목표:
- 수동 입력 또는 RSS를 통해 article을 저장한다.
- source와 article을 분리 관리한다.
- content hash 기반 중복 후보를 탐지한다.

완료 기준:
- `POST /sources`, `GET /sources`가 동작한다.
- `POST /articles`, `GET /articles`, `GET /articles/{id}`가 동작한다.
- 동일 본문 article은 `DUPLICATE_CANDIDATE` 상태가 된다.

## Phase 2. 본문 정제와 Evidence Span 구조

목표:
- article 원문을 정제하고 문장 단위 evidence span을 생성한다.
- 이후 fact/claim이 sentence id와 offset을 근거로 참조할 수 있게 한다.

완료 기준:
- `POST /articles/{id}/clean`이 `clean_text`와 sentence span을 생성한다.
- sentence span은 paragraph index, sentence index, start/end offset을 가진다.

## Phase 3. LLM Provider Abstraction

목표:
- LLM provider를 교체 가능한 인터페이스로 분리한다.
- JSON 응답 파싱과 실패 시 retry 흐름을 표준화한다.
- article text는 untrusted data로 취급하는 guardrail을 둔다.

완료 기준:
- fake provider 기반 테스트가 가능하다.
- JSON parsing 실패 후 retry가 가능하다.
- provider interface가 서비스 로직과 분리되어 있다.

## Phase 4. Entity / Mention 추출 MVP

목표:
- Entity, EntityAlias, Mention 모델을 만든다.
- seeded alias를 기반으로 article sentence에서 mention 후보를 추출한다.

완료 기준:
- `POST /entities`, `GET /entities`, `POST /entities/{id}/aliases`가 동작한다.
- `POST /articles/{id}/extract`가 mention 후보를 생성한다.
- mention은 sentence와 연결된다.

## Phase 5. Entity Linking MVP

목표:
- mention을 기존 canonical entity와 연결한다.
- exact alias, ticker, type match를 기반으로 score를 계산한다.
- 애매한 경우 억지 연결하지 않고 review 상태로 보낸다.

완료 기준:
- `POST /articles/{id}/link`가 mention linking 상태를 갱신한다.
- `LINKED`, `PROVISIONAL_LINK`, `AMBIGUOUS`, `UNRESOLVED` 상태를 구분한다.
- ambiguous alias는 `needs_review=true`가 된다.

## Phase 6. Fact / Claim 추출 MVP

목표:
- Fact와 Claim을 별도 모델로 저장한다.
- 모든 Fact/Claim에 evidence reference를 강제한다.

완료 기준:
- evidence 없는 Fact/Claim 저장이 불가능하다.
- Fact와 Claim 구분 실패 시 review 상태로 보낸다.

## Phase 7. Verification MVP

목표:
- 추출된 fact를 기존 DB와 비교하고 verification status를 관리한다.

완료 기준:
- subject/predicate/object/time/value 기준 비교가 가능하다.
- 수치/기간/출처 충돌 상태를 부여할 수 있다.
- 공식자료 없이는 `VERIFIED`를 남발하지 않는다.

## Phase 8. Event / Issue Builder MVP

목표:
- article, fact, claim을 event와 issue로 묶는다.

완료 기준:
- 여러 article을 같은 event로 묶을 수 있다.
- event를 issue에 연결하고 이유와 confidence를 저장한다.

## Phase 9. 분석 MVP

목표:
- issue 단위로 stakeholder, debate, cause, risk, scenario 분석 초안을 만든다.

완료 기준:
- 확인된 fact와 분석적 추론이 분리되어 저장된다.
- 분석 결과가 evidence refs를 가진다.

## Phase 10. Research Integrity Layer MVP

목표:
- 분석의 근거 수준, 반론, 이해관계, 전제, 균형성을 점검한다.

완료 기준:
- 주요 결론에 반대 가설과 break condition이 기록된다.
- 한쪽 관점만 있을 경우 balance warning이 발생한다.

## Phase 11. Report Generation MVP

목표:
- issue 기반 markdown report draft를 생성한다.

완료 기준:
- `evidence_checked` 전까지 publish할 수 없다.
- `balance_checked` 전까지 approve할 수 없다.

## Phase 12. Human Review Workflow

목표:
- 사람이 검토해야 하는 항목을 queue로 분리하고 승인/반려/수정요청을 처리한다.

완료 기준:
- review queue 조회와 review action이 가능하다.
- review 결과가 audit log로 남는다.

## Phase 13. Audit / Evaluation

목표:
- agent 판단, task 실행, prompt version, 품질 평가를 추적한다.

완료 기준:
- 주요 pipeline 실행마다 audit log가 생성된다.
- evaluation fixture 기반 regression test가 가능하다.

## Phase 14. 대시보드

목표:
- article, fact, issue, report, review 흐름을 관리자가 웹에서 확인한다.

완료 기준:
- article -> fact -> issue -> report 흐름을 UI에서 추적할 수 있다.
- review action이 가능하다.

## Phase 15. 고도화

목표:
- 통합형 agent를 전문 agent로 분리하고 공식자료/PDF/공시 처리 등을 확장한다.

완료 기준:
- 전문 agent별 독립 테스트와 audit log가 존재한다.
- update/correction/prediction review workflow가 동작한다.

