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
- [ ] MVP-Free 대안: `window.gtag` (Google Analytics) 또는 Vercel Analytics (`track` 함수) 호출
- [ ] Adblocker 등 브라우저 환경에서 트래커가 차단될 수 있으므로, 에러 없이 안전하게 실행되는 래퍼(Wrapper) 함수 작성:
  ```typescript
  export function trackCtaClick(reportId: string) {
    try {
      // 1. Vercel Analytics (기본 내장 우선)
      if (typeof window !== "undefined" && (window as any).va) {
        (window as any).va('track', 'cta_click', { reportId });
      }
      // 2. Google Analytics (설정 시)
      if (typeof window !== "undefined" && typeof (window as any).gtag === "function") {
        (window as any).gtag('event', 'cta_click', { 'report_id': reportId });
      }
    } catch (e) {
      console.warn('Analytics tracking blocked or failed', e);
    }
  }
  ```
- [ ] (필요시) V1.5 이상에서 자체 DB 기록이 필요한 경우 별도의 Server Action으로 확장할 수 있도록 구조 유지.

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: CTA 클릭 시 이벤트 발송**
- Given: 리포트 뷰의 CTA 버튼이 렌더링됨
- When: 사용자가 CTA 버튼을 클릭함
- Then: `trackCtaClick` 유틸리티가 호출되어 브라우저의 Network 탭에 analytics 관련 요청이 전송된다.

**Scenario 2: Adblocker 동작 시 방어 로직 (안정성)**
- Given: 사용자의 브라우저에 광고/트래커 차단 익스텐션이 켜져 있음
- When: 사용자가 CTA 버튼을 클릭함
- Then: 브라우저 환경에서 `window.va` 또는 `window.gtag`가 없거나 실패하더라도 애플리케이션 에러를 발생시키지 않고 조용히 실패(Soft fail)한다.

## :gear: Technical & Non-Functional Constraints
- DB 확장(Event 테이블 추가)을 지양하고, 시스템 복잡도를 낮추기 위해 서버 로그(stdout)나 프론트엔드 분석 툴(GA, Mixpanel 등) 활용 권장.

## :checkered_flag: Definition of Done (DoD)
- [ ] `logCtaClick` Server Action 구현 (로그 전용)
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** Q-005 (리포트 뷰)
- **Blocks:** FE-006 (CTA 컴포넌트)
