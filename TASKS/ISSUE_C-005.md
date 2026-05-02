---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] C-005: AI 진단 리포트 생성 + Zod 검증 + Report 저장"
labels: 'feature, backend, command, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [C-005] AI 진단 리포트 생성 + Zod 검증 + Report 저장
- 목적: Gemini API를 호출하여 진단 리포트 JSON을 생성하고, DiagnosisReportSchema로 Zod 검증한 후 Report 테이블에 draft 상태로 저장한다. 환각 차단의 핵심 — Zod 검증 실패 시 Report를 생성하지 않고 AiRun에 실패를 기록한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 시퀀스 1: [`SRS_v1.md#§3.4`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 301~311
- AI 코딩 Prompt 3: SRS Appendix D Lines 738~756
- 기능 요구사항:
  - REQ-FREE-FUNC-020 (AI 진단 리포트 생성)
  - REQ-FREE-FUNC-021 (sourceQuestionCodes 필수)
  - REQ-FREE-FUNC-022 (AI 실패 시 실패 상태 기록)
- Zod Schema: API-004 (DiagnosisReportSchema)
- AI payload: C-004 (buildAiPayload)
- AiRun 상태: DATA-004 (AiRunStatus, AiRunTaskType)
- Report 상태: DATA-003 (ReportStatus.DRAFT)

## :white_check_mark: Task Breakdown (실행 계획)

### 입력

- diagnosisId
- answers: questionCode + answerText

### 처리 절차

1. Diagnosis 존재 여부 확인
2. Answer 16건 존재 여부 확인
3. AI payload 익명화
4. AiRun.status=processing 생성
5. Gemini API 호출
6. 응답 JSON 파싱
7. DiagnosisReportSchema로 Zod 검증
8. Report.status=draft 저장
9. AiRun.status=completed 변경
10. Diagnosis.status=report_generated 변경

### 예외 처리

| 상황 | 처리 |
|---|---|
| Diagnosis 없음 | 404 |
| Answer 16건 미만 | 422 |
| Gemini API 실패 | AiRun.status=failed |
| JSON 파싱 실패 | AiRun.status=failed |
| Zod 검증 실패 | AiRun.status=failed |
| timeout | 처리 중 안내 또는 실패 기록 |

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 정상 리포트 생성 완료**
- Given: 올바른 진단과 16개 답변
- When: AI 리포트 생성을 요청함
- Then: AI가 응답하고 Zod 검증을 통과하여 Report.status가 draft로 생성되며, AiRun이 completed로 업데이트됨.

**Scenario 2: 생성 실패 및 재시도 가능 상태 처리**
- Given: AI 생성 중 타임아웃 또는 Zod 검증 실패 발생
- When: 예외가 발생함
- Then: Report가 생성되지 않고, AiRun이 failed 상태로 로그를 남기며 원본 Answer 데이터는 보존됨.

## :gear: Technical & Non-Functional Constraints
- Gemini 2.0 Flash 사용 (Free Tier 호환)
- AI 응답에서 JSON 추출 시 마크다운 코드블록(```json```) 제거 필요
- Zod 검증이 환각 차단의 마지막 방어선 — 실패 시 절대 Report를 생성하지 않음
- AiRun은 AI 호출 시작 시점에 먼저 생성 (processing) → 완료 후 업데이트
- Vercel Hobby 서버리스 타임아웃(10초) 고려 — 대용량 답변 시 주의

## :checkered_flag: Definition of Done (DoD)
- [ ] generateDiagnosisReport() 함수 구현 완료
- [ ] Gemini API 호출 → Zod 검증 → Report 저장 플로우 동작 확인
- [ ] Zod 실패 시 Report 미생성 + AiRun 실패 기록 확인
- [ ] Diagnosis 상태 전이(submitted→report_generated) 확인
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** C-004 (buildAiPayload), API-004 (DiagnosisReportSchema), DB-005 (Report), DB-006 (AiRun), DATA-002~004 (상태 상수), INF-003 (Gemini API 키 설정)
- **Blocks:** C-003 (submitDiagnosis에서 트리거), C-010 (재생성 로직 재사용), FE-002 (제출 후 리포트 상태 표시), T-005 (Zod 통과 테스트), T-006 (AI 실패 테스트)
