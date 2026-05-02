---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] MOCK-002: AI 진단 리포트 성공 JSON Mock 데이터 (Zod 스키마 준수)"
labels: 'feature, mock, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-002] AI 진단 리포트 성공 JSON Mock 데이터
- 목적: AI 리포트 생성 결과의 Mock JSON을 제공하여, 관리자 콘솔(FE-003~004)과 리포트 웹뷰(Q-005)가 백엔드/AI 완성 없이 독립 개발할 수 있도록 한다. 성공/Zod 위반/부분 데이터 3종 fixture를 포함한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#Appendix B — AI 진단 리포트 JSON Schema`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 603~632
- Zod Schema: API-004 (DiagnosisReportSchema)
- 기능 요구사항: REQ-FREE-FUNC-020, 021 (리포트 구조, sourceQuestionCodes)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/mocks/report.mock.ts` 파일 생성
- [ ] 성공 Mock — Zod 스키마 준수 완전한 DiagnosisReport:
  ```typescript
  export const mockValidReport: DiagnosisReport = {
    summary: "30년간 IT 분야에서 축적한 기술 리더십과 팀 관리 경험이 돋보입니다. 특히 복잡한 프로젝트를 성공적으로 이끈 사례에서 강한 실행력과 전략적 사고가 드러납니다.",
    strengths: [
      { title: "기술 리더십", description: "30년 IT 경험 기반의 기술적 판단력과 의사결정 역량", sourceQuestionCodes: ["Q1", "Q6"] },
      { title: "팀 빌딩 역량", description: "다양한 배경의 인재를 하나의 목표로 결집시키는 능력", sourceQuestionCodes: ["Q8", "Q9"] },
    ],
    weaknesses: [
      { title: "개인 브랜딩 경험 부족", description: "조직 내 역할에 집중하여 외부 브랜딩 활동이 제한적", sourceQuestionCodes: ["Q15", "Q26"] },
    ],
    brandDirection: {
      oneSentence: "기술과 사람을 잇는 시니어 IT 리더",
      description: "축적된 기술 전문성과 팀 리더십을 바탕으로, 차세대 기술 인재를 양성하는 멘토이자 컨설턴트로서의 브랜드 방향을 제안합니다.",
      sourceQuestionCodes: ["Q26", "Q41"],
    },
    recommendedNextStep: {
      message: "전문가와 함께 구체적인 브랜드 전략을 수립해보세요.",
      ctaLabel: "상담 신청하기",
    },
    warnings: [],
  }
  ```
- [ ] Zod 위반 Mock — summary 30자 미만:
  ```typescript
  export const mockInvalidReportShortSummary = {
    ...mockValidReport,
    summary: "짧은 요약",  // 30자 미만
  }
  ```
- [ ] Zod 위반 Mock — sourceQuestionCodes 누락:
  ```typescript
  export const mockInvalidReportNoCodes = {
    ...mockValidReport,
    strengths: [{ title: "강점", description: "설명" }],  // sourceQuestionCodes 없음
  }
  ```
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 성공 Mock이 Zod 검증 통과**
- Given: mockValidReport가 정의됨
- When: `DiagnosisReportSchema.parse(mockValidReport)`를 실행함
- Then: 검증이 성공하고 DiagnosisReport 타입 객체가 반환된다

**Scenario 2: 짧은 summary Mock이 Zod 검증 실패**
- Given: mockInvalidReportShortSummary가 정의됨
- When: `DiagnosisReportSchema.parse(mockInvalidReportShortSummary)`를 실행함
- Then: ZodError가 발생한다

**Scenario 3: sourceQuestionCodes 누락 Mock이 Zod 검증 실패**
- Given: mockInvalidReportNoCodes가 정의됨
- When: `DiagnosisReportSchema.parse(mockInvalidReportNoCodes)`를 실행함
- Then: ZodError가 발생한다

**Scenario 4: 5060 전문가 톤 유지**
- Given: mockValidReport의 텍스트 내용을 확인함
- When: summary, strengths, brandDirection을 읽음
- Then: 5060 고경력 전문가 맥락에 적합한 한글 콘텐츠가 포함되어 있다

## :gear: Technical & Non-Functional Constraints
- Mock 데이터의 한글 콘텐츠는 5060 전문가 브랜딩 맥락 유지 (IT 리더, 컨설턴트 등)
- sourceQuestionCodes는 DATA-001의 16문항 코드 범위 내에서 사용
- 3종 fixture: 성공 1개 + Zod 위반 2개 (다양한 에러 케이스)

## :checkered_flag: Definition of Done (DoD)
- [ ] 성공 Mock 1개가 DiagnosisReportSchema 검증 통과
- [ ] Zod 위반 Mock 2개가 검증 실패
- [ ] 5060 전문가 맥락 한글 콘텐츠 포함
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** API-004 (DiagnosisReportSchema)
- **Blocks:** MOCK-003 (관리자 화면 Mock), FE-003 (리포트 수정 편집기 개발), Q-005 (리포트 웹뷰 개발), T-005 (Zod 스키마 테스트)
