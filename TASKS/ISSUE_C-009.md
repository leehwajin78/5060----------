---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] C-009: ReviewLog 생성 (Audit Trail) 로직"
labels: 'feature, backend, command, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [C-009] ReviewLog 생성 로직
- 목적: 관리자가 리포트에 가하는 모든 조작(수정, 승인, 거부)에 대해 불변의 감사 추적(Audit Trail) 기록을 남긴다. 이 로직은 C-007, C-008 내부 트랜잭션에서 호출되거나 재사용 가능한 유틸리티 형태로 구현된다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- DB 모델: ReviewLog (SRS Appendix A Lines 586~597)
- C-007 (리포트 수정), C-008 (승인/거부)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/services/review-log.service.ts` 파일 생성
- [ ] `createReviewLog(tx, data)` 형태의 유틸리티 함수 구현 (Prisma 트랜잭션 클라이언트 주입 지원):
  ```typescript
  import { Prisma } from "@prisma/client"

  type CreateReviewLogInput = {
    reportId: string
    action: string
    note?: string | null
    beforeJson: any
    afterJson: any
  }

  export async function createReviewLog(
    tx: Prisma.TransactionClient, 
    input: CreateReviewLogInput
  ) {
    return tx.reviewLog.create({
      data: {
        reportId: input.reportId,
        action: input.action,
        note: input.note,
        beforeJson: input.beforeJson,
        afterJson: input.afterJson,
      },
    })
  }
  ```
- [ ] C-007, C-008에서 인라인으로 구현된 ReviewLog 생성 코드를 이 유틸리티로 리팩토링 (선택 사항)

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: ReviewLog 정상 생성**
- Given: 트랜잭션 컨텍스트와 유효한 입력이 주어짐
- When: `createReviewLog(tx, input)`를 실행함
- Then: ReviewLog 레코드가 생성되어 반환된다

## :gear: Technical & Non-Functional Constraints
- 감사 추적(Audit Trail) 목적이므로 수정/삭제 기능 없음 (Append-only)
- 트랜잭션 내부에서 실행되어야 하므로 `tx` 객체를 매개변수로 받아야 함

## :checkered_flag: Definition of Done (DoD)
- [ ] createReviewLog 유틸리티 구현
- [ ] 트랜잭션 주입 지원
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** DB-007 (ReviewLog)
- **Blocks:** C-007, C-008 (호출부)
