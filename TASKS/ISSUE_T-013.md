---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-013: 비동기 AI 생성 아키텍처 및 타임아웃 검증 (Vercel 호환)"
labels: 'feature, testing, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [T-013] Vercel 타임아웃/Edge 대비 테스트
- 목적: `submitDiagnosis`(C-003)이 10초 룰(Vercel Hobby Tier 제약)을 위반하지 않도록, AI 리포트 생성(`generateDiagnosisReport`)이 논블로킹(백그라운드)으로 트리거되는 구조인지 검증한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: C-003, C-005
- 요구사항: REQ-NF-FREE-010 (Vercel Serverless Function 10초 타임아웃 회피)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `__tests__/architecture/async-ai-trigger.test.ts` 파일 생성
- [ ] `submitDiagnosis` 테스트 내에서 `generateDiagnosisReport` 함수 Mocking:
  - `generateDiagnosisReport` 호출을 지연(Delay)시키도록 모킹함 (예: 5초 대기)
- [ ] 타이머 검증 (Vitest의 `vi.useFakeTimers()` 활용):
  - `submitDiagnosis` 함수 호출이 5초를 다 기다리지 않고, DB 저장 후 즉시 반환(Resolve)되는지 확인한다.
  - 즉, 백그라운드 Promise가 `await` 되지 않았음을 구조적으로 증명한다.

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: AI 호출 논블로킹 작동 확인**
- Given: AI 생성 함수가 의도적으로 오래 걸리게 Mocking됨
- When: `submitDiagnosis`를 호출함
- Then: DB 저장이 끝난 직후 빠른 시간(수 밀리초 내)에 반환 응답을 받는다

**Scenario 2: Fire and Forget 에러 핸들링**
- Given: AI 생성 백그라운드 작업이 에러를 발생시킴
- When: `submitDiagnosis`를 호출함
- Then: 제출 자체는 성공 응답(`success: true`)을 유지하며, Unhandled Promise Rejection이 서버를 크래시 내지 않아야 한다 (catch 블록이 바인딩 되어 있어야 함)

## :gear: Technical & Non-Functional Constraints
- 아키텍처 상 매우 중요한 NFR 방어선이다. Serverless 환경에서 Fire-and-forget 패턴이 Next.js 최신 버전(App Router)에서 완벽히 백그라운드 실행을 보장하는지 `after()` API(Next.js 15) 사용 여부도 검토/테스트한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 비동기 트리거 테스트 작성 및 Pass
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** C-003
- **Blocks:** Vercel 배포 시 NFR 확보
