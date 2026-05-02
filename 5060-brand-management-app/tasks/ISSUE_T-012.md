---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-012: 리포트 하단 상담 CTA 렌더링 및 URL 주입 테스트"
labels: 'feature, testing, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [T-012] 상담 CTA 동작 테스트
- 목적: 승인 리포트 하단에 노출되는 CTA 버튼(FE-006)이 환경변수(구글 폼 URL 등)를 올바르게 읽어들여 렌더링되는지 확인한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: FE-006 (`ReportCTA` 컴포넌트)
- 요구사항: REQ-FREE-FUNC-041

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `__tests__/components/ReportCTA.test.tsx` 파일 생성 (React Testing Library 활용)
- [ ] `process.env.NEXT_PUBLIC_CTA_LINK` 환경변수 Mocking
- [ ] 렌더링 검증:
  - 지정한 환경변수에 맞게 버튼 라벨이 표시되는지 확인
  - 컴포넌트의 클릭 이벤트 핸들러가 정상 바인딩되었는지 확인
- [ ] `logCtaClick`(C-011) Mocking 및 호출 여부 검증 (선택적)

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: CTA 컴포넌트 정상 렌더링**
- Given: CTA_LABEL 환경변수가 "무료 상담 신청"으로 세팅됨
- When: `<ReportCTA />`를 렌더링함
- Then: 화면에 "무료 상담 신청"이라는 텍스트를 가진 버튼이 존재한다

**Scenario 2: 환경변수 누락 대비 방어 코드**
- Given: 환경변수가 세팅되지 않음
- When: `<ReportCTA />`를 렌더링함
- Then: 디폴트 라벨("상담 신청하기")로 버튼이 렌더링된다

## :gear: Technical & Non-Functional Constraints
- 프론트엔드 UI 컴포넌트 단위 테스트이므로 `vitest`와 `testing-library/react`를 사용한다.
- `window.open` 같은 브라우저 전용 API 호출 여부를 Mocking하여 테스트할 수 있다.

## :checkered_flag: Definition of Done (DoD)
- [ ] CTA 컴포넌트 렌더링 단위 테스트 작성 및 Pass
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** FE-006
- **Blocks:** None
