---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] C-006: AI 생성 실패 처리 로직 (fallback + 사용자 안내)"
labels: 'feature, backend, command, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [C-006] AI 생성 실패 처리 로직
- 목적: AI 리포트 생성(C-005)이 실패한 경우의 후속 처리를 구현한다. 답변 데이터는 보존하고, Diagnosis 상태를 `report_pending`으로 설정하여 관리자가 수동 재생성하거나 대응할 수 있도록 한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: REQ-FREE-FUNC-022 (AI 생성 실패 시 상태 기록, 답변 보존)
- SRS 시퀀스 1: Lines 305~308 — "GenAI 실패 → report_pending 상태"
- 상태 상수: DATA-002 (DiagnosisStatus.REPORT_PENDING)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/services/ai-report.service.ts`에 실패 처리 로직 추가 (C-005 catch 블록 확장):
  ```typescript
  async function handleAiFailure(diagnosisId: string, aiRunId: string, error: unknown) {
    // 1. Diagnosis 상태 → report_pending
    await prisma.diagnosis.update({
      where: { id: diagnosisId },
      data: { status: DiagnosisStatus.REPORT_PENDING },
    })

    // 2. 에러 로깅
    console.error(`[AI Failure] diagnosisId=${diagnosisId}, aiRunId=${aiRunId}`, error)
  }
  ```
- [ ] C-005의 catch 블록에서 `handleAiFailure()` 호출
- [ ] submitDiagnosis(C-003) 응답에서 AI 실패 시 사용자 안내 메시지 분기:
  ```typescript
  // AI 실패 시
  return {
    success: true,  // 답변 저장은 성공
    diagnosisId: result.diagnosisId,
    reportStatus: "report_pending",
    message: "답변이 안전하게 저장되었습니다. 검수 후 리포트를 안내드리겠습니다.",
  }
  ```
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: AI 실패 시 Diagnosis 상태 전이**
- Given: AI 리포트 생성이 실패함
- When: handleAiFailure()가 실행됨
- Then: Diagnosis.status가 `report_pending`으로 업데이트된다

**Scenario 2: AI 실패 시 답변 데이터 보존**
- Given: AI 리포트 생성이 실패함
- When: Answer 테이블을 조회함
- Then: 16건의 Answer 레코드가 그대로 존재한다 (삭제되지 않음)

**Scenario 3: 사용자에게 부분 성공 안내**
- Given: submitDiagnosis에서 AI가 실패함
- When: 반환 응답을 확인함
- Then: `{ success: true, reportStatus: "report_pending", message: "답변이 안전하게 저장..." }` 구조가 반환된다

**Scenario 4: 에러 로그 기록**
- Given: AI 호출이 타임아웃으로 실패함
- When: 서버 로그를 확인함
- Then: diagnosisId, aiRunId, 에러 내용이 포함된 로그가 기록되어 있다

## :gear: Technical & Non-Functional Constraints
- AI 실패 ≠ 진단 제출 실패 — 답변은 이미 트랜잭션으로 저장 완료 (C-003)
- `report_pending` 상태는 관리자에게 "AI 리포트 미생성" 시그널
- 관리자는 수동 재생성(C-010) 또는 직접 리포트 작성 가능

## :checkered_flag: Definition of Done (DoD)
- [ ] handleAiFailure() 함수 구현
- [ ] Diagnosis 상태 report_pending 전이 동작 확인
- [ ] 답변 데이터 보존 확인
- [ ] 사용자 안내 메시지 분기 동작 확인
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** C-005 (AI 리포트 생성 — catch 블록), DATA-002 (DiagnosisStatus.REPORT_PENDING)
- **Blocks:** T-006 (AI 실패 테스트), LOG-001 (실패 로깅)
