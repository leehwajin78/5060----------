---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-002: 진단 답변 유효성 검증 테스트 (3단어 미만/공백 차단)"
labels: 'feature, testing, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [T-002] 진단 답변 유효성 검증 테스트
- 목적: 진단 폼의 16개 답변 필드에 대해 3단어 미만이거나 의미 없는 공백만 입력된 경우 이를 차단하는 비즈니스 규칙이 정상 동작하는지 테스트한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 검증 로직: C-002 (validateDiagnosisInput), API-002 (SubmitDiagnosisInputSchema)
- 요구사항: REQ-FREE-FUNC-004 (답변 품질 방어)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `__tests__/validation/answer.test.ts` 파일 생성
- [ ] Zod 스키마의 `answerText` 검증 단위 테스트 작성:
  - 테스트 케이스 1: 3단어 이상 포함된 정상 문장 (통과)
  - 테스트 케이스 2: 2단어로 구성된 문장 (차단)
  - 테스트 케이스 3: 1단어(예: "없음") (차단)
  - 테스트 케이스 4: 공백만 포함된 문자열 (차단)
  - 테스트 케이스 5: 특수문자만 포함된 문자열 (차단 여부 로직 확인 및 방어)
- [ ] 3단어 계산 로직의 엣지 케이스(연속된 공백, 줄바꿈 포함 등) 테스트

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 3단어 이상 입력**
- Given: "저는 IT 분야 전문가입니다." (단어 4개 추정)
- When: 스키마 검증을 수행함
- Then: `success: true`가 반환된다

**Scenario 2: 2단어 입력 차단**
- Given: "특별히 없음" (단어 2개)
- When: 스키마 검증을 수행함
- Then: `success: false`가 반환되고, "3단어 이상" 에러 메시지가 포함된다

## :gear: Technical & Non-Functional Constraints
- 테스트 프레임워크: Vitest
- 단어 수(Word count) 측정 로직(일반적으로 `trim().split(/\s+/).length`)이 한글 조사/띄어쓰기 패턴에서 의도대로 동작하는지 검증하는 것이 핵심.

## :checkered_flag: Definition of Done (DoD)
- [ ] `answer.test.ts` 작성 완료
- [ ] 모든 테스트 케이스 Pass
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** API-002 (스키마 - refine 로직)
- **Blocks:** None
