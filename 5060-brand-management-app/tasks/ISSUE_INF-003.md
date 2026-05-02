---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] INF-003: Gemini API 연동 및 설정 최적화"
labels: 'feature, infrastructure, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [INF-003] Gemini API 연동 설정
- 목적: `generateDiagnosisReport`(C-005) 등에서 사용할 `@google/generative-ai` SDK를 설치하고, Gemini 2.0 Flash 모델의 Generation Config (Temperature, Response Schema 지원 여부 등)를 최적화하여 환각을 최소화한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- AI 로직: C-005
- 환각 차단 요구사항: REQ-FREE-FUNC-021
- 타겟 코드: `src/lib/services/ai-report.service.ts`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `@google/generative-ai` 라이브러리 설치 유무 재확인
- [ ] `model` 인스턴스 생성 시 최적화 파라미터 적용:
  ```typescript
  import { GoogleGenerativeAI } from "@google/generative-ai"

  const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!)
  export const geminiModel = genAI.getGenerativeModel({
    model: "gemini-2.0-flash", // 비용/성능 타겟 모델
    generationConfig: {
      temperature: 0.2, // 환각을 줄이고 결정론적 답변(분석) 유도
      topP: 0.8,
      topK: 40,
      responseMimeType: "application/json", // JSON 모드 강제화
    },
  })
  ```
- [ ] Zod 스키마 연동 시 `geminiModel`의 JSON 반환 설정을 통해 파싱 실패 확률을 획기적으로 낮춤.

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 모델 인스턴스화 검증**
- Given: GEMINI_API_KEY가 설정된 환경
- When: 서버 구동 및 모델 초기화 코드가 실행됨
- Then: 에러 없이 인스턴스가 반환되고, 파라미터가 적용된다.

**Scenario 2: JSON 모드 출력**
- Given: Gemini API에 프롬프트 전송
- When: 결과를 반환받음
- Then: 마크다운 코드 블럭(```json ... ```) 없이 순수한 JSON 문자열이 반환될 확률이 높아져 파싱이 매끄럽게 진행된다.

## :gear: Technical & Non-Functional Constraints
- Gemini 2.0 Flash 모델 지정.
- `responseMimeType: "application/json"`은 지원 모델 버전에서 매우 효과적이므로 필수로 적용한다. (프롬프트에도 "JSON 형식으로 반환해"를 추가하는 방어적 이중 설계 권장)

## :checkered_flag: Definition of Done (DoD)
- [ ] `ai-report.service.ts` 내에 SDK 설정 및 Configuration 적용
- [ ] TypeScript 컴파일 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** C-005
- **Blocks:** None
