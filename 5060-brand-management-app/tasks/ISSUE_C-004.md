---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] C-004: AI payload 구성 로직 (PII 마스킹 + 질문코드-답변 매핑)"
labels: 'feature, backend, command, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [C-004] AI payload 구성 로직
- 목적: DB에 저장된 Answer 16건을 조회하여 AI API(Gemini)에 전송할 payload를 구성한다. 핵심은 PII 마스킹 — 실명, 이메일, 전화번호를 payload에서 완전히 제외하고, 질문코드+답변 텍스트만 포함한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: REQ-FREE-FUNC-023 (AI API payload에 실명/이메일/전화번호 미포함)
- SRS 문서: REQ-NF-FREE-030 (AI API에 민감 정보 비전송)
- DTO 참조: API-003 (GenerateReportRequestSchema)
- AI 코딩 Prompt 3: SRS Appendix D Lines 738~756 — "답변 원문(질문코드+텍스트만) 전달"

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/services/ai-payload.service.ts` 파일 생성
- [ ] `buildAiPayload(diagnosisId)` 함수 구현:
  ```typescript
  import { prisma } from "@/lib/prisma"
  import { GenerateReportRequest } from "@/lib/schemas/ai-report.schema"

  export async function buildAiPayload(diagnosisId: string): Promise<GenerateReportRequest | null> {
    const answers = await prisma.answer.findMany({
      where: { diagnosisId },
      select: {
        questionCode: true,
        answerText: true,
        // ⚠️ 의도적으로 Lead 정보를 SELECT하지 않음 (PII 마스킹)
      },
      orderBy: { createdAt: "asc" },
    })

    if (answers.length !== 16) return null

    return {
      diagnosisId,
      answers: answers.map(a => ({
        questionCode: a.questionCode,
        answerText: a.answerText,
      })),
    }
  }
  ```
- [ ] PII 미포함 검증 — payload 객체에 name, contact, email, phone 키가 없음을 주석으로 명시
- [ ] payload null 반환 시(Answer 16건 미달) 호출 측에서 에러 처리 가이드
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: payload 정상 구성**
- Given: Diagnosis D에 Answer 16건이 존재함
- When: `buildAiPayload(D)`를 실행함
- Then: `{ diagnosisId: D, answers: [{questionCode, answerText}, ...] }` 16건이 반환된다

**Scenario 2: PII 미포함 확인**
- Given: payload가 구성됨
- When: payload 객체의 모든 키를 재귀 탐색함
- Then: name, contact, email, phone 키가 존재하지 않는다

**Scenario 3: Answer 16건 미달 시 null 반환**
- Given: Diagnosis D에 Answer가 15건만 존재함
- When: `buildAiPayload(D)`를 실행함
- Then: null이 반환된다

**Scenario 4: 질문 코드 순서 보존**
- Given: Answer가 createdAt 순서로 생성됨
- When: payload.answers의 순서를 확인함
- Then: createdAt 오름차순(생성 순서)으로 정렬되어 있다

## :gear: Technical & Non-Functional Constraints
- Prisma `select`에서 Lead 관계를 명시적으로 제외 — ORM 레벨 PII 마스킹
- payload는 GenerateReportRequest 타입(API-003)에 정확히 부합해야 함
- Answer 16건 미달은 데이터 무결성 문제 — null 반환 후 상위에서 에러 처리
- 이 함수는 C-005(AI 리포트 생성)에서 호출됨

## :checkered_flag: Definition of Done (DoD)
- [ ] buildAiPayload() 함수 구현 완료
- [ ] PII 미포함 — payload에 name/contact/email/phone 없음 확인
- [ ] Answer 16건 정상 / 미달 시 null 반환 동작 확인
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** DB-004 (Answer 테이블), API-003 (GenerateReportRequest 타입), DB-001 (Prisma Client)
- **Blocks:** C-005 (AI 리포트 생성 — payload 입력), SEC-001 (PII 마스킹 검증), T-007 (PII 미포함 테스트)
