---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DATA-002: Diagnosis 상태값 enum 상수 정의"
labels: 'feature, data, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DATA-002] Diagnosis 상태값 enum 상수 정의
- 목적: Diagnosis 모델의 status 필드에 사용되는 허용값을 TypeScript 상수로 정의하여, 하드코딩된 문자열 비교를 제거하고 타입 안전성을 확보한다. 진단 흐름(submitted → report_pending → report_generated → reviewed) 전체에서 참조되는 SSOT이다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#Appendix A — 최소 상태값`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 506~512
- Diagnosis 상태값: `submitted | report_pending | report_generated | reviewed`
- 기능 요구사항: REQ-FREE-FUNC-012 (Diagnosis.status 정상 저장)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/constants/status.ts` 파일 생성 (또는 기존 파일에 추가)
- [ ] DiagnosisStatus 상수 객체 정의:
  ```typescript
  export const DiagnosisStatus = {
    SUBMITTED: "submitted",
    REPORT_PENDING: "report_pending",
    REPORT_GENERATED: "report_generated",
    REVIEWED: "reviewed",
  } as const
  
  export type DiagnosisStatusType = typeof DiagnosisStatus[keyof typeof DiagnosisStatus]
  ```
- [ ] 상태 전이 순서 주석 추가: `submitted → report_pending → report_generated → reviewed`
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 상수 값 정확성**
- Given: DiagnosisStatus 상수가 정의됨
- When: 4개 키(SUBMITTED, REPORT_PENDING, REPORT_GENERATED, REVIEWED)를 확인함
- Then: SRS Appendix A에 명시된 4개 문자열과 정확히 일치한다

**Scenario 2: 타입 안전성**
- Given: DiagnosisStatusType 타입이 정의됨
- When: `const s: DiagnosisStatusType = "invalid_status"`를 작성함
- Then: TypeScript 컴파일 에러가 발생한다

**Scenario 3: import 정상 동작**
- Given: status.ts가 export됨
- When: 다른 파일에서 `import { DiagnosisStatus } from "@/lib/constants/status"` 함
- Then: import가 정상 동작하고 `DiagnosisStatus.SUBMITTED === "submitted"`이 true다

## :gear: Technical & Non-Functional Constraints
- Prisma 스키마에서는 String 타입 사용 — enum은 애플리케이션 레벨 상수로만 관리
- `as const` assertion으로 리터럴 타입 추론 활성화
- DATA-003(Report), DATA-004(AiRun)과 동일 파일에 정의하여 관리 용이성 확보

## :checkered_flag: Definition of Done (DoD)
- [ ] DiagnosisStatus 상수 4개 값이 SRS 명세와 일치
- [ ] DiagnosisStatusType 타입이 export됨
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** INF-001 (프로젝트 존재)
- **Blocks:** C-003 (submitDiagnosis — status 설정), C-005 (AI 리포트 생성 — status 전이), Q-006 (목록 조회 — status 필터링)
