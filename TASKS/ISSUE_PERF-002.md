---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] PERF-002: 리포트 웹뷰 Vercel Data Cache 설정 (비용 방어)"
labels: 'feature, infrastructure, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [PERF-002] 리포트 웹뷰 Vercel Data Cache 설정
- 목적: 리포트 웹뷰(`/report/[id]`)는 승인 후에는 내용이 거의 변경되지 않는 읽기 전용 데이터이므로, Next.js의 Data Cache(`unstable_cache` 또는 `fetch` 캐시 옵션)를 적용하여 DB(Supabase) 조회 호출 수를 줄이고 프리티어 한도를 방어한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: Q-008 (`getApprovedReport`), FE-005
- 요구사항: O2, NFR (Supabase Free Tier 호출량 최적화)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/queries/report.queries.ts`의 `getApprovedReport` 함수에 Next.js Data Cache 적용:
  ```typescript
  import { unstable_cache } from "next/cache"
  import { prisma } from "@/lib/prisma"
  import { ReportStatus } from "@/lib/constants/status"

  export const getApprovedReportCached = unstable_cache(
    async (id: string) => {
      const report = await prisma.report.findUnique({
        where: { id },
        select: { id: true, status: true, reportJson: true, updatedAt: true },
      })
      if (!report || report.status !== ReportStatus.APPROVED) return null
      return report
    },
    ['approved-report'],
    { tags: ['report'], revalidate: 3600 } // 1시간 캐시 또는 명시적 태그 무효화
  )
  ```
- [ ] 관리자가 리포트를 수정(C-007) 하거나 승인/거부(C-008) 할 때 캐시 무효화(`revalidateTag('report')` 또는 특정 ID 무효화) 추가.
- [ ] `src/app/report/[id]/page.tsx`에서 기존 쿼리 대신 `getApprovedReportCached`를 호출하도록 수정.

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 반복 조회 시 캐시 히트(DB 미호출)**
- Given: 리포트 페이지에 최초 접근하여 캐시가 생성됨
- When: 같은 페이지에 새로고침으로 연속 접근함
- Then: DB 쿼리가 발생하지 않고 캐시된 데이터가 빠르게 반환된다.

**Scenario 2: 관리자 수정 시 캐시 무효화**
- Given: 캐시된 리포트 데이터
- When: 관리자가 `modifyReport`를 통해 JSON을 수정하고 저장함
- Then: `revalidateTag`가 호출되어 캐시가 무효화되고, 고객이 새로고침 시 변경된 데이터가 노출된다.

## :gear: Technical & Non-Functional Constraints
- 비용 최적화를 위한 핵심. 5060 전문가(사용자)가 지인들에게 링크를 무한히 공유(트래픽 발생)하더라도, DB 부하를 차단하는 강력한 방패막 역할을 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `unstable_cache` 적용
- [ ] `modifyReport` 및 `reviewReportStatus`에 `revalidateTag` 추가
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** Q-008, C-007, C-008
- **Blocks:** None
