---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] Q-008: 승인 리포트 조회 로직 (고객 웹뷰용 접근 제어)"
labels: 'feature, backend, query, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [Q-008] 승인 리포트 조회 로직 (고객 웹뷰용)
- 목적: 리포트 웹뷰(Q-005) 또는 API(API-007)에 데이터를 공급하는 서버 측 조회 로직을 구현한다. 고객에게 공개되는 엔드포인트이므로, `status === "approved"` 조건 검사(접근 제어)가 쿼리 레벨에서 강제되어야 한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§4.1 F-Report-Lite`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — REQ-FREE-FUNC-034 (미승인 차단), REQ-FREE-FUNC-040
- 상태 상수: DATA-003 (ReportStatus.APPROVED)
- DTO 참조: API-007 (PublicReportResponse)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/queries/report.queries.ts` 파일 생성
- [ ] `getApprovedReport(id)` 함수 구현:
  ```typescript
  import { ReportStatus } from "@/lib/constants/status"

  export async function getApprovedReport(id: string) {
    const report = await prisma.report.findUnique({
      where: { id },
      select: { id: true, status: true, reportJson: true, updatedAt: true },
    })

    if (!report) return null
    if (report.status !== ReportStatus.APPROVED) return null // 보안: 미승인 사실 비노출(null 반환)

    return report
  }
  ```
- [ ] 에러 반환을 명확히 할 경우, 에러 코드를 포함하는 Result 객체 패턴 적용 검토 (API-007 스펙에 맞춰 `NOT_FOUND` vs `NOT_APPROVED` 구분 필요 시)
- [ ] `reportJson`을 `DiagnosisReport` 타입으로 단언(Type Assertion) 또는 Zod 파싱 후 반환
- [ ] API-007 라우트 핸들러 또는 Q-005 Server Component에서 호출 연동

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 승인 리포트 조회 성공**
- Given: Report R이 `status="approved"`로 존재함
- When: `getApprovedReport(R)`을 실행함
- Then: 리포트 객체가 반환된다

**Scenario 2: 미승인 리포트 접근 차단**
- Given: Report R이 `status="draft"`로 존재함
- When: `getApprovedReport(R)`을 실행함
- Then: null (또는 NOT_APPROVED 에러)이 반환된다

**Scenario 3: 거부된 리포트 접근 차단**
- Given: Report R이 `status="rejected"`로 존재함
- When: `getApprovedReport(R)`을 실행함
- Then: null이 반환된다

**Scenario 4: 존재하지 않는 ID**
- Given: DB에 없는 ID가 주어짐
- When: `getApprovedReport("invalid")`를 실행함
- Then: null이 반환된다

## :gear: Technical & Non-Functional Constraints
- 보안 핵심 로직: 쿼리에서 `status === ReportStatus.APPROVED` 필터링 강제
- `NOT_FOUND`와 `NOT_APPROVED`를 동일하게 404 처리할지 여부는 API-007 스펙을 따른다. (기본적으로는 미승인 사실 노출 방지를 위해 둘 다 null 반환 후 404 응답 권장)

## :checkered_flag: Definition of Done (DoD)
- [ ] `getApprovedReport()` 함수 구현
- [ ] `approved` 상태 외에는 모두 null 반환 동작 확인
- [ ] 반환된 `reportJson`의 타입 추론 지원
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** DB-005 (Report), DATA-003 (ReportStatus), API-004 (리포트 타입)
- **Blocks:** Q-005 (웹뷰 UI 데이터 연동), API-007 (웹뷰 API 연동)
