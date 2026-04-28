---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-004: Answer 16건 저장 트랜잭션 단위 테스트"
labels: 'feature, testing, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [T-004] Answer 16건 저장 트랜잭션 단위 테스트
- 목적: `submitDiagnosis` Server Action 내에서 핵심 데이터 무결성 요건인 "Lead + Diagnosis + Answer(정확히 16건) 원자적 저장"이 `prisma.$transaction`을 통해 제대로 묶여 있는지 검증한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: C-003 (`submitDiagnosis`)
- 요구사항: REQ-FREE-FUNC-011 (16개 답변 모두 저장)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `__tests__/integration/diagnosis.transaction.test.ts` 파일 생성
- [ ] Prisma Mocking 설정 (`$transaction` Mocking 포함)
- [ ] `submitDiagnosis` 호출 테스트:
  - Mock 트랜잭션 콜백이 실행되는지 확인
  - `tx.lead.create`, `tx.diagnosis.create`, `tx.answer.createMany`가 모두 호출되는지 확인
  - `createMany`에 전달된 데이터의 배열 길이가 정확히 16인지 검증
- [ ] 부분 실패 시나리오 테스트 (예: `answer.createMany`에서 에러 발생 시 전체 액션이 `success: false` 반환하는지)

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 16건 트랜잭션 성공**
- Given: 16개 질문이 모두 포함된 정상 입력 데이터
- When: `submitDiagnosis`를 호출함
- Then: 트랜잭션 내에서 `createMany`가 length 16인 배열을 인자로 호출된다

**Scenario 2: 트랜잭션 원자성 유지**
- Given: `answer.createMany` Mock이 강제로 에러를 던짐
- When: `submitDiagnosis`를 호출함
- Then: 에러를 catch하여 `success: false`를 반환하며 예외가 터져 애플리케이션이 죽지 않는다

## :gear: Technical & Non-Functional Constraints
- `prisma.$transaction`을 Mocking하는 것은 까다로울 수 있으므로, Mock 프레임워크 문서(vitest-mock-extended)를 참조하여 콜백을 직접 실행해주는 방식으로 구현한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 트랜잭션 로직 테스트 케이스 작성 완료
- [ ] 모든 테스트 Pass
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** C-003 (트랜잭션 로직)
- **Blocks:** None
