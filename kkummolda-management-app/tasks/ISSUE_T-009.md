---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-009: 관리자 리포트 수정 및 감사 로깅(ReviewLog) 단위/통합 테스트"
labels: 'feature, testing, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [T-009] 관리자 리포트 수정 및 감사 로깅(ReviewLog) 테스트
- 목적: `modifyReport`(C-007) 실행 시 Zod 재검증이 작동하여 잘못된 수정을 막아내는지, 그리고 정상 수정 시 Report 업데이트와 함께 `ReviewLog`에 `beforeJson` 및 `afterJson`이 정확히 기록되는지 트랜잭션의 동작을 확인한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: C-007 (`modifyReport`)
- 스키마: API-004 (`DiagnosisReportSchema`)
- 요구사항: REQ-FREE-FUNC-032

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `__tests__/integration/report-modify.test.ts` 파일 생성
- [ ] Prisma Mock 설정 및 `DiagnosisReportSchema` 임포트
- [ ] `modifyReport` 테스트 시나리오 구현:
  - 수정된 JSON이 Zod를 통과하는 경우: 트랜잭션 성공 및 `ReviewLog.create` 호출 인자 확인
  - 수정된 JSON이 Zod 스키마에 어긋난 경우: 에러 반환 및 DB 업데이트가 일어났는지(안 일어났는지) 여부 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: Zod 비준수 수정 시도 차단**
- Given: 관리자가 `summary` 항목을 제거한 리포트 JSON
- When: `modifyReport` 실행
- Then: 트랜잭션(DB 조작)이 실행되지 않고 `success: false`가 반환된다

**Scenario 2: 정상 수정 시 ReviewLog 생성**
- Given: 올바르게 수정된 리포트 JSON 데이터와 `reviewNote`
- When: `modifyReport` 실행
- Then: `ReviewLog.create`가 `action: "modify"`, `beforeJson`, `afterJson`을 포함하여 호출됨을 확인한다

## :gear: Technical & Non-Functional Constraints
- 트랜잭션 내부에서 생성되는 감사 기록은 원자성을 가지며, Zod 검증을 통과한 데이터만 DB에 적재되는지 재차 확인하는 방어적 테스트다.

## :checkered_flag: Definition of Done (DoD)
- [ ] Zod 재검증 테스트 작성
- [ ] ReviewLog 생성 매핑 확인 테스트 작성
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** C-007
- **Blocks:** None
