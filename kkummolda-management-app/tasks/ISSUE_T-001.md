---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-001: 리드 정보 유효성 검증 테스트 (연락처 필수)"
labels: 'feature, testing, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [T-001] 리드 정보 유효성 검증 테스트
- 목적: 진단 폼 제출 시 가장 중요한 리드 정보(이름, 연락처)가 누락되지 않았는지 검증하는 비즈니스 규칙이 정상 동작하는지 테스트 코드로 확인한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 검증 로직: C-002 (validateDiagnosisInput), API-001 (CreateLeadInputSchema)
- 요구사항: REQ-FREE-FUNC-003 (이름+연락처 필수)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `__tests__/validation/lead.test.ts` 파일 생성
- [ ] `CreateLeadInputSchema.safeParse()`를 활용한 단위 테스트 작성:
  - 테스트 케이스 1: 정상적인 이름과 이메일 입력 시 통과
  - 테스트 케이스 2: 정상적인 이름과 전화번호 입력 시 통과
  - 테스트 케이스 3: 이름 누락 시 검증 실패
  - 테스트 케이스 4: 연락처 누락 시 검증 실패
- [ ] Jest 또는 Vitest (Next.js 환경에 맞게 선택, 기본은 Vitest 권장) 환경에서 실행 가능하도록 구성

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 정상 리드 정보 검증**
- Given: `{ name: "김전문", contact: "expert@example.com" }` 객체
- When: 스키마 검증을 수행함
- Then: `success: true`가 반환된다

**Scenario 2: 연락처 누락 검증**
- Given: `{ name: "김전문", contact: "" }` 객체
- When: 스키마 검증을 수행함
- Then: `success: false`가 반환되고 에러 메시지에 연락처 관련 내용이 포함된다

## :gear: Technical & Non-Functional Constraints
- 테스트 프레임워크: Vitest (속도 및 설정 용이성 목적)
- Zod 스키마 단위 테스트이므로 DB 연동(Mocking) 불필요, 순수 함수 테스트로 작성

## :checkered_flag: Definition of Done (DoD)
- [ ] `lead.test.ts` 작성 완료
- [ ] 모든 테스트 케이스 Pass (`npm run test`)
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** API-001 (스키마)
- **Blocks:** None
