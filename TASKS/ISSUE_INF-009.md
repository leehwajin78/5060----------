---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] INF-009: 반응형 뷰포트(Mobile-First) 및 안전 영역(Safe Area) 설정"
labels: 'feature, infrastructure, ui, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [INF-009] 반응형 뷰포트 및 안전 영역 설정
- 목적: 모바일 웹뷰 환경(카카오톡 인앱 브라우저 등)에서 화면이 깨지거나 잘리지 않도록 뷰포트(Viewport) 메타 태그를 최적화하고, `env(safe-area-inset-*)`를 전역 레이아웃에 적용한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: `src/app/layout.tsx`, `src/app/globals.css`
- 요구사항: REQ-NF-FREE-002 (반응형 웹디자인)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/app/layout.tsx` 내 `viewport` 객체 설정:
  ```typescript
  import { Viewport } from 'next'

  export const viewport: Viewport = {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 1,
    userScalable: false, // 폼 입력 시 줌인 방지 (모바일 최적화)
    viewportFit: 'cover', // 노치(Notch) 대응
  }
  ```
- [ ] `globals.css` 전역 컨테이너에 Safe Area 패딩 적용:
  ```css
  .safe-area-pt { padding-top: env(safe-area-inset-top); }
  .safe-area-pb { padding-bottom: env(safe-area-inset-bottom); }
  ```
- [ ] `globals.css`에 모바일 브라우저의 100vh 문제 해결을 위한 `min-h-[100dvh]`(Dynamic Viewport Height) 속성 활용 보장.

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 모바일 입력 줌 방지**
- Given: 모바일 환경에서 진단 폼(Q-002)의 `input` 필드 포커스
- When: 사용자가 텍스트를 입력하려 함
- Then: 화면이 자동으로 확대(Zoom-in)되지 않고 레이아웃을 유지한다.

**Scenario 2: 노치 및 하단 인디케이터 방어**
- Given: 아이폰 등 노치가 있는 기기
- When: 웹뷰가 렌더링됨
- Then: 콘텐츠가 노치나 하단 홈 인디케이터에 가려지지 않는다.

## :gear: Technical & Non-Functional Constraints
- 고객군(5060)은 카카오톡 브라우저를 통한 유입이 절대 다수이므로, 데스크탑보다 모바일 디스플레이 최적화가 더욱 중요하다.

## :checkered_flag: Definition of Done (DoD)
- [ ] viewport 메타데이터 적용
- [ ] safe-area 및 dvh 전역 클래스(또는 Tailwind 유틸) 추가
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** 전체 Layout 컴포넌트
- **Blocks:** None
