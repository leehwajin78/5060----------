---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-008: 공통 에러 응답 코드 및 유틸리티 정의"
labels: 'feature, backend, contract, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [API-008] 공통 에러 응답 코드 및 유틸리티 정의
- 목적: 모든 Server Action과 Route Handler에서 일관되게 사용하는 공통 에러 응답 구조, HTTP 상태 코드 매핑, Zod 에러 변환 유틸리티를 정의한다. 프론트엔드가 에러를 예측 가능하게 처리할 수 있도록 통일된 계약을 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§3.3 API Overview`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 256~283
- 기능 요구사항:
  - REQ-FREE-FUNC-004 (유효하지 않은 답변 → 오류 메시지)
  - REQ-FREE-FUNC-022 (AI 실패 → "검수 후 안내" 메시지)
  - REQ-FREE-FUNC-034 (미승인 리포트 → 차단)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/errors.ts` 파일 생성
- [ ] 공통 에러 코드 상수 정의:
  ```typescript
  export const ErrorCode = {
    // 클라이언트 에러 (4xx)
    VALIDATION_FAILED: "VALIDATION_FAILED",
    NOT_FOUND: "NOT_FOUND",
    NOT_APPROVED: "NOT_APPROVED",
    UNAUTHORIZED: "UNAUTHORIZED",
    RATE_LIMIT_EXCEEDED: "RATE_LIMIT_EXCEEDED",
    // 서버 에러 (5xx)
    AI_GENERATION_FAILED: "AI_GENERATION_FAILED",
    ZOD_VALIDATION_FAILED: "ZOD_VALIDATION_FAILED",
    DATABASE_ERROR: "DATABASE_ERROR",
    INTERNAL_ERROR: "INTERNAL_ERROR",
  } as const

  export type ErrorCodeType = typeof ErrorCode[keyof typeof ErrorCode]
  ```
- [ ] 공통 에러 응답 타입 정의:
  ```typescript
  export type ActionError = {
    success: false
    error: string
    errorCode: ErrorCodeType
    fieldErrors?: Record<string, string[]>
  }
  ```
- [ ] Zod 에러 → fieldErrors 변환 유틸리티:
  ```typescript
  import { ZodError } from "zod"

  export function formatZodError(error: ZodError): ActionError {
    const fieldErrors: Record<string, string[]> = {}
    error.errors.forEach(err => {
      const path = err.path.join(".")
      if (!fieldErrors[path]) fieldErrors[path] = []
      fieldErrors[path].push(err.message)
    })
    return {
      success: false,
      error: "입력값이 올바르지 않습니다",
      errorCode: ErrorCode.VALIDATION_FAILED,
      fieldErrors,
    }
  }
  ```
- [ ] HTTP 상태 코드 매핑 상수:
  ```typescript
  export const ErrorHttpStatus: Record<ErrorCodeType, number> = {
    VALIDATION_FAILED: 400,
    NOT_FOUND: 404,
    NOT_APPROVED: 404,  // 미승인 사실 비노출
    UNAUTHORIZED: 401,
    RATE_LIMIT_EXCEEDED: 429,
    AI_GENERATION_FAILED: 500,
    ZOD_VALIDATION_FAILED: 500,
    DATABASE_ERROR: 500,
    INTERNAL_ERROR: 500,
  }
  ```
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: formatZodError 변환 정상 동작**
- Given: Zod 검증 실패로 ZodError가 발생함 (name 필드 에러)
- When: `formatZodError(zodError)`를 실행함
- Then: `{ success: false, errorCode: "VALIDATION_FAILED", fieldErrors: { name: ["..."] } }` 구조가 반환된다

**Scenario 2: 에러 코드 → HTTP 상태 코드 매핑**
- Given: ErrorHttpStatus 매핑이 정의됨
- When: `ErrorHttpStatus["VALIDATION_FAILED"]`를 확인함
- Then: 400이 반환된다

**Scenario 3: 모든 에러 코드에 HTTP 상태 존재**
- Given: ErrorCode의 모든 키가 존재함
- When: ErrorHttpStatus에서 각 키를 조회함
- Then: 모든 키에 대해 유효한 HTTP 상태 코드가 존재한다

**Scenario 4: NOT_APPROVED 에러가 404로 매핑**
- Given: 미승인 리포트 접근 시 NOT_APPROVED 에러가 발생함
- When: `ErrorHttpStatus["NOT_APPROVED"]`를 확인함
- Then: 404가 반환된다 (미승인 사실 비노출을 위해 403 대신 404)

## :gear: Technical & Non-Functional Constraints
- NOT_APPROVED → 404 (403이 아닌 404) — 리포트 존재 여부 자체를 비노출 (REQ-NF-FREE-033)
- formatZodError는 모든 Server Action에서 catch 블록의 표준 변환기로 사용
- Server Action에서는 HTTP 상태 코드를 직접 반환하지 않으나, Route Handler에서 ErrorHttpStatus를 사용
- fieldErrors 구조는 Zod `flatten()` 결과와 호환

## :checkered_flag: Definition of Done (DoD)
- [ ] ErrorCode 상수, ActionError 타입, formatZodError 유틸리티, ErrorHttpStatus 매핑 정의 완료
- [ ] 모든 에러 코드에 HTTP 상태 매핑 존재
- [ ] formatZodError가 ZodError를 정상 변환
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** None (독립 유틸리티)
- **Blocks:** C-001~C-010 (모든 Command 로직의 에러 처리), Q-006~Q-009 (모든 Query 로직의 에러 처리), FE-001~FE-006 (프론트엔드 에러 표시)
