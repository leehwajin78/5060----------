---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-007: GET /api/reports/[id] Response DTO 정의"
labels: 'feature, backend, contract, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [API-007] GET /api/reports/[id] Response DTO 정의
- 목적: 승인된 리포트를 고객 웹뷰에 제공하는 Route Handler의 응답 타입을 정의한다. `approved` 상태만 반환하고, 미승인(draft/rejected) 리포트는 404 또는 "준비 중" 응답을 반환하는 접근 제어 계약을 포함한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§3.3 Route Handlers — /api/reports/[id]`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 272
- 시퀀스 2: SRS §3.4 Lines 331~338 — "approved 상태 리포트 조회, not approved → 404 또는 준비 중"
- 기능 요구사항:
  - REQ-FREE-FUNC-034 (미승인 리포트 고객 비공개)
  - REQ-FREE-FUNC-040 (승인 리포트 웹뷰 표시)
  - REQ-FREE-FUNC-041 (리포트 하단 상담 CTA)
  - REQ-NF-FREE-033 (미승인 리포트 외부 URL 비공개)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/schemas/public-report.schema.ts` 파일 생성
- [ ] PublicReportResponse 타입 정의:
  ```typescript
  import { DiagnosisReport } from "./report.schema"

  export type PublicReportResponse = {
    success: true
    report: DiagnosisReport
    approvedAt: string  // ISO 8601
  } | {
    success: false
    error: string
    errorCode: "NOT_FOUND" | "NOT_APPROVED" | "INTERNAL_ERROR"
    statusCode: 404 | 403 | 500
  }
  ```
- [ ] CTA 설정 타입 정의:
  ```typescript
  export type CtaConfig = {
    type: "google_form" | "email" | "kakao"
    url: string
    label: string
  }
  ```
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 승인 리포트 정상 응답**
- Given: Report R이 status="approved"로 존재함
- When: `GET /api/reports/R`을 요청함
- Then: `{ success: true, report: DiagnosisReport, approvedAt: "..." }` 응답과 HTTP 200이 반환된다

**Scenario 2: 미승인 리포트 접근 차단**
- Given: Report R이 status="draft"로 존재함
- When: `GET /api/reports/R`을 요청함
- Then: `{ success: false, errorCode: "NOT_APPROVED", statusCode: 404 }` 응답이 반환된다

**Scenario 3: 존재하지 않는 리포트**
- Given: Report ID가 존재하지 않음
- When: `GET /api/reports/invalid-id`를 요청함
- Then: `{ success: false, errorCode: "NOT_FOUND", statusCode: 404 }` 응답이 반환된다

**Scenario 4: rejected 리포트 접근 차단**
- Given: Report R이 status="rejected"로 존재함
- When: `GET /api/reports/R`을 요청함
- Then: `{ success: false, errorCode: "NOT_APPROVED", statusCode: 404 }` 응답이 반환된다

## :gear: Technical & Non-Functional Constraints
- approved 상태만 HTTP 200 반환 — 나머지는 모두 404 (미승인 사실 노출 방지를 위해 403 대신 404 사용)
- DiagnosisReport 타입은 API-004에서 정의한 스키마 참조
- approvedAt: Report.updatedAt(승인 시점) 기준 ISO 8601 문자열
- CTA 설정은 환경변수에서 읽어 응답에 포함하거나, 프론트엔드에서 별도 관리 가능

## :checkered_flag: Definition of Done (DoD)
- [ ] PublicReportResponse 타입 정의 완료
- [ ] CtaConfig 타입 정의 완료
- [ ] approved/draft/rejected/not-found 각 케이스의 응답 구조 명확
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** API-004 (DiagnosisReportSchema — report 필드 타입), DB-005 (Report.status)
- **Blocks:** Q-005 (리포트 웹뷰 UI), Q-008 (승인 리포트 조회 로직), FE-005 (미승인 접근 차단), FE-006 (CTA 버튼), SEC-003 (외부 URL 접근 차단), T-011 (접근 차단 테스트), T-012 (승인 리포트 표시 테스트)
