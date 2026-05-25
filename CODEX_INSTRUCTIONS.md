# Codex Instructions

Phase 단위로 구현한다. 각 Phase는 테스트와 migration을 포함해야 한다.

## Phase 문서 관리

아래 세 문서를 분리 관리한다.

- `docs/PHASE_GOALS.md`: 단계별 구현 목표와 완료 기준
- `docs/PROGRESS.md`: 현재 진행상황, 완료된 phase, 검증 결과, 다음 작업
- `docs/CHANGELOG.md`: 실제 변경사항

phase를 시작하거나 완료할 때는 반드시 위 문서들을 갱신한다.

절대 원칙:

- 기사 원문과 AI 분석 결과를 섞지 않는다.
- evidence 없는 Fact/Claim 저장을 허용하지 않는다.
- 상태값은 enum으로 관리한다.
- LLM 호출부를 서비스 로직에 직접 박지 않는다.
- 프롬프트는 중앙에서 관리한다.
