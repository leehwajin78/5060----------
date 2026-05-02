---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-019: 개인정보 마스킹 snapshot 테스트"
labels: 'feature, testing, priority:high'
assignees: ''
---

# [T-019] 개인정보 마스킹 snapshot 테스트

## 1. 목적
- AI API로 전달되는 Payload에 PII(개인식별정보)가 포함되지 않도록 마스킹 로직이 올바르게 동작하는지 스냅샷으로 고정하여 검증한다.

## 2. 구현 범위
- `__tests__/unit/pii-masking.test.ts`

## 3. 처리 로직
1. 이름, 전화번호(010-1234-5678), 이메일(test@example.com)이 포함된 더미 Answer 생성
2. `buildAiPayload` 실행
3. 반환된 Payload 내에 이름, 전화번호, 이메일이 적절한 문자열(`[EMAIL_REMOVED]`, `[PHONE_REMOVED]`)로 치환되었는지 검증
4. Jest Snapshot을 생성하여 이후 마스킹 로직 변경 시 감지되도록 설정

## 4. 완료 기준
- [ ] 스냅샷 파일 생성됨
- [ ] PII 유출이 없음을 확인

## 5. 관련 태스크
- 선행: SEC-001
- 후행: None
