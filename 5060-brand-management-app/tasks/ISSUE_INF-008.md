---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] INF-008: 프리미엄 브랜드 컬러 및 테마 토큰 정의"
labels: 'feature, infrastructure, ui, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [INF-008] 브랜드 테마 시스템 구축
- 목적: 5060 전문가 대상의 '프리미엄, 신뢰감, 여유로움'을 전달할 수 있는 디자인 테마(컬러 패레트, 타이포그래피, 라운딩 등)를 Tailwind CSS 환경설정에 전역 토큰으로 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: `tailwind.config.ts`, `src/app/globals.css`
- 요구사항: O5 (프리미엄 디자인 전략 적용)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `globals.css` 내 CSS 변수(CSS Variables) 정의:
  - `primary`: 신뢰감을 주는 차분한 네이비 또는 고급스러운 딥그린 계열.
  - `secondary`: 우아한 골드 베이지 또는 웜그레이 계열 (보조색).
  - `background`: 완전한 흰색(`#ffffff`) 대신 눈이 편안한 오프화이트(`#fdfdfd` 또는 `#fcfcfc`).
  - `card`, `popover`, `border` 등 shadcn 컴포넌트 변수 매핑 조정.
- [ ] `tailwind.config.ts` 확장(Extend):
  - `colors` 항목에 CSS 변수를 참조하도록 설정.
  - 프리미엄한 느낌을 위한 `boxShadow` 추가 (예: `shadow-premium`: 넓고 부드러운 그림자).
  - 테두리 곡률 `borderRadius` 조정 (너무 둥글지 않은, 세련된 느낌의 `0.3rem` ~ `0.5rem`).

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 테마 토큰 작동 검증**
- Given: `<div className="bg-primary text-primary-foreground">테스트</div>`
- When: 화면에 렌더링됨
- Then: 지정한 프리미엄 컬러(네이비/딥그린 등)로 배경이, 대비되는 텍스트 색상으로 렌더링된다.

**Scenario 2: 다크 모드(선택 사항) 대응**
- Given: (만약 다크모드를 지원한다면) `.dark` 클래스가 최상단에 적용됨
- When: CSS 변수가 전환됨
- Then: 텍스트 가독성이 무너지지 않는 고급스러운 다크 그레이 배경과 조정된 primary 컬러가 나타난다.

## :gear: Technical & Non-Functional Constraints
- "Vibe-coding"의 핵심 중 하나. UI를 처음 보는 순간 사용자가 "WOW" 할 수 있도록 단순하지만 밀도 있는 컬러 코드를 선택한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `globals.css` 컬러 토큰 업데이트
- [ ] `tailwind.config.ts` 테마 연동 완료
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** INF-007 (shadcn 기본 설정)
- **Blocks:** UI 스타일링 세부 작업
