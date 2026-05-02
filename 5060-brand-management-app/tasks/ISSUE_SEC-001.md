---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] SEC-001: 정적 분석(ESLint/Husky) 및 PII 마스킹 강제화 규칙 설정"
labels: 'feature, security, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [SEC-001] 정적 분석 및 PII 마스킹 강제화 설정
- 목적: `buildAiPayload`와 같은 핵심 보안 구간에서 Lead 정보(name, contact 등)를 실수로 조회(select)하지 않도록 정적 분석 룰과 린트(ESLint) 구성을 최적화하여 1인 개발/vibe-coding 과정의 휴먼 에러를 방지한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: 루트 디렉토리 설정 파일들 (`.eslintrc.json`, `package.json`)
- 요구사항: REQ-NF-FREE-030, REQ-NF-FREE-031
- 테스트: T-007

## :white_check_mark: Task Breakdown (실행 계획)

### 제거 대상

| 대상 | 예시 | 처리 |
|---|---|---|
| 이메일 | test@example.com | `[EMAIL_REMOVED]` |
| 전화번호 | 010-1234-5678 | `[PHONE_REMOVED]` |
| lead.name | 홍길동 | payload에 포함 금지 |
| lead.contact | 이메일/전화번호 | payload에 포함 금지 |

### 처리 기준

- AI payload에는 questionCode와 answerText만 포함한다.
- leadInfo 전체 객체는 AI payload에 포함하지 않는다.
- answerText 내부에 이메일/전화번호가 포함된 경우 정규식으로 마스킹한다.

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: AI Payload 익명화 및 필터링**
- Given: 이름, 연락처가 포함된 Lead 정보와 이메일 주소가 기재된 Answer 데이터
- When: `buildAiPayload`를 실행함
- Then: payload 스냅샷에 name/contact 필드가 전혀 포함되지 않으며, Answer 내부의 이메일이나 전화번호 텍스트는 마스킹 처리되어 반환됨.

## :gear: Technical & Non-Functional Constraints
- Vibe-coding 시 AI가 멋대로 불필요한 데이터를 조회하는 것을 막는 것이 핵심이므로, 해당 함수(`buildAiPayload`) 주변에 명확한 Instruction 주석을 다는 것도 이 태스크에 포함된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 정적 분석 룰 (린트) 검토/강화
- [ ] 보안 관련 코드 주석(Instruction) 작성
- [ ] `npm run lint` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** INF-001
- **Blocks:** None
