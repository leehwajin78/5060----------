---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-005: 리포트 웹뷰 접근 제어 (미승인/404 UI 처리)"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-005] 리포트 웹뷰 접근 제어
- 목적: 고객이 전달받은 리포트 URL(`/report/[id]`)에 접속했을 때, 해당 리포트가 존재하지 않거나 승인(approved)되지 않은 상태라면 내용을 숨기고 404/안내 페이지를 보여주어 보안을 유지한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- UI: Q-005 (승인 리포트 웹뷰)
- 쿼리: Q-008 (승인 리포트 조회 로직)
- 요구사항: REQ-FREE-FUNC-034 (미승인 차단)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/app/report/[id]/page.tsx` 내부 데이터 패칭 로직 확인
- [ ] `getApprovedReport(params.id)` (Q-008) 결과가 null일 경우의 예외 처리 로직 추가:
  ```typescript
  import { notFound } from "next/navigation"

  export default async function ReportPage({ params }: { params: { id: string } }) {
    const report = await getApprovedReport(params.id)

    if (!report) {
      // 존재하지 않거나 승인되지 않은 경우 동일하게 404 처리 (비노출)
      notFound()
    }
    
    // ... 정상 렌더링
  }
  ```
- [ ] `src/app/not-found.tsx` 컴포넌트(글로벌 404 페이지) 개선 (또는 report 폴더 전용 404 페이지 구현):
  - "페이지를 찾을 수 없거나 아직 준비 중인 리포트입니다." 등 고객 친화적 메시지 제공
  - 메인화면(랜딩페이지)으로 돌아가기 버튼 제공

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 승인된 리포트 접근**
- Given: 승인된 리포트 URL
- When: 사용자가 URL로 접근함
- Then: 리포트 내용이 정상적으로 표시된다

**Scenario 2: 미승인(Draft/Rejected) 리포트 접근**
- Given: 승인되지 않은 리포트 URL
- When: 사용자가 URL로 접근함
- Then: Next.js의 404(Not Found) 페이지가 렌더링되며 리포트 내용은 노출되지 않는다

**Scenario 3: 존재하지 않는 ID 접근**
- Given: DB에 없는 임의의 ID
- When: 접근함
- Then: 404 페이지가 렌더링된다

## :gear: Technical & Non-Functional Constraints
- 보안 요구사항: 고객이 URL 파라미터 조작으로 다른 사람의 임시/거부 리포트를 엿보지 못하게 차단하는 핵심 방어선.
- Server Component 레벨에서 `notFound()`를 호출하여 렌더링 자체를 방지함.

## :checkered_flag: Definition of Done (DoD)
- [ ] `report/[id]` 페이지에 접근 제어 적용 완료
- [ ] 404 안내 UI(not-found.tsx) 구현 완료
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** Q-008 (getApprovedReport), Q-005 (웹뷰 UI)
- **Blocks:** 배포 전 보안 검수
