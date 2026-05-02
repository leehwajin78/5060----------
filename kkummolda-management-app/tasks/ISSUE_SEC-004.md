---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] SEC-004: Next.js (Vercel) 웹 보안 헤더 설정 (CSP/XSS 방어)"
labels: 'feature, security, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [SEC-004] 웹 보안 헤더 설정
- 목적: `next.config.mjs`에 강력한 HTTP 보안 헤더(CSP, X-Frame-Options 등)를 주입하여 XSS, Clickjacking 등의 프론트엔드 보안 위협으로부터 애플리케이션을 보호한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: `next.config.mjs`
- 요구사항: REQ-NF-FREE-034 (보안 무결성)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `next.config.mjs` 설정에 `headers()` 함수 추가:
  ```javascript
  const securityHeaders = [
    { key: 'X-DNS-Prefetch-Control', value: 'on' },
    { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
    { key: 'X-Frame-Options', value: 'SAMEORIGIN' }, // Clickjacking 방지
    { key: 'X-Content-Type-Options', value: 'nosniff' },
    { key: 'Referrer-Policy', value: 'origin-when-cross-origin' },
  ];

  /** @type {import('next').NextConfig} */
  const nextConfig = {
    async headers() {
      return [
        {
          source: '/(.*)',
          headers: securityHeaders,
        },
      ];
    },
  };

  export default nextConfig;
  ```
- [ ] (옵션) CSP(Content Security Policy) 헤더 구성은 MVP 개발 단계에서는 인라인 스크립트 에러를 유발할 수 있으므로, V1.5 백로그로 넘기거나 Report 뷰 등 주요 화면에만 적용.

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 보안 헤더 주입 확인**
- Given: Vercel에 배포된 애플리케이션
- When: 개발자 도구의 Network 탭에서 첫 Document 리스폰스 헤더를 확인한다
- Then: `X-Frame-Options: SAMEORIGIN` 및 `X-Content-Type-Options: nosniff` 헤더가 응답에 포함되어 있다.

## :gear: Technical & Non-Functional Constraints
- Vercel Edge 네트워크에서 처리되므로 애플리케이션 성능 저하 없이 강력한 브라우저 레벨 보안을 획득할 수 있다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `next.config.mjs` 보안 헤더 설정 완료
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** 전체 앱
- **Blocks:** 배포 전 보안 검토
