---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-001: 16문항 진단 폼 클라이언트 유효성 검증 로직"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-001] 16문항 진단 폼 클라이언트 유효성 검증 로직
- 목적: 16문항 진단 폼(Q-002) 제출 전, 브라우저 단에서 즉시 피드백을 제공하여 서버 부하를 줄이고 사용자 경험을 개선한다. Zod + React Hook Form 조합으로 필수 입력, 3단어 검사를 수행한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: REQ-FREE-FUNC-003, 004 (필수 입력, 3단어 이상 검증)
- DTO 참조: API-002 (SubmitDiagnosisInputSchema)
- UI: Q-002

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/app/diagnose/page.tsx` 또는 폼 컴포넌트 내부에 `react-hook-form` 설정
- [ ] Zod Resolver 적용 (`@hookform/resolvers/zod` 사용)
- [ ] `SubmitDiagnosisInputSchema`를 리졸버로 주입:
  ```typescript
  const form = useForm<SubmitDiagnosisInput>({
    resolver: zodResolver(SubmitDiagnosisInputSchema),
    defaultValues: {
      lead: { name: "", contact: "", channel: "" },
      answers: QUESTIONS.map(q => ({ questionCode: q.code, answerText: "" })),
      consentChecked: false,
    }
  })
  ```
- [ ] 오류 메시지 표시 로직 구현 (각 Textarea 및 Input 하단에 빨간색 텍스트로 에러 표시)
- [ ] 3단어 미만 입력 시 실시간/제출 시점 에러 피드백
- [ ] 개인정보 동의 체크박스 검증 연결

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 필수 필드 누락 시 제출 차단**
- Given: 리드 이름이나 연락처가 비어있음
- When: "제출하기" 버튼 클릭
- Then: 제출되지 않고 빈 필드 아래에 에러 메시지가 표시된다

**Scenario 2: 3단어 미만 답변 시 에러 표시**
- Given: 한 질문에 2단어만 입력함
- When: "제출하기" 버튼 클릭
- Then: 제출되지 않고 해당 질문 아래에 "3단어 이상 상세히 적어주세요" 에러가 표시된다

**Scenario 3: 모든 검증 통과 시 제출 동작**
- Given: 모든 필수값 입력, 16개 질문 모두 3단어 이상 입력, 동의 체크 완료
- When: "제출하기" 버튼 클릭
- Then: 검증을 통과하고 `onSubmit` 핸들러가 호출된다

## :gear: Technical & Non-Functional Constraints
- React Hook Form 최적화로 렌더링 성능 유지
- 클라이언트 검증을 통과해야만 서버(Server Action) 요청 발생 (보안/비용 효율)
- 스키마는 API-002를 그대로 재사용하여 FE/BE 규칙 단일화(SSOT)

## :checkered_flag: Definition of Done (DoD)
- [ ] react-hook-form + zodResolver 설정 완료
- [ ] 누락 필드/3단어 미만/동의 미체크에 대한 에러 UI 표시
- [ ] 검증 통과 시에만 Submit 핸들러 트리거
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** Q-002 (진단 폼 UI), API-002 (Zod Schema)
- **Blocks:** FE-002 (서버 액션 연동)
