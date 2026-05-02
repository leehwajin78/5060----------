---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] INF-006: Vercel Web Analytics 연동"
labels: 'feature, infrastructure, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [INF-006] Vercel Web Analytics 연동
- 목적: 랜딩페이지 트래픽, 진단 폼 전환율 등 애플리케이션의 기본적인 사용량과 퍼포먼스를 측정하기 위해 Vercel에서 기본 제공하는 Analytics 모듈을 연동한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: `src/app/layout.tsx`
- 요구사항: REQ-NF-FREE-010 (Vercel 배포 시너지 활용)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `@vercel/analytics` 패키지 설치
- [ ] 루트 레이아웃(`src/app/layout.tsx`) 최상단 렌더링 트리에 `<Analytics />` 컴포넌트 추가:
  ```tsx
  import { Analytics } from '@vercel/analytics/react'

  export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
      <html lang="ko">
        <body>
          {children}
          <Analytics />
        </body>
      </html>
    )
  }
  ```
- [ ] `track()` 함수 유틸리티 활용 (C-011 참조):
  - CTA 버튼 클릭(`cta_click`), 진단 시작(`diagnosis_start`) 등 핵심 퍼널 이벤트를 트래킹할 수 있도록 Vercel Analytics `track` API를 사전에 테스트한다.
  - Vercel Dashboard의 'Analytics' 탭에서 활성화(Enable) 처리가 필요함을 README 등에 명시한다.

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: Analytics 컴포넌트 렌더링 및 페이지 뷰 기록**
- Given: Vercel에 배포된 프로덕션 환경의 URL에 접속함
- When: 웹 페이지 로딩이 완료됨
- Then: 브라우저 Network 탭에서 Vercel Analytics 모듈 스크립트가 로드되며, Vercel 대시보드에 Page View 트래픽이 기록되기 시작한다.

**Scenario 2: 개발 환경에서의 Analytics 비활성화**
- Given: 개발자 로컬 환경(`NODE_ENV="development"`)
- When: 애플리케이션을 실행하고 페이지에 접속함
- Then: Vercel Analytics 컴포넌트는 무시되거나 Mocking 처리되어, 로컬에서 발생하는 불필요한 트래픽이 대시보드에 혼선을 주지 않는다.

## :gear: Technical & Non-Functional Constraints
- 구글 애널리틱스(GA)를 대체할 수 있는 가장 가볍고 무료(Vercel Hobby Tier 내장)인 트래픽 분석 솔루션이다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `<Analytics />` 루트 레이아웃 추가
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** Vercel 배포 (INF-002)
- **Blocks:** None
