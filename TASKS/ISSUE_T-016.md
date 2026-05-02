---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] T-016: AI 응답 Zod 실패 테스트"
labels: 'feature, testing, priority:high'
assignees: ''
---

# [T-016] AI 응답 Zod 실패 테스트

## 1. 목적
- AI가 스키마에 맞지 않는 JSON을 반환했을 때 (환각 상황) Report 생성을 방어하고 안전하게 실패 처리되는지 검증한다.

## 2. 구현 범위
- `__tests__/integration/ai-report-zod.test.ts` 작성

## 3. 입력/출력
### Input
- `generateDiagnosisReport` 호출, 이때 Gemini API 응답을 잘못된 스키마로 Mocking

### Output
- `success: false` 및 에러 반환, DB 확인

## 4. 처리 로직
1. `model.generateContent` Mocking: 필수 필드가 빠져있거나 타입이 다른 JSON 문자열 반환
2. `generateDiagnosisReport` 함수 실행
3. `AiRun` 레코드가 `FAILED`로 저장되었는지 확인
4. `Report` 레코드가 생성되지 않았는지 확인
5. `Diagnosis` 상태가 업데이트되지 않고 보존되는지 확인

## 5. 완료 기준
- [ ] 잘못된 JSON에 대한 방어 로직 정상 작동
- [ ] Jest/Vitest 테스트 성공

## 6. 관련 태스크
- 선행: C-005, C-006
- 후행: None
