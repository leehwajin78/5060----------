---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] C-002: submitDiagnosis 입력 유효성 검증 로직"
labels: 'feature, backend, command, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [C-002] submitDiagnosis 입력 유효성 검증 로직
- 목적: 16문항 진단 제출의 전체 입력(리드 정보 + 16개 답변 + 동의 체크)을 서버 측에서 Zod로 검증하는 로직을 구현한다. 3단어 미만 답변 차단, 16문항 누락 검사, questionCode 유효성 교차 검증을 포함하며, C-003(DB 저장)의 전처리 단계이다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: REQ-FREE-FUNC-004 (답변 3단어 미만/공백 차단), REQ-FREE-FUNC-011 (16문항 답변)
- DTO 참조: API-002 (SubmitDiagnosisInputSchema)
- 16문항 코드: DATA-001 (QUESTION_CODES)
- 에러 유틸리티: API-008 (formatZodError, ErrorCode)
- 시퀀스 1: SRS §3.4 Lines 296~300 — "Lead + Answer 유효성 검증"

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/actions/diagnosis.actions.ts` 파일 생성 (`"use server"`)
- [ ] `validateDiagnosisInput()` 검증 함수 구현:
  ```typescript
  import { SubmitDiagnosisInputSchema, SubmitDiagnosisInput } from "@/lib/schemas/diagnosis.schema"
  import { QUESTION_CODES } from "@/lib/questions"
  import { formatZodError, ErrorCode } from "@/lib/errors"

  export function validateDiagnosisInput(input: unknown) {
    // 1단계: Zod 구조 검증
    const parsed = SubmitDiagnosisInputSchema.safeParse(input)
    if (!parsed.success) {
      return { valid: false, error: formatZodError(parsed.error) }
    }

    // 2단계: questionCode 유효성 교차 검증
    const submittedCodes = parsed.data.answers.map(a => a.questionCode)
    const invalidCodes = submittedCodes.filter(c => !QUESTION_CODES.includes(c))
    if (invalidCodes.length > 0) {
      return {
        valid: false,
        error: {
          success: false,
          error: `유효하지 않은 질문 코드: ${invalidCodes.join(", ")}`,
          errorCode: ErrorCode.VALIDATION_FAILED,
        },
      }
    }

    // 3단계: 중복 questionCode 검사
    const uniqueCodes = new Set(submittedCodes)
    if (uniqueCodes.size !== 16) {
      return {
        valid: false,
        error: {
          success: false,
          error: "중복된 질문 코드가 포함되어 있습니다.",
          errorCode: ErrorCode.VALIDATION_FAILED,
        },
      }
    }

    return { valid: true, data: parsed.data }
  }
  ```
- [ ] 3단어 판별 로직이 Zod 스키마(API-002)에 이미 포함되어 있으므로, 이 함수에서는 추가 검증에 집중
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 정상 입력 검증 성공**
- Given: 유효한 리드 정보 + 16개 답변(각 3단어 이상) + 동의 체크가 주어짐
- When: `validateDiagnosisInput(input)`를 실행함
- Then: `{ valid: true, data: SubmitDiagnosisInput }` 이 반환된다

**Scenario 2: 3단어 미만 답변 차단**
- Given: answers[0].answerText가 "두 단어"(2단어)임
- When: `validateDiagnosisInput(input)`를 실행함
- Then: `{ valid: false, error: { fieldErrors: ... } }`가 반환되며, 3단어 미만 에러가 포함된다

**Scenario 3: 유효하지 않은 questionCode 차단**
- Given: answers 배열에 "Q99"(존재하지 않는 코드)가 포함됨
- When: `validateDiagnosisInput(input)`를 실행함
- Then: `{ valid: false }`가 반환되며, "유효하지 않은 질문 코드" 에러가 포함된다

**Scenario 4: 중복 questionCode 차단**
- Given: answers 배열에 "Q1"이 2번 포함됨 (15종 코드 + Q1 중복)
- When: `validateDiagnosisInput(input)`를 실행함
- Then: `{ valid: false }`가 반환되며, "중복된 질문 코드" 에러가 포함된다

**Scenario 5: 동의 미체크 차단**
- Given: consentChecked가 false임
- When: `validateDiagnosisInput(input)`를 실행함
- Then: `{ valid: false }`가 반환된다

**Scenario 6: 공백만 입력된 답변 차단**
- Given: answers[5].answerText가 "   "(공백만)임
- When: `validateDiagnosisInput(input)`를 실행함
- Then: `{ valid: false }`가 반환된다

## :gear: Technical & Non-Functional Constraints
- 3단 검증 파이프라인: Zod 구조 → questionCode 교차 → 중복 코드 검사
- 3단어 판별은 Zod 스키마(API-002)의 `.refine()`에서 처리 — 이 함수에서 중복 구현 불필요
- QUESTION_CODES(DATA-001)와의 교차 검증으로, 클라이언트에서 조작된 questionCode를 서버에서 차단
- 이 함수는 순수 검증 전용 — DB 저장은 C-003에서 수행 (관심사 분리)

## :checkered_flag: Definition of Done (DoD)
- [ ] `validateDiagnosisInput()` 함수 구현 완료
- [ ] 3단 검증(Zod + questionCode 교차 + 중복 코드) 동작 확인
- [ ] 6가지 시나리오 검증 동작 확인
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** API-002 (SubmitDiagnosisInputSchema), DATA-001 (QUESTION_CODES), API-008 (formatZodError)
- **Blocks:** C-003 (submitDiagnosis DB 저장 — validateDiagnosisInput 호출), T-001 (연락처 필수 테스트), T-002 (3단어 차단 테스트)
