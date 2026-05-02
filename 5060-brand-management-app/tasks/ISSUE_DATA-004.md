---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DATA-004: AiRun 상태값 enum 상수 정의"
labels: 'feature, data, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DATA-004] AiRun 상태값 enum 상수 정의
- 목적: AiRun 모델의 status 필드에 사용되는 허용값을 TypeScript 상수로 정의한다. AI 호출의 생명주기(pending → processing → completed/failed)를 추적하며, 호출 로깅(LOG-001) 및 실패 처리(C-006)의 상태 판별 기준이 된다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#Appendix A — 최소 상태값`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 506~512
- AiRun 상태값: `pending | processing | completed | failed`
- 기능 요구사항:
  - S12 (최소 AI 호출 로그)
  - REQ-FREE-FUNC-022 (AI 생성 실패 시 실패 상태 기록)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/constants/status.ts`에 AiRunStatus 상수 추가:
  ```typescript
  export const AiRunStatus = {
    PENDING: "pending",
    PROCESSING: "processing",
    COMPLETED: "completed",
    FAILED: "failed",
  } as const
  
  export type AiRunStatusType = typeof AiRunStatus[keyof typeof AiRunStatus]
  ```
- [ ] AiRun taskType 상수 추가:
  ```typescript
  export const AiRunTaskType = {
    GENERATE_REPORT: "generateReport",
    REGENERATE_REPORT: "regenerateReport",
  } as const
  
  export type AiRunTaskTypeValue = typeof AiRunTaskType[keyof typeof AiRunTaskType]
  ```
- [ ] 상태 전이 주석: `pending → processing → completed | failed`
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: AiRunStatus 상수 값 정확성**
- Given: AiRunStatus 상수가 정의됨
- When: 4개 키를 확인함
- Then: `pending`, `processing`, `completed`, `failed`와 정확히 일치한다

**Scenario 2: AiRunTaskType 상수 값 정확성**
- Given: AiRunTaskType 상수가 정의됨
- When: 2개 키를 확인함
- Then: `generateReport`, `regenerateReport`와 정확히 일치한다

**Scenario 3: 타입 안전성**
- Given: AiRunStatusType 타입이 정의됨
- When: `const s: AiRunStatusType = "running"`을 작성함
- Then: TypeScript 컴파일 에러가 발생한다

## :gear: Technical & Non-Functional Constraints
- DATA-002, DATA-003과 동일 파일(`src/lib/constants/status.ts`)에 함께 정의
- AiRunTaskType도 함께 정의하여 taskType 필드의 타입 안전성 확보

## :checkered_flag: Definition of Done (DoD)
- [ ] AiRunStatus 상수 4개 값이 SRS 명세와 일치
- [ ] AiRunTaskType 상수 2개 값이 SRS 명세와 일치
- [ ] 두 타입이 모두 export됨
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** INF-001 (프로젝트 존재)
- **Blocks:** C-005 (AI 리포트 생성 — AiRun 상태 전이), C-006 (실패 처리 — failed 설정), C-010 (재생성 — taskType 구분), LOG-001 (AI 호출 로깅), T-006 (AI 실패 테스트)
