---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-007: AI Payload 구성 PII(개인정보) 마스킹 단위 테스트"
labels: 'feature, testing, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [T-007] AI Payload 구성 PII 마스킹 단위 테스트
- 목적: `buildAiPayload`(C-004) 함수가 DB에서 데이터를 추출하여 AI 서비스로 전달하기 위한 Payload를 만들 때, 이름, 전화번호, 이메일 등의 PII(개인 식별 정보)가 포함되지 않음을 강력하게 보장하는 테스트를 작성한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: C-004 (`buildAiPayload`)
- 요구사항: REQ-NF-FREE-030 (AI API PII 마스킹)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `__tests__/unit/ai-payload.test.ts` 파일 생성
- [ ] Prisma `findMany` 모킹:
  - Lead 정보가 섞여 있더라도 (물론 C-004 설계상 select 하지 않지만, 모의 데이터에는 포함시켜봄) 반환되는 최종 Payload 객체에는 존재하지 않음을 확인.
- [ ] 반환된 Payload 객체 순회 검증:
  - `JSON.stringify` 결과나 객체 트리에 `name`, `contact`, `email`, `phone` 키가 존재하는지 재귀적으로 검사.
- [ ] Answer가 16건 미만일 때 null을 반환하는지 테스트.

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: PII 완전 배제 확인**
- Given: Mock DB에서 16건의 답변 데이터를 반환함
- When: `buildAiPayload` 실행
- Then: 반환된 Payload의 어떤 깊이에도 `name`이나 `contact` 등 민감 정보의 키값이 존재하지 않는다

**Scenario 2: 데이터 무결성 검증 (16건 미만)**
- Given: Mock DB가 15건의 답변만 반환함
- When: `buildAiPayload` 실행
- Then: `null`이 반환된다

## :gear: Technical & Non-Functional Constraints
- 보안과 직결되는 핵심 테스트이므로, 속성 이름(Keys) 검증을 엄격하게 수행한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] Payload PII 검증 테스트 작성
- [ ] 16건 미만 방어 테스트 작성
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** C-004
- **Blocks:** 배포 전 보안 검수
