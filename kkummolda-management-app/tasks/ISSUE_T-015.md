---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-015: 고객 진단 제출 E2E 플로우 테스트 (선택적)"
labels: 'feature, testing, e2e, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [T-015] 고객 진단 제출 E2E 플로우 테스트
- 목적: 고객이 랜딩페이지(Q-001)에서 진단 폼(Q-002)으로 진입하여, 16문항을 작성하고 제출한 뒤 성공 모달을 보기까지의 E2E(End-to-End) 사용자 경험을 Playwright나 Cypress를 활용해 검증한다. (MVP-Free 단계에서는 수동 테스트로 대체 가능하나, 자동화 구성을 권장함)

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 플로우: 랜딩(`/`) -> 진단 폼(`/diagnose`) -> 제출 -> 성공 처리
- 요구사항: REQ-FREE-FUNC-005 (제출 완료 화면 제공)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] (테스트 프레임워크 도입 시) Playwright 설치 및 기본 설정
- [ ] E2E 스크립트 작성 (`e2e/customer-flow.spec.ts`):
  - 메인 페이지 접속 및 "진단 시작하기" 버튼 클릭 검증
  - 진단 폼에서 이름, 연락처(필수) 입력
  - 16개 질문 필드에 3단어 이상 텍스트 입력 매크로
  - 개인정보 동의 체크박스 클릭
  - "제출하기" 버튼 클릭
  - 제출 성공 모달이나 알림이 화면에 표시되는지 검증
- [ ] (수동 테스트 시나리오 문서화) E2E 툴을 쓰지 않는다면, 개발자가 커밋 전 반드시 확인할 수동 QA 체크리스트로 본 문서를 활용

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: Happy Path 진단 완료**
- Given: 브라우저가 랜딩페이지에 열려 있음
- When: 사용자가 전체 폼을 유효하게 채우고 제출함
- Then: 로딩 스피너 이후 "제출 완료" 메시지가 화면에 나타난다.

## :gear: Technical & Non-Functional Constraints
- Vercel 배포 후 Preview 환경에서 이 테스트를 수행하면 빌드 무결성을 완벽하게 보장할 수 있다.

## :checkered_flag: Definition of Done (DoD)
- [ ] E2E 테스트 스크립트 작성 또는 수동 QA 문서화
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** FE-001, FE-002
- **Blocks:** None
