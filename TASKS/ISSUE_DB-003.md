---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-003: Diagnosis 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, backend, database, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-003] Diagnosis 테이블 스키마 및 마이그레이션 작성
- 목적: 16문항 브랜드 진단의 제출 단위를 관리하는 Diagnosis 모델을 정의한다. Lead와 1:N 관계로 연결되며, 상태(status)를 통해 진단 흐름 전체의 진행 상황을 추적하는 핵심 엔터티이다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#Appendix A — Prisma Schema (Diagnosis 모델)`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 537~547
- ERD: SRS Appendix E — Diagnosis 엔터티 (Lines 811~819)
- 상태값 명세: SRS Appendix A 최소 상태값 — `submitted | report_pending | report_generated | reviewed`
- 기능 요구사항: SRS §4.1 F4-Lite — REQ-FREE-FUNC-012 (Diagnosis 상태 저장)
- 시퀀스 다이어그램: SRS §3.4 시퀀스 1 (고객 진단 제출 → AI 리포트 생성)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/schema.prisma`에 Diagnosis 모델 추가:
  ```prisma
  model Diagnosis {
    id        String   @id @default(cuid())
    leadId    String
    lead      Lead     @relation(fields: [leadId], references: [id])
    status    String   @default("submitted")
    // submitted | report_pending | report_generated | reviewed
    createdAt DateTime @default(now())
    answers   Answer[]
    reports   Report[]
    aiRuns    AiRun[]
  }
  ```
- [ ] Lead 모델에 `diagnoses Diagnosis[]` 관계 필드 확인 (DB-002에서 이미 추가됨)
- [ ] `npx prisma validate` 실행 — 스키마 유효성 검사 통과
- [ ] `npx prisma migrate dev --name add-diagnosis-table` 실행
- [ ] 마이그레이션 SQL 파일 생성 확인
- [ ] Diagnosis.status 기본값이 `"submitted"`로 설정되는지 확인
- [ ] Lead → Diagnosis FK 관계 정상 동작 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: Diagnosis 테이블 정상 생성**
- Given: Diagnosis 모델이 schema.prisma에 정의됨
- When: `npx prisma migrate dev --name add-diagnosis-table`을 실행함
- Then: 로컬 SQLite DB에 Diagnosis 테이블이 leadId FK와 함께 생성된다

**Scenario 2: Diagnosis 생성 시 기본 status**
- Given: Diagnosis 모델의 status 기본값이 `"submitted"`임
- When: `prisma.diagnosis.create({ data: { leadId: "valid-lead-id" } })`를 실행함
- Then: Diagnosis.status가 `"submitted"`로 저장된다

**Scenario 3: Lead-Diagnosis 관계 조회**
- Given: Lead A에 연결된 Diagnosis 2건이 존재함
- When: `prisma.lead.findUnique({ where: { id: A }, include: { diagnoses: true } })`를 실행함
- Then: diagnoses 배열에 2건의 Diagnosis가 포함되어 반환된다

**Scenario 4: 존재하지 않는 leadId로 생성 시 FK 에러**
- Given: 존재하지 않는 leadId 값이 주어짐
- When: 해당 leadId로 Diagnosis를 생성하려 시도함
- Then: Prisma가 Foreign Key 제약 위반 에러를 반환한다

## :gear: Technical & Non-Functional Constraints
- Diagnosis.status: `String` 타입으로 저장, 허용값은 `submitted | report_pending | report_generated | reviewed` (SRS Appendix A)
  - Prisma 레벨의 enum이 아닌 String + 애플리케이션 레벨 상수로 관리 (DATA-002에서 enum 상수 정의)
- Lead:Diagnosis = 1:N 관계 (`Lead ||--o{ Diagnosis`)
- Diagnosis:Answer = 1:N, Diagnosis:Report = 1:N, Diagnosis:AiRun = 1:N (관계 필드는 선언하되, Answer/Report/AiRun 모델은 DB-004~006에서 정의)
- 이 마이그레이션은 Lead 테이블이 먼저 존재해야 FK가 정상 생성됨

## :checkered_flag: Definition of Done (DoD)
- [ ] `prisma/schema.prisma`에 Diagnosis 모델이 SRS 명세대로 정의됨
- [ ] Lead → Diagnosis FK 관계가 정상 설정됨
- [ ] Diagnosis.status 기본값 `"submitted"` 확인
- [ ] `npx prisma validate` 에러 0건
- [ ] `npx prisma migrate dev` 성공
- [ ] Diagnosis CRUD + Lead 관계 조회 정상 동작
- [ ] `npm run build` 에러 0건 유지

## :construction: Dependencies & Blockers
- **Depends on:** DB-001 (Prisma 초기화), DB-002 (Lead 테이블 — FK 참조 대상)
- **Blocks:** DB-004 (Answer — diagnosisId FK), DB-005 (Report — diagnosisId FK), DB-006 (AiRun — diagnosisId FK), API-002 (submitDiagnosis DTO), C-002~C-003 (submitDiagnosis 로직), Q-003 (관리자 목록)
