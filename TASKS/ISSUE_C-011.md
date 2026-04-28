---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] C-011: CTA 클릭 이벤트 추적을 위한 데이터/로직"
labels: 'feature, backend, command, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [C-011] CTA 클릭 이벤트 추적 로직 (선택적)
- 목적: 고객이 리포트 웹뷰(Q-005) 하단의 CTA 버튼을 클릭했을 때 클릭 이벤트를 기록하여, 진단 서비스의 최종 전환율(Conversion Rate)을 측정할 수 있는 기반을 제공한다. MVP-Free에서는 DB 스키마 확장을 최소화하기 위해 외부 툴(Google Analytics) 권장.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: REQ-FREE-FUNC-041 (CTA 제공)
- (DB 스키마에 이벤트 추적 테이블이 없으므로, V1.5 백로그로 넘기거나 GA 연동으로 대체)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] FE-006 (CTA 버튼 컴포넌트)에 `onClick` 이벤트 핸들러 추가
- [ ] MVP-Free 대안: `window.gtag` (Google Analytics) 호출 또는 서버 측 로그 기록
- [ ] (필요시) 별도의 Server Action으로 로그만 남김:
  ```typescript
  "use server"
  export async function logCtaClick(reportId: string, leadId: string) {
    console.log(`[CTA_CLICK] reportId=${reportId}, leadId=${leadId}`);
    // MVP-Free에서는 별도 DB 테이블 없이 서버 로그로 기록
  }
  ```

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: CTA 클릭 시 로그 기록**
- Given: 리포트 뷰의 CTA 버튼
- When: 사용자가 클릭함
- Then: 서버(또는 GA)에 클릭 이벤트가 기록된다

## :gear: Technical & Non-Functional Constraints
- DB 확장(Event 테이블 추가)을 지양하고, 시스템 복잡도를 낮추기 위해 서버 로그(stdout)나 프론트엔드 분석 툴(GA, Mixpanel 등) 활용 권장.

## :checkered_flag: Definition of Done (DoD)
- [ ] `logCtaClick` Server Action 구현 (로그 전용)
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** Q-005 (리포트 뷰)
- **Blocks:** FE-006 (CTA 컴포넌트)
