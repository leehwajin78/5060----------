---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DATA-001: 16문항 질문 데이터 파일 작성 (lib/questions.ts)"
labels: 'feature, data, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [DATA-001] 16문항 질문 데이터 파일 작성
- 목적: 축약 16문항 브랜드 진단의 정적 질문 데이터를 `lib/questions.ts`에 정의한다. 각 질문은 코드(code), 질문 텍스트(text), PART 구분(part), 브랜드 자산 안내 문구(assetHint)를 포함하며, 진단 폼 UI(Q-002)와 AI payload 구성(C-004) 모두의 SSOT 역할을 한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#§1.2 S2~S3`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — S2 (축약 16문항), S3 (질문별 브랜드 자산 안내)
- 기능 요구사항:
  - REQ-FREE-FUNC-001 (16문항 진단 폼 PART 순서 제공)
  - REQ-FREE-FUNC-002 (각 질문에 브랜드 자산 안내 문구 표시)
- 가치 보존 체크리스트: SRS Appendix F — "16문항 진단 유지: Q1·Q2·Q4·Q6·Q7·Q8·Q9·Q11·Q13·Q15·Q26·Q28·Q33·Q40·Q41·Q42 → lib/questions.ts"
- Build Plan: SRS Appendix C Step 4 — "lib/questions.ts 생성, 질문 코드·브랜드 자산 매핑 포함"
- AI 코딩 Prompt 2: SRS Appendix D — "질문 데이터 구조: { code, text, assetHint }"
- 원본 가이드: REF-04 (나다운 브랜딩 5060 코칭 가이드 42문항 — 꿈몰다 내부 IP)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/questions.ts` 파일 생성
- [ ] Question 타입 인터페이스 정의:
  ```typescript
  export interface Question {
    code: string       // "Q1", "Q2", "Q4", ...
    part: string       // PART 구분 (예: "PART 1: 정체성", "PART 2: 경험" 등)
    text: string       // 질문 본문
    assetHint: string  // 이 질문이 연결되는 브랜드 자산 안내 문구
  }
  ```
- [ ] 16문항 데이터 배열 작성 — SRS S2에 명시된 코드 순서:
  Q1, Q2, Q4, Q6, Q7, Q8, Q9, Q11, Q13, Q15, Q26, Q28, Q33, Q40, Q41, Q42
- [ ] 각 질문에 PART 구분 할당 (원본 42문항 코칭 가이드 기반)
- [ ] 각 질문에 assetHint 작성 (REQ-FREE-FUNC-002 — 브랜드 자산 연결 안내)
- [ ] `QUESTIONS` 상수 export: `export const QUESTIONS: Question[] = [...]`
- [ ] 질문 코드 목록 유틸리티 export: `export const QUESTION_CODES = QUESTIONS.map(q => q.code)`
- [ ] 질문 코드로 질문 찾기 유틸리티: `export const getQuestionByCode = (code: string) => QUESTIONS.find(q => q.code === code)`
- [ ] TypeScript 컴파일 에러 0건 확인
- [ ] 16문항 누락/중복 없음 검증

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 16문항 정확성**
- Given: `lib/questions.ts`가 작성됨
- When: `QUESTIONS.length`를 확인함
- Then: 정확히 16이 반환된다

**Scenario 2: 질문 코드 완전성**
- Given: SRS에서 정의한 16문항 코드 목록이 주어짐
- When: `QUESTION_CODES`를 SRS 목록 `["Q1","Q2","Q4","Q6","Q7","Q8","Q9","Q11","Q13","Q15","Q26","Q28","Q33","Q40","Q41","Q42"]`과 비교함
- Then: 두 배열이 동일하다 (누락/중복 없음)

**Scenario 3: 모든 질문에 assetHint 존재**
- Given: QUESTIONS 배열이 존재함
- When: 모든 항목의 assetHint 필드를 확인함
- Then: 모든 항목에 빈 문자열이 아닌 assetHint가 존재한다

**Scenario 4: 모든 질문에 part 존재**
- Given: QUESTIONS 배열이 존재함
- When: 모든 항목의 part 필드를 확인함
- Then: 모든 항목에 빈 문자열이 아닌 part 구분이 존재한다

**Scenario 5: getQuestionByCode 유틸리티 동작**
- Given: QUESTIONS에 Q26이 포함됨
- When: `getQuestionByCode("Q26")`을 실행함
- Then: code가 "Q26"인 Question 객체가 반환된다

**Scenario 6: 존재하지 않는 코드 조회**
- Given: QUESTIONS에 Q99는 존재하지 않음
- When: `getQuestionByCode("Q99")`를 실행함
- Then: undefined가 반환된다

## :gear: Technical & Non-Functional Constraints
- 파일 경로: `src/lib/questions.ts` (SRS Appendix C Step 4, Appendix F)
- 16문항 코드 목록은 SRS §1.2 S2에서 고정: Q1·Q2·Q4·Q6·Q7·Q8·Q9·Q11·Q13·Q15·Q26·Q28·Q33·Q40·Q41·Q42
  - 이 코드 목록은 변경 불가 — 42문항 중 MVP 선별된 16개
- 질문 텍스트와 assetHint는 REF-04 (나다운 브랜딩 5060 코칭 가이드 42문항)를 참조하여 작성
  - 원본 가이드 미확보 시, 질문 코드별 적절한 placeholder 텍스트로 초기 작성 후 운영자 검수
- PART 구분은 원본 42문항의 파트 체계를 따름 (예: 정체성, 경험/역량, 가치관, 미래 비전 등)
- 이 파일은 런타임에 DB 조회 없이 사용되는 정적 상수 — 빌드 타임에 포함
- Answer 테이블의 questionCode와 1:1 매핑됨

## :checkered_flag: Definition of Done (DoD)
- [ ] `src/lib/questions.ts` 파일이 생성됨
- [ ] Question 타입 인터페이스가 정의됨 (code, part, text, assetHint)
- [ ] QUESTIONS 배열에 정확히 16문항이 포함됨
- [ ] 모든 질문 코드가 SRS S2 목록과 일치함 (누락/중복 없음)
- [ ] 모든 질문에 비어있지 않은 text, part, assetHint가 존재함
- [ ] QUESTION_CODES, getQuestionByCode 유틸리티가 export됨
- [ ] TypeScript 컴파일 에러 0건
- [ ] `npm run build` 에러 0건 유지

## :construction: Dependencies & Blockers
- **Depends on:** INF-001 (Next.js 프로젝트 존재 — src/lib/ 디렉토리)
- **Blocks:** Q-002 (진단 폼 UI — 질문 카드 렌더링), FE-001 (폼 유효성 검증 — 질문 수 기준), C-002 (submitDiagnosis 검증 — 유효 questionCode 목록), C-004 (AI payload — 질문코드+답변 매핑), MOCK-001 (Mock 진단 데이터 — 질문 코드 참조), API-002 (submitDiagnosis DTO — answers[] 질문 코드)
