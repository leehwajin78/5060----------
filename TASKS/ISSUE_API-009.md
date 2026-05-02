---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-009: 공통 ApiResponse 타입 정의"
labels: 'feature, backend, contract, priority:high'
assignees: ''
---

# [API-009] 공통 ApiResponse 타입 정의

## 1. 목적
- 백엔드(Server Action, API Route)에서 프론트엔드로 반환하는 모든 응답 형식을 하나로 통일하여 일관된 에러 핸들링과 타입 추론을 제공한다.

## 2. 구현 범위
- `src/lib/types/api.ts` 또는 `types/global.d.ts` 에 공통 타입 정의

## 3. 입력/출력
### Output
```typescript
type ApiResponse<T> = {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: unknown;
  };
};
```

## 4. 처리 로직
1. ApiResponse 타입 정의
2. 기존 Server Action들(API-001, API-002, API-005)에 적용

## 5. 완료 기준
- [ ] `ApiResponse` 타입이 전역 혹은 공통 모듈로 export 됨
- [ ] 성공/실패 응답 형태가 통일됨

## 7. 관련 태스크
- 선행: INF-001
- 후행: API-001~008
