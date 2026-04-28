# PRD v0.3 변경 요약 — 코칭 가이드 42문항 통합

| 항목 | 내용 |
| :--- | :--- |
| **문서 목적** | 기존 PRD v0.2에 「나다운 브랜딩 5060 코칭 가이드 42문항」의 인사이트를 제품 요건으로 반영하기 위한 변경 분석 |
| **작성일** | 2026-04-25 |
| **대상 문서** | PRD v0.2 → PRD v0.3 |

---

## 1. 핵심 변경 방향

| # | 기존 PRD v0.2 관점 | PRD v0.3 관점 (코칭 가이드 통합) |
| :---: | :--- | :--- |
| 1 | AI 마스터 브리프 생성기 = 텍스트 생성 기능 | **42문항 기반 브랜드 자산 변환 엔진** |
| 2 | AI 브랜드 진단 툴 = 5문항 리드 퍼널 | **축약형 12~16문항 브랜딩 진단 모듈** |
| 3 | 42문항 인터뷰 = 정보 수집 도구 | **제품 핵심 데이터 구조 + AI 코칭 로직의 원천** |
| 4 | 최종 산출물 = 제안서·강의안 | **브랜드 프로필 → 제안서·강의안·코칭 업셀** |
| 5 | Pain 정의 = 경력 언어화 실패 중심 | **직함 의존 정체성, 자기축소, 실패 회피, 디지털 피로까지 확장** |

---

## 2. 섹션별 수정 방향표

| 기존 섹션 | 수정 유형 | 변경 핵심 |
| :--- | :---: | :--- |
| **§1. 개요·목표** | 보강 | Product Vision 재정의, 핵심 작동 구조(답변→패턴→태깅→해석→코칭→변환) 추가, Pain 지표 5항목으로 확장 |
| **§2. 사용자와 페르소나** | 보강 | 각 페르소나에 브랜딩 장애 유형·예상 답변 패턴·코칭 방식·최종 변환 자산 추가 |
| **§3. 사용자 스토리와 AC** | 보강 | Story 1~4 AC에 답변 충분성·패턴 분석·브랜드 매핑·출력 품질 AC 추가 |
| **§4. 기능 요구사항** | 보강+추가 | F1 확장, F9~F14 신규 6개 기능 추가 |
| **§5. 비기능 요구사항** | 보강 | AI 코칭 품질 NFR 7항목, 보안 자기서사 데이터 보호 3항목 추가 |
| **§6. 데이터·인터페이스** | 보강 | 9개 신규 엔터티, MVP jsonb → V2 정규화 전환 로드맵 |
| **§7. 범위, 리스크, 가정** | 보강 | In MVP 5항목, Out V1 5항목, 리스크 5항목 추가 |
| **§8. 실험·롤아웃·측정** | 보강 | E5~E8 코칭 가이드 기반 실험 4건 추가 |
| **§9. 근거 (Proof)** | 유지 | 변경 없음 |
| **신규 §A** | 신설 | Coaching Framework |
| **신규 §B** | 신설 | Question Architecture |
| **신규 §C** | 신설 | Answer Pattern Taxonomy |
| **신규 §D** | 신설 | Branding Output Map |
| **신규 §E** | 신설 | Human Coaching Handoff |

---

## 3. 신규 기능 요약 (F9~F14)

| 우선순위 | 기능명 | 핵심 설명 | MVP 포함 |
| :---: | :--- | :--- | :---: |
| **Must** | F9. Question Architecture Engine | 42문항 메타데이터 관리(브랜딩 요소, 의도, 산출물 연결) | ✅ |
| **Must** | F10. Answer Pattern Classifier | 답변 패턴 분류(직함 중심, 자기축소, 회피 등 10개 유형) | ✅ |
| **Must** | F11. Branding Output Mapper | 답변→브랜드 산출물 매핑(원라이너, 가치선언문, USP 등) | ✅ |
| **Should** | F12. Coaching Feedback Generator | 패턴별 5060 특화 코칭 피드백 및 보완 질문 생성 | V1.5 |
| **Should** | F13. Report Generation Rule Engine | 누적 답변 기반 브랜드 프로필·진단 리포트 구조화 생성 | V1.5 |
| **Could** | F14. Human Coaching Handoff | AI 한계 영역 식별 → 사람 코치 연결 트리거 | V2 |

---

## 4. 데이터 모델 변경 포인트

### MVP (V1) — jsonb 확장

기존 `DIAGNOSIS.answers jsonb` + `BRIEF.ai_output jsonb` 내에 다음 구조를 포함:

```json
{
  "question_id": "Q01",
  "raw_text": "사용자 원문 답변",
  "branding_element": "브랜드 정체성",
  "detected_pattern": "직함·역할만 말함",
  "ai_coaching_note": "직함 의존 정체성 패턴. 직함 제거 후 가치·태도 추출 필요",
  "output_mapping": ["브랜드 원라이너", "프로필 소개문"]
}
```

### V2 — 정규화 테이블 전환

9개 신규 엔터티: QUESTION, QUESTION_PART, BRANDING_ELEMENT, ANSWER, ANSWER_PATTERN, COACHING_FEEDBACK, OUTPUT_MAPPING, BRAND_PROFILE, REPORT_SECTION

---

## 5. 최종 PRD v0.3 목차 제안

```
1. 개요·목표
   1-1. 문제 정의 (Pain 지표 포함)
   1-2. 목표 (Desired Outcome 수치화)
   1-3. 성공 지표 (KPI)
   1-4. 핵심 작동 구조 (NEW)

2. 사용자와 페르소나
   2-1. 핵심 페르소나 요약
   2-2. 페르소나별 코칭 프로필 (NEW)
   2-3. 고객 여정 Pain·Needs 맵

3. Coaching Framework (NEW — 챕터 A)

4. Question Architecture (NEW — 챕터 B)

5. Answer Pattern Taxonomy (NEW — 챕터 C)

6. Branding Output Map (NEW — 챕터 D)

7. 사용자 스토리와 수용 기준 (AC)
   Story 1~4 + 코칭 기반 AC 보강

8. 기능 요구사항 (Functional)
   8-1. 우선순위 매트릭스
   8-2. 기능 목록 (F1~F14)

9. 비기능 요구사항 (NFR)
   9-1~9-5 기존 + 9-6 AI 코칭 품질 (NEW)

10. 데이터·인터페이스 개요
    10-1. 핵심 엔터티 ERD (확장)
    10-2. 신규 엔터티 상세 (NEW)
    10-3. 외부/내부 API 개요

11. Human Coaching Handoff (NEW — 챕터 E)

12. 범위 (In/Out), 리스크·가정·의존성
    12-1. 범위 정의 (확장)
    12-2. 리스크 매트릭스 (확장)
    12-3. 가정 및 의존성

13. 실험·롤아웃·측정
    13-1. 롤아웃 계획
    13-2. 실험 설계 (E1~E8)
    13-3. 벤치마크 계획

14. 근거 (Proof)

15. 다음 단계
```
