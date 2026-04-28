---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-011: 미승인 리포트 접근 차단(보안) 테스트"
labels: 'feature, testing, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [T-011] 미승인 리포트 접근 차단(보안) 테스트
- 목적: 리포트 웹뷰(Q-005) 렌더링 시, DB의 리포트 상태가 `approved`가 아닌 모든 경우(draft, rejected, regeneration_requested)에 대해 고객 노출을 원천 차단(404 Not Found 반환)하는 로직을 검증한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: Q-008 (`getApprovedReport`), FE-005 (리포트 웹뷰 접근 제어)
- 요구사항: REQ-FREE-FUNC-034 (미승인 리포트 고객 비공개)
- 제약사항: REQ-NF-FREE-033

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `__tests__/integration/report-access.test.ts` 파일 생성
- [ ] `getApprovedReport` 함수 통합 테스트:
  - `status: "approved"` 인 Report Mock 조회 시 정상 반환 확인
  - `status: "draft"` 인 Report Mock 조회 시 `null` 반환 확인
  - `status: "rejected"` 인 Report Mock 조회 시 `null` 반환 확인
- [ ] (선택) Next.js 서버사이드 렌더링 환경에서 `getApprovedReport` 결과가 `null`일 때 `notFound()` 예외가 던져지는지 확인하는 테스트 (Vitest 환경에 맞게)

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 승인된 리포트 접근**
- Given: Report(status="approved") 데이터가 존재
- When: `getApprovedReport`를 호출함
- Then: 정상적인 Report 객체가 반환된다

**Scenario 2: 미승인 리포트 접근 차단**
- Given: Report(status="draft") 데이터가 존재
- When: `getApprovedReport`를 호출함
- Then: `null`이 반환되어 뷰에서 Not Found 처리되도록 유도한다

**Scenario 3: 거부된 리포트 접근 차단**
- Given: Report(status="rejected") 데이터가 존재
- When: `getApprovedReport`를 호출함
- Then: `null`이 반환된다

## :gear: Technical & Non-Functional Constraints
- 보안과 밀접한 관련이 있으므로, 데이터가 실제로 존재하더라도 상태값 하나로 인해 노출이 완벽히 차단됨을 타입 및 로직 레벨에서 보장해야 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 모든 상태(approved 외)에 대한 `null` 반환 테스트 작성 및 Pass
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** Q-008
- **Blocks:** None
