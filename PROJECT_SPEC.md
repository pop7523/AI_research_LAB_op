# AI 뉴스 분석 플랫폼 SPEC

이 프로젝트는 파편화된 기사, 공식자료, 공시, 보고서, 발언, 수치 정보를 구조화하고
기존 지식과 연결하여 검증 상태와 불확실성을 관리하는 AI 기반 뉴스룸 + 리서치센터다.

핵심 원칙:

- Fact, Claim, Analysis, Opinion, Scenario를 분리한다.
- 모든 Fact와 Claim은 evidence reference를 가져야 한다.
- 불확실성은 오류가 아니라 정상 상태로 관리한다.
- 자동 발행보다 검증 상태 관리와 사람 검토가 우선이다.
- 모든 에이전트 판단은 audit log로 남긴다.

