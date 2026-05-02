---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-004: AI 진단 리포트 Zod Schema (DiagnosisReportSchema) 작성"
labels: 'feature, backend, contract, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [API-004] AI 진단 리포트 Zod Schema 작성
- 목적: AI(Gemini)가 생성하는 진단 리포트 JSON의 구조를 Zod 스키마로 엄격하게 정의하여, AI 출력 검증·환각 차단·Report.reportJson 저장의 계약(Contract)을 확립한다. 이 스키마는 프론트엔드(웹뷰), 백엔드(AI 호출), 관리자(검수) 모두가 참조하는 단일 진실 공급원(SSOT)이다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#Appendix B — AI 진단 리포트 JSON Schema`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 599~666
- JSON 구조 예시: SRS Appendix B Lines 603~632
- Zod Schema TypeScript: SRS Appendix B Lines 637~665
- 기능 요구사항:
  - REQ-FREE-FUNC-020 (강점, 약점, 브랜드 방향, 추천 문장, 상담 CTA 포함 JSON)
  - REQ-FREE-FUNC-021 (sourceQuestionCodes 필수 포함)
  - REQ-NF-FREE-040 (원문 답변 근거 질문 번호 포함)
- 가치 보존 체크리스트: SRS Appendix F — "환각 차단: Zod 검증 실패 시 draft 상태 유지"

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `npm install zod` 의존성 설치 (미설치 시)
- [ ] `src/lib/schemas/report.schema.ts` 파일 생성
- [ ] StrengthSchema 정의:
  ```typescript
  const StrengthSchema = z.object({
    title: z.string(),
    description: z.string(),
    sourceQuestionCodes: z.array(z.string()),
  })
  ```
- [ ] BrandDirectionSchema 정의:
  ```typescript
  const BrandDirectionSchema = z.object({
    oneSentence: z.string().max(80),
    description: z.string(),
    sourceQuestionCodes: z.array(z.string()),
  })
  ```
- [ ] DiagnosisReportSchema 정의:
  ```typescript
  export const DiagnosisReportSchema = z.object({
    summary: z.string().min(30).max(500),
    strengths: z.array(StrengthSchema).min(1).max(5),
    weaknesses: z.array(StrengthSchema).min(1).max(3),
    brandDirection: BrandDirectionSchema,
    recommendedNextStep: z.object({
      message: z.string(),
      ctaLabel: z.string(),
    }),
    warnings: z.array(z.string()).optional(),
  })
  ```
- [ ] `DiagnosisReport` 타입 export: `export type DiagnosisReport = z.infer<typeof DiagnosisReportSchema>`
- [ ] 유효한 Mock JSON으로 `.parse()` 성공 확인
- [ ] 유효하지 않은 JSON(summary 30자 미만, strengths 빈 배열, sourceQuestionCodes 누락)으로 `.parse()` 실패 확인
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 유효한 리포트 JSON 검증 성공**
- Given: SRS Appendix B 예시에 부합하는 완전한 JSON 객체가 주어짐
- When: `DiagnosisReportSchema.parse(validJson)`를 실행함
- Then: 검증이 성공하고 파싱된 `DiagnosisReport` 타입 객체가 반환된다

**Scenario 2: summary 길이 제약 위반**
- Given: summary가 29자(30자 미만)인 JSON이 주어짐
- When: `DiagnosisReportSchema.parse(shortSummary)`를 실행함
- Then: ZodError가 발생하며, summary 필드의 min 제약 위반 메시지가 포함된다

**Scenario 3: strengths 빈 배열 시 실패**
- Given: strengths가 빈 배열(`[]`)인 JSON이 주어짐
- When: `DiagnosisReportSchema.parse(emptyStrengths)`를 실행함
- Then: ZodError가 발생하며, strengths의 min(1) 제약 위반 메시지가 포함된다

**Scenario 4: sourceQuestionCodes 누락 시 실패**
- Given: strengths[0]에서 sourceQuestionCodes 필드가 누락된 JSON이 주어짐
- When: `DiagnosisReportSchema.parse(missingCodes)`를 실행함
- Then: ZodError가 발생한다

**Scenario 5: brandDirection.oneSentence 80자 초과 시 실패**
- Given: brandDirection.oneSentence가 81자인 JSON이 주어짐
- When: `DiagnosisReportSchema.parse(longOneSentence)`를 실행함
- Then: ZodError가 발생하며, max(80) 제약 위반 메시지가 포함된다

**Scenario 6: warnings 필드 생략 허용**
- Given: warnings 필드가 없는 JSON이 주어짐
- When: `DiagnosisReportSchema.parse(noWarnings)`를 실행함
- Then: 검증이 성공한다 (warnings는 optional)

**Scenario 7: weaknesses 최대 3건 초과 시 실패**
- Given: weaknesses에 4건이 포함된 JSON이 주어짐
- When: `DiagnosisReportSchema.parse(tooManyWeaknesses)`를 실행함
- Then: ZodError가 발생하며, max(3) 제약 위반 메시지가 포함된다

## :gear: Technical & Non-Functional Constraints
- 파일 경로: `src/lib/schemas/report.schema.ts` (SRS Appendix B 명세)
- Zod ≥ 3.x
- summary: 30~500자 (`.min(30).max(500)`)
- strengths: 1~5개 (`.min(1).max(5)`)
- weaknesses: 1~3개 (`.min(1).max(3)`)
- brandDirection.oneSentence: 최대 80자 (`.max(80)`)
- sourceQuestionCodes: `z.array(z.string())` — 16문항 코드(Q1, Q2, Q4 등)가 포함되어야 함
- warnings: optional (`z.array(z.string()).optional()`)
- 이 스키마는 AI 출력 검증(C-005), 관리자 수정 검증(C-007), 프론트엔드 렌더링(Q-005) 모두에서 참조됨
- Zod 검증 실패 시 Report는 draft 상태로 유지 — 고객에게 자동 공개 불가 (SRS Appendix F 환각 차단)

## :checkered_flag: Definition of Done (DoD)
- [ ] `src/lib/schemas/report.schema.ts` 파일이 생성됨
- [ ] DiagnosisReportSchema가 SRS Appendix B 명세와 정확히 일치함
- [ ] DiagnosisReport 타입이 export됨
- [ ] 유효 JSON → `.parse()` 성공 확인
- [ ] 무효 JSON 7가지 시나리오 → `.parse()` 실패 + ZodError 확인
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건 유지

## :construction: Dependencies & Blockers
- **Depends on:** None (Zod는 독립 라이브러리, 프로젝트 존재만 필요)
- **Blocks:** API-003 (generate-report DTO — 응답 검증에 사용), C-005 (AI 리포트 생성 — Zod 검증 후 저장), C-007 (관리자 수정 — 수정된 JSON 재검증), MOCK-002 (Mock 리포트 데이터 — 스키마 준수), T-005 (Zod 스키마 통과 테스트), Q-005 (리포트 웹뷰 — 타입 안전 렌더링)
