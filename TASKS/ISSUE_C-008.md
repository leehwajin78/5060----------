---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] C-008: 관리자 리포트 승인/거부 상태 전이 로직"
labels: 'feature, backend, command, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [C-008] 관리자 리포트 승인/거부 상태 전이 로직
- 목적: 관리자가 리포트를 승인(approved)하거나 거부(rejected)할 때 Report 및 Diagnosis 상태를 업데이트하고, 해당 이력을 ReviewLog(C-009)에 기록하는 로직을 구현한다. 승인 시 리포트가 외부에 공개된다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: REQ-FREE-FUNC-033 (승인/거부 시 상태 전이)
- SRS 시퀀스 2: Lines 331~338 — "상태 변경(approved) → ReviewLog 기록"
- DTO 참조: API-005 (ReviewReportInputSchema — action: "approve" | "reject")
- 상태 상수: DATA-002 (DiagnosisStatus), DATA-003 (ReportStatus)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/actions/report.actions.ts`에 `reviewReportStatus(input)` 함수 추가:
  ```typescript
  export async function reviewReportStatus(input: ReviewReportInput): Promise<ReviewReportOutput> {
    if (input.action !== ReviewAction.APPROVE && input.action !== ReviewAction.REJECT) {
      return { success: false, error: "잘못된 action입니다." }
    }

    const report = await prisma.report.findUnique({ where: { id: input.reportId } })
    if (!report) return { success: false, error: "리포트를 찾을 수 없습니다." }

    const newReportStatus = input.action === ReviewAction.APPROVE 
      ? ReportStatus.APPROVED 
      : ReportStatus.REJECTED;

    const newDiagnosisStatus = input.action === ReviewAction.APPROVE
      ? DiagnosisStatus.REVIEWED
      : DiagnosisStatus.REPORT_GENERATED; // 거부 시 다시 생성 가능하도록

    // 트랜잭션: Report 업데이트 + Diagnosis 업데이트 + ReviewLog 생성
    const result = await prisma.$transaction(async (tx) => {
      const updated = await tx.report.update({
        where: { id: input.reportId },
        data: { status: newReportStatus },
      })

      await tx.diagnosis.update({
        where: { id: report.diagnosisId },
        data: { status: newDiagnosisStatus },
      })

      const log = await tx.reviewLog.create({
        data: {
          reportId: input.reportId,
          action: input.action,
          note: input.reviewNote ?? null,
          beforeJson: report.reportJson, // 상태만 변경되므로 before/after 동일
          afterJson: report.reportJson,
        },
      })

      return { reportId: updated.id, newStatus: updated.status, reviewLogId: log.id }
    })

    return {
      success: true,
      reportId: result.reportId,
      newStatus: result.newStatus,
      reviewLogId: result.reviewLogId,
    }
  }
  ```
- [ ] 승인/거부 시 Report.status 및 Diagnosis.status 동기화 전이
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 리포트 승인 정상 처리**
- Given: Report(draft)가 주어짐
- When: `action="approve"`로 실행함
- Then: Report.status가 "approved"가 되고, Diagnosis.status가 "reviewed"가 되며 ReviewLog가 생성된다

**Scenario 2: 리포트 거부 정상 처리**
- Given: Report(draft)가 주어짐
- When: `action="reject"`로 실행함
- Then: Report.status가 "rejected"가 되고, ReviewLog가 생성된다

**Scenario 3: 존재하지 않는 리포트**
- Given: 잘못된 reportId가 주어짐
- When: 실행함
- Then: `{ success: false, error: "리포트를 찾을 수 없습니다." }` 반환

## :gear: Technical & Non-Functional Constraints
- 승인(approved) 순간부터 Q-008(승인 리포트 조회 로직)을 통해 고객 웹뷰 노출이 가능해짐 (보안 임계점)
- 상태 전이는 반드시 트랜잭션으로 묶어 Report와 Diagnosis의 상태 불일치를 방지

## :checkered_flag: Definition of Done (DoD)
- [ ] reviewReportStatus() 함수 구현 완료
- [ ] approve/reject 상태 전이 확인
- [ ] 트랜잭션 및 ReviewLog 생성 동작 확인
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** DB-005(Report), DB-003(Diagnosis), DB-007(ReviewLog), API-005(DTO)
- **Blocks:** FE-004(승인/거부 버튼 연동), Q-008(승인 리포트 노출)
