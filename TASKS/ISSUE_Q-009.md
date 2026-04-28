---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] Q-009: AiRun 로그 조회 로직 (진단별 AI 호출 이력)"
labels: 'feature, backend, query, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [Q-009] AiRun 로그 조회 로직
- 목적: 특정 진단에 연결된 AI 호출 이력(AiRun)을 조회하여, 관리자가 AI 호출 성공/실패 상태, 소요 시간, 재생성 횟수를 확인할 수 있도록 한다. 재생성 호출 횟수 제한(C-010)의 사전 카운트 조회에도 활용된다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: S12 (최소 AI 호출 로그 — 성공/실패, 생성 시간, 오류 메시지)
- DB 모델: AiRun (SRS Appendix A Lines 571~583)
- 상태 상수: DATA-004 (AiRunStatus, AiRunTaskType)
- 제약사항: REQ-NF-FREE-023 (진단당 AI 호출 최대 2회)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/queries/airun.queries.ts` 파일 생성
- [ ] `getAiRunsByDiagnosis(diagnosisId)` 함수 구현:
  ```typescript
  export async function getAiRunsByDiagnosis(diagnosisId: string) {
    return prisma.aiRun.findMany({
      where: { diagnosisId },
      orderBy: { createdAt: "desc" },
    })
  }
  ```
- [ ] `getAiRunCount(diagnosisId)` 함수 구현 — 호출 횟수 제한 검증용:
  ```typescript
  export async function getAiRunCount(diagnosisId: string) {
    return prisma.aiRun.count({
      where: { diagnosisId },
    })
  }
  ```
- [ ] 반환 타입 정의

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: AI 호출 이력 조회**
- Given: Diagnosis D에 AiRun 2건(generateReport 성공 + regenerateReport 실패)이 존재함
- When: `getAiRunsByDiagnosis(D)`를 실행함
- Then: 2건의 AiRun이 최신순으로 반환된다

**Scenario 2: 호출 횟수 카운트**
- Given: Diagnosis D에 AiRun 2건이 존재함
- When: `getAiRunCount(D)`를 실행함
- Then: 2가 반환된다

**Scenario 3: AiRun 없는 진단**
- Given: Diagnosis D에 AiRun이 0건임
- When: `getAiRunsByDiagnosis(D)`를 실행함
- Then: 빈 배열 `[]`이 반환된다

**Scenario 4: 소요 시간 확인 가능**
- Given: AiRun에 startedAt과 completedAt이 모두 기록됨
- When: 반환된 AiRun 객체를 확인함
- Then: startedAt, completedAt, status, errorMessage를 통해 소요 시간과 결과를 확인할 수 있다

## :gear: Technical & Non-Functional Constraints
- `getAiRunCount()`는 C-010(재생성 호출 횟수 제한)에서 재사용 — 2회 초과 시 차단 판별 기준
- 관리자 상세 페이지(Q-004)에서 AiRun 이력을 부가 정보로 표시 가능
- 소요 시간 = completedAt - startedAt (nullable이므로 null 체크 필요)

## :checkered_flag: Definition of Done (DoD)
- [ ] getAiRunsByDiagnosis(), getAiRunCount() 함수 구현
- [ ] 최신순 정렬, 빈 배열 반환 동작 확인
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** DB-006 (AiRun 테이블)
- **Blocks:** C-010 (재생성 호출 횟수 제한 — getAiRunCount 사용), Q-004 (상세 UI — AiRun 이력 표시), LOG-001 (AI 호출 로깅)
