---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] Q-004: 관리자 진단 상세 조회 UI (/admin/diagnoses/[id])"
labels: 'feature, frontend, admin, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [Q-004] 관리자 진단 상세 조회 UI
- 목적: 관리자가 특정 진단의 리드 정보, 16문항 답변 원문, AI 진단 리포트를 한 화면에서 확인할 수 있는 상세 페이지를 구현한다. 이 페이지는 리포트 수정·승인(FE-003, FE-004)의 기반이 된다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§4.1 F3-Lite`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — REQ-FREE-FUNC-031
- AI 코딩 Prompt 4: SRS Appendix D Lines 769~771
- Mock 데이터: MOCK-003 (mockDiagnosisDetail)
- 리포트 JSON 구조: API-004 (DiagnosisReportSchema)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/app/admin/diagnoses/[id]/page.tsx` 파일 생성
- [ ] 리드 정보 섹션:
  - 이름, 연락처, 유입경로, 제출일 표시
- [ ] 답변 원문 섹션:
  - 16문항 답변을 질문코드별로 표시
  - 질문 텍스트(QUESTIONS에서 조회) + 답변 원문 나란히 표시
  - 접기/펼치기(Accordion) 또는 전체 표시
- [ ] AI 리포트 섹션:
  - Report.reportJson을 구조화하여 표시
  - summary, strengths[], weaknesses[], brandDirection, recommendedNextStep, warnings 각 영역
  - sourceQuestionCodes를 해당 답변 원문과 연결 표시
- [ ] Report 상태 Badge 표시 (draft/approved/rejected)
- [ ] 목록으로 돌아가기 링크 (`/admin`)
- [ ] 초기 개발 시 MOCK-003 데이터로 렌더링

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 답변 원문 16건 표시**
- Given: `/admin/diagnoses/[id]` 페이지에 접속함
- When: 답변 섹션을 확인함
- Then: 16개 질문에 대한 답변 원문이 질문코드와 함께 표시된다

**Scenario 2: AI 리포트 구조화 표시**
- Given: AI 리포트(reportJson)가 존재함
- When: 리포트 섹션을 확인함
- Then: summary, 강점 목록, 약점 목록, 브랜드 방향, CTA 문구가 구조화되어 표시된다

**Scenario 3: sourceQuestionCodes 표시**
- Given: 리포트 strengths[0].sourceQuestionCodes가 ["Q1", "Q6"]임
- When: 해당 강점 항목을 확인함
- Then: "Q1, Q6" 참조 코드가 표시된다

**Scenario 4: 리드 정보 표시**
- Given: 진단 상세 페이지에 접속함
- When: 리드 정보 영역을 확인함
- Then: 이름, 연락처, 유입경로, 제출일이 표시된다

**Scenario 5: Report 미존재 시 안내**
- Given: AI 리포트가 아직 생성되지 않음 (reportJson이 null)
- When: 리포트 섹션을 확인함
- Then: "리포트가 아직 생성되지 않았습니다" 안내가 표시된다

## :gear: Technical & Non-Functional Constraints
- 동적 라우트: `src/app/admin/diagnoses/[id]/page.tsx`
- QUESTIONS 배열(DATA-001)과 questionCode를 매칭하여 질문 텍스트 표시
- reportJson은 DiagnosisReport 타입(API-004)으로 파싱하여 렌더링
- 이 태스크는 읽기 전용 UI — 수정(FE-003)과 승인(FE-004)은 별도 태스크

## :checkered_flag: Definition of Done (DoD)
- [ ] `/admin/diagnoses/[id]` 경로에서 상세 페이지 정상 렌더링
- [ ] 리드 정보, 답변 원문 16건, AI 리포트 구조화 표시
- [ ] sourceQuestionCodes 표시
- [ ] Report 미존재 시 안내 메시지
- [ ] 목록 페이지 복귀 링크 동작
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** Q-003 (관리자 목록 — 네비게이션), MOCK-003 (초기 개발 데이터), DATA-001 (질문 텍스트 조회), API-004 (리포트 타입)
- **Blocks:** FE-003 (리포트 수정 편집기), FE-004 (승인/거부 버튼)
