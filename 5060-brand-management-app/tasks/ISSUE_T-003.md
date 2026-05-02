---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-003: Lead 생성 Server Action 통합 테스트"
labels: 'feature, testing, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [T-003] Lead 생성 Server Action 통합 테스트
- 목적: `createLead` Server Action이 유효한 입력값을 받았을 때 실제로 DB(Prisma)에 데이터를 저장하고 성공 결과를 반환하는지 통합 환경에서 검증한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: C-001 (`createLead` Server Action)
- DB 모델: DB-002 (Lead)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `__tests__/integration/lead.action.test.ts` 파일 생성
- [ ] Prisma Mocking (또는 테스트 전용 DB 환경 설정 - MVP-Free에서는 속도 향상을 위해 `vitest-mock-extended` 기반 Prisma Mocking 권장)
- [ ] `createLead` 함수 테스트 케이스:
  - 정상적인 데이터로 호출 시 `success: true`와 `leadId` 반환, Prisma `create` 호출 확인
  - 비정상 데이터(이름 누락 등) 호출 시 `success: false` 반환, Prisma `create` 미호출 확인
  - Prisma 에러 발생 시 `success: false` 및 graceful 한 에러 메시지 반환 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: Lead 저장 성공**
- Given: Mock된 Prisma Client와 정상 입력 데이터
- When: `createLead`를 호출함
- Then: `prisma.lead.create`가 1회 호출되고, 반환값에 `success: true`가 포함된다

**Scenario 2: DB 저장 실패 시 예외 처리**
- Given: `prisma.lead.create`가 에러를 던지도록 Mocking됨
- When: `createLead`를 호출함
- Then: `success: false`와 함께 "저장에 실패했습니다" 등의 일반 에러 메시지가 반환된다

## :gear: Technical & Non-Functional Constraints
- 테스트 실행 시 실제 DB에 데이터를 넣지 않고 Mocking을 활용하여 순수 비즈니스 로직(검증 -> 저장 호출 -> 응답)만 빠르게 검증.
- `vitest-mock-extended` 라이브러리 사용 권장.

## :checkered_flag: Definition of Done (DoD)
- [ ] Prisma Mock 환경 구성
- [ ] 통합 테스트 코드 작성 및 Pass
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** C-001 (액션 로직), 인프라(테스트 환경 설정)
- **Blocks:** None
