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
- [ ] `src/lib/utils/logger.ts` 유틸리티 생성 (단순 `console` 래퍼):
  ```typescript
  export const logger = {
    info: (message: string, meta?: any) => console.log(JSON.stringify({ level: 'INFO', message, ...meta })),
    error: (message: string, error?: any, meta?: any) => console.error(JSON.stringify({ level: 'ERROR', message, error, ...meta })),
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
- Then: 서버 콘솔에 JSON 형태의 INFO 레벨 로그가 2회(시작, 완료) 찍힌다.

**Scenario 2: 에러 시 로깅**
- Given: Gemini API가 타임아웃됨
- When: catch 블록으로 진입함
- Then: 서버 콘솔에 JSON 형태의 ERROR 레벨 로그가 에러 객체와 함께 찍힌다.

## :gear: Technical & Non-Functional Constraints
- Vercel의 로그 뷰어에서 JSON 형태를 자동으로 파싱하여 보여주므로 `JSON.stringify` 기반 출력이 모니터링에 매우 유리하다.

## :checkered_flag: Definition of Done (DoD)
- [ ] logger 유틸리티 작성 및 C-005, C-006 적용
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** C-005, C-006
- **Blocks:** None
