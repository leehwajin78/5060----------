---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-014: 재생성 횟수 제한(비용 방어) 로직 단위/통합 테스트"
labels: 'feature, testing, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [T-014] 재생성 횟수 제한 방어 테스트
- 목적: `regenerateReport`(C-010) 실행 시, 1진단 당 AI 호출 횟수(최초 1회 + 재생성 1회 = 총 2회) 제한 룰이 올바르게 작동하여 초과 호출(비용 증가)을 방어하는지 검증한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: C-010 (`regenerateReport`), Q-009 (`getAiRunCount`)
- 요구사항: REQ-NF-FREE-023

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `__tests__/integration/regenerate-limit.test.ts` 파일 생성
- [ ] Prisma `aiRun.count` 모킹 설정
- [ ] `regenerateReport` 테스트 케이스 작성:
  - 카운트가 1일 때: 통과 및 새로운 리포트 생성(또는 `generateDiagnosisReport` 호출) 검증
  - 카운트가 2(또는 그 이상)일 때: `success: false` 반환 및 `RATE_LIMIT_EXCEEDED` 에러 코드 반환 확인, `generateDiagnosisReport`가 호출되지 않음 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 재생성 허용 횟수 이내 호출**
- Given: 기존 AiRun 기록이 1건 존재하는 상황
- When: `regenerateReport`를 호출함
- Then: 로직이 차단되지 않고 AI 생성 프로세스가 실행된다

**Scenario 2: 재생성 허용 횟수 초과 차단**
- Given: 기존 AiRun 기록이 2건 이상 존재하는 상황
- When: `regenerateReport`를 호출함
- Then: 로직이 차단되며 `RATE_LIMIT_EXCEEDED` 에러가 반환된다

## :gear: Technical & Non-Functional Constraints
- 비용 최적화(Zero-cost) MVP의 NFR을 방어하는 핵심 로직.

## :checkered_flag: Definition of Done (DoD)
- [ ] 횟수 제한 초과 차단 통합 테스트 작성 및 Pass
- [ ] 허용 횟수 이내 진행 통과 테스트 작성 및 Pass
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** C-010
- **Blocks:** None
