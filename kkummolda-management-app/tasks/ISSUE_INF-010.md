---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] INF-010: 접근성(a11y) 린트 규칙 설정 (5060 사용자 경험 강화)"
labels: 'feature, infrastructure, ui, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [INF-010] 접근성(a11y) 린트 규칙 설정
- 목적: 주 사용층이 5060 세대임을 감안하여, 버튼 텍스트의 크기, 대비(Contrast), 스크린 리더용 `aria` 속성 누락 등을 개발 단계에서 자동으로 경고하도록 `eslint-plugin-jsx-a11y`를 구성한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: `.eslintrc.json`
- 요구사항: REQ-NF-FREE-006 (고연령층 배려 UX)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `eslint-plugin-jsx-a11y` 패키지 설치 확인 (Next.js에 기본 내장되어 있으나 엄격도 상향 필요)
- [ ] `.eslintrc.json` 수정:
  ```json
  {
    "extends": [
      "next/core-web-vitals",
      "plugin:jsx-a11y/recommended"
    ],
    "rules": {
      "jsx-a11y/alt-text": "error",
      "jsx-a11y/aria-props": "error",
      "jsx-a11y/role-has-required-aria-props": "error",
      "jsx-a11y/click-events-have-key-events": "warn",
      "jsx-a11y/no-static-element-interactions": "warn"
    }
  }
  ```
- [ ] (선택) 컴포넌트 작성 시 `aria-label` 강제를 위한 Vibe-coding 지침(프롬프트)에 "5060을 위한 시맨틱 마크업" 원칙 명시.

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 접근성 린트 검증**
- Given: `<img src="logo.png" />` (alt 없음) 태그가 있는 코드
- When: `npm run lint` 실행
- Then: `jsx-a11y/alt-text` 에러가 발생하여 빌드/커밋을 경고한다.

## :gear: Technical & Non-Functional Constraints
- 5060 사용자의 브라우저 확대 기능(접근성 모드)이나 스크린 리더기 환경에서 심각한 결함이 발생하지 않도록 돕는 최소한의 개발 가이드레일.

## :checkered_flag: Definition of Done (DoD)
- [ ] a11y 린트 규칙 적용 완료
- [ ] `npm run lint` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** SEC-001 (린트 환경)
- **Blocks:** None
