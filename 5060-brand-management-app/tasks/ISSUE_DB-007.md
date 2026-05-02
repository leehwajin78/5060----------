---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-007: ReviewLog 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, backend, database, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-007] ReviewLog 테이블 스키마 및 마이그레이션 작성
- 목적: 관리자의 리포트 수정·승인·거부·재생성 요청 이력을 불변 기록으로 저장하는 ReviewLog 모델을 정의한다. 변경 전/후 JSON 스냅샷(beforeJson/afterJson)을 보관하여 검수 과정의 감사 추적(Audit Trail)을 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#Appendix A — Prisma Schema (ReviewLog 모델)`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 585~594
- ERD: SRS Appendix E — ReviewLog 엔터티 (Lines 846~854)
- 기능 요구사항:
  - REQ-FREE-FUNC-032 (관리자 리포트 수정 → beforeJson/afterJson 저장)
  - REQ-FREE-FUNC-033 (관리자 승인/거부 → action 기록)
- 시퀀스 다이어그램: SRS §3.4 시퀀스 2 (관리자 검수 → 승인)
- AI 코딩 Prompt 4: SRS Appendix D — "ReviewLog에 action, note, beforeJson, afterJson을 저장"

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/schema.prisma`에 ReviewLog 모델 추가:
  ```prisma
  model ReviewLog {
    id         String   @id @default(cuid())
    reportId   String
    report     Report   @relation(fields: [reportId], references: [id])
    action     String   // "approve" | "reject" | "modify" | "regenerate_request"
    note       String?
    beforeJson Json?
    afterJson  Json?
    createdAt  DateTime @default(now())
  }
  ```
- [ ] Report 모델에 `reviewLogs ReviewLog[]` 관계 필드 존재 확인 (DB-005에서 선언)
- [ ] `npx prisma validate` 실행
- [ ] `npx prisma migrate dev --name add-reviewlog-table` 실행
- [ ] 마이그레이션 SQL 파일 생성 확인
- [ ] ReviewLog 레코드 생성 및 Report 관계 조회 동작 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: ReviewLog 테이블 정상 생성**
- Given: ReviewLog 모델이 schema.prisma에 정의됨
- When: `npx prisma migrate dev --name add-reviewlog-table`을 실행함
- Then: 로컬 DB에 ReviewLog 테이블이 reportId FK와 함께 생성된다

**Scenario 2: 승인 이력 기록**
- Given: Report R이 draft 상태로 존재함
- When: 관리자가 승인하여 `prisma.reviewLog.create({ data: { reportId: R, action: "approve", note: "승인 완료" } })`를 실행함
- Then: ReviewLog 레코드가 action="approve"로 생성된다

**Scenario 3: 수정 이력 — beforeJson/afterJson 저장**
- Given: Report R의 reportJson이 `{ summary: "원본" }`임
- When: 관리자가 summary를 수정하여 ReviewLog를 생성함 (`beforeJson: { summary: "원본" }, afterJson: { summary: "수정됨" }`)
- Then: beforeJson과 afterJson이 각각 수정 전/후 JSON으로 정확히 저장된다

**Scenario 4: Report → ReviewLog 관계 조회**
- Given: Report R에 연결된 ReviewLog가 3건 존재함 (modify, modify, approve 순서)
- When: `prisma.report.findUnique({ where: { id: R }, include: { reviewLogs: true } })`를 실행함
- Then: reviewLogs 배열에 3건이 createdAt 순서대로 포함된다

**Scenario 5: note nullable**
- Given: 관리자가 메모 없이 거부함
- When: note를 지정하지 않고 ReviewLog를 생성함
- Then: note가 null로 저장되며 에러가 발생하지 않는다

## :gear: Technical & Non-Functional Constraints
- ReviewLog.action 허용값: `"approve" | "reject" | "modify" | "regenerate_request"` (SRS Appendix A)
- ReviewLog.beforeJson / afterJson: Prisma `Json?` — 수정 시 변경 전/후 스냅샷 저장
  - action이 "approve"/"reject"인 경우 afterJson은 null일 수 있음
  - action이 "modify"인 경우 반드시 beforeJson/afterJson 모두 기록 (C-009에서 로직 구현)
- ReviewLog는 불변 레코드 — 생성만 가능, 수정/삭제 불가 (Append-only audit trail)
- Report:ReviewLog = 1:N 관계

## :checkered_flag: Definition of Done (DoD)
- [ ] `prisma/schema.prisma`에 ReviewLog 모델이 SRS 명세대로 정의됨
- [ ] Report → ReviewLog FK 관계 정상 동작
- [ ] action, note, beforeJson, afterJson 필드 저장/조회 정상
- [ ] `npx prisma validate` 에러 0건
- [ ] `npx prisma migrate dev` 성공
- [ ] `npm run build` 에러 0건 유지

## :construction: Dependencies & Blockers
- **Depends on:** DB-005 (Report — reportId FK 참조)
- **Blocks:** API-005 (reviewReport DTO), C-009 (ReviewLog 생성 로직), T-010 (승인/거부 + ReviewLog 생성 테스트)
