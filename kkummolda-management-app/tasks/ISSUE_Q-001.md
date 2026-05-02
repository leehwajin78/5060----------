---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] Q-001: 랜딩페이지 서비스 소개 및 진단 시작 CTA UI 구현"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [Q-001] 랜딩페이지 서비스 소개 및 진단 시작 CTA UI 구현
- 목적: 서비스 첫 화면으로 5060 전문가 대상 브랜드 진단 서비스를 소개하고, 진단 시작(CTA) 버튼을 통해 `/diagnose` 페이지로 이동시키는 랜딩페이지를 구현한다. MVP의 첫 인상을 결정하는 페이지이다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§1.2 S1`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — S1 (랜딩페이지: 서비스 소개, 진단 시작 CTA)
- 비기능 요구사항: REQ-NF-FREE-001 (랜딩페이지 3초 이내 표시 목표)
- 기술 스택: Tailwind CSS + shadcn/ui (INF-001)
- 컴포넌트 다이어그램: SRS §3.2 — LP[Landing Page]

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/app/page.tsx` 파일 수정 — 랜딩페이지 레이아웃 구현
- [ ] Hero 섹션 구현:
  - 서비스 타이틀: "나다운 브랜딩 — 5060 프리미엄 브랜드 진단"
  - 서비스 설명: 5060 고경력 전문가를 위한 AI 기반 브랜드 진단 서비스 소개 (2~3줄)
  - CTA 버튼: "무료 브랜드 진단 시작하기" → `/diagnose` 링크
- [ ] Value Proposition 섹션:
  - 진단 소요 시간 안내 (약 15~20분)
  - 결과물 안내 (AI 브랜드 진단 리포트 제공)
  - 프로세스 안내 (진단 → AI 분석 → 전문가 검수 → 리포트 제공)
- [ ] 하단 CTA 반복 배치: "지금 시작하기" 버튼
- [ ] SEO 메타 태그 설정:
  - `<title>나다운 브랜딩 | 5060 프리미엄 브랜드 진단</title>`
  - `<meta name="description" content="..." />`
- [ ] 반응형 레이아웃 (모바일/태블릿/데스크톱)
- [ ] shadcn/ui Button, Card 컴포넌트 활용

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 랜딩페이지 접근 성공**
- Given: Next.js 개발 서버가 실행 중임
- When: `http://localhost:3000`에 접속함
- Then: 랜딩페이지가 정상 렌더링된다 (HTTP 200)

**Scenario 2: 진단 시작 CTA 동작**
- Given: 랜딩페이지가 표시됨
- When: "무료 브랜드 진단 시작하기" 버튼을 클릭함
- Then: `/diagnose` 페이지로 이동한다

**Scenario 3: 서비스 소개 콘텐츠 표시**
- Given: 랜딩페이지가 렌더링됨
- When: 페이지 내용을 확인함
- Then: 서비스 타이틀, 설명, 프로세스 안내가 모두 표시된다

**Scenario 4: 모바일 반응형**
- Given: 모바일 뷰포트(375px)로 접속함
- When: 페이지를 확인함
- Then: 레이아웃이 깨지지 않고 CTA 버튼이 터치 가능한 크기로 표시된다

**Scenario 5: 페이지 로드 성능**
- Given: 랜딩페이지가 정적 콘텐츠로 구성됨
- When: 일반 네트워크에서 로딩 시간을 측정함
- Then: 3초 이내 표시를 목표로 한다 (Soft Target)

## :gear: Technical & Non-Functional Constraints
- Next.js App Router의 `src/app/page.tsx` — 루트 경로 (`/`)
- 정적 콘텐츠 위주 — DB 조회 없음, Server Component로 구현
- Tailwind CSS 유틸리티 + shadcn/ui 컴포넌트 사용
- 이미지/일러스트: MVP에서는 텍스트 중심, 필요시 최소한의 아이콘 사용
- 성능: 3초 이내 표시 (REQ-NF-FREE-001, Soft Target)
- SEO: title, meta description 필수

## :checkered_flag: Definition of Done (DoD)
- [ ] `/` 경로에서 랜딩페이지 정상 렌더링
- [ ] CTA 버튼 클릭 시 `/diagnose`로 이동
- [ ] 서비스 소개, 프로세스 안내 콘텐츠 표시
- [ ] 모바일/데스크톱 반응형 레이아웃 정상
- [ ] SEO 메타 태그 설정
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** INF-001 (Next.js + Tailwind + shadcn/ui 프로젝트)
- **Blocks:** PERF-001 (랜딩페이지 성능 검증), 사용자 유입 시작점
