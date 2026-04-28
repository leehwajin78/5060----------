---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-005: reviewReport Server Action Request/Response DTO 정의"
labels: 'feature, backend, contract, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [API-005] reviewReport Server Action Request/Response DTO 정의
- 목적: 관리자가 AI 리포트를 수정·승인·거부하는 `reviewReport` Server Action의 입출력 타입을 정의한다. 상태 변경(approved/rejected) + 리포트 JSON 수정 + ReviewLog 생성을 단일 트랜잭션으로 처리하기 위한 계약이다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§3.3 Server Actions — reviewReport()`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 264
- 시퀀스 2: SRS §3.4 Lines 314~338 — 관리자 검수 → 승인
- 기능 요구사항:
  - REQ-FREE-FUNC-032 (관리자 리포트 수정)
  - REQ-FREE-FUNC-033 (승인/거부 상태 변경)
- DB 모델: Report (status, reportJson, reviewNote) + ReviewLog (action, note, beforeJson, afterJson)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/schemas/review.schema.ts` 파일 생성
- [ ] ReviewAction enum 상수 정의:
  ```typescript
  export const ReviewAction = {
    APPROVE: "approve",
    REJECT: "reject",
    MODIFY: "modify",
    REGENERATE_REQUEST: "regenerate_request",
  } as const
  export type ReviewActionType = typeof ReviewAction[keyof typeof ReviewAction]
  ```
- [ ] ReviewReportInput Zod 스키마 정의:
  ```typescript
  export const ReviewReportInputSchema = z.object({
    reportId: z.string().min(1),
    action: z.enum(["approve", "reject", "modify", "regenerate_request"]),
    updatedReportJson: z.any().optional(),  // action이 modify일 때만 필수
    reviewNote: z.string().optional(),
  }).refine(data => {
    if (data.action === "modify" && !data.updatedReportJson) {
      return false
    }
    return true
  }, { message: "수정(modify) 시 updatedReportJson은 필수입니다" })

  export type ReviewReportInput = z.infer<typeof ReviewReportInputSchema>
  ```
- [ ] ReviewReportOutput 타입 정의:
  ```typescript
  export type ReviewReportOutput = {
    success: true
    reportId: string
    newStatus: string
    reviewLogId: string
  } | {
    success: false
    error: string
  }
  ```
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 승인 요청 검증 성공**
- Given: `{ reportId: "r1", action: "approve", reviewNote: "LGTM" }`이 주어짐
- When: `ReviewReportInputSchema.parse(input)`를 실행함
- Then: 검증이 성공한다

**Scenario 2: 수정 요청 시 updatedReportJson 필수**
- Given: `{ reportId: "r1", action: "modify" }`이 주어짐 (updatedReportJson 없음)
- When: `ReviewReportInputSchema.parse(input)`를 실행함
- Then: ZodError가 발생하며 "updatedReportJson은 필수" 에러가 포함된다

**Scenario 3: 수정 요청 — JSON 포함 시 성공**
- Given: `{ reportId: "r1", action: "modify", updatedReportJson: {...}, reviewNote: "강점 보완" }`이 주어짐
- When: `ReviewReportInputSchema.parse(input)`를 실행함
- Then: 검증이 성공한다

**Scenario 4: 잘못된 action 값 시 실패**
- Given: `{ reportId: "r1", action: "invalid" }`이 주어짐
- When: `ReviewReportInputSchema.parse(input)`를 실행함
- Then: ZodError가 발생한다

**Scenario 5: 성공 응답 구조**
- Given: 승인 처리가 완료됨
- When: ReviewReportOutput 성공 객체를 구성함
- Then: `{ success: true, reportId, newStatus: "approved", reviewLogId }` 구조를 만족한다

## :gear: Technical & Non-Functional Constraints
- action이 "modify"일 때만 updatedReportJson 필수 — 조건부 검증 (`refine`)
- updatedReportJson은 DiagnosisReportSchema(API-004)로 별도 재검증 (C-007에서 수행)
- ReviewLog에는 beforeJson(변경 전 reportJson)과 afterJson(변경 후) 모두 기록 (C-009)
- reviewNote는 항상 optional

## :checkered_flag: Definition of Done (DoD)
- [ ] ReviewAction 상수, ReviewReportInputSchema, ReviewReportOutput 타입 정의 완료
- [ ] action별 조건부 검증(modify → updatedReportJson 필수) 동작 확인
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** DB-005 (Report 모델), DB-007 (ReviewLog 모델)
- **Blocks:** C-007 (리포트 수정 로직), C-008 (승인/거부 로직), C-009 (ReviewLog 생성), FE-003 (수정 편집기), FE-004 (승인/거부 버튼), T-009 (수정 테스트), T-010 (승인/거부 테스트)
