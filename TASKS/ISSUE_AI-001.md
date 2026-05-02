---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] AI-001: AI 프롬프트 템플릿 파일 분리"
labels: 'feature, ai, priority:medium'
assignees: ''
---

# [AI-001] AI 프롬프트 템플릿 파일 분리

## 1. 목적
- 하드코딩된 프롬프트를 별도의 모듈 혹은 JSON, markdown 파일로 분리하여 유지보수성을 높이고, 필요시 비개발자도 문구를 수정하기 쉽게 구성한다.

## 2. 구현 범위
- `src/lib/ai/prompts.ts` 또는 유사 모듈 생성
- 시스템 프롬프트 및 사용자 데이터 템플릿화 적용

## 3. 입력/출력
### Input
- answers 배열

### Output
- 파싱된 프롬프트 string

## 4. 처리 로직
1. 프롬프트 생성 헬퍼 함수 작성 (`buildPrompt(answers)`)
2. 프롬프트 내 JSON 스키마 명시 강화 (DiagnosisReportSchema 기반)
3. C-005에서 해당 헬퍼 함수 호출 연동

## 5. 완료 기준
- [ ] 프롬프트 템플릿 분리
- [ ] 프롬프트 내용에 따른 응답 포맷 일치 여부 확인

## 7. 관련 태스크
- 선행: API-004
- 후행: C-005
