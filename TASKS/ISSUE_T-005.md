---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-005: AI 진단 리포트 JSON Zod 스키마 검증 테스트 (환각 차단)"
labels: 'feature, testing, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [T-005] AI 진단 리포트 JSON Zod 스키마 검증 테스트
- 목적: AI가 반환한 JSON 문자열이 시스템의 단일 진실 공급원(SSOT)인 `DiagnosisReportSchema`를 정확히 통과하는지, 필수 필드가 누락되었을 때 정상적으로 차단하는지(환각 방어)를 검증한다.

## :link: References (Spec & Context)
> :bulb: AI 기획 및 개발 가이드라인:
- 타겟 스키마: API-004 (`DiagnosisReportSchema`)
- Mock 데이터: MOCK-002 (성공/실패 JSON)
- 요구사항: REQ-FREE-FUNC-021 (sourceQuestionCodes 필수, 스키마 준수)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `__tests__/validation/report-schema.test.ts` 파일 생성
- [ ] MOCK-002에서 정의한 데이터 임포트
- [ ] 검증 케이스 작성:
  - 정상적인 JSON 객체 파싱 성공 테스트
  - `summary` 필드가 짧거나 누락된 경우 실패 테스트
  - `strengths` 또는 `weaknesses` 배열에 항목이 없는 경우(min 1) 실패 테스트
  - 항목 내 `sourceQuestionCodes`가 누락된 경우 실패 테스트
  - `brandDirection.oneSentence` 누락 시 실패 테스트

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 정상 리포트 객체 통과**
- Given: MOCK-002의 `mockValidReport` 데이터
- When: `DiagnosisReportSchema.parse()` 실행
- Then: 예외가 발생하지 않고 파싱된 객체가 반환된다

**Scenario 2: sourceQuestionCodes 누락 차단 (환각 차단)**
- Given: 강점 항목 중 하나에 `sourceQuestionCodes`가 누락된 객체
- When: `DiagnosisReportSchema.parse()` 실행
- Then: ZodError가 발생하며, 해당 필드가 Required임을 명시한다

**Scenario 3: summary 글자수 미달 차단**
- Given: `summary` 필드의 텍스트가 20자인 객체 (최소 30자 요구)
- When: `DiagnosisReportSchema.parse()` 실행
- Then: ZodError가 발생한다

## :gear: Technical & Non-Functional Constraints
- 환각을 방어하는 최후의 보루이므로 Edge 케이스(배열 비어있음, null 값 등)를 꼼꼼히 확인해야 한다.
- 순수 Zod 검증 테스트이므로 매우 빠르게 동작해야 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] Zod 스키마 테스트 케이스 작성 및 통과
- [ ] 엣지 케이스 방어 확인
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** API-004 (스키마), MOCK-002 (테스트 데이터)
- **Blocks:** None
