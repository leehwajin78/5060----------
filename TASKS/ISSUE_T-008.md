---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-008: 관리자 목록 최신순 정렬 및 데이터 매핑 테스트"
labels: 'feature, testing, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [T-008] 관리자 목록 최신순 정렬 및 데이터 매핑 테스트
- 목적: `getDiagnosisList`(Q-006) 쿼리가 Diagnosis 데이터를 `createdAt` 역순으로 올바르게 가져오는지, Lead 정보와 Report 최신 1건이 올바르게 매핑되어 반환되는지 검증한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: Q-006 (`getDiagnosisList`)
- UI 요구사항: Q-003

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `__tests__/integration/diagnosis-list.query.test.ts` 생성
- [ ] Prisma Mocking 설정:
  - `findMany`가 날짜가 다른 여러 Diagnosis 목 데이터를 반환하도록 설정
  - `include`된 lead와 reports 배열(length 1) 포함
- [ ] 반환된 목록의 정렬 순서가 Mock 데이터의 기대값과 일치하는지 검증
- [ ] Lead의 `name`과 `contact`, Report의 `status`가 정상적으로 접근 가능한지 속성 검증

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 최신순 정렬 검증**
- Given: 날짜가 각기 다른 3개의 목업 Diagnosis 데이터 (가장 최근 것부터 배열)
- When: `getDiagnosisList`를 실행함
- Then: 반환된 배열의 첫 번째 항목이 가장 최근 데이터이다

**Scenario 2: Join 데이터 매핑 확인**
- Given: 목업 데이터에 Lead와 Report 정보가 포함됨
- When: 함수를 실행함
- Then: 각 항목의 `lead.name` 및 `reports[0].status`에 접근이 가능하다

**Scenario 3: 빈 데이터 반환**
- Given: DB에 일치하는 Diagnosis 데이터가 하나도 없음
- When: `getDiagnosisList`를 실행함
- Then: 빈 배열 `[]`이 반환되고 에러가 발생하지 않는다

**Scenario 4: Report가 아직 생성되지 않은 경우 (진행 중 상태)**
- Given: Diagnosis는 있으나 연결된 Report가 없음 (진단 진행 중이거나 실패한 상태)
- When: `getDiagnosisList`를 실행함
- Then: `reports` 배열이 비어있음(`[]`)을 안전하게 처리하여 크래시 없이 리스트를 반환한다

## :gear: Technical & Non-Functional Constraints
- 단순한 쿼리 로직이지만, Prisma의 `include` 및 `take: 1` 설정이 런타임 결과에 어떻게 매핑되는지 타입 시스템 레벨에서 확인하는 목적도 가진다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 정렬 및 매핑 통합 테스트 작성
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** Q-006
- **Blocks:** None
