---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] Q-003: 관리자 진단 목록 조회 UI (/admin)"
labels: 'feature, frontend, admin, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [Q-003] 관리자 진단 목록 조회 UI (/admin)
- 목적: 관리자가 제출된 진단 목록을 최신순으로 확인할 수 있는 `/admin` 페이지를 구현한다. 각 항목에 리드명, 제출일, 리포트 상태를 표시하고 상세 페이지로 이동하는 링크를 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§4.1 F3-Lite`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — REQ-FREE-FUNC-030
- AI 코딩 Prompt 4: SRS Appendix D Lines 759~776
- Mock 데이터: MOCK-003 (mockDiagnosisList)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/app/admin/page.tsx` 파일 생성
- [ ] 진단 목록 테이블/카드 구현:
  - 리드 이름 (leadName)
  - 리드 연락처 (leadContact)
  - 제출일 (createdAt — 한국 시간 포맷)
  - Diagnosis 상태 (status — Badge 컴포넌트)
  - Report 상태 (reportStatus — 색상 구분 Badge)
  - 상세 보기 링크 → `/admin/diagnoses/[id]`
- [ ] 최신순 정렬 (createdAt 역순)
- [ ] 상태별 Badge 색상 분기:
  - draft → 회색, approved → 녹색, rejected → 빨간색, regeneration_requested → 노란색
- [ ] 빈 목록 시 "제출된 진단이 없습니다" 안내 메시지
- [ ] shadcn/ui Table, Badge, Button 활용
- [ ] 초기 개발 시 MOCK-003 데이터로 렌더링 (DB 연동은 Q-006에서)

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 진단 목록 표시**
- Given: `/admin` 페이지에 접속함
- When: 진단 데이터가 존재함
- Then: 리드명, 제출일, 상태가 포함된 목록이 최신순으로 표시된다

**Scenario 2: 상세 페이지 이동**
- Given: 진단 목록 항목이 표시됨
- When: 특정 항목의 상세 보기를 클릭함
- Then: `/admin/diagnoses/[id]` 페이지로 이동한다

**Scenario 3: 상태 Badge 색상 분기**
- Given: 다양한 reportStatus를 가진 진단 항목들이 표시됨
- When: Badge를 확인함
- Then: draft(회색), approved(녹색), rejected(빨간색)이 각각 다른 색상으로 표시된다

**Scenario 4: 빈 목록 안내**
- Given: 제출된 진단이 0건임
- When: `/admin` 페이지에 접속함
- Then: "제출된 진단이 없습니다" 메시지가 표시된다

## :gear: Technical & Non-Functional Constraints
- 관리자 인증 가드(FE-007)가 별도 적용 — 이 태스크는 UI만 구현
- 초기에는 MOCK-003 데이터로 개발, 이후 Q-006(조회 로직)과 연동
- Server Component로 구현 가능 (데이터 fetch는 서버 측)

## :checkered_flag: Definition of Done (DoD)
- [ ] `/admin` 경로에서 진단 목록 정상 렌더링
- [ ] 리드명, 제출일, 상태 Badge 표시
- [ ] 최신순 정렬
- [ ] 상세 보기 링크 동작
- [ ] 빈 목록 안내 메시지
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** INF-001 (shadcn/ui), MOCK-003 (초기 개발용), DB-002/003/005 (DB 연동 시)
- **Blocks:** Q-004 (관리자 상세 UI), Q-006 (DB 연동 조회 로직)
