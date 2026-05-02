---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-017: 관리자 승인 후 외부 리포트 접근 가능 테스트"
labels: 'feature, testing, priority:high'
assignees: ''
---

# [T-017] 관리자 승인 후 외부 리포트 접근 가능 테스트

## 1. 목적
- 미승인 상태의 리포트가 외부에 노출되는 것을 방지하고, 승인(Approved) 상태일 때만 접근 가능한지 검증한다.

## 2. 구현 범위
- `__tests__/integration/report-access.test.ts`

## 3. 입력/출력
### Input
- API Route `/api/reports/[id]` 또는 Server Action 호출
- 다양한 상태(draft, rejected, approved)의 리포트 ID

### Output
- `success: true` 와 `reportJson` 반환 (approved인 경우)
- 404 또는 `success: false` 반환 (approved가 아닌 경우)

## 4. 처리 로직
1. DB Mocking: 각기 다른 상태의 Report 3건 준비
2. `draft` 리포트 요청 -> 차단 확인
3. `rejected` 리포트 요청 -> 차단 확인
4. `approved` 리포트 요청 -> 통과 확인

## 5. 완료 기준
- [ ] 상태별 분기 처리가 정확히 동작하는지 검증
- [ ] 테스트 정상 통과

## 6. 관련 태스크
- 선행: SEC-003, Q-008
- 후행: None
