---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] LOG-001: AI 호출 실패/성공 서버 로깅 체계 (stdout)"
labels: 'feature, infrastructure, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [LOG-001] AI 호출 서버 로그 기록
- 목적: 에러 추적 및 Vercel 로그 대시보드 모니터링을 위해, AI 리포트 생성(C-005) 및 에러 핸들링(C-006) 구간에서 구조화된 표준 출력(stdout) 로그를 남긴다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: C-005, C-006 내부
- 요구사항: S12 (로그 확인 기능 - Vercel 로그로 대체)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/utils/logger.ts` 유틸리티 생성 (단순 `console` 래퍼되 직렬화 안전성 보장):
  ```typescript
  export const logger = {
    info: (message: string, meta?: any) => {
      try {
        console.log(JSON.stringify({ level: 'INFO', message, timestamp: new Date().toISOString(), ...meta }));
      } catch (e) {
        console.log(`[INFO] ${message} (meta serialization failed)`);
      }
    },
    error: (message: string, error?: any, meta?: any) => {
      try {
        const errorMsg = error instanceof Error ? error.message : String(error);
        const stack = error instanceof Error ? error.stack : undefined;
        console.error(JSON.stringify({ level: 'ERROR', message, error: errorMsg, stack, timestamp: new Date().toISOString(), ...meta }));
      } catch (e) {
        console.error(`[ERROR] ${message} (serialization failed)`);
      }
    },
  }
  ```
- [ ] `generateDiagnosisReport`(C-005) 내에 `logger.info` 및 `logger.error` 적용:
  - 시작 시: `logger.info('AI Report Generation Started', { diagnosisId })`
  - 완료 시: `logger.info('AI Report Generation Completed', { diagnosisId, aiRunId })`
  - 에러 시: `logger.error('AI Report Generation Failed', error, { diagnosisId })`

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 성공 시 로깅**
- Given: 리포트 생성이 정상적으로 완료됨
- When: C-005가 완료됨
- Then: 서버 콘솔에 JSON 형태의 INFO 레벨 로그가 2회(시작, 완료) 찍힌다. (timestamp 포함)

**Scenario 2: 에러 시 로깅 (Stack Trace 포함)**
- Given: Gemini API가 에러를 던짐 (Error 객체)
- When: catch 블록으로 진입함
- Then: 서버 콘솔에 JSON 형태의 ERROR 레벨 로그가 찍히며, message와 stack 속성을 포함하여 디버깅을 돕는다.

**Scenario 3: 직렬화(Serialization) 실패 방어**
- Given: `meta` 파라미터에 순환 참조(Circular Dependency)를 가진 객체가 전달됨
- When: `logger.info` 또는 `logger.error`가 호출됨
- Then: JSON.stringify 에러로 인해 앱이 다운되지 않고, 안전한 폴백(Fallback) 텍스트가 콘솔에 출력된다.

## :gear: Technical & Non-Functional Constraints
- Vercel의 로그 뷰어에서 JSON 형태를 자동으로 파싱하여 보여주므로 `JSON.stringify` 기반 출력이 모니터링에 매우 유리하다.

## :checkered_flag: Definition of Done (DoD)
- [ ] logger 유틸리티 작성 및 C-005, C-006 적용
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** C-005, C-006
- **Blocks:** None
