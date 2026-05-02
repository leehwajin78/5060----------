---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-011: 개인정보 보존·삭제 기준 필드 검토"
labels: 'feature, database, priority:high'
assignees: ''
---

# [DB-011] 개인정보 보존·삭제 기준 필드 검토

## 1. 목적
- 개인정보 보호법에 따른 보유 기간 제한을 준수하기 위해, `Lead` 등의 엔티티에 파기 기한(`expiresAt`) 또는 논리 삭제(`deletedAt`) 필드를 추가한다.

## 2. 구현 범위
- `Lead` 모델 수정
- 보존 기간에 대한 상수 정책 수립

## 3. 입력/출력
### Input
- 개인정보 처리방침 정책

### Output
- 업데이트된 `schema.prisma` 마이그레이션

## 4. 처리 로직
1. `Lead` 테이블에 `deletedAt` (DateTime?) 필드 추가
2. `expiresAt` 필드를 추가하여 1년 등 특정 기한을 명시적으로 기록
3. 마이그레이션 파일 생성

## 5. 예외 처리
| 상황 | 처리 방식 | 사용자 메시지 |
|---|---|---|
| 이전 데이터 호환 | 기존 레코드는 null 허용 | N/A |

## 6. 완료 기준
- [ ] `schema.prisma`에 개인정보 관련 필드 반영 완료
- [ ] 마이그레이션 실행 완료

## 7. 관련 태스크
- 선행: DB-002
- 후행: DPR-001
