---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-009: 주요 FK 및 status/createdAt 인덱스 추가"
labels: 'feature, database, priority:high'
assignees: ''
---

# [DB-009] 주요 FK 및 status/createdAt 인덱스 추가

## 1. 목적
- 관리자 목록 및 상세 조회 쿼리의 성능을 최적화하기 위해 데이터베이스의 핵심 외래키(FK)와 상태(status), 생성일(createdAt) 컬럼에 인덱스를 추가한다.

## 2. 구현 범위
- `Lead`, `Diagnosis`, `Answer`, `Report`, `AiRun`, `ReviewLog` 테이블의 인덱스 최적화
- `schema.prisma` 파일 수정 및 마이그레이션 생성

## 3. 입력/출력
### Input
- 기존 `schema.prisma`

### Output
- `@@index([status, createdAt(sort: Desc)])` 등이 적용된 새로운 `schema.prisma` 및 마이그레이션 파일

## 4. 처리 로직
1. `Diagnosis` 테이블에 `@@index([status, createdAt])` 추가
2. `Report` 테이블에 `@@index([status])` 및 `@@index([diagnosisId])` 추가
3. `Answer` 테이블에 `@@index([diagnosisId])` 추가
4. `AiRun` 테이블에 `@@index([diagnosisId, status])` 추가
5. `npx prisma migrate dev --name add_performance_indexes` 실행

## 5. 예외 처리
| 상황 | 처리 방식 | 사용자 메시지 |
|---|---|---|
| 마이그레이션 충돌 | `prisma migrate reset` 안내 작성 | N/A |

## 6. 완료 기준
- [ ] 모든 FK에 인덱스 설정됨
- [ ] 빈번한 조회 조건(status, createdAt)에 복합 인덱스 설정됨
- [ ] 마이그레이션 정상 실행

## 7. 관련 태스크
- 선행: DB-001 ~ DB-008
- 후행: Q-006, Q-008
