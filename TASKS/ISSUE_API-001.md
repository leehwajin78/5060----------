---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-001: createLead Server Action Request/Response DTO 정의"
labels: 'feature, backend, contract, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [API-001] createLead Server Action Request/Response DTO 정의
- 목적: 리드 정보(이름, 연락처, 유입경로)를 수집하는 `createLead` Server Action의 입출력 타입을 Zod 스키마 기반으로 정의한다. 프론트엔드 폼 데이터와 백엔드 저장 로직 사이의 데이터 계약을 확립하여, 양측이 독립적으로 개발할 수 있도록 한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§3.3 Server Actions — createLead()`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 260~263
- 기능 요구사항:
  - REQ-FREE-FUNC-003 (이름, 이메일 또는 전화번호 중 최소 1개 연락처 필수)
  - REQ-FREE-FUNC-010 (리드 정보를 Lead 테이블에 저장)
  - S4 (이름, 이메일 또는 전화번호, 유입경로 저장)
- DB 모델: SRS Appendix A — Lead (id, name, contact, channel, createdAt)
- 에러 코드: API-008 (400 유효성 실패, 500 서버 오류)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/schemas/lead.schema.ts` 파일 생성
- [ ] CreateLeadInput Zod 스키마 정의:
  ```typescript
  import { z } from "zod"

  export const CreateLeadInputSchema = z.object({
    name: z.string().min(1, "이름은 필수입니다"),
    contact: z.string().min(1, "이메일 또는 전화번호는 필수입니다"),
    channel: z.string().optional(),
  })

  export type CreateLeadInput = z.infer<typeof CreateLeadInputSchema>
  ```
- [ ] CreateLeadOutput 타입 정의:
  ```typescript
  export type CreateLeadOutput = {
    success: true
    leadId: string
  } | {
    success: false
    error: string
    fieldErrors?: Record<string, string[]>
  }
  ```
- [ ] contact 필드 커스텀 검증 추가 — 이메일 형식 또는 전화번호 형식 중 하나에 부합하는지 (`.refine()`)
- [ ] TypeScript 컴파일 에러 0건 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 유효한 리드 정보 검증 성공**
- Given: `{ name: "홍길동", contact: "hong@example.com" }`이 주어짐
- When: `CreateLeadInputSchema.parse(input)`를 실행함
- Then: 검증이 성공하고 파싱된 객체가 반환된다

**Scenario 2: 이름 누락 시 검증 실패**
- Given: `{ name: "", contact: "hong@example.com" }`이 주어짐
- When: `CreateLeadInputSchema.parse(input)`를 실행함
- Then: ZodError가 발생하며 name 필드 에러 메시지가 포함된다

**Scenario 3: 연락처 누락 시 검증 실패**
- Given: `{ name: "홍길동", contact: "" }`이 주어짐
- When: `CreateLeadInputSchema.parse(input)`를 실행함
- Then: ZodError가 발생하며 contact 필드 에러 메시지가 포함된다

**Scenario 4: channel 생략 허용**
- Given: `{ name: "홍길동", contact: "010-1234-5678" }`이 주어짐 (channel 없음)
- When: `CreateLeadInputSchema.parse(input)`를 실행함
- Then: 검증이 성공하고 channel은 undefined로 처리된다

**Scenario 5: 전화번호 형식 연락처 허용**
- Given: `{ name: "홍길동", contact: "010-1234-5678" }`이 주어짐
- When: `CreateLeadInputSchema.parse(input)`를 실행함
- Then: 검증이 성공한다 (이메일 또는 전화번호 모두 허용)

**Scenario 6: CreateLeadOutput 성공 응답 구조**
- Given: Lead가 정상 생성됨
- When: 성공 응답을 구성함
- Then: `{ success: true, leadId: "cuid..." }` 구조가 반환된다

**Scenario 7: CreateLeadOutput 실패 응답 구조**
- Given: 검증 실패가 발생함
- When: 실패 응답을 구성함
- Then: `{ success: false, error: "메시지", fieldErrors: { name: ["..."] } }` 구조가 반환된다

## :gear: Technical & Non-Functional Constraints
- Lead.contact는 이메일 또는 전화번호 중 하나를 저장하는 단일 String 필드 (SRS Appendix A)
  - 엄격한 이메일/전화 형식 검증보다는 비어있지 않음(min 1) 검증이 MVP 우선
  - 고급 형식 검증은 `.refine()`으로 추가 가능하나, MVP에서는 선택 사항
- Server Action의 반환 타입은 직렬화 가능해야 함 (Next.js 제약 — 순수 JSON)
- fieldErrors는 Zod의 `flatten()` 결과와 호환되는 구조

## :checkered_flag: Definition of Done (DoD)
- [ ] `src/lib/schemas/lead.schema.ts` 파일 생성됨
- [ ] CreateLeadInputSchema가 Zod로 정의됨
- [ ] CreateLeadInput, CreateLeadOutput 타입이 export됨
- [ ] 유효/무효 입력에 대한 parse 동작 확인
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** DB-002 (Lead 모델 — 필드 구조 참조)
- **Blocks:** C-001 (createLead 비즈니스 로직), FE-001 (폼 유효성 검증 — 클라이언트 사이드 연동), FE-002 (폼 제출 Server Action 호출), T-003 (Lead 생성 테스트)
