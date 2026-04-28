---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-016: 관리자 로그인 및 검수 워크플로 E2E 테스트 (선택적)"
labels: 'feature, testing, e2e, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [T-016] 관리자 로그인 및 검수 워크플로 E2E 테스트
- 목적: 관리자가 로그인(SEC-002) 후 목록(Q-003)을 확인하고, 상세 페이지(Q-004)에 진입하여 리포트를 승인(FE-004)하는 핵심 어드민 플로우를 E2E 레벨에서 검증한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 플로우: 로그인(`/admin/login`) -> 목록(`/admin/diagnoses`) -> 상세(`/admin/diagnoses/[id]`) -> 승인 버튼
- 요구사항: REQ-FREE-FUNC-031, 033

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] E2E 스크립트 작성 (`e2e/admin-flow.spec.ts`):
  - `/admin/login` 페이지 접속 및 `ADMIN_PASSWORD` 입력 
  - 인증 성공 후 `/admin/diagnoses` 리다이렉트 확인
  - 목록 첫 번째 행(최신 진단) 클릭하여 상세 페이지 이동
  - 상세 페이지에서 데이터(답변, AI 리포트 등) 렌더링 확인
  - "승인하기" 버튼 클릭 및 모달 확인
  - 리포트 상태가 "승인 완료" 등 긍정적 상태로 UI에 반영되는지 확인
- [ ] (수동 테스트 시나리오 문서화) 1인 개발 특성상 E2E 툴 적용이 부담된다면, 배포 전 체크리스트로 활용한다.

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 관리자 검수 워크플로 완료**
- Given: 미승인 진단이 1건 존재하는 DB
- When: 관리자가 로그인하여 해당 진단을 승인함
- Then: 리포트가 고객 웹뷰(`/report/[id]`)에서 정상적으로 보이게 된다.

## :gear: Technical & Non-Functional Constraints
- 승인 동작은 실제 데이터 변경을 수반하므로, E2E 테스트 시 별도의 Test DB 환경을 구성하거나 상태를 복구하는 로직이 필요하다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 관리자 플로우 E2E 테스트 작성 또는 수동 QA 문서화
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** SEC-002, FE-003, FE-004
- **Blocks:** None
