---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] Q-002: 16문항 진단 폼 UI 구현 (/diagnose)"
labels: 'feature, frontend, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [Q-002] 16문항 진단 폼 UI — 질문 카드, assetHint, textarea
- 목적: 5060 전문가가 축약 16문항에 답변하고 리드 정보를 입력하는 진단 폼 페이지를 구현한다. 각 질문에 브랜드 자산 안내(assetHint)를 표시하여 답변의 의미를 안내하며, PART 순서대로 카드 형태로 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§4.1 F2-Lite`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — REQ-FREE-FUNC-001, 002
- AI 코딩 Prompt 2: SRS Appendix D Lines 712~730
- 질문 데이터: DATA-001 (`lib/questions.ts` — code, text, part, assetHint)
- 16문항 코드: SRS §1.2 S2

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/app/diagnose/page.tsx` 파일 생성
- [ ] QUESTIONS 배열 import (`@/lib/questions`)
- [ ] 질문 카드 컴포넌트 구현:
  - PART 구분 헤더 표시 (PART별 그룹핑)
  - 질문 번호 + 질문 텍스트 표시
  - **브랜드 자산 안내(assetHint)** 문구를 질문 카드 상단/하단에 강조 표시
  - textarea 입력 필드 (최소 3줄 높이)
- [ ] 리드 정보 입력 영역:
  - 이름 (필수) — Input 컴포넌트
  - 연락처: 이메일 또는 전화번호 (필수) — Input 컴포넌트
  - 유입경로 (선택) — Input 컴포넌트
- [ ] 진행 상황 표시 (현재 답변 수 / 16)
- [ ] 제출 버튼 ("진단 제출하기")
- [ ] shadcn/ui Card, Textarea, Input, Label, Button 활용
- [ ] 반응형 레이아웃 (모바일 우선)

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 16문항 카드 렌더링**
- Given: `/diagnose` 페이지에 접속함
- When: 페이지를 확인함
- Then: 16개 질문 카드가 PART 순서대로 렌더링된다

**Scenario 2: 브랜드 자산 안내 표시**
- Given: 각 질문 카드가 렌더링됨
- When: 질문 카드의 assetHint 영역을 확인함
- Then: 모든 16개 질문에 비어있지 않은 브랜드 자산 안내 문구가 표시된다

**Scenario 3: textarea 입력 가능**
- Given: 질문 카드에 textarea가 표시됨
- When: 사용자가 텍스트를 입력함
- Then: 입력 내용이 폼 상태에 반영된다

**Scenario 4: 리드 정보 입력 필드 표시**
- Given: 진단 폼 페이지가 렌더링됨
- When: 페이지 상단 또는 하단의 리드 정보 영역을 확인함
- Then: 이름, 연락처, 유입경로 입력 필드가 표시된다

**Scenario 5: 모바일 반응형**
- Given: 375px 뷰포트에서 접속함
- When: 질문 카드와 입력 필드를 확인함
- Then: 카드가 전체 너비로 표시되고 스크롤로 탐색 가능하다

## :gear: Technical & Non-Functional Constraints
- `src/app/diagnose/page.tsx` — Next.js App Router 페이지
- Client Component (`"use client"`) — 폼 상태 관리 필요
- QUESTIONS 배열(DATA-001)에서 질문 데이터 import — 하드코딩 금지
- shadcn/ui 컴포넌트: Card, CardHeader, CardContent, Textarea, Input, Label, Button
- 이 태스크는 UI 렌더링만 담당 — 유효성 검증(FE-001)과 제출 연동(FE-002)은 별도 태스크

## :checkered_flag: Definition of Done (DoD)
- [ ] `/diagnose` 경로에서 16문항 질문 카드 정상 렌더링
- [ ] 모든 질문에 assetHint 브랜드 자산 안내 표시
- [ ] PART 순서대로 질문 그룹핑
- [ ] 이름/연락처/유입경로 입력 필드 표시
- [ ] 모바일/데스크톱 반응형 정상
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** DATA-001 (QUESTIONS 배열), INF-001 (shadcn/ui)
- **Blocks:** FE-001 (폼 유효성 검증), FE-002 (제출 연동), DPR-001 (동의 체크박스)
