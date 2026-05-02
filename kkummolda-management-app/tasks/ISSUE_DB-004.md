---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-004: Answer 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, backend, database, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-004] Answer 테이블 스키마 및 마이그레이션 작성
- 목적: 16문항 브랜드 진단의 질문별 답변 원문을 질문 코드(questionCode)와 함께 저장하는 Answer 모델을 정의한다. 이 데이터는 AI 진단 리포트 생성의 입력 원본이며, 관리자 검수 시 원문 참조 대상이다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#Appendix A — Prisma Schema (Answer 모델)`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 549~556
- ERD: SRS Appendix E — Answer 엔터티 (Lines 820~826)
- 기능 요구사항:
  - REQ-FREE-FUNC-011 (16문항 답변 원문을 질문 코드와 함께 Answer 테이블에 저장)
  - REQ-FREE-FUNC-004 (3단어 미만/공백 답변 차단 — 애플리케이션 레벨 검증)
- 16문항 질문 코드: SRS §1.2 S2 — Q1·Q2·Q4·Q6·Q7·Q8·Q9·Q11·Q13·Q15·Q26·Q28·Q33·Q40·Q41·Q42

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/schema.prisma`에 Answer 모델 추가:
  ```prisma
  model Answer {
    id           String    @id @default(cuid())
    diagnosisId  String
    diagnosis    Diagnosis @relation(fields: [diagnosisId], references: [id])
    questionCode String    // "Q1", "Q2", "Q4", ...
    answerText   String
    createdAt    DateTime  @default(now())
  }
  ```
- [ ] Diagnosis 모델에 `answers Answer[]` 관계 필드 확인 (DB-003에서 선언됨)
- [ ] `npx prisma validate` 실행 — 스키마 유효성 검사
- [ ] `npx prisma migrate dev --name add-answer-table` 실행
- [ ] 마이그레이션 SQL 파일 생성 확인
- [ ] Answer 레코드 생성/조회 동작 확인 — 특히 Diagnosis 1건에 Answer 16건 연결

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: Answer 테이블 정상 생성**
- Given: Answer 모델이 schema.prisma에 정의됨
- When: `npx prisma migrate dev --name add-answer-table`을 실행함
- Then: 로컬 SQLite DB에 Answer 테이블이 diagnosisId FK와 함께 생성된다

**Scenario 2: 16문항 답변 일괄 생성**
- Given: 유효한 Diagnosis ID가 존재함
- When: 16개의 Answer를 `createMany`로 생성함 (questionCode: Q1~Q42 중 16개, answerText: 각 3단어 이상)
- Then: Answer 레코드 16건이 정상 생성되고, 모두 동일한 diagnosisId를 가진다

**Scenario 3: Diagnosis → Answer 관계 조회**
- Given: Diagnosis D에 연결된 Answer 16건이 존재함
- When: `prisma.diagnosis.findUnique({ where: { id: D }, include: { answers: true } })`를 실행함
- Then: answers 배열에 16건의 Answer가 포함되어 반환된다

**Scenario 4: 존재하지 않는 diagnosisId로 생성 시 FK 에러**
- Given: 존재하지 않는 diagnosisId가 주어짐
- When: 해당 diagnosisId로 Answer를 생성하려 시도함
- Then: Prisma가 Foreign Key 제약 위반 에러를 반환한다

**Scenario 5: questionCode 저장 형식**
- Given: questionCode가 "Q1", "Q26" 등 문자열 형식임
- When: `prisma.answer.create({ data: { diagnosisId: D, questionCode: "Q26", answerText: "답변 내용" } })`를 실행함
- Then: questionCode가 "Q26"으로 정확히 저장된다

## :gear: Technical & Non-Functional Constraints
- Answer.questionCode: SRS에서 정의한 16문항 코드 (Q1, Q2, Q4, Q6, Q7, Q8, Q9, Q11, Q13, Q15, Q26, Q28, Q33, Q40, Q41, Q42)
  - DB 레벨 enum이 아닌 String — 유효성 검증은 애플리케이션 레벨 (C-002 태스크)에서 수행
- Answer.answerText: String 타입, 최소 3단어 검증은 서버 로직에서 처리 (REQ-FREE-FUNC-004)
- Diagnosis:Answer = 1:N 관계 (`Diagnosis ||--|{ Answer`)
  - 1 Diagnosis당 정확히 16건의 Answer가 생성됨 (REQ-FREE-FUNC-011)
- AI 리포트 생성 시 Answer.answerText만 payload에 포함, 실명/연락처 제외 (REQ-FREE-FUNC-023)

## :checkered_flag: Definition of Done (DoD)
- [ ] `prisma/schema.prisma`에 Answer 모델이 SRS 명세대로 정의됨
- [ ] Diagnosis → Answer FK 관계 정상 동작
- [ ] `npx prisma validate` 에러 0건
- [ ] `npx prisma migrate dev` 성공
- [ ] Answer 16건 일괄 생성 + Diagnosis 관계 조회 정상 동작
- [ ] `npm run build` 에러 0건 유지

## :construction: Dependencies & Blockers
- **Depends on:** DB-003 (Diagnosis 테이블 — diagnosisId FK 참조)
- **Blocks:** API-002 (submitDiagnosis DTO — answers[] 포함), C-003 (submitDiagnosis 저장 로직), C-004 (AI payload 구성 — Answer 원문 사용), Q-004 (관리자 상세 — 답변 원문 표시), Q-007 (관리자 상세 조회 로직)
