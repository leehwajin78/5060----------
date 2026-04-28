---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] Q-006: 관리자 진단 목록 조회 로직 (Prisma join, 최신순)"
labels: 'feature, backend, query, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [Q-006] 관리자 진단 목록 조회 로직
- 목적: 관리자 콘솔 목록 페이지(Q-003)에 데이터를 공급하는 서버 측 조회 로직을 구현한다. Diagnosis + Lead를 join하고 최신순 정렬하며, 연결된 Report의 최신 상태를 함께 반환한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§4.1 F3-Lite`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — REQ-FREE-FUNC-030
- DB 모델: Lead, Diagnosis, Report (SRS Appendix A, E)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/queries/diagnosis.queries.ts` 파일 생성
- [ ] `getDiagnosisList()` 함수 구현:
  ```typescript
  export async function getDiagnosisList() {
    return prisma.diagnosis.findMany({
      orderBy: { createdAt: "desc" },
      include: {
        lead: { select: { name: true, contact: true } },
        reports: {
          select: { id: true, status: true, updatedAt: true },
          orderBy: { updatedAt: "desc" },
          take: 1,  // 최신 리포트 1건만
        },
      },
    })
  }
  ```
- [ ] 반환 타입 정의:
  ```typescript
  export type DiagnosisListItem = Awaited<ReturnType<typeof getDiagnosisList>>[number]
  ```
- [ ] Q-003 페이지에서 getDiagnosisList() 호출 연동 (Server Component data fetch)
- [ ] MOCK-003 데이터 제거 후 실제 DB 조회로 전환

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 최신순 정렬**
- Given: Diagnosis 3건이 서로 다른 createdAt으로 존재함
- When: `getDiagnosisList()`를 실행함
- Then: createdAt 역순(최신→과거)으로 정렬되어 반환된다

**Scenario 2: Lead 정보 포함**
- Given: Diagnosis D가 Lead L과 연결됨
- When: `getDiagnosisList()`를 실행함
- Then: 각 항목에 lead.name과 lead.contact가 포함된다

**Scenario 3: 최신 Report 상태 포함**
- Given: Diagnosis D에 Report 2건(draft, approved)이 연결됨
- When: `getDiagnosisList()`를 실행함
- Then: reports 배열에 가장 최신 Report 1건만 포함된다

**Scenario 4: 빈 목록 반환**
- Given: Diagnosis가 0건임
- When: `getDiagnosisList()`를 실행함
- Then: 빈 배열 `[]`이 반환된다

## :gear: Technical & Non-Functional Constraints
- Prisma Client를 사용한 서버 측 조회 — `src/lib/prisma.ts` 싱글턴 import
- `include`로 Lead/Report를 join — N+1 쿼리 방지
- Report는 최신 1건만 take(1) — 재생성 시 여러 Report가 존재할 수 있으므로
- Server Component에서 직접 호출 (API Route 불필요)

## :checkered_flag: Definition of Done (DoD)
- [ ] getDiagnosisList() 함수 구현 및 타입 정의
- [ ] 최신순 정렬, Lead join, 최신 Report 포함 동작 확인
- [ ] Q-003 페이지 연동
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** DB-002 (Lead), DB-003 (Diagnosis), DB-005 (Report), DB-001 (Prisma Client)
- **Blocks:** Q-003 (목록 UI DB 연동), T-008 (최신순 정렬 테스트)
