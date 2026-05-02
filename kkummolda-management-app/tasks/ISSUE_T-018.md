---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-018: 관리자 미인증 접근 차단 E2E 테스트"
labels: 'feature, testing, priority:high'
assignees: ''
---

# [T-018] 관리자 미인증 접근 차단 E2E 테스트

## 1. 목적
- 인증되지 않은 사용자가 `/admin` 라우트에 접근했을 때 정상적으로 차단되고 로그인 페이지로 리다이렉트되는지 검증한다.

## 2. 구현 범위
- `__tests__/e2e/admin-auth.spec.ts` (Playwright 또는 Cypress 활용)

## 3. 처리 로직
1. 세션이 없는 상태에서 `/admin/diagnoses` 접근 시도
2. `/admin/login` 페이지로 리다이렉트 확인
3. 잘못된 패스워드 입력 시 접근 거부 확인
4. 올바른 패스워드 입력 후 세션 발급 및 `/admin/diagnoses` 진입 확인

## 4. 완료 기준
- [ ] 미인증 접근이 미들웨어 단에서 완벽하게 차단됨을 증명
- [ ] E2E 테스트 통과

## 5. 관련 태스크
- 선행: SEC-002
- 후행: None
