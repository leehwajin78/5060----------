---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] INF-005: 글로벌 에러 핸들링 및 Not Found 화면 (App Router)"
labels: 'feature, infrastructure, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [INF-005] 글로벌 에러 핸들링 및 Not Found 화면
- 목적: 애플리케이션의 어느 곳에서든 예상치 못한 예외가 발생하거나, 존재하지 않는 페이지(라우트) 접근 시 우아하게(graceful) 대처하여 사용자에게 일관된 5060 프리미엄 브랜드의 톤앤매너를 유지한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: `src/app/error.tsx`, `src/app/not-found.tsx`, `src/app/global-error.tsx`
- 요구사항: REQ-NF-FREE-003 (Graceful Error Handling), FE-005 (리포트 404)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/app/not-found.tsx` 컴포넌트 구현:
  - 404 페이지 템플릿 작성 (랜딩페이지 톤앤매너 유지)
  - "요청하신 페이지를 찾을 수 없습니다." 문구와 함께 메인 페이지 이동 버튼 제공.
- [ ] `src/app/error.tsx` 컴포넌트 구현 (`"use client"`):
  - 로직 실행 중 발생하는 런타임 예외를 잡는 컴포넌트
  - "일시적인 문제가 발생했습니다." 안내 메시지
  - 다시 시도하기(`reset()`) 버튼 제공
- [ ] (선택) 루트 레이아웃 에러를 위한 `src/app/global-error.tsx` 컴포넌트 작성 (html 태그 포함).

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 404 접근**
- Given: 정의되지 않은 라우트(예: `/unknown-path`)
- When: 사용자가 URL로 접근함
- Then: `not-found.tsx` 화면이 렌더링되고 메인화면으로 복귀할 수 있다.

**Scenario 2: 클라이언트 컴포넌트 오류 발생**
- Given: 특정 페이지 렌더링 중 `throw new Error()`가 발생함
- When: React 렌더링 트리가 에러를 캐치함
- Then: 전체 페이지가 죽는(White screen of death) 대신, `error.tsx` 화면이 나타나고 에러 로깅 함수가 내부적으로 호출된다.

## :gear: Technical & Non-Functional Constraints
- 프리미엄 브랜드 이미지를 위해 에러 페이지조차 심미적으로 우수하게 제작한다. (UI WOW 요소)
- 에러 객체(`error.message` 등)를 화면에 그대로 노출하지 않는다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `not-found.tsx` 컴포넌트 추가
- [ ] `error.tsx` 컴포넌트 추가
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** 공통 Layout UI
- **Blocks:** None
