---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-010: 공통 ValidationError 타입 정의"
labels: 'feature, backend, contract, priority:high'
assignees: ''
---

# [API-010] 공통 ValidationError 타입 정의

## 1. 목적
- Zod 검증 실패 시 프론트엔드 폼에서 각 필드별 에러 메시지를 표시할 수 있도록 `fieldErrors` 구조를 표준화한다.

## 2. 구현 범위
- `src/lib/types/api.ts`

## 3. 입력/출력
### Output
```typescript
export type ValidationErrorDetails = {
  fieldErrors: Record<string, string[]>;
};
```

## 4. 처리 로직
1. ValidationErrorDetails 정의
2. ZodError를 `ValidationErrorDetails` 포맷으로 변환하는 헬퍼 유틸리티 함수 작성 (`parseZodError`)

## 5. 완료 기준
- [ ] ValidationError 헬퍼 구현
- [ ] 프론트엔드 연동 테스트

## 7. 관련 태스크
- 선행: API-009
- 후행: C-002
