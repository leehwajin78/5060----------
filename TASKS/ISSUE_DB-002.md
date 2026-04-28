---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-002: Lead 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, backend, database, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-002] Lead 테이블 스키마 및 마이그레이션 작성
- 목적: 파일럿 고객의 이름, 연락처(이메일 또는 전화번호), 유입경로를 저장하는 Lead 모델을 Prisma 스키마에 정의하고 마이그레이션을 실행하여, 리드 정보 수집의 데이터 기반을 확보한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#Appendix A — Prisma Schema (Lead 모델)`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 528~535
- ERD: SRS Appendix E — Lead 엔터티 (Lines 803~810)
- 기능 요구사항: SRS §4.1 F4-Lite — REQ-FREE-FUNC-010 (리드 정보 Lead 테이블 저장)
- 데이터 모델: SRS Appendix A 필수 엔터티 — Lead (필수)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/schema.prisma`에 Lead 모델 추가:
  ```prisma
  model Lead {
    id        String      @id @default(cuid())
    name      String
    contact   String      // 이메일 또는 전화번호
    channel   String?     // 유입 경로 (nullable)
    createdAt DateTime    @default(now())
    diagnoses Diagnosis[]
  }
  ```
- [ ] `npx prisma validate` 실행 — 스키마 유효성 검사 통과
- [ ] `npx prisma migrate dev --name add-lead-table` 실행 — SQLite 로컬 마이그레이션
- [ ] 마이그레이션 SQL 파일 생성 확인 (`prisma/migrations/` 하위)
- [ ] Prisma Studio로 Lead 테이블 생성 확인 (`npx prisma studio`)
- [ ] Lead 모델 필드 코멘트/주석 추가 (contact: "이메일 또는 전화번호", channel: "유입 경로")

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: Lead 테이블 정상 생성**
- Given: Lead 모델이 schema.prisma에 정의됨
- When: `npx prisma migrate dev --name add-lead-table`을 실행함
- Then: `prisma/migrations/` 디렉토리에 마이그레이션 SQL 파일이 생성되고, 로컬 SQLite DB에 Lead 테이블이 생성된다

**Scenario 2: Lead 레코드 CRUD 확인**
- Given: Lead 테이블이 존재함
- When: Prisma Client로 `prisma.lead.create({ data: { name: "테스트", contact: "test@example.com" } })`를 실행함
- Then: Lead 레코드가 생성되고, id(cuid)와 createdAt이 자동 할당된다

**Scenario 3: 필수 필드 누락 시 에러**
- Given: Lead 모델에서 name, contact는 필수(non-nullable)임
- When: `prisma.lead.create({ data: { name: "" } })`처럼 contact 없이 생성을 시도함
- Then: Prisma Client가 유효성 에러를 반환한다

**Scenario 4: channel 필드 nullable**
- Given: channel 필드가 `String?`(nullable)로 정의됨
- When: channel 없이 Lead를 생성함
- Then: channel이 null로 저장되며 에러가 발생하지 않는다

## :gear: Technical & Non-Functional Constraints
- Lead.id: `cuid()` 자동 생성 (SRS Appendix A 명세)
- Lead.contact: 이메일 또는 전화번호 중 하나를 저장하는 단일 String 필드 (SRS §4.1 REQ-FREE-FUNC-003)
- Lead.channel: 유입 경로 — nullable, 선택 입력 (SRS S4)
- Lead는 Diagnosis와 1:N 관계 (`Lead ||--o{ Diagnosis`)
- 이 태스크에서는 Lead 모델만 정의하며, Diagnosis 모델은 DB-003에서 정의 (관계 필드는 placeholder 가능)

## :checkered_flag: Definition of Done (DoD)
- [ ] `prisma/schema.prisma`에 Lead 모델이 SRS Appendix A 명세대로 정의됨
- [ ] `npx prisma validate` 에러 0건
- [ ] `npx prisma migrate dev` 성공 — 마이그레이션 SQL 파일 생성
- [ ] 로컬 SQLite DB에 Lead 테이블 존재 확인 (Prisma Studio 또는 직접 조회)
- [ ] Lead 레코드 Create/Read 동작 확인
- [ ] `npm run build` 에러 0건 유지

## :construction: Dependencies & Blockers
- **Depends on:** DB-001 (Prisma 프로젝트 초기화 완료)
- **Blocks:** DB-003 (Diagnosis — leadId FK 참조), API-001 (createLead DTO), C-001 (createLead 비즈니스 로직), Q-003 (관리자 목록 UI), Q-006 (관리자 목록 조회 로직)
