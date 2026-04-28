---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] Q-005: 승인 리포트 웹뷰 UI (/report/[id])"
labels: 'feature, frontend, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [Q-005] 승인 리포트 웹뷰 UI
- 목적: 관리자가 승인한 AI 진단 리포트를 고객에게 공유하는 웹뷰 페이지를 구현한다. summary, 강점 목록, 약점 목록, 브랜드 방향, 상담 CTA를 프리미엄 디자인으로 표시하며, 미승인 리포트는 접근을 차단한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§4.1 F-Report-Lite`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — REQ-FREE-FUNC-040, 041
- AI 코딩 Prompt 5: SRS Appendix D Lines 780~795
- 시퀀스 2: SRS §3.4 Lines 331~338
- 리포트 JSON: API-004 (DiagnosisReportSchema)
- CTA 설정: API-007 (CtaConfig), REQ-FREE-FUNC-041

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/app/report/[id]/page.tsx` 파일 생성
- [ ] 리포트 헤더:
  - "나다운 브랜딩 — 브랜드 진단 리포트" 타이틀
  - 프리미엄 느낌의 디자인 (그라데이션 배경 등)
- [ ] Summary 섹션:
  - 3~5문장 요약 텍스트 표시 (큰 폰트, 강조)
- [ ] 강점(Strengths) 섹션:
  - 강점 카드 목록 (title + description)
  - 각 카드에 sourceQuestionCodes 참조 표시 (선택)
- [ ] 약점/보완 지점(Weaknesses) 섹션:
  - 보완 지점 카드 목록 (title + description)
- [ ] 브랜드 방향(Brand Direction) 섹션:
  - oneSentence 강조 표시 (큰 폰트)
  - description 설명 텍스트
- [ ] 상담 CTA 섹션 (하단 고정):
  - recommendedNextStep.message 표시
  - CTA 버튼 (recommendedNextStep.ctaLabel)
  - 버튼 클릭 → 환경변수 기반 구글폼/이메일/카카오 링크
- [ ] 경고(Warnings) 표시 — warnings 배열이 존재할 경우
- [ ] 반응형 레이아웃 (모바일 최적화 — 고객이 모바일로 접근할 가능성 높음)
- [ ] 초기 개발 시 MOCK-002 데이터로 렌더링

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 승인 리포트 정상 표시**
- Given: approved 상태의 리포트가 존재함
- When: `/report/[id]`에 접속함
- Then: summary, 강점, 약점, 브랜드 방향, CTA가 구조화되어 표시된다

**Scenario 2: CTA 버튼 표시**
- Given: 리포트 하단에 CTA 섹션이 존재함
- When: CTA 영역을 확인함
- Then: recommendedNextStep의 message와 ctaLabel이 표시되고 클릭 가능하다

**Scenario 3: 강점 카드 렌더링**
- Given: strengths 배열에 2건이 존재함
- When: 강점 섹션을 확인함
- Then: 2개의 강점 카드가 title과 description으로 표시된다

**Scenario 4: 브랜드 방향 oneSentence 강조**
- Given: brandDirection.oneSentence가 존재함
- When: 브랜드 방향 섹션을 확인함
- Then: oneSentence가 강조된 폰트/스타일로 표시된다

**Scenario 5: 모바일 반응형**
- Given: 375px 뷰포트에서 접속함
- When: 리포트 페이지를 확인함
- Then: 모든 섹션이 읽기 편하게 표시되고 CTA 버튼이 터치 가능하다

## :gear: Technical & Non-Functional Constraints
- 동적 라우트: `src/app/report/[id]/page.tsx`
- 고객 공개 페이지 — 프리미엄 디자인 중요 (5060 전문가 대상)
- 접근 제어(FE-005)와 CTA 링크(FE-006)는 별도 태스크로 분리
- Server Component로 데이터 fetch + Client Component로 인터랙션
- SEO 메타 태그: 공유 URL용 og:title, og:description 설정

## :checkered_flag: Definition of Done (DoD)
- [ ] `/report/[id]` 경로에서 리포트 정상 렌더링
- [ ] summary, 강점, 약점, 브랜드 방향, CTA 모든 섹션 표시
- [ ] 프리미엄 디자인 적용 (5060 전문가 대상 톤)
- [ ] 모바일/데스크톱 반응형 정상
- [ ] SEO 메타 태그 설정
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** API-004 (DiagnosisReport 타입), API-007 (PublicReportResponse), MOCK-002 (초기 개발 데이터), INF-001 (shadcn/ui)
- **Blocks:** FE-005 (미승인 접근 차단), FE-006 (CTA 링크 연결), C-011 (CTA 이벤트 기록)
