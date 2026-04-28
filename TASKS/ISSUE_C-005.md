---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] C-005: AI 진단 리포트 생성 + Zod 검증 + Report 저장"
labels: 'feature, backend, command, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [C-005] AI 진단 리포트 생성 + Zod 검증 + Report 저장
- 목적: Gemini API를 호출하여 진단 리포트 JSON을 생성하고, DiagnosisReportSchema로 Zod 검증한 후 Report 테이블에 draft 상태로 저장한다. 환각 차단의 핵심 — Zod 검증 실패 시 Report를 생성하지 않고 AiRun에 실패를 기록한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 시퀀스 1: [`SRS_v1.md#§3.4`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 301~311
- AI 코딩 Prompt 3: SRS Appendix D Lines 738~756
- 기능 요구사항:
  - REQ-FREE-FUNC-020 (AI 진단 리포트 생성)
  - REQ-FREE-FUNC-021 (sourceQuestionCodes 필수)
  - REQ-FREE-FUNC-022 (AI 실패 시 실패 상태 기록)
- Zod Schema: API-004 (DiagnosisReportSchema)
- AI payload: C-004 (buildAiPayload)
- AiRun 상태: DATA-004 (AiRunStatus, AiRunTaskType)
- Report 상태: DATA-003 (ReportStatus.DRAFT)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/services/ai-report.service.ts` 파일 생성
- [ ] Gemini API 클라이언트 설정:
  ```typescript
  import { GoogleGenerativeAI } from "@google/generative-ai"
  const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!)
  const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" })
  ```
- [ ] `generateDiagnosisReport(diagnosisId)` 함수 구현:
  ```typescript
  export async function generateDiagnosisReport(diagnosisId: string) {
    // 1. AiRun 레코드 생성 (status: processing)
    const aiRun = await prisma.aiRun.create({
      data: {
        diagnosisId,
        taskType: AiRunTaskType.GENERATE_REPORT,
        status: AiRunStatus.PROCESSING,
        startedAt: new Date(),
      },
    })

    try {
      // 2. payload 구성 (C-004)
      const payload = await buildAiPayload(diagnosisId)
      if (!payload) throw new Error("Answer 16건 미달")

      // 3. Gemini API 호출
      const prompt = buildPrompt(payload.answers)
      const result = await model.generateContent(prompt)
      const rawJson = extractJson(result.response.text())

      // 4. Zod 검증 (환각 차단)
      const parsed = DiagnosisReportSchema.parse(rawJson)

      // 5. Report 저장 (draft)
      const report = await prisma.report.create({
        data: {
          diagnosisId,
          status: ReportStatus.DRAFT,
          reportJson: parsed,
        },
      })

      // 6. Diagnosis 상태 업데이트
      await prisma.diagnosis.update({
        where: { id: diagnosisId },
        data: { status: DiagnosisStatus.REPORT_GENERATED },
      })

      // 7. AiRun 성공 기록
      await prisma.aiRun.update({
        where: { id: aiRun.id },
        data: { status: AiRunStatus.COMPLETED, completedAt: new Date() },
      })

      return { success: true, reportId: report.id, aiRunId: aiRun.id }
    } catch (error) {
      // 8. AiRun 실패 기록
      await prisma.aiRun.update({
        where: { id: aiRun.id },
        data: {
          status: AiRunStatus.FAILED,
          errorMessage: error instanceof Error ? error.message : "Unknown error",
          completedAt: new Date(),
        },
      })
      console.error("[generateDiagnosisReport] Error:", error)
      return { success: false, aiRunId: aiRun.id, error: String(error) }
    }
  }
  ```
- [ ] `buildPrompt(answers)` 프롬프트 구성 함수:
  - 시스템 프롬프트: "5060 전문가 브랜드 진단 AI" 역할 지시
  - 출력 형식: JSON 구조 명시 (DiagnosisReportSchema와 일치)
  - 답변 데이터 삽입
- [ ] `extractJson(text)` 유틸리티 — AI 응답에서 JSON 블록 추출 (마크다운 코드블록 제거)
- [ ] 환경변수: `GEMINI_API_KEY` 필요
- [ ] `npm install @google/generative-ai` 의존성 설치

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: AI 리포트 생성 성공 (E2E)**
- Given: Diagnosis D에 Answer 16건이 존재하고 GEMINI_API_KEY가 설정됨
- When: `generateDiagnosisReport(D)`를 실행함
- Then: Report(status=draft, reportJson=Zod검증통과)가 생성되고, AiRun(status=completed)이 기록된다

**Scenario 2: Zod 검증 실패 시 Report 미생성**
- Given: AI가 스키마에 맞지 않는 JSON을 반환함
- When: DiagnosisReportSchema.parse()가 ZodError를 throw함
- Then: Report는 생성되지 않고, AiRun(status=failed, errorMessage="...")이 기록된다

**Scenario 3: AiRun 성공 기록**
- Given: AI 호출이 성공함
- When: AiRun을 조회함
- Then: status=completed, startedAt과 completedAt이 모두 기록됨

**Scenario 4: AiRun 실패 기록**
- Given: AI API 호출이 타임아웃됨
- When: AiRun을 조회함
- Then: status=failed, errorMessage에 에러 내용이 기록됨

**Scenario 5: Diagnosis 상태 전이**
- Given: AI 리포트 생성이 성공함
- When: Diagnosis를 조회함
- Then: status가 `report_generated`로 업데이트됨

## :gear: Technical & Non-Functional Constraints
- Gemini 2.0 Flash 사용 (Free Tier 호환)
- AI 응답에서 JSON 추출 시 마크다운 코드블록(```json```) 제거 필요
- Zod 검증이 환각 차단의 마지막 방어선 — 실패 시 절대 Report를 생성하지 않음
- AiRun은 AI 호출 시작 시점에 먼저 생성 (processing) → 완료 후 업데이트
- Vercel Hobby 서버리스 타임아웃(10초) 고려 — 대용량 답변 시 주의

## :checkered_flag: Definition of Done (DoD)
- [ ] generateDiagnosisReport() 함수 구현 완료
- [ ] Gemini API 호출 → Zod 검증 → Report 저장 플로우 동작 확인
- [ ] Zod 실패 시 Report 미생성 + AiRun 실패 기록 확인
- [ ] Diagnosis 상태 전이(submitted→report_generated) 확인
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** C-004 (buildAiPayload), API-004 (DiagnosisReportSchema), DB-005 (Report), DB-006 (AiRun), DATA-002~004 (상태 상수), INF-003 (Gemini API 키 설정)
- **Blocks:** C-003 (submitDiagnosis에서 트리거), C-010 (재생성 로직 재사용), FE-002 (제출 후 리포트 상태 표시), T-005 (Zod 통과 테스트), T-006 (AI 실패 테스트)
