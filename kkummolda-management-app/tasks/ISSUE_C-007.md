---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] C-007: 관리자 리포트 수정 로직 (reportJson 업데이트 + Zod 재검증)"
labels: 'feature, backend, command, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [C-007] 관리자 리포트 수정 로직
- 목적: 관리자가 AI 생성 리포트의 JSON을 직접 수정할 때, 수정된 JSON을 DiagnosisReportSchema로 재검증한 후 Report.reportJson을 업데이트한다. 변경 전/후 JSON 스냅샷은 ReviewLog(C-009)에 기록된다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: REQ-FREE-FUNC-032 (관리자 리포트 수정)
- DTO 참조: API-005 (ReviewReportInputSchema — action: "modify")
- Zod Schema: API-004 (DiagnosisReportSchema)
- ReviewLog: C-009

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/actions/report.actions.ts` 파일 생성 (`"use server"`)
- [ ] `modifyReport(input)` 함수 구현:
  ```typescript
  export async function modifyReport(input: ReviewReportInput): Promise<ReviewReportOutput> {
    if (input.action !== ReviewAction.MODIFY) {
      return { success: false, error: "잘못된 action입니다." }
    }

    // 1. 기존 Report 조회
    const report = await prisma.report.findUnique({ where: { id: input.reportId } })
    if (!report) return { success: false, error: "리포트를 찾을 수 없습니다." }

    // 2. 수정된 JSON Zod 재검증
    const parsed = DiagnosisReportSchema.safeParse(input.updatedReportJson)
    if (!parsed.success) {
      return {
        success: false,
        error: "수정된 리포트가 스키마를 충족하지 않습니다: " + parsed.error.message,
      }
    }

    // 3. Report 업데이트 + ReviewLog 생성 (트랜잭션)
    const result = await prisma.$transaction(async (tx) => {
      const updated = await tx.report.update({
        where: { id: input.reportId },
        data: {
          reportJson: parsed.data,
          reviewNote: input.reviewNote ?? null,
        },
      })

      const log = await tx.reviewLog.create({
        data: {
          reportId: input.reportId,
          action: ReviewAction.MODIFY,
          note: input.reviewNote ?? null,
          beforeJson: report.reportJson,
          afterJson: parsed.data,
        },
      })

      return { reportId: updated.id, reviewLogId: log.id }
    })

    return {
      success: true,
      reportId: result.reportId,
      newStatus: report.status, // 수정만으로 상태 변경 없음
      reviewLogId: result.reviewLogId,
    }
  }
  ```
- [ ] Zod 재검증 실패 시 수정 차단 — 스키마 비준수 데이터 저장 방지
- [ ] beforeJson/afterJson 스냅샷 기록
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 유효한 수정 성공**
- Given: Report R이 존재하고 수정된 JSON이 Zod 스키마를 준수함
- When: `modifyReport({ reportId: R, action: "modify", updatedReportJson: {...} })`를 실행함
- Then: Report.reportJson이 업데이트되고, ReviewLog(action=modify, beforeJson, afterJson)가 생성된다

**Scenario 2: Zod 재검증 실패 시 수정 차단**
- Given: 수정된 JSON의 summary가 30자 미만임
- When: `modifyReport(input)`를 실행함
- Then: `{ success: false, error: "스키마를 충족하지 않습니다..." }`가 반환되고, Report는 변경되지 않는다

**Scenario 3: beforeJson/afterJson 스냅샷 기록**
- Given: 수정 전 reportJson이 A, 수정 후가 B임
- When: 수정이 성공하고 ReviewLog를 조회함
- Then: ReviewLog.beforeJson = A, afterJson = B로 기록되어 있다

**Scenario 4: 존재하지 않는 Report**
- Given: 존재하지 않는 reportId가 주어짐
- When: `modifyReport(input)`를 실행함
- Then: `{ success: false, error: "리포트를 찾을 수 없습니다." }`가 반환된다

## :gear: Technical & Non-Functional Constraints
- 수정만으로 Report.status는 변경되지 않음 (승인/거부는 C-008에서 처리)
- Zod 재검증은 환각 차단과 동일한 레벨 — 관리자가 스키마 위반 데이터를 저장하는 것도 방지
- beforeJson/afterJson은 감사 추적(Audit Trail)용 불변 기록

## :checkered_flag: Definition of Done (DoD)
- [ ] modifyReport() 함수 구현 완료
- [ ] Zod 재검증 성공/실패 분기 동작 확인
- [ ] ReviewLog beforeJson/afterJson 기록 확인
- [ ] 트랜잭션 원자성 (Report 업데이트 + ReviewLog 생성) 확인
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** DB-005 (Report), DB-007 (ReviewLog), API-004 (DiagnosisReportSchema), API-005 (ReviewReportInput)
- **Blocks:** FE-003 (수정 편집기 연동), T-009 (수정 테스트)
