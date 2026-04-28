---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-005: Report 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, backend, database, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-005] Report 테이블 스키마 및 마이그레이션 작성
- 목적: AI 진단 리포트와 관리자 검수 상태를 저장하는 Report 모델을 정의한다. `reportJson`(JSON 타입)에 Zod 검증을 통과한 리포트 구조가 저장되며, `status` 필드를 통해 draft → approved/rejected 승인 게이트를 구현하는 핵심 엔터티이다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#Appendix A — Prisma Schema (Report 모델)`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 558~569
- ERD: SRS Appendix E — Report 엔터티 (Lines 827~836)
- 상태값 명세: SRS Appendix A — `draft | approved | rejected | regeneration_requested`
- 기능 요구사항:
  - REQ-FREE-FUNC-020 (AI 진단 리포트 생성 → JSON 저장)
  - REQ-FREE-FUNC-032 (관리자 리포트 수정)
  - REQ-FREE-FUNC-033 (관리자 승인/거부)
  - REQ-FREE-FUNC-034 (미승인 리포트 고객 비공개)
  - REQ-FREE-FUNC-040 (승인 리포트 웹뷰 표시)
- AI 리포트 JSON Schema: SRS Appendix B (Lines 603~632)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/schema.prisma`에 Report 모델 추가:
  ```prisma
  model Report {
    id          String      @id @default(cuid())
    diagnosisId String
    diagnosis   Diagnosis   @relation(fields: [diagnosisId], references: [id])
    status      String      @default("draft")
    // draft | approved | rejected | regeneration_requested
    reportJson  Json?       // AI 생성 리포트 JSON (Zod 검증 통과)
    reviewNote  String?     // 관리자 수정 메모
    createdAt   DateTime    @default(now())
    updatedAt   DateTime    @updatedAt
    reviewLogs  ReviewLog[]
  }
  ```
- [ ] Diagnosis 모델에 `reports Report[]` 관계 필드 존재 확인 (DB-003에서 선언)
- [ ] `npx prisma validate` 실행
- [ ] `npx prisma migrate dev --name add-report-table` 실행
- [ ] 마이그레이션 SQL 파일 생성 확인
- [ ] Report.status 기본값 `"draft"` 자동 설정 확인
- [ ] Report.reportJson에 JSON 객체 저장/조회 동작 확인
- [ ] Report.updatedAt `@updatedAt` 자동 갱신 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: Report 테이블 정상 생성**
- Given: Report 모델이 schema.prisma에 정의됨
- When: `npx prisma migrate dev --name add-report-table`을 실행함
- Then: 로컬 DB에 Report 테이블이 diagnosisId FK와 함께 생성된다

**Scenario 2: Report 생성 시 기본 status = draft**
- Given: Report 모델의 status 기본값이 `"draft"`임
- When: `prisma.report.create({ data: { diagnosisId: "valid-id", reportJson: { summary: "..." } } })`를 실행함
- Then: Report.status가 `"draft"`로 저장된다

**Scenario 3: reportJson에 JSON 객체 저장·조회**
- Given: DiagnosisReport 구조의 JSON 객체가 준비됨
- When: Report.reportJson 필드에 해당 JSON을 저장하고 다시 조회함
- Then: 저장한 JSON 구조가 그대로 반환된다 (필드 손실 없음)

**Scenario 4: reportJson nullable — AI 실패 시 null 허용**
- Given: AI 리포트 생성이 실패한 상황
- When: `prisma.report.create({ data: { diagnosisId: "valid-id" } })`를 실행함 (reportJson 미지정)
- Then: Report.reportJson이 null로 저장되며 에러가 발생하지 않는다

**Scenario 5: updatedAt 자동 갱신**
- Given: Report 레코드가 존재함
- When: Report.status를 `"approved"`로 업데이트함
- Then: Report.updatedAt이 현재 시각으로 자동 갱신된다

**Scenario 6: Diagnosis → Report 관계 조회**
- Given: Diagnosis D에 연결된 Report 1건이 존재함
- When: `prisma.diagnosis.findUnique({ where: { id: D }, include: { reports: true } })`를 실행함
- Then: reports 배열에 1건의 Report가 포함되어 반환된다

## :gear: Technical & Non-Functional Constraints
- Report.reportJson: Prisma `Json?` 타입 — SQLite에서도 JSON 저장 지원 (문자열 직렬화)
- Report.status 허용값: `draft | approved | rejected | regeneration_requested` (SRS Appendix A)
  - `approved` 상태만 고객 공개 (REQ-FREE-FUNC-034, REQ-NF-FREE-033)
- Report.reviewNote: 관리자 수정 메모용 — nullable
- Diagnosis:Report = 1:N, Report:ReviewLog = 1:N
- `@updatedAt`으로 최종 수정 시각 자동 추적

## :checkered_flag: Definition of Done (DoD)
- [ ] `prisma/schema.prisma`에 Report 모델이 SRS 명세대로 정의됨
- [ ] Diagnosis → Report FK 관계 정상 동작
- [ ] status 기본값 `"draft"`, reportJson nullable, updatedAt 자동 갱신 확인
- [ ] `npx prisma validate` 에러 0건
- [ ] `npx prisma migrate dev` 성공
- [ ] Report CRUD + JSON 저장/조회 정상 동작
- [ ] `npm run build` 에러 0건 유지

## :construction: Dependencies & Blockers
- **Depends on:** DB-003 (Diagnosis — diagnosisId FK 참조)
- **Blocks:** DB-007 (ReviewLog — reportId FK), API-003 (generate-report DTO), API-005 (reviewReport DTO), API-007 (reports/[id] DTO), C-005 (AI 리포트 저장), C-007~C-009 (reviewReport 로직), Q-005 (리포트 웹뷰), Q-008 (승인 리포트 조회), FE-005 (접근 제어)
