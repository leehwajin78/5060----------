---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-006: regenerateReport Server Action Request/Response DTO 정의"
labels: 'feature, backend, contract, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [API-006] regenerateReport Server Action Request/Response DTO 정의
- 목적: 관리자가 AI 리포트 재생성을 요청하는 `regenerateReport` Server Action의 입출력 타입을 정의한다. 진단당 재생성은 1회로 제한(REQ-NF-FREE-023)되므로, 호출 횟수 검증을 위한 입력 구조와 제한 초과 에러 응답을 포함한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§3.3 Server Actions — regenerateReport()`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 265
- 기능 요구사항:
  - REQ-NF-FREE-023 (AI 호출 1회 진단당 기본 1회 + 관리자 재생성 1회)
- DB 모델: AiRun (taskType: "regenerateReport"), Report (status: "regeneration_requested")

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/schemas/regenerate.schema.ts` 파일 생성
- [ ] RegenerateReportInput Zod 스키마 정의:
  ```typescript
  import { z } from "zod"

  export const RegenerateReportInputSchema = z.object({
    diagnosisId: z.string().min(1),
    reportId: z.string().min(1),
    reason: z.string().optional(),  // 재생성 사유
  })

  export type RegenerateReportInput = z.infer<typeof RegenerateReportInputSchema>
  ```
- [ ] RegenerateReportOutput 타입 정의:
  ```typescript
  export type RegenerateReportOutput = {
    success: true
    newReportId: string
    aiRunId: string
    message: string
  } | {
    success: false
    error: string
    errorCode: "RATE_LIMIT_EXCEEDED" | "DIAGNOSIS_NOT_FOUND" | "AI_GENERATION_FAILED" | "INTERNAL_ERROR"
  }
  ```
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 유효한 재생성 요청 검증 성공**
- Given: `{ diagnosisId: "d1", reportId: "r1", reason: "강점 누락" }`이 주어짐
- When: `RegenerateReportInputSchema.parse(input)`를 실행함
- Then: 검증이 성공한다

**Scenario 2: diagnosisId 누락 시 실패**
- Given: `{ diagnosisId: "", reportId: "r1" }`이 주어짐
- When: `RegenerateReportInputSchema.parse(input)`를 실행함
- Then: ZodError가 발생한다

**Scenario 3: 성공 응답 구조**
- Given: 재생성이 정상 완료됨
- When: 성공 응답을 구성함
- Then: `{ success: true, newReportId, aiRunId, message }` 구조를 만족한다

**Scenario 4: 호출 제한 초과 응답**
- Given: 이미 재생성 1회를 소진함
- When: 실패 응답을 구성함
- Then: `{ success: false, errorCode: "RATE_LIMIT_EXCEEDED" }` 구조를 만족한다

## :gear: Technical & Non-Functional Constraints
- 진단당 AI 호출 최대 2회 (기본 1회 + 재생성 1회) — C-010에서 AiRun count 기반 검증
- 재생성 시 기존 Report는 status="regeneration_requested"로 변경, 새 Report(draft)가 생성됨
- reason은 optional — ReviewLog에 기록 용도

## :checkered_flag: Definition of Done (DoD)
- [ ] RegenerateReportInputSchema, RegenerateReportOutput 타입 정의 완료
- [ ] 에러 코드 상수 포함 (RATE_LIMIT_EXCEEDED 등)
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** DB-005 (Report), DB-006 (AiRun)
- **Blocks:** C-010 (재생성 로직 + 호출 횟수 제한), FE-004 (재생성 버튼), T-014 (호출 횟수 제한 테스트)
