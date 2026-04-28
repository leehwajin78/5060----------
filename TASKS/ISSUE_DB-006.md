---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-006: AiRun 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, backend, database, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-006] AiRun 테이블 스키마 및 마이그레이션 작성
- 목적: AI API(Gemini) 호출 1회를 추적하는 AiRun 모델을 정의한다. 생성/재생성 요청의 성공·실패 상태, 소요 시간, 오류 메시지를 기록하여 AI 호출 로그 및 호출 횟수 제한(진단당 최대 2회)의 기반을 마련한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#Appendix A — Prisma Schema (AiRun 모델)`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 571~583
- ERD: SRS Appendix E — AiRun 엔터티 (Lines 837~845)
- 상태값: SRS Appendix A — `pending | processing | completed | failed`
- 기능 요구사항:
  - S12 (최소 AI 호출 로그 — 성공/실패, 생성 시간, 오류 메시지)
  - REQ-FREE-FUNC-022 (AI 생성 실패 시 실패 상태 기록)
  - REQ-NF-FREE-023 (AI 호출 1회 진단당 기본 1회 + 재생성 1회 제한)
- 용어 정의: SRS §1.3 — AiRun: "AI 호출 1회를 추적하는 DB 모델"

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/schema.prisma`에 AiRun 모델 추가:
  ```prisma
  model AiRun {
    id           String     @id @default(cuid())
    diagnosisId  String?
    diagnosis    Diagnosis? @relation(fields: [diagnosisId], references: [id])
    taskType     String     // "generateReport" | "regenerateReport"
    provider     String     @default("gemini")
    status       String     @default("pending")
    // pending | processing | completed | failed
    errorMessage String?
    startedAt    DateTime?
    completedAt  DateTime?
    createdAt    DateTime   @default(now())
  }
  ```
- [ ] Diagnosis 모델에 `aiRuns AiRun[]` 관계 필드 존재 확인 (DB-003에서 선언)
- [ ] `npx prisma validate` 실행
- [ ] `npx prisma migrate dev --name add-airun-table` 실행
- [ ] 마이그레이션 SQL 파일 생성 확인
- [ ] AiRun.status 기본값 `"pending"`, provider 기본값 `"gemini"` 확인
- [ ] AiRun.diagnosisId nullable 확인 (orphan 허용)

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: AiRun 테이블 정상 생성**
- Given: AiRun 모델이 schema.prisma에 정의됨
- When: `npx prisma migrate dev --name add-airun-table`을 실행함
- Then: 로컬 DB에 AiRun 테이블이 생성된다

**Scenario 2: AI 호출 시작 기록**
- Given: 진단 제출 후 AI 리포트 생성 요청이 발생함
- When: `prisma.aiRun.create({ data: { diagnosisId: D, taskType: "generateReport", status: "processing", startedAt: new Date() } })`를 실행함
- Then: AiRun 레코드가 status="processing", provider="gemini"으로 생성된다

**Scenario 3: AI 호출 성공 기록**
- Given: AiRun 레코드가 status="processing"으로 존재함
- When: `prisma.aiRun.update({ where: { id }, data: { status: "completed", completedAt: new Date() } })`를 실행함
- Then: status가 "completed"로, completedAt이 현재 시각으로 업데이트된다

**Scenario 4: AI 호출 실패 기록**
- Given: Gemini API 호출이 실패함
- When: `prisma.aiRun.update({ where: { id }, data: { status: "failed", errorMessage: "API timeout", completedAt: new Date() } })`를 실행함
- Then: status="failed", errorMessage="API timeout"으로 저장된다

**Scenario 5: diagnosisId nullable**
- Given: diagnosisId가 nullable로 정의됨
- When: diagnosisId 없이 AiRun을 생성함
- Then: diagnosisId가 null로 저장되며 에러가 발생하지 않는다

**Scenario 6: 진단별 AiRun 카운트 조회**
- Given: Diagnosis D에 연결된 AiRun이 2건 존재 (generateReport 1건 + regenerateReport 1건)
- When: `prisma.aiRun.count({ where: { diagnosisId: D } })`를 실행함
- Then: 2가 반환된다 (호출 횟수 제한 검증 기반)

## :gear: Technical & Non-Functional Constraints
- AiRun.taskType: `"generateReport" | "regenerateReport"` — 초기 생성과 재생성을 구분
- AiRun.provider: 기본값 `"gemini"` — 향후 모델 전환 대비
- AiRun.diagnosisId: `String?` (nullable) — Diagnosis 관계가 optional (SRS 명세)
- AI 호출 횟수 제한: 진단당 기본 1회 + 관리자 재생성 1회 = 최대 2회 (REQ-NF-FREE-023)
  - 제한 로직 자체는 C-010에서 구현, 이 태스크는 카운트 조회 기반만 제공
- startedAt/completedAt: nullable DateTime — 소요 시간 계산용

## :checkered_flag: Definition of Done (DoD)
- [ ] `prisma/schema.prisma`에 AiRun 모델이 SRS 명세대로 정의됨
- [ ] Diagnosis → AiRun FK 관계 정상 (nullable)
- [ ] status 기본값 `"pending"`, provider 기본값 `"gemini"` 확인
- [ ] `npx prisma validate` 에러 0건
- [ ] `npx prisma migrate dev` 성공
- [ ] AiRun CRUD + 성공/실패 상태 전환 동작 확인
- [ ] `npm run build` 에러 0건 유지

## :construction: Dependencies & Blockers
- **Depends on:** DB-003 (Diagnosis — diagnosisId FK 참조)
- **Blocks:** API-006 (regenerateReport DTO), C-006 (AI 실패 처리 로직), C-010 (재생성 호출 횟수 제한), Q-009 (AiRun 로그 조회), LOG-001 (AI 호출 로깅), T-006 (AI 실패 테스트), T-014 (호출 횟수 제한 테스트)
