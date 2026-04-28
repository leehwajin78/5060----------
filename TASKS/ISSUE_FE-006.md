---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-006: 상담 CTA 동작 연동 및 환경변수 주입"
labels: 'feature, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-006] 상담 CTA 동작 연동 및 환경변수 주입
- 목적: 승인 리포트 웹뷰(Q-005) 하단에 표시되는 CTA(Call To Action) 버튼의 클릭 동작을 구현하고, 환경변수로 설정된 외부 URL(구글 폼 등)로 이동시킨다. (선택적) C-011 클릭 이벤트 추적을 연동한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- UI: Q-005 (승인 리포트 웹뷰 CTA 영역)
- 로직: C-011 (CTA 클릭 로깅)
- 요구사항: REQ-FREE-FUNC-041 (리포트 하단 상담 CTA 제공)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `.env.local` (및 배포 환경)에 CTA 링크 환경변수 정의:
  ```env
  NEXT_PUBLIC_CTA_LINK="https://forms.gle/..."
  NEXT_PUBLIC_CTA_LABEL="전문가와 1:1 상담 신청하기"
  ```
- [ ] `src/app/report/[id]/page.tsx` 내 CTA 컴포넌트에 환경변수 값 적용
- [ ] 버튼 클릭 핸들러 작성:
  ```typescript
  "use client"
  import { logCtaClick } from "@/lib/actions/log.actions" // C-011

  export function ReportCTA({ reportId, leadId }: { reportId: string, leadId: string }) {
    const ctaLink = process.env.NEXT_PUBLIC_CTA_LINK || "#"
    const ctaLabel = process.env.NEXT_PUBLIC_CTA_LABEL || "상담 신청하기"

    const handleClick = () => {
      // 1. 이벤트 로깅 (Fire and forget)
      logCtaClick(reportId, leadId).catch(console.error)
      // 2. 외부 링크 이동 (새 탭)
      window.open(ctaLink, "_blank")
    }

    return (
      <Button onClick={handleClick} size="lg" className="w-full">
        {ctaLabel}
      </Button>
    )
  }
  ```
- [ ] AI 리포트 데이터(recommendedNextStep.message)와 CTA 버튼 텍스트 조화롭게 표시

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: CTA 링크 설정 및 동작**
- Given: `.env.local`에 NEXT_PUBLIC_CTA_LINK가 설정됨
- When: 사용자가 CTA 버튼을 클릭함
- Then: 새 탭이 열리며 해당 URL로 이동한다

**Scenario 2: 클릭 이벤트 로깅**
- Given: CTA 버튼 클릭 핸들러
- When: 클릭됨
- Then: `logCtaClick` Server Action이 백그라운드에서 호출된다

## :gear: Technical & Non-Functional Constraints
- Client Component에서 처리 (`"use client"`)
- `window.open`을 사용하여 원래 리포트 창을 닫지 않음(사용자 편의)
- 환경변수 누락 시 기본 동작/안내를 방어 코드로 작성

## :checkered_flag: Definition of Done (DoD)
- [ ] 환경변수 기반 링크/라벨 연동 완료
- [ ] 클릭 시 새 탭 이동 동작 확인
- [ ] (선택) 로깅 액션 연동 확인
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** Q-005 (UI 레이아웃), C-011 (옵션: 로깅 액션)
- **Blocks:** 테스트(고객 전환 플로우)
