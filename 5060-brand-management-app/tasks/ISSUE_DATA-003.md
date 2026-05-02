---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DATA-003: Report 상태값 enum 상수 정의"
labels: 'feature, data, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DATA-003] Report 상태값 enum 상수 정의
- 목적: Report 모델의 status 필드에 사용되는 허용값을 TypeScript 상수로 정의한다. 이 상태값은 승인 게이트(draft → approved/rejected)의 핵심이며, 고객 공개 여부를 결정하는 가장 중요한 비즈니스 규칙의 기반이다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#Appendix A — 최소 상태값`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 506~512
- Report 상태값: `draft | approved | rejected | regeneration_requested`
- 기능 요구사항:
  - REQ-FREE-FUNC-033 (승인/거부 상태 변경)
  - REQ-FREE-FUNC-034 (미승인 리포트 고객 비공개)
  - REQ-FREE-FUNC-040 (approved 상태만 웹뷰 표시)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/constants/status.ts`에 ReportStatus 상수 추가:
  ```typescript
  export const ReportStatus = {
    DRAFT: "draft",
    APPROVED: "approved",
    REJECTED: "rejected",
    REGENERATION_REQUESTED: "regeneration_requested",
  } as const
  
  export type ReportStatusType = typeof ReportStatus[keyof typeof ReportStatus]
  ```
- [ ] 승인 게이트 규칙 주석 추가: `approved 상태만 고객 공개, draft/rejected/regeneration_requested는 비공개`
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 상수 값 정확성**
- Given: ReportStatus 상수가 정의됨
- When: 4개 키를 확인함
- Then: `draft`, `approved`, `rejected`, `regeneration_requested`와 정확히 일치한다

**Scenario 2: 타입 안전성**
- Given: ReportStatusType 타입이 정의됨
- When: `const s: ReportStatusType = "pending"`을 작성함
- Then: TypeScript 컴파일 에러가 발생한다 (허용되지 않는 값)

**Scenario 3: 승인 상태 판별 활용**
- Given: ReportStatus.APPROVED가 "approved"임
- When: `report.status === ReportStatus.APPROVED` 비교를 수행함
- Then: 정확한 타입 추론과 비교가 가능하다

## :gear: Technical & Non-Functional Constraints
- `approved` 상태만 고객 공개 — 이 규칙은 Q-008, FE-005, SEC-003에서 모두 참조
- DATA-002와 동일 파일(`src/lib/constants/status.ts`)에 함께 정의

## :checkered_flag: Definition of Done (DoD)
- [ ] ReportStatus 상수 4개 값이 SRS 명세와 일치
- [ ] ReportStatusType 타입이 export됨
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** INF-001 (프로젝트 존재)
- **Blocks:** C-005 (AI 리포트 저장 — draft 설정), C-008 (승인/거부 상태 변경), Q-008 (approved 필터링), FE-005 (미승인 접근 차단), T-011 (접근 제어 테스트)
