---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] MOCK-003: 관리자 목록/상세 화면용 진단·리포트 Mock 데이터"
labels: 'feature, mock, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-003] 관리자 목록/상세 화면용 진단·리포트 Mock 데이터
- 목적: 관리자 콘솔(Q-003, Q-004)이 DB 연동 없이 독립 개발할 수 있도록, 진단 목록(여러 건) + 상세(답변 원문 + 리포트)의 Mock 데이터를 제공한다. 다양한 Report 상태(draft/approved/rejected)를 포함하여 UI 분기 개발을 지원한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§4.1 F3-Lite`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — REQ-FREE-FUNC-030~034
- DB 모델: Lead + Diagnosis + Answer + Report (SRS Appendix A)
- 참조 Mock: MOCK-001 (진단 입력), MOCK-002 (리포트 JSON)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/mocks/admin.mock.ts` 파일 생성
- [ ] 목록 화면용 Mock — 3~5건의 진단 요약:
  ```typescript
  export const mockDiagnosisList = [
    {
      id: "diag-001", leadName: "김전문", leadContact: "expert@example.com",
      status: "report_generated", reportStatus: "draft",
      createdAt: "2026-04-25T10:00:00Z",
    },
    {
      id: "diag-002", leadName: "이경력", leadContact: "010-1234-5678",
      status: "reviewed", reportStatus: "approved",
      createdAt: "2026-04-24T14:30:00Z",
    },
    {
      id: "diag-003", leadName: "박시니어", leadContact: "senior@company.com",
      status: "report_generated", reportStatus: "rejected",
      createdAt: "2026-04-23T09:15:00Z",
    },
  ]
  ```
- [ ] 상세 화면용 Mock — 답변 원문 16건 + 리포트:
  ```typescript
  export const mockDiagnosisDetail = {
    id: "diag-001",
    lead: { name: "김전문", contact: "expert@example.com", channel: "지인 추천" },
    answers: QUESTIONS.map(q => ({
      questionCode: q.code,
      answerText: `[${q.code}] 에 대한 상세 답변 내용입니다. 30년 경력 기반의 답변.`,
    })),
    report: mockValidReport,  // MOCK-002 참조
    reportStatus: "draft",
    createdAt: "2026-04-25T10:00:00Z",
  }
  ```
- [ ] 상태별 리포트 Mock — draft/approved/rejected 각 1건
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 목록 Mock에 최소 3건 포함**
- Given: mockDiagnosisList가 정의됨
- When: 배열 길이를 확인함
- Then: 3건 이상이다

**Scenario 2: 목록 Mock에 다양한 상태 포함**
- Given: mockDiagnosisList가 정의됨
- When: reportStatus 값들을 확인함
- Then: draft, approved, rejected 중 최소 2종 이상이 포함된다

**Scenario 3: 상세 Mock에 답변 16건 포함**
- Given: mockDiagnosisDetail이 정의됨
- When: answers 배열 길이를 확인함
- Then: 정확히 16건이다

**Scenario 4: 상세 Mock의 리포트가 DiagnosisReport 구조 준수**
- Given: mockDiagnosisDetail.report가 정의됨
- When: DiagnosisReportSchema로 검증함
- Then: 검증이 성공한다

## :gear: Technical & Non-Functional Constraints
- MOCK-001, MOCK-002를 import하여 재사용 — 데이터 일관성 유지
- 목록 Mock은 최신순 정렬 시뮬레이션 (createdAt 역순)
- 한글 이름/답변 사용 — 실제 관리자 화면 개발 시 레이아웃 확인 용도

## :checkered_flag: Definition of Done (DoD)
- [ ] 목록 Mock 3건 이상, 상세 Mock 1건 이상 정의
- [ ] 다양한 Report 상태(draft/approved/rejected) 포함
- [ ] 상세 Mock 답변 16건 + 리포트 Zod 검증 통과
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** MOCK-001 (진단 입력 Mock), MOCK-002 (리포트 JSON Mock), DATA-001 (QUESTIONS 배열)
- **Blocks:** Q-003 (관리자 목록 UI 개발), Q-004 (관리자 상세 UI 개발), FE-003 (리포트 수정 편집기)
