---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-006: AI 실패 상태 전이 통합 테스트 (report_pending)"
labels: 'feature, testing, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [T-006] AI 실패 상태 전이 통합 테스트
- 목적: `generateDiagnosisReport`(C-005) 실행 중 Gemini API 호출이 실패하거나 예외가 발생했을 때, `Diagnosis` 상태가 `report_pending`으로 올바르게 전이되고, 답변 데이터가 보존되며, `AiRun`에 실패 로그가 기록되는지 검증한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: C-005, C-006 (`generateDiagnosisReport`, `handleAiFailure`)
- 요구사항: REQ-FREE-FUNC-022 (AI 실패 시 답변 보존 및 상태 기록)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `__tests__/integration/ai-report.failure.test.ts` 파일 생성
- [ ] Gemini API 클라이언트 Mocking (강제로 예외 발생시키기)
- [ ] Prisma Mocking 설정
- [ ] `generateDiagnosisReport` 호출 테스트 케이스:
  - Gemini API에서 Timeout 에러 모사
  - `prisma.diagnosis.update`가 `status: "report_pending"`으로 호출되는지 검증
  - `prisma.aiRun.update`가 `status: "failed"`와 함께 에러 메시지를 기록하는지 검증
  - (중요) `prisma.answer.delete`나 트랜잭션 롤백에 의해 답변이 삭제되는 로직이 호출되지 않음을 검증

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: AI 실패 시 상태 전이**
- Given: Gemini API가 에러를 던지도록 설정된 환경
- When: `generateDiagnosisReport`를 호출함
- Then: `Diagnosis` 업데이트 쿼리에 `status: "report_pending"` 파라미터가 전달됨을 확인한다

**Scenario 2: AiRun 실패 기록**
- Given: 동일한 에러 환경
- When: `generateDiagnosisReport` 호출
- Then: `AiRun` 업데이트 쿼리에 `status: "failed"`와 해당 에러 메시지가 포함됨을 확인한다

## :gear: Technical & Non-Functional Constraints
- 외부 API 호출은 철저히 Mocking하여 실제 과금이나 네트워크 지연이 테스트에 영향을 주지 않도록 한다.
- `vitest`의 `vi.mock`을 활용해 `@google/generative-ai` 모듈을 모킹한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] AI 실패 시나리오 테스트 작성
- [ ] 모킹을 통한 외부 의존성 분리 확인
- [ ] 모든 테스트 Pass
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** C-005, C-006
- **Blocks:** None
