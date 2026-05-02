---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] C-003: submitDiagnosis DB 저장 로직 (Lead+Diagnosis+Answer 트랜잭션)"
labels: 'feature, backend, command, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [C-003] submitDiagnosis DB 저장 로직
- 목적: 검증 통과된 진단 입력(C-002)을 받아 Lead → Diagnosis → Answer 16건을 단일 Prisma 트랜잭션으로 생성한다. 원자성을 보장하여 부분 저장을 방지하고, 저장 완료 후 AI 리포트 생성(C-005)을 트리거한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 시퀀스 1: [`SRS_v1.md#§3.4`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Lines 289~312
- 기능 요구사항:
  - REQ-FREE-FUNC-010 (Lead 테이블 저장)
  - REQ-FREE-FUNC-011 (Answer 16건 질문코드와 함께 저장)
  - REQ-FREE-FUNC-012 (Diagnosis.status 정상 저장)
- DTO: API-002 (SubmitDiagnosisInput/Output)
- 검증: C-002 (validateDiagnosisInput)
- 상태 상수: DATA-002 (DiagnosisStatus)

## :white_check_mark: Task Breakdown (실행 계획)

### 처리 절차

1. submitDiagnosis DTO 검증
2. Lead 생성 또는 저장
3. Diagnosis 생성
4. Answer 16건 bulk insert
5. Diagnosis.status를 report_pending으로 설정
6. 저장 성공 응답 반환

### Transaction 범위

아래 작업은 반드시 하나의 transaction으로 처리한다.

- Lead 생성
- Diagnosis 생성
- Answer 16건 생성

### 예외 처리

| 상황 | 처리 |
|---|---|
| Answer 저장 중 일부 실패 | 전체 rollback |
| 중복 questionCode | 저장 전 차단 |
| DB 연결 실패 | 사용자에게 “제출 처리 중 문제가 발생했습니다” 안내 |

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 정상 제출 — Lead+Diagnosis+Answer 16건 생성**
- Given: 유효한 입력이 검증을 통과함
- When: `submitDiagnosis(input)`를 실행함
- Then: DB에 Lead 1건, Diagnosis 1건(status=submitted), Answer 16건이 정확히 생성되고 성공 반환.

**Scenario 2: 트랜잭션 원자성 — 부분 실패 시 전체 롤백**
- Given: Answer 저장 중 에러 발생
- When: 트랜잭션이 실패함
- Then: Lead와 Diagnosis도 전체 롤백되어 아무것도 저장되지 않는다.

## :gear: Technical & Non-Functional Constraints
- `prisma.$transaction()` 인터랙티브 트랜잭션 사용 — 원자성 보장
- `createMany`는 SQLite에서도 지원 (Prisma 5.x)
- AI 리포트 생성은 트랜잭션 외부에서 비동기 호출 — 실패해도 답변 데이터 보존 (REQ-FREE-FUNC-022)
- Server Action 반환 타입은 직렬화 가능 JSON

## :checkered_flag: Definition of Done (DoD)
- [ ] submitDiagnosis() Server Action 구현 완료
- [ ] 트랜잭션으로 Lead+Diagnosis+Answer 원자적 생성 동작 확인
- [ ] 검증 실패 / 트랜잭션 성공 / 트랜잭션 실패 3가지 경로 동작 확인
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** C-002 (validateDiagnosisInput), DB-002 (Lead), DB-003 (Diagnosis), DB-004 (Answer), DATA-002 (DiagnosisStatus), API-002 (DTO)
- **Blocks:** C-005 (AI 리포트 생성 트리거), FE-002 (폼 제출 연동), T-004 (Answer 16건 저장 테스트)
