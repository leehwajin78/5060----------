---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] PERF-001: 랜딩페이지 성능/번들 최적화 (Soft Target 3초)"
labels: 'feature, infrastructure, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [PERF-001] 랜딩페이지 렌더링 성능 최적화
- 목적: 랜딩페이지(Q-001)의 로딩 속도를 높여 이탈률을 낮추기 위해, 불필요한 JS 번들 로드를 줄이고 이미지/폰트 최적화를 적용한다. (목표: 3초 이내 표시)

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: `src/app/page.tsx`, `next.config.mjs`, `src/app/layout.tsx`
- 요구사항: REQ-NF-FREE-001 (화면 표시 3초)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `next/font/google` 적용: 외부 폰트 요청 최적화 (예: Pretendard 폰트를 로컬 폰트로 최적화하거나 Google 폰트 Inter 적용)
- [ ] 랜딩페이지 내 `next/image` 컴포넌트 사용 강제 (`priority` 속성 활용)
- [ ] 랜딩페이지를 완전한 Static/Server Component로 유지:
  - 클라이언트 인터랙션(버튼 클릭 등)이 필요한 요소만 최하단 노드로 분리 (예: `"use client"`가 달린 `<CTAButton />`만 분리)
- [ ] `npm run build` 로그를 통해 랜딩페이지(`/`)가 정적(`○  (Static)`)으로 빌드되었는지 확인.

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 정적 페이지 빌드 확인**
- Given: 소스 코드 구현 완료 상태
- When: `npm run build`를 실행함
- Then: `/` 경로가 `○  (Static)` 또는 `●  (SSG)` 마크업으로 빌드되었음을 확인한다.

**Scenario 2: Lighthouse 성능 측정 (Soft)**
- Given: Vercel 배포 완료 후 랜딩페이지 URL
- When: Lighthouse 검사를 수행함
- Then: Performance 점수가 80점 이상이거나 초기 렌더링이 체감상 3초 이내에 이루어진다.

## :gear: Technical & Non-Functional Constraints
- Next.js App Router의 강점인 Server Component를 최대한 활용하여 JS 번들을 줄이는 것이 비용 없는 성능 향상의 핵심이다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 폰트 및 이미지 최적화 적용
- [ ] Server Component 분리 최적화
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** Q-001
- **Blocks:** None
