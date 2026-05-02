---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-010: seed 데이터 및 개발용 fixture 구성"
labels: 'feature, database, priority:high'
assignees: ''
---

# [DB-010] seed 데이터 및 개발용 fixture 구성

## 1. 목적
- 초기 개발, 테스트, UI 작업을 신속하게 진행할 수 있도록 `prisma/seed.ts`를 작성하여 각 상태별(submitted, drafted, approved 등) mock 데이터를 DB에 생성한다.

## 2. 구현 범위
- `prisma/seed.ts` 스크립트 작성
- 테스트용 Lead, Diagnosis, Answer, Report 데이터 일괄 삽입 로직

## 3. 입력/출력
### Input
- `MOCK-001`, `MOCK-002` 데이터

### Output
- DB에 적재된 테스트 레코드들

## 4. 처리 로직
1. 기존 데이터 초기화 (선택적)
2. `Lead` 3건 생성
3. 각 Lead별로 `Diagnosis` 1건씩 생성 (status: submitted, report_generated, reviewed)
4. 각 Diagnosis별 `Answer` 16건 생성
5. report_generated, reviewed 상태의 Diagnosis에 대해 `Report` 레코드(draft, approved) 생성

## 5. 예외 처리
| 상황 | 처리 방식 | 사용자 메시지 |
|---|---|---|
| 중복 키 에러 | seed 스크립트 멱등성 보장 (upsert 사용) | N/A |

## 6. 완료 기준
- [ ] `npx prisma db seed` 명령어로 정상 실행
- [ ] 각 상태별 테스트 데이터가 최소 1건 이상 적재됨

## 7. 관련 태스크
- 선행: DB-001 ~ DB-008
- 후행: Q-003, Q-004, FE-003
