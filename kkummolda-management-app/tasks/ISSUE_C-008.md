---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] C-008: 관리자 리포트 승인/거부 상태 전이 로직"
labels: 'feature, backend, command, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [C-008] 관리자 리포트 승인/거부 상태 전이 로직
- 목적: 관리자가 리포트를 승인(approved)하거나 거부(rejected)할 때 Report 및 Diagnosis 상태를 업데이트하고, 해당 이력을 ReviewLog(C-009)에 기록하는 로직을 구현한다. 승인 시 리포트가 외부에 공개된다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: REQ-FREE-FUNC-033 (승인/거부 시 상태 전이)
- SRS 시퀀스 2: Lines 331~338 — "상태 변경(approved) → ReviewLog 기록"
- DTO 참조: API-005 (ReviewReportInputSchema — action: "approve" | "reject")
- 상태 상수: DATA-002 (DiagnosisStatus), DATA-003 (ReportStatus)

## :white_check_mark: Task Breakdown (실행 계획)

### 입력

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| reportId | string | Y | 대상 리포트 ID |
| status | enum | Y | approved 또는 rejected |
| reviewNote | string | N | 검수 메모 |

### 상태 전이 규칙

| 현재 상태 | 변경 가능 상태 |
|---|---|
| draft | approved, rejected |
| rejected | approved, regeneration_requested |
| approved | rejected 가능하나 이력 기록 필수 |
| regeneration_requested | draft |

### 처리 절차

1. 관리자 인증 확인
2. Report 조회
3. 변경 가능한 상태인지 검증
4. Report.status 변경
5. ReviewLog 생성
6. 성공 응답 반환

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 상태 전이 및 ReviewLog 기록**
- Given: 적절한 권한을 가진 관리자와 draft 상태의 리포트
- When: 관리자가 승인(approve) 처리함
- Then: Report 상태가 approved로, Diagnosis 상태가 reviewed로 변경되며, beforeJson과 afterJson이 포함된 ReviewLog가 생성됨.

**Scenario 2: 유효하지 않은 상태 전이 시도 방지**
- Given: 이미 approved 상태인 리포트를 draft로 변경하려는 요청
- When: 요청을 실행함
- Then: 허용되지 않은 상태 전이로 거부(400)됨.

## :gear: Technical & Non-Functional Constraints
- 승인(approved) 순간부터 Q-008(승인 리포트 조회 로직)을 통해 고객 웹뷰 노출이 가능해짐 (보안 임계점)
- 상태 전이는 반드시 트랜잭션으로 묶어 Report와 Diagnosis의 상태 불일치를 방지

## :checkered_flag: Definition of Done (DoD)
- [ ] reviewReportStatus() 함수 구현 완료
- [ ] approve/reject 상태 전이 확인
- [ ] 트랜잭션 및 ReviewLog 생성 동작 확인
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** DB-005(Report), DB-003(Diagnosis), DB-007(ReviewLog), API-005(DTO)
- **Blocks:** FE-004(승인/거부 버튼 연동), Q-008(승인 리포트 노출)
