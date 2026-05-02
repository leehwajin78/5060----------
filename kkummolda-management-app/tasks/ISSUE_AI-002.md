---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] AI-002: AI 응답 파싱 실패 복구 로직"
labels: 'feature, ai, priority:high'
assignees: ''
---

# [AI-002] AI 응답 파싱 실패 복구 로직

## 1. 목적
- AI가 간헐적으로 완전하지 않거나 마크다운 등 부가 텍스트가 포함된 JSON을 반환할 때, 단순 정규식으로 복구하여 Zod 파싱 성공률을 높인다.

## 2. 구현 범위
- `src/lib/utils/json-parser.ts`

## 3. 입력/출력
### Input
- raw string (Gemini API 응답 원문)

### Output
- 유효한 JSON 객체 또는 ParseError

## 4. 처리 로직
1. ` ```json ` 마크다운 블록 제거 정규식 처리
2. 앞뒤 불필요한 텍스트 제거 (`{` 부터 `}` 까지 추출)
3. 추출된 문자열을 `JSON.parse` 시도
4. 파싱 에러 발생 시 커스텀 에러 로깅 처리

## 5. 예외 처리
| 상황 | 처리 방식 | 사용자 메시지 |
|---|---|---|
| 정규식 후에도 파싱 불가 | Zod 실패 처럼 AiRun failed 로깅 | N/A |

## 6. 완료 기준
- [ ] 추출 유틸리티 구현
- [ ] 마크다운 블록이 섞인 Mock 응답으로 파싱 테스트 성공

## 7. 관련 태스크
- 선행: AI-001
- 후행: C-005
