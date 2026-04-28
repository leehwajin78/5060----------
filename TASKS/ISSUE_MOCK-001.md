---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] MOCK-001: 16문항 진단 제출 성공/실패 Mock 데이터"
labels: 'feature, mock, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-001] 16문항 진단 제출 성공/실패 Mock 데이터
- 목적: 프론트엔드(Q-002, FE-001, FE-002)가 백엔드 완성을 기다리지 않고 독립 개발할 수 있도록, 16문항 진단 제출의 성공/실패 시나리오별 Mock 데이터 fixture를 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§4.1 F2-Lite`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — REQ-FREE-FUNC-001~004
- 16문항 코드: Q1·Q2·Q4·Q6·Q7·Q8·Q9·Q11·Q13·Q15·Q26·Q28·Q33·Q40·Q41·Q42
- DTO 참조: API-002 (SubmitDiagnosisInput/Output)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/mocks/diagnosis.mock.ts` 파일 생성
- [ ] 성공 케이스 Mock — 유효한 SubmitDiagnosisInput:
  ```typescript
  export const mockValidDiagnosisInput: SubmitDiagnosisInput = {
    lead: { name: "김전문", contact: "expert@example.com", channel: "지인 추천" },
    answers: QUESTIONS.map(q => ({
      questionCode: q.code,
      answerText: `${q.code}에 대한 충분한 답변 내용입니다 테스트용`,
    })),
    consentChecked: true,
  }
  ```
- [ ] 성공 응답 Mock:
  ```typescript
  export const mockDiagnosisSuccessOutput: SubmitDiagnosisOutput = {
    success: true,
    diagnosisId: "mock-diagnosis-001",
    reportStatus: "draft",
    message: "진단이 정상 제출되었습니다. 검수 후 리포트를 안내드립니다.",
  }
  ```
- [ ] 실패 케이스 Mock — 답변 3단어 미만:
  ```typescript
  export const mockInvalidShortAnswer = {
    ...mockValidDiagnosisInput,
    answers: QUESTIONS.map((q, i) => ({
      questionCode: q.code,
      answerText: i === 0 ? "두 단어" : `${q.code}에 대한 충분한 답변입니다 테스트`,
    })),
  }
  ```
- [ ] 실패 케이스 Mock — 연락처 미입력:
  ```typescript
  export const mockInvalidNoContact = {
    ...mockValidDiagnosisInput,
    lead: { name: "김전문", contact: "" },
  }
  ```
- [ ] AI 실패 시 부분 성공 응답 Mock:
  ```typescript
  export const mockDiagnosisAiFailOutput: SubmitDiagnosisOutput = {
    success: true,
    diagnosisId: "mock-diagnosis-002",
    reportStatus: "report_pending",
    message: "답변이 저장되었습니다. 검수 후 안내드리겠습니다.",
  }
  ```
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 성공 Mock 데이터 스키마 준수**
- Given: mockValidDiagnosisInput이 정의됨
- When: `SubmitDiagnosisInputSchema.parse(mockValidDiagnosisInput)`를 실행함
- Then: 검증이 성공한다

**Scenario 2: 실패 Mock 데이터 스키마 위반**
- Given: mockInvalidShortAnswer가 정의됨
- When: `SubmitDiagnosisInputSchema.parse(mockInvalidShortAnswer)`를 실행함
- Then: ZodError가 발생한다 (3단어 미만)

**Scenario 3: 16문항 코드 완전성**
- Given: mockValidDiagnosisInput.answers가 정의됨
- When: questionCode 목록을 추출함
- Then: DATA-001의 QUESTION_CODES와 동일하다

## :gear: Technical & Non-Functional Constraints
- Mock 데이터는 테스트와 FE 개발 양쪽에서 사용 — fixture 패턴으로 구현
- QUESTIONS 배열(DATA-001)을 import하여 questionCode 일관성 보장
- 한글 텍스트 사용 — 실제 5060 전문가 답변 톤 유지

## :checkered_flag: Definition of Done (DoD)
- [ ] 성공/실패 Mock 데이터 각 최소 2종 이상 정의
- [ ] 성공 Mock이 SubmitDiagnosisInputSchema 검증 통과
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** DATA-001 (QUESTIONS 배열), API-002 (SubmitDiagnosisInput/Output 타입)
- **Blocks:** FE-001 (폼 검증 개발 시 테스트 데이터), FE-002 (제출 연동 개발), MOCK-003 (관리자 화면 Mock)
