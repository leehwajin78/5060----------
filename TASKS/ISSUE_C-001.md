---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] C-001: createLead Server Action 비즈니스 로직 구현"
labels: 'feature, backend, command, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [C-001] createLead Server Action 비즈니스 로직
- 목적: 리드 정보(이름, 연락처, 유입경로)를 Zod 검증 후 DB에 저장하는 Server Action을 구현한다. 진단 폼 제출 플로우에서 submitDiagnosis(C-003) 내부에서 호출되거나, 독립적으로 사용될 수 있다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§3.3 Server Actions — createLead()`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 260~263
- DTO 참조: API-001 (CreateLeadInputSchema, CreateLeadOutput)
- 에러 유틸리티: API-008 (formatZodError)
- 기능 요구사항: REQ-FREE-FUNC-003 (이름+연락처 필수), REQ-FREE-FUNC-010 (Lead 테이블 저장)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/actions/lead.actions.ts` 파일 생성 (`"use server"`)
- [ ] `createLead()` Server Action 구현:
  ```typescript
  "use server"
  import { CreateLeadInputSchema, CreateLeadOutput } from "@/lib/schemas/lead.schema"
  import { prisma } from "@/lib/prisma"
  import { formatZodError } from "@/lib/errors"

  export async function createLead(input: unknown): Promise<CreateLeadOutput> {
    // 1. Zod 검증
    const parsed = CreateLeadInputSchema.safeParse(input)
    if (!parsed.success) {
      return formatZodError(parsed.error)
    }

    try {
      // 2. DB 저장
      const lead = await prisma.lead.create({
        data: {
          name: parsed.data.name,
          contact: parsed.data.contact,
          channel: parsed.data.channel ?? null,
        },
      })

      // 3. 성공 응답
      return { success: true, leadId: lead.id }
    } catch (error) {
      console.error("[createLead] DB Error:", error)
      return { success: false, error: "리드 정보 저장에 실패했습니다." }
    }
  }
  ```
- [ ] 에러 로깅: try-catch에서 console.error로 서버 로그 기록
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 유효한 리드 생성 성공**
- Given: `{ name: "김전문", contact: "expert@example.com", channel: "지인 추천" }`이 주어짐
- When: `createLead(input)`를 실행함
- Then: `{ success: true, leadId: "cuid..." }`가 반환되고, DB에 Lead 레코드가 존재한다

**Scenario 2: 이름 누락 시 Zod 검증 실패**
- Given: `{ name: "", contact: "test@test.com" }`이 주어짐
- When: `createLead(input)`를 실행함
- Then: `{ success: false, errorCode: "VALIDATION_FAILED", fieldErrors: { name: [...] } }`가 반환된다

**Scenario 3: 연락처 누락 시 검증 실패**
- Given: `{ name: "홍길동", contact: "" }`이 주어짐
- When: `createLead(input)`를 실행함
- Then: `{ success: false, fieldErrors: { contact: [...] } }`가 반환된다

**Scenario 4: channel 생략 시 null 저장**
- Given: `{ name: "홍길동", contact: "010-1234-5678" }`이 주어짐 (channel 없음)
- When: `createLead(input)`를 실행함
- Then: Lead 레코드의 channel이 null로 저장된다

**Scenario 5: DB 에러 시 graceful 실패**
- Given: DB 연결에 문제가 있음
- When: `createLead(input)`를 실행함
- Then: `{ success: false, error: "리드 정보 저장에 실패했습니다." }`가 반환되고 console.error 로그가 기록된다

## :gear: Technical & Non-Functional Constraints
- Next.js Server Action (`"use server"`) — 클라이언트에서 직접 호출 가능
- 입력은 `unknown` 타입으로 받아 Zod `safeParse`로 검증 (타입 안전성)
- DB 에러는 사용자에게 구체적 메시지 노출 금지 — 일반 에러 메시지 반환
- 이 함수는 C-003(submitDiagnosis) 내부에서도 호출될 수 있음

## :checkered_flag: Definition of Done (DoD)
- [ ] `createLead()` Server Action 구현 완료
- [ ] Zod 검증 → DB 저장 → 성공/실패 응답 플로우 동작 확인
- [ ] 유효/무효 입력 5가지 시나리오 동작 확인
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** DB-002 (Lead 테이블), API-001 (CreateLeadInputSchema), API-008 (formatZodError), DB-001 (Prisma Client)
- **Blocks:** C-003 (submitDiagnosis — Lead 생성 포함), FE-002 (폼 제출 연동), T-003 (Lead 생성 테스트)
