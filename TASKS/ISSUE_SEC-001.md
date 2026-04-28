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
- [ ] ESLint 플러그인 설정 강화 (`eslint-plugin-security` 등 필요 시 추가)
- [ ] Husky 및 lint-staged 설정 (선택 사항, 커밋 전 테스트 실행 강제화)
- [ ] (선택) `src/lib/services/ai-payload.service.ts`의 `select` 구문에 대하여 Prisma-level type 제한을 명시적으로 주는 JSDoc / Type definition 강화
  - *개발 과정에서 코파일럿이나 AI 에이전트가 실수로 `include: { lead: true }`를 쓰지 못하도록 주석을 강력히 달고 스키마 단위에서 방어*

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: Lint / Build 시 에러 미발생**
- Given: 설정된 ESLint 룰
- When: `npm run lint` 실행
- Then: 에러 0건으로 통과한다

**Scenario 2: (옵션) 커밋 전 단위 테스트 실행 (Husky)**
- Given: Husky pre-commit 훅
- When: 코드를 커밋함
- Then: `npm run test:unit` (또는 해당 T-007 등의 보안 테스트)이 실행되어 실패 시 커밋을 차단한다

## :gear: Technical & Non-Functional Constraints
- Vibe-coding 시 AI가 멋대로 불필요한 데이터를 조회하는 것을 막는 것이 핵심이므로, 해당 함수(`buildAiPayload`) 주변에 명확한 Instruction 주석을 다는 것도 이 태스크에 포함된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 정적 분석 룰 (린트) 검토/강화
- [ ] 보안 관련 코드 주석(Instruction) 작성
- [ ] `npm run lint` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** INF-001
- **Blocks:** None
