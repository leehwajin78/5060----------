---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-003: POST /api/ai/generate-report Request/Response DTO 정의"
labels: 'feature, backend, contract, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [API-003] POST /api/ai/generate-report Request/Response DTO 정의
- 목적: AI 진단 리포트 생성 Route Handler의 입출력 타입을 정의한다. Request에는 질문코드+답변 텍스트만 포함하고 실명/연락처를 제외하는 PII 마스킹 계약을 확립하며, Response는 DiagnosisReportSchema(API-004)를 준수하는 JSON 또는 에러 구조를 반환한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§3.3 Route Handlers — /api/ai/generate-report`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 269~271
- 시퀀스 1: SRS §3.4 Lines 289~312 — "답변 원문(질문코드+텍스트만) 기반 진단 리포트 생성 요청, 실명·연락처 제외 payload"
- 기능 요구사항:
  - REQ-FREE-FUNC-020 (AI 진단 리포트 생성)
  - REQ-FREE-FUNC-023 (AI API payload에 실명/이메일/전화번호 미포함)
  - REQ-NF-FREE-030 (AI API에 민감 정보 비전송)
- AI 리포트 Zod Schema: API-004 (DiagnosisReportSchema)
- AI 리포트 JSON 구조: SRS Appendix B Lines 603~632

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/schemas/ai-report.schema.ts` 파일 생성
- [ ] GenerateReportRequest Zod 스키마 정의:
  ```typescript
  import { z } from "zod"

  export const GenerateReportAnswerSchema = z.object({
    questionCode: z.string(),
    answerText: z.string(),
  })

  export const GenerateReportRequestSchema = z.object({
    diagnosisId: z.string(),
    answers: z.array(GenerateReportAnswerSchema).length(16),
  })

  export type GenerateReportRequest = z.infer<typeof GenerateReportRequestSchema>
  ```
- [ ] Request 스키마에 PII 필드 부재 확인 주석 추가: `// ⚠️ name, contact, email, phone 필드 의도적 제외 (REQ-FREE-FUNC-023)`
- [ ] GenerateReportResponse 타입 정의:
  ```typescript
  import { DiagnosisReport } from "./report.schema"

  export type GenerateReportResponse = {
    success: true
    report: DiagnosisReport
    aiRunId: string
  } | {
    success: false
    error: string
    errorCode: "AI_GENERATION_FAILED" | "ZOD_VALIDATION_FAILED" | "RATE_LIMIT_EXCEEDED" | "INTERNAL_ERROR"
    aiRunId?: string
  }
  ```
- [ ] 에러 코드 상수 정의:
  ```typescript
  export const GenerateReportErrorCode = {
    AI_GENERATION_FAILED: "AI_GENERATION_FAILED",
    ZOD_VALIDATION_FAILED: "ZOD_VALIDATION_FAILED",
    RATE_LIMIT_EXCEEDED: "RATE_LIMIT_EXCEEDED",
    INTERNAL_ERROR: "INTERNAL_ERROR",
  } as const
  ```
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 유효한 Request 검증 성공**
- Given: diagnosisId와 16개 답변(questionCode+answerText)이 주어짐
- When: `GenerateReportRequestSchema.parse(input)`를 실행함
- Then: 검증이 성공한다

**Scenario 2: Request에 PII 필드가 없음을 확인**
- Given: GenerateReportRequestSchema가 정의됨
- When: 스키마의 shape 키를 확인함
- Then: name, contact, email, phone 키가 존재하지 않는다

**Scenario 3: answers 16건 미만 시 실패**
- Given: answers 배열에 15건만 포함됨
- When: `GenerateReportRequestSchema.parse(input)`를 실행함
- Then: ZodError가 발생한다

**Scenario 4: 성공 Response 구조 검증**
- Given: AI 리포트 생성이 성공함
- When: GenerateReportResponse 성공 객체를 구성함
- Then: `{ success: true, report: DiagnosisReport, aiRunId: string }` 구조를 만족한다

**Scenario 5: 실패 Response 구조 검증**
- Given: AI 리포트 생성이 실패함
- When: GenerateReportResponse 실패 객체를 구성함
- Then: `{ success: false, error: string, errorCode: "AI_GENERATION_FAILED" }` 구조를 만족한다

## :gear: Technical & Non-Functional Constraints
- Request payload에 실명/연락처 절대 포함 금지 — PII 마스킹 계약의 핵심 (REQ-NF-FREE-030)
- Response의 report 필드는 DiagnosisReportSchema(API-004) 준수
- AI 호출 제한: 진단당 기본 1회 + 재생성 1회 (REQ-NF-FREE-023) → RATE_LIMIT_EXCEEDED 에러 코드
- HTTP 상태 코드 매핑: 200(성공), 400(입력 오류), 429(호출 제한), 500(서버 오류)

## :checkered_flag: Definition of Done (DoD)
- [ ] GenerateReportRequestSchema, GenerateReportResponse 타입 정의 완료
- [ ] Request에 PII 필드 없음 확인
- [ ] 에러 코드 상수 정의 완료
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** API-004 (DiagnosisReportSchema — Response 타입 참조), DB-005 (Report 모델)
- **Blocks:** C-004 (AI payload 구성), C-005 (AI 리포트 생성 로직), MOCK-002 (Mock 엔드포인트), SEC-001 (익명화 파이프라인), T-007 (PII 미포함 테스트)
