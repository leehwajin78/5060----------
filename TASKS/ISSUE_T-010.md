---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-010: 리포트 승인/거부 상태 전이(State Transition) 테스트"
labels: 'feature, testing, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [T-010] 리포트 승인/거부 상태 전이 테스트
- 목적: `reviewReportStatus`(C-008) 실행 시, `Report`의 상태와 연관된 `Diagnosis`의 상태가 정책(승인 시 -> `APPROVED` & `REVIEWED`, 거부 시 -> `REJECTED` & `REPORT_GENERATED`)에 맞게 전이되는지 검증한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: C-008 (`reviewReportStatus`)
- 상태 상수: DATA-002 (`DiagnosisStatus`), DATA-003 (`ReportStatus`)
- 요구사항: REQ-FREE-FUNC-033

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `__tests__/integration/report-status.test.ts` 파일 생성
- [ ] `reviewReportStatus` 액션의 `approve` 시나리오 테스트:
  - `action: "approve"` 입력 시
  - `Report`가 `ReportStatus.APPROVED`로, `Diagnosis`가 `DiagnosisStatus.REVIEWED`로 업데이트되는지 확인
- [ ] `reviewReportStatus` 액션의 `reject` 시나리오 테스트:
  - `action: "reject"` 입력 시
  - `Report`가 `ReportStatus.REJECTED`로, `Diagnosis`가 `DiagnosisStatus.REPORT_GENERATED`로 업데이트되는지 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 승인(Approve) 시 상태 전이**
- Given: 대기 중인 리포트
- When: 관리자가 `approve` 액션을 실행함
- Then: DB(또는 Mock DB)에 `Report`는 `approved`, `Diagnosis`는 `reviewed` 상태로 업데이트되는 쿼리가 전달된다

**Scenario 2: 거부(Reject) 시 상태 전이**
- Given: 대기 중인 리포트
- When: 관리자가 `reject` 액션을 실행함
- Then: DB(또는 Mock DB)에 `Report`는 `rejected`, `Diagnosis`는 `report_generated` 상태로 업데이트되는 쿼리가 전달된다

## :gear: Technical & Non-Functional Constraints
- 승인 여부는 고객 노출을 결정짓는 핵심 플래그이므로, 오타나 잘못된 상수 매핑이 없는지 엄격히 확인.

## :checkered_flag: Definition of Done (DoD)
- [ ] Approve 상태 전이 테스트 작성
- [ ] Reject 상태 전이 테스트 작성
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** C-008, DATA-002, DATA-003
- **Blocks:** None
