---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] Q-007: 관리자 진단 상세 조회 로직 (Diagnosis+Answer+Report)"
labels: 'feature, backend, query, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [Q-007] 관리자 진단 상세 조회 로직
- 목적: 관리자 상세 페이지(Q-004)에 데이터를 공급하는 서버 측 조회 로직을 구현한다. Diagnosis + Lead + Answer 16건 + Report(최신) + ReviewLog 이력을 한 번의 쿼리로 조회한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS: REQ-FREE-FUNC-031 (답변 원문과 AI 리포트 확인)
- DB 모델: Lead, Diagnosis, Answer, Report, ReviewLog (SRS Appendix A, E)
- 시퀀스 2: SRS §3.4 Lines 326~327 — "Diagnosis / Answer / Report 조회"

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/queries/diagnosis.queries.ts`에 `getDiagnosisDetail(id)` 함수 추가:
  ```typescript
  export async function getDiagnosisDetail(id: string) {
    return prisma.diagnosis.findUnique({
      where: { id },
      include: {
        lead: true,
        answers: { orderBy: { createdAt: "asc" } },
        reports: {
          orderBy: { updatedAt: "desc" },
          take: 1,
          include: { reviewLogs: { orderBy: { createdAt: "desc" } } },
        },
        aiRuns: { orderBy: { createdAt: "desc" } },
      },
    })
  }
  ```
- [ ] 반환 타입 정의: `export type DiagnosisDetail = Awaited<ReturnType<typeof getDiagnosisDetail>>`
- [ ] null 반환 시(존재하지 않는 ID) 처리 가이드 주석 추가
- [ ] Q-004 페이지에서 호출 연동

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 상세 조회 성공**
- Given: Diagnosis D가 Lead, Answer 16건, Report 1건과 연결됨
- When: `getDiagnosisDetail(D)`를 실행함
- Then: lead, answers(16건), reports(1건), aiRuns가 모두 포함된 객체가 반환된다

**Scenario 2: Answer 정렬**
- Given: Answer 16건이 존재함
- When: 반환된 answers를 확인함
- Then: createdAt 오름차순(생성 순서)으로 정렬되어 있다

**Scenario 3: ReviewLog 포함**
- Given: Report R에 ReviewLog 2건이 존재함
- When: 반환된 reports[0].reviewLogs를 확인함
- Then: ReviewLog 2건이 createdAt 역순으로 포함된다

**Scenario 4: 존재하지 않는 ID**
- Given: 존재하지 않는 diagnosisId가 주어짐
- When: `getDiagnosisDetail("invalid")`를 실행함
- Then: null이 반환된다

## :gear: Technical & Non-Functional Constraints
- 단일 Prisma 쿼리로 N+1 방지 (include 중첩)
- Report는 최신 1건만 take(1) — 재생성 이력 있을 수 있음
- Server Component에서 직접 호출

## :checkered_flag: Definition of Done (DoD)
- [ ] getDiagnosisDetail() 함수 구현 및 타입 정의
- [ ] Lead + Answer 16건 + Report + ReviewLog + AiRun 포함 조회 동작 확인
- [ ] null 반환 처리
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** DB-003 (Diagnosis), DB-004 (Answer), DB-005 (Report), DB-006 (AiRun), DB-007 (ReviewLog)
- **Blocks:** Q-004 (상세 UI DB 연동), FE-003 (수정 편집기 데이터), FE-004 (승인/거부 데이터)
