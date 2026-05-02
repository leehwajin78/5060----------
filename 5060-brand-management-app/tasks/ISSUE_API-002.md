---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-002: submitDiagnosis Server Action Request/Response DTO 정의"
labels: 'feature, backend, contract, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [API-002] submitDiagnosis Server Action Request/Response DTO 정의
- 목적: 16문항 진단 제출의 전체 페이로드(리드 정보 + 16개 답변 배열)를 수집하는 `submitDiagnosis` Server Action의 입출력 타입을 Zod 스키마 기반으로 정의한다. 가장 복잡한 Server Action이므로, 리드 검증(API-001)과 답변 검증(3단어 미만 차단)을 통합한 계약이 필요하다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§3.3 Server Actions — submitDiagnosis()`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 260~263
- 시퀀스 다이어그램: SRS §3.4 시퀀스 1 (고객 진단 제출 → AI 리포트 생성) — Lines 289~312
- 기능 요구사항:
  - REQ-FREE-FUNC-003 (이름 + 연락처 최소 1개 필수)
  - REQ-FREE-FUNC-004 (답변 3단어 미만/공백 차단)
  - REQ-FREE-FUNC-011 (16문항 답변 원문 질문 코드와 함께 저장)
  - REQ-FREE-FUNC-012 (Diagnosis.status 정상 저장)
- DB 모델: Lead + Diagnosis + Answer (SRS Appendix A)
- 16문항 코드: Q1·Q2·Q4·Q6·Q7·Q8·Q9·Q11·Q13·Q15·Q26·Q28·Q33·Q40·Q41·Q42

## :white_check_mark: Task Breakdown (실행 계획)

### Request DTO

| 필드 | 타입 | 필수 | 검증 조건 | 설명 |
|---|---|---|---|---|
| leadInfo.name | string | Y | 1자 이상 50자 이하 | 신청자 이름 |
| leadInfo.contact | string | Y | 이메일 또는 전화번호 형식 | 연락처 |
| leadInfo.channel | string | N | 100자 이하 | 유입 채널 |
| answers | array | Y | 정확히 16개 | 진단 답변 목록 |
| answers[].questionCode | string | Y | Q01~Q16 | 질문 코드 |
| answers[].answerText | string | Y | 3단어 이상, 공백만 입력 불가 | 답변 내용 |

### 처리 기준

1. leadInfo 검증
2. answers 배열 개수 검증
3. questionCode 중복 여부 검증
4. answerText 공백 제거 후 3단어 미만 여부 검증
5. transaction으로 Lead, Diagnosis, Answer 16건 저장
6. Diagnosis.status=submitted 또는 report_pending으로 저장

### 예외 처리

| 상황 | 처리 |
|---|---|
| 연락처 없음 | 400 validation error |
| 답변 16개 미만 | 422 validation error |
| questionCode 중복 | 422 validation error |
| 3단어 미만 답변 | 422 validation error |
| DB 저장 실패 | 500 internal error |

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 정상 진단 제출 검증 성공**
- Given: 이름, 연락처, 동의 체크, 16개 답변(각 3단어 이상)이 주어짐
- When: `SubmitDiagnosisInputSchema.parse(input)`를 실행함
- Then: 검증이 성공하고 파싱된 객체가 반환되며, DB 저장 후 Diagnosis 1건과 Answer 16건이 정상 생성됨.

**Scenario 2: 유효성 검사 실패 시 에러 응답**
- Given: 답변이 3단어 미만이거나 누락된 필드가 있음
- When: 입력값을 검증함
- Then: ZodError가 발생하며 DB 저장 없이 적절한 검증 에러(422/400)가 반환됨.

## :gear: Technical & Non-Functional Constraints
- 3단어 판별 기준: `str.trim().split(/\s+/).filter(Boolean).length >= 3` — 한글은 띄어쓰기 기준
- answers 배열은 정확히 16건 (`.length(16)`)
- questionCode는 DATA-001의 QUESTION_CODES와 교차 검증 (커스텀 `.refine()`)
- consentChecked: 개인정보 수집·AI 처리 동의 (REQ-NF-FREE-031, DPR-001 연계)
- Server Action 반환 타입은 직렬화 가능 JSON (Next.js 제약)
- AI 리포트 생성 실패해도 답변 데이터는 보존 → reportStatus를 "report_pending"으로 반환 (REQ-FREE-FUNC-022)

## :checkered_flag: Definition of Done (DoD)
- [ ] `src/lib/schemas/diagnosis.schema.ts` 파일 생성됨
- [ ] AnswerInputSchema, SubmitDiagnosisInputSchema가 Zod로 정의됨
- [ ] SubmitDiagnosisInput, SubmitDiagnosisOutput 타입이 export됨
- [ ] 3단어 미만 차단, 16건 배열 검증, 동의 체크 검증 동작 확인
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** DB-002 (Lead 필드 구조), DB-003 (Diagnosis 필드 구조), DB-004 (Answer 필드 구조), DATA-001 (16문항 코드 목록 — questionCode 교차 검증)
- **Blocks:** C-002 (submitDiagnosis 유효성 검증 로직), C-003 (submitDiagnosis DB 저장 로직), FE-001 (폼 클라이언트 검증), FE-002 (폼 제출 연동), T-001 (연락처 차단 테스트), T-002 (3단어 차단 테스트), T-004 (Answer 16건 저장 테스트)
