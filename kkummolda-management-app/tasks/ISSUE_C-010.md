---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] C-010: 리포트 재생성 및 AI 호출 횟수 제한 로직"
labels: 'feature, backend, command, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [C-010] 리포트 재생성 및 AI 호출 횟수 제한 로직
- 목적: 관리자가 리포트 재생성을 요청할 때, 허용된 최대 재생성 횟수(1회)를 검증하고 이를 초과하지 않은 경우 기존 리포트를 보관(재생성_요청) 처리한 후 AI를 재호출한다. Free Tier 보호를 위한 방어 로직이다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: REQ-NF-FREE-023 (진단당 AI 호출 1회 + 재생성 1회)
- DTO 참조: API-006 (RegenerateReportInputSchema)
- 조회 로직: Q-009 (getAiRunCount)
- AI 호출 로직: C-005 (generateDiagnosisReport)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/actions/report.actions.ts`에 `regenerateReport(input)` 함수 추가:
  ```typescript
  export async function regenerateReport(input: RegenerateReportInput): Promise<RegenerateReportOutput> {
    // 1. Zod 검증
    
    // 2. 호출 횟수 검증 (Q-009 재사용 또는 count 쿼리)
    const runCount = await prisma.aiRun.count({
      where: { diagnosisId: input.diagnosisId, status: AiRunStatus.COMPLETED }
    })
    
    // 기본 1회 + 재생성 1회 = 최대 2회
    if (runCount >= 2) {
      return { success: false, error: "재생성 허용 횟수(1회)를 초과했습니다.", errorCode: "RATE_LIMIT_EXCEEDED" }
    }

    // 3. 기존 리포트 상태 업데이트 (트랜잭션)
    await prisma.$transaction(async (tx) => {
      await tx.report.update({
        where: { id: input.reportId },
        data: { status: ReportStatus.REGENERATION_REQUESTED }
      })
      
      // ReviewLog에 재생성 사유 기록 (선택 사항)
      if (input.reason) {
        await tx.reviewLog.create({
          data: {
            reportId: input.reportId,
            action: "regenerate_request",
            note: input.reason,
            beforeJson: {}, // 기존 데이터 스냅샷이 이미 있으므로 생략 가능
            afterJson: {}
          }
        })
      }
    })

    // 4. 비동기 AI 재호출 (C-005 재사용하되 taskType만 구분 가능하도록 수정 필요)
    // generateDiagnosisReport 내부에서 taskType을 REGENERATE_REPORT로 지정하도록 매개변수 추가
    const result = await generateDiagnosisReport(input.diagnosisId, AiRunTaskType.REGENERATE_REPORT)
    
    if (!result.success) {
      return { success: false, error: "재생성 중 오류 발생", errorCode: "AI_GENERATION_FAILED" }
    }

    return { success: true, newReportId: result.reportId, aiRunId: result.aiRunId, message: "재생성 완료" }
  }
  ```
- [ ] C-005 `generateDiagnosisReport`에 `taskType` 인자 추가(기본값: GENERATE_REPORT)
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 정상 재생성**
- Given: AiRun 카운트가 1회인 진단 D
- When: `regenerateReport()`를 실행함
- Then: 기존 리포트가 `regeneration_requested`가 되고, 새 리포트가 생성된다

**Scenario 2: 호출 횟수 초과 차단**
- Given: AiRun 카운트가 2회(초과)인 진단 D
- When: `regenerateReport()`를 실행함
- Then: RATE_LIMIT_EXCEEDED 에러가 반환된다

## :gear: Technical & Non-Functional Constraints
- 비용 방어를 위한 중요 로직
- 기존 리포트를 덮어쓰지 않고 새로운 Report 레코드를 추가하여 버전을 유지함

## :checkered_flag: Definition of Done (DoD)
- [ ] regenerateReport() 함수 구현 완료
- [ ] 횟수 제한(2회 이상 차단) 로직 검증
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** Q-009 (AiRun count), C-005 (generateDiagnosisReport 수정)
- **Blocks:** FE-004 (관리자 화면 재생성 버튼)
