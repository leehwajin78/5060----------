# Software Requirements Specification (SRS)

Document ID: SRS-001
Revision: 1.0
Date: 2026-04-25
Standard: ISO/IEC/IEEE 29148:2018

---

| 항목 | 내용 |
| :--- | :--- |
| **Document ID** | SRS-001 |
| **Revision** | 1.0 |
| **Date** | 2026-04-25 |
| **Standard** | ISO/IEC/IEEE 29148:2018 |
| **Source PRD** | PRD_v0_4_2.md (5060 프리미엄 브랜드 매니지먼트 PRD v0.4.2) |
| **Status** | Draft |
| **Authors** | 브랜드 매니지먼트 사업부 (AI Ops) |

---

## 1. Introduction

### 1.1 Purpose

본 SRS는 **5060 프리미엄 브랜드 매니지먼트 시스템 (이하 "시스템")**의 소프트웨어 요구사항을 ISO/IEC/IEEE 29148:2018 표준에 따라 완전하고 명확하게 명세하는 목적으로 작성되었다.

시스템의 핵심 목적은 다음과 같다:

- 5060 고경력 전문가(퇴직·전환기 임원, 연구원, 전문직)의 암묵지를 구조화된 42문항 인터뷰를 통해 진단하고
- 10가지 답변 패턴을 AI로 분류·해석하여 5060 특화 코칭 피드백을 생성하고
- 브랜드 원라이너·핵심 가치·USP·타깃 페르소나·스토리·채널 전략·브랜드 WHY 등 8개 섹션으로 구성된 마스터 브리프와 B2B 제안서·강의안 구조로 변환하는 AI 기반 Done-for-you 프리미엄 매니지먼트 시스템을 구축하는 것이다.

본 문서는 PRD v0.4.2를 유일한 비즈니스·기능 요구의 원천(Source of Truth)으로 사용한다.

---

### 1.2 Scope

#### In-Scope (MVP V1)

| # | 항목 | 대응 기능 |
| :---: | :--- | :--- |
| S1 | AI 브랜드 진단 툴 — 축약 12~16문항, 웹 기반 | F2 |
| S2 | AI 마스터 브리프 생성기 — 관리자 콘솔 중심 | F1 |
| S3 | 리드 DB 자동 적재 (Supabase) | F4 |
| S4 | 랜딩페이지 (Next.js) | F2 보조 |
| S5 | 진단 결과 리포트 웹뷰 출력 | F2 |
| S6 | 질문별 브랜딩 요소 태깅 | F9 MVP |
| S7 | 답변 패턴 분류 최소 버전 | F10 MVP |
| S8 | 브랜드 원라이너·핵심 가치·강점·타깃·프로필 소개문 생성 | F11 MVP |
| S9 | 운영자 검수용 AI 해석 메모 | F1 보강 |
| S10 | 축약 12~16문항 기반 진단 | F2 |
| S11 | F15 Coach Session Brief Generator (Stage 1·3 코치 분석 노트 자동 생성 + 원라이너 초안 3종) | F15 |
| S12 | 단계 간 교차 분석 (Q1↔Q41, Q6×Q20, Q26+Q33) | F10·F15 |

#### Out-of-Scope (V1 제외)

| # | 항목 | 비고 |
| :---: | :--- | :--- |
| O1 | 결제 시스템 | 수동 계좌이체로 대체 |
| O2 | SNS 회원가입 / OAuth 로그인 | V2 |
| O3 | PPT 자동 Export | F8 — V2 이후 |
| O4 | STT 음성 자동 변환 | F7 — V2 이후 |
| O5 | 완전 자동 코칭 (사람 검수 없는 자동 납품) | V2 이후 |
| O6 | 무검수 자동 리포트 납품 | V2 이후 |
| O7 | 자동 PPT 디자인 생성 | V2 이후 |
| O8 | 모바일 네이티브 앱 | V2 이후 |
| O9 | 심리상담 또는 치료적 해석 기능 | 영구 제외 |

#### Constraints (제약사항 및 가정)

| # | 구분 | 내용 |
| :---: | :--- | :--- |
| C1 | ADR — LLM 선택 | Claude 3.5 API 채택 (컨텍스트 윈도우 크기 + 한국어 뉘앙스 처리 우수성). 대체 불가 |
| C2 | ADR — DB/Backend | 초기 스키마 변경 빈도를 고려해 관계형 DB 정규화 대신 Supabase JSONB 구조를 1스프린트 핵심 전략으로 결정 |
| C3 | 개발 체제 | 1인 개발 체제, 1스프린트(2주) 내 MVP 구현 가능 범위로 복잡한 프론트엔드 UI 대신 관리자 콘솔 API 연동 위주로 스코프 설계 |
| C4 | 가정 — AI 프롬프트 | 42문항 코칭 가이드의 126개 패턴 코칭 스크립트(AI 개발용 정본)가 Claude API System Prompt에 효과적으로 삽입 가능 |
| C5 | 가정 — 축약 진단 | 축약 12~16문항만으로 상담 전환에 충분한 자기인식 효과 달성 가능 |
| C6 | 가정 — 분류 정확도 | 답변 패턴 분류가 NLP 키워드 매칭 + LLM 문맥 분석 결합으로 ≥ 85% 정확도 달성 가능 |
| C7 | IP 의존성 | 나다운 브랜딩 5060 코칭 가이드 42문항 — 제품의 핵심 IP. 질문 구조·패턴 코칭·브랜드 프로필 연결의 원천 문서 |
| C8 | 데이터 보호 | 고객 답변 데이터를 AI 학습용으로 재사용 금지 또는 별도 동의 필요 (Claude API 이용 약관 내 데이터 보호 조항 준수) |

---

### 1.3 Definitions, Acronyms, Abbreviations

| 용어 / 약어 | 정의 |
| :--- | :--- |
| **5060 전문가** | 퇴직·전환기에 있는 50~60대 고경력 임원, 연구원, 전문직 종사자 |
| **마스터 브리프** | 42문항 인터뷰 분석 결과를 8개 섹션(브랜드 원라이너·핵심 가치·강점 명제문·타깃 페르소나·브랜드 스토리·핵심 메시지·채널 전략·브랜드 WHY)으로 구조화한 최종 브랜드 자산 문서 |
| **브랜드 원라이너** | "나는 [대상]이 [문제]를 해결하도록 [방식]으로 돕는 사람이다" 구조의 1문장 자기 정의 |
| **Stage 1~4** | 42문항을 코칭 흐름 기준으로 분류한 4개 답변 그룹 (9+11+12+10=42문항) |
| **PART 1~4** | 42문항을 브랜드 자산 관점으로 분류한 4개 파트 |
| **P1~P10** | 답변 패턴 10가지 분류 (직함 중심형·가치 중심형·자기축소형·회피형·타깃 과확장형·경험 나열형·방법론 보유형·채널 과욕형·실패 통합형·실패 회피형) |
| **마스터 브리프 생성기** | F1. AI가 42 OUTPUT 변수를 입력으로 받아 8개 섹션의 브랜드 자산 문서를 생성하는 핵심 엔진 |
| **코치 분석 노트** | F15가 Stage 1 또는 Stage 3 답변 수신 후 자동 생성하는 6개 항목 분석 결과물 (1차·2차 세션 준비용) |
| **원라이너 초안 3종** | 2차 세션 전 AI가 자동 생성하는 전문성형·공감형·결과형 3가지 버전의 원라이너 후보 |
| **교차 검증 매트릭스** | 9개 답변 조합의 정합성을 검증하는 게이트. F1 마스터 브리프 생성 전 전체 통과 필수 |
| **AOS** | Adjusted Opportunity Score — 기회점수 (조정값) |
| **DOS** | Discovered Opportunity Score — 발견 기회점수 |
| **JTBD** | Jobs-to-be-Done — 완수할 과업 |
| **USP** | Unique Selling Proposition — 고유 가치 제안 |
| **NPS** | Net Promoter Score — 순추천지수 |
| **LLM** | Large Language Model |
| **STT** | Speech-to-Text |
| **JSONB** | JSON Binary — PostgreSQL/Supabase 가변 JSON 저장 타입 |
| **MVP** | Minimum Viable Product — 최소 기능 제품 |
| **CTA** | Call-to-Action |
| **Done-for-you** | 전문가가 대신 완성해주는 서비스 형태 |
| **WHY** | Simon Sinek의 Golden Circle 개념에서 파생. 브랜드의 궁극적 목적·존재 이유 |
| **가치 일관성 점수** | Q2·Q6·Q20 교차 검증 결과를 0~1 범위로 수치화한 값 |
| **환각(Hallucination)** | LLM이 답변 텍스트에 없는 내용을 사실처럼 출력하는 현상 |
| **검수자** | 운영자·코치가 AI 출력 결과를 승인/수정/거부 처리하는 역할 |

---

### 1.4 References

| Ref ID | 문서명 | 출처 |
| :--- | :--- | :--- |
| REF-01 | PRD v0.4.2 — 5060 프리미엄 브랜드 매니지먼트 | 브랜드 매니지먼트 사업부 (2026-04-25) |
| REF-02 | 나다운 브랜딩 5060 AI 개발용 코칭 가이드 완전판 | 꿈몰다 내부 IP — 의사 코드 AI 처리 로직 + 42 OUTPUT 변수 + Stage 4단계 구조 출처 |
| REF-03 | 나다운 브랜딩 5060 코칭 가이드 42문항 | 꿈몰다 내부 IP — 168 패턴 코칭 스크립트 출처 (코치용 풀 버전) |
| REF-04 | 나다운 브랜딩 5060 코칭 실전 완전 가이드 | 꿈몰다 내부 IP — 코칭 흐름 운영 가이드 |
| REF-05 | PRD v0.2 | 브랜드 매니지먼트 사업부 — 기존 KPI·API 표 원천 |
| REF-06 | ISO/IEC/IEEE 29148:2018 | 국제 표준 — SRS 작성 기준 |
| REF-07 | Supabase 공식 문서 | https://supabase.com/docs |
| REF-08 | Anthropic Claude API 공식 문서 | https://docs.anthropic.com |

---

## 2. Stakeholders

| 역할 (Role) | 책임 (Responsibility) | 관심사 (Interest) |
| :--- | :--- | :--- |
| **고객** (5060 고경력 전문가) | Stage 1·3·4 질문지 응답, 마스터 브리프 검토·승인, CTA 진입 | B2B 수주 기회 확보, 직함 대체용 브랜드 언어 확보, 암묵지의 시장 자산 변환 |
| **운영자 / 사람 코치** | 1차·2차 코칭 세션 진행, AI 분석 결과 검수(승인/수정/거부), 마스터 브리프 최종 확정, 사람 핸드오프 판단 | 세션 준비 시간 단축(60분 → 15분), 월 6건 병렬 처리 능력, 일반론 방지, 코칭 품질 일관성 |
| **AI 분석 엔진** (시스템 내부 Actor) | 답변 패턴 분류(10유형), 브랜딩 요소 태깅(8종), 교차 검증, 코치 분석 노트 자동 생성, 원라이너 초안 3종 생성, 마스터 브리프 생성 | 정확도 ≥ 85%, 환각률 < 5%, 자동 트리거 성공률 100% |
| **시스템 관리자 / 개발자** | 시스템 배포·운영·모니터링, Supabase DB 관리, Claude API 연동 유지 | 99.9% 가용성, P95 응답 성능, 에러율 < 1% |
| **비즈니스 오너** | 제품 비전·방향 결정, KPI 관리, 파일럿 운영 | 고객 1인당 B2B 수주 ≥ 2건/분기, Option B 전환율 ≥ 10%, NPS ≥ 70 |

---

## 3. System Context and Interfaces

### 3.1 External Systems

| 외부 시스템 | 연동 방식 | 역할 |
| :--- | :--- | :--- |
| **Claude API (Anthropic)** | HTTPS REST API (POST /v1/messages) | LLM 추론 — 패턴 분류, 코칭 피드백 생성, 마스터 브리프 생성, 원라이너 초안 생성 |
| **Supabase** | PostgreSQL + JSONB, Supabase Client SDK | 리드 DB, 프로젝트 데이터, 브랜드 프로필, ANSWER_OUTPUT 저장 |
| **GA4 (Google Analytics 4)** | JavaScript SDK (이벤트 트래킹) | 진단 완료율, CTA 클릭율, 퍼널 분석 |
| **Typeform** | Webhook + REST API | NPS 설문 발송 및 응답 수집 |
| **UptimeRobot** | 외부 핑 모니터링 | 99.9% 가용성 감시 |
| **Datadog / Sentry** | SDK 삽입 | API Latency, 에러율 모니터링 및 Slack 알림 |

### 3.2 Client Applications

| 클라이언트 | 기술 스택 | 대상 사용자 |
| :--- | :--- | :--- |
| **랜딩페이지 + 진단 폼** | Next.js (웹) | 고객 (5060 전문가) |
| **진단 리포트 웹뷰** | Next.js (웹) | 고객 |
| **관리자 콘솔** | Next.js 또는 Retool (웹) | 운영자·코치 |

### 3.3 API Overview

| API 분류 | Endpoint (경로) | Method | 호출 주체 | 설명 |
| :--- | :--- | :---: | :--- | :--- |
| 진단 제출 | `/api/diagnosis/submit` | POST | 클라이언트 (고객) | 축약 12~16문항 답변 제출, Supabase `DIAGNOSIS` 저장, 리포트 생성 트리거 |
| 리드 생성 | `/api/leads` | POST | 클라이언트 (고객) | 진단 전 리드 정보 등록 (이름·전화·이메일) |
| 패턴 분류 | `/api/ai/classify-patterns` | POST | 관리자 콘솔 | F10 — 42문항 답변 입력 → 패턴 분류 결과 반환 |
| 브랜딩 매핑 | `/api/ai/map-branding` | POST | 관리자 콘솔 | F11 — 패턴 분류 결과 → 8개 브랜딩 요소 매핑 |
| 코치 분석 노트 | `/api/ai/coach-brief` | POST | 시스템 자동 트리거 | F15 — Stage 1 또는 Stage 3 제출 시 자동 호출, 코치 분석 노트 6항목 반환 |
| 마스터 브리프 생성 | `/api/ai/master-brief` | POST | 시스템 자동 트리거 (Q42 완료 시) | F1 — 42 OUTPUT 변수 입력 → 8개 섹션 마스터 브리프 생성 |
| 브리프 검수 | `/api/briefs/{id}/review` | PATCH | 관리자 콘솔 (검수자) | 검수자 승인·수정·거부 처리 |
| 리포트 조회 | `/api/reports/{diagnosis_id}` | GET | 클라이언트 (고객) | 진단 리포트 웹뷰 조회 |
| 고객 대시보드 | `/api/clients/{id}/dashboard` | GET | 클라이언트 (고객) | F5 — V1.5 이후 |

### 3.4 Interaction Sequences (핵심 시퀀스 다이어그램)

#### 시퀀스 1: 고객 축약 진단 → 리포트 → CTA 흐름

```mermaid
sequenceDiagram
    actor 고객
    participant LandingPage as 랜딩페이지 (Next.js)
    participant API as 백엔드 API
    participant Supabase
    participant ClaudeAPI as Claude API
    participant GA4

    고객->>LandingPage: 진단 시작 클릭
    LandingPage->>API: POST /api/leads (이름·이메일·전화)
    API->>Supabase: INSERT LEAD
    Supabase-->>API: lead_id
    API-->>LandingPage: lead_id 반환

    고객->>LandingPage: 12~16문항 답변 입력 및 제출
    LandingPage->>API: POST /api/diagnosis/submit {lead_id, answers[]}
    API->>Supabase: INSERT DIAGNOSIS (answers JSONB)
    API->>ClaudeAPI: System Prompt (126 정본 패턴) + 답변 텍스트
    ClaudeAPI-->>API: 패턴 분류 결과 + 브랜드 지수 + 리포트 초안
    API->>Supabase: UPDATE DIAGNOSIS (report, coaching_insights, brand_score)
    API-->>LandingPage: diagnosis_id
    LandingPage->>GA4: 이벤트: diagnosis_complete
    LandingPage->>고객: 진단 리포트 웹뷰 표시 + CTA 버튼
    고객->>LandingPage: CTA 클릭 (상담 신청)
    LandingPage->>GA4: 이벤트: cta_click
```

#### 시퀀스 2: F15 코치 분석 노트 자동 생성 흐름 (Stage 1)

```mermaid
sequenceDiagram
    actor 고객
    actor 코치
    participant API as 백엔드 API
    participant Supabase
    participant ClaudeAPI as Claude API
    participant AdminConsole as 관리자 콘솔

    고객->>API: Stage 1 (9문항) 제출 완료
    API->>Supabase: INSERT/UPDATE BRIEF (stage1_answers)
    API->>ClaudeAPI: POST /api/ai/coach-brief {stage=1, answers[9]}
    Note over ClaudeAPI: 126 정본 System Prompt<br/>EXTRACT Q1 정체성<br/>EXTRACT Q2 감정어<br/>CROSS-CHECK Q6×Q20<br/>CLASSIFY Q3 버팀목<br/>CLASSIFY Q32 추상도<br/>GENERATE 집중질문 2개
    ClaudeAPI-->>API: coach_note {6항목 + 스크립트 인용}
    API->>Supabase: UPDATE BRIEF (coach_note_stage1)
    API->>AdminConsole: 알림 푸시 (Stage 1 노트 생성 완료)
    코치->>AdminConsole: 코치 분석 노트 6항목 조회
    AdminConsole->>API: GET /api/briefs/{id}
    API->>Supabase: SELECT BRIEF
    Supabase-->>API: brief data
    API-->>AdminConsole: 노트 6항목 + 원문 인용
    코치->>AdminConsole: 항목별 승인/수정/거부
    AdminConsole->>API: PATCH /api/briefs/{id}/review
    API->>Supabase: UPDATE BRIEF (review_status)
```

#### 시퀀스 3: Q42 자동 트리거 → 마스터 브리프 생성 흐름

```mermaid
sequenceDiagram
    actor 고객
    actor 코치
    participant API as 백엔드 API
    participant Supabase
    participant ClaudeAPI as Claude API
    participant AdminConsole as 관리자 콘솔

    고객->>API: Stage 4 마지막 Q42 답변 제출
    API->>Supabase: INSERT ANSWER_OUTPUT (brand_why_final)
    Note over API: Q42 완료 감지 — 자동 트리거
    API->>API: 42 OUTPUT 변수 완전성 검증 (누락 < 5개 확인)
    alt OUTPUT 변수 누락 ≥ 5개
        API-->>고객: "추가 답변 필요 문항" 목록 표시, 브리프 생성 보류
    else OUTPUT 변수 충족
        API->>API: §5-5 교차 검증 매트릭스 9개 통과 검증
        alt 교차 검증 1개 이상 fail
            API->>AdminConsole: fail 항목 표시 + 사람 코치 핸드오프 권장 안내
            AdminConsole-->>코치: 검수자 명시 승인 요청
            코치->>AdminConsole: 명시 승인 처리
        end
        API->>ClaudeAPI: POST /api/ai/master-brief {all 42 OUTPUT variables}
        ClaudeAPI-->>API: 마스터 브리프 8개 섹션 + 원천 답변 추적 정보
        API->>Supabase: INSERT BRIEF (ai_output, output_mappings)
        API->>AdminConsole: 알림 — 마스터 브리프 생성 완료, 검수 요청
        코치->>AdminConsole: 브리프 검수·확정
        AdminConsole->>API: PATCH /api/briefs/{id}/review {status: approved}
        API->>고객: 마스터 브리프 납품 안내
    end
```

---

## 4. Specific Requirements

### 4.1 Functional Requirements

#### F1 — AI 마스터 브리프 생성기 관련 요구사항

| REQ-ID | 요구사항 설명 | Source (Story/Feature) | Priority | Acceptance Criteria |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-FUNC-001** | 시스템은 Q42 답변이 완료되는 즉시(완료 후 5초 이내) F1 마스터 브리프 생성기를 자동 호출해야 한다. | F1, §5-4-5, AC-Logic-5 | Must | **Given** Q42(`brand_why_final`) OUTPUT 변수가 Supabase에 저장될 때 **When** 시스템이 Q42 완료를 감지하면 **Then** 5초 이내에 `/api/ai/master-brief` 자동 호출 성공률 **100%**, 42 OUTPUT 변수 전달 완전성 **100%** |
| **REQ-FUNC-002** | 마스터 브리프 생성기는 42개 OUTPUT 변수를 입력으로 받아 8개 섹션(브랜드 원라이너·핵심 가치 3·강점 명제문·타깃 페르소나·브랜드 스토리·핵심 메시지·채널 전략·브랜드 WHY)을 각 1건 이상 생성해야 한다. | F1, AC-Out-1 | Must | **Given** 20문항 이상 응답 + 매핑 완료 **When** 마스터 브리프 생성 완료 시 **Then** 8개 섹션 생성률 **100%** |
| **REQ-FUNC-003** | 마스터 브리프의 각 섹션은 원천 답변 추적 정보(질문 번호 + 답변 일부 인용 + Stage 표시)를 포함해야 한다. | US-6, AC-Out-4 | Must | **Given** 마스터 브리프 8개 섹션 생성 완료 **When** 고객이 검토할 때 **Then** 각 섹션마다 원천 답변 추적 표시. 추적성 **100%**, 인용 정확도 **100%** |
| **REQ-FUNC-004** | AI 코칭 해석 메모의 일반론·뻔한 조언 비율은 검수자 태깅 기준 10% 미만이어야 한다. | F1, AC-Out-3 | Must | **Given** 브리프 생성 완료 **When** 검수자가 AI 코칭 해석 메모를 검토 **Then** 일반론 비율 < **10%** |
| **REQ-FUNC-005** | F1 마스터 브리프 생성 전 §5-5 교차 검증 매트릭스 9개를 모두 통과해야 한다. 1개 이상 fail 시 검수자 명시 승인 또는 사람 코치 핸드오프를 자동 권장한다. | AC-Neg-6 | Must | **Given** F1·F15가 §5-5 교차 검증 매트릭스 9개 중 1개 이상 fail **When** 마스터 브리프 생성 시도 **Then** fail 항목을 코치 검수 화면에 표시 + 사람 코치 핸드오프 자동 권장. 검수자 명시 승인 없이 생성 진입 불가 |

---

#### F2 — AI 브랜드 진단 툴 관련 요구사항

| REQ-ID | 요구사항 설명 | Source | Priority | Acceptance Criteria |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-FUNC-010** | 시스템은 축약 16문항(Q1·Q2·Q4·Q6·Q7·Q8·Q9·Q11·Q13·Q15·Q26·Q28·Q33·Q40·Q41·Q42) 기반의 웹 진단 폼을 제공해야 한다. | F2, §4-4 | Must | **Given** 고객이 진단 폼에 접근 **When** 진단을 진행 **Then** 16문항이 순서(PART 1→2→3→4)대로 표시됨. 문항 순서 오류 **0건** |
| **REQ-FUNC-011** | 진단 폼의 각 질문에는 "이 답변이 어디에 쓰이는지"(브랜드 자산 매핑 안내 문구)가 표시되어야 한다. | US-1, AC-Suf-1, E7 | Must | **Given** 고객이 42문항 중 20문항 이상 응답 **When** 진단 폼 진행 **Then** 각 질문 하단에 브랜드 자산 매핑 안내 표시. 안내 그룹 완주율이 미표시 그룹 대비 **+15%p** 이상 (E7 기준) |
| **REQ-FUNC-012** | 진단 완료 시 AI가 브랜드 지수·약점·강점 리포트를 즉시 생성하고, 하단에 프리미엄 매니지먼트 상담 CTA 버튼을 표시해야 한다. | F2, §11-3 | Must | **Given** 고객이 12문항 이상 응답 완료 **When** 진단 제출 **Then** 30초 이내에 리포트 화면 표시, CTA 버튼 노출. 리포트 CTA 클릭율 목표 **≥ 10%** (KPI 보조 5) |
| **REQ-FUNC-013** | 주관식 문항에 최소 단어수 3개 미만의 무의미한 텍스트(특수문자·"ㅋㅋㅋ" 등) 입력 시 클라이언트 단에서 유효성 검사 실패를 표시하고 서버로 전송을 차단해야 한다. | AC-Neg-3 | Must | **Given** 사용자가 주관식 문항에 3단어 미만·특수문자만 입력 **When** 제출 버튼 클릭 **Then** 유효성 검사 차단율 **100%**, 서버 전송 없음 |

---

#### F3 — 관리자 콘솔 관련 요구사항

| REQ-ID | 요구사항 설명 | Source | Priority | Acceptance Criteria |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-FUNC-020** | 관리자 콘솔은 AI 분석 노트(코치 분석 노트 6항목)를 한 화면에 표시하며, 각 항목별 원문 인용과 수정·승인 버튼을 제공해야 한다. | US-2, AC-Sess-2 | Must | **Given** Stage 1 코치 분석 노트 생성 완료 **When** 코치가 관리자 콘솔에서 노트 조회 **Then** 6개 항목 모두 한 화면에 표시 + 각 항목별 답변 원문 인용 + 수정·승인 버튼 제공. 화면 표시 정확도 **100%** |
| **REQ-FUNC-021** | 검수자가 AI 출력에서 환각(Hallucination) 문장을 "거부(Reject)" 태깅하면 해당 브리프 생성을 즉각 보류 처리해야 한다. | AC-Neg-2 | Must | **Given** AI가 답변 내용과 무관한 환각 텍스트를 포함 **When** 검수자가 "거부(Reject)" 태깅 **Then** 브리프 생성 즉각 보류 처리. 환각 비율 < **5%** 유지 목표 |
| **REQ-FUNC-022** | 고객 미승인 상태로 최종 리포트를 외부 전송 시도 시 시스템이 자동 차단해야 한다. | §9-3 | Must | **Given** 운영자가 고객 미승인 상태에서 리포트 외부 전송 시도 **When** 전송 버튼 클릭 **Then** 시스템 자동 차단 + 경고 메시지 표시. 차단율 **100%** |
| **REQ-FUNC-023** | 관리자 콘솔은 운영자 1인이 월 6건 병렬 처리할 수 있도록 프로젝트별 현황을 목록 형태로 제공해야 한다. | F3 | Must | **Given** 운영자가 관리자 콘솔 접속 **When** 프로젝트 목록 조회 **Then** 전체 프로젝트 현황(Stage, 상태, 최근 활동)을 단일 화면에 표시. 동시 6건 프로젝트 표시 오류 **0건** |

---

#### F4 — 리드 DB 관련 요구사항

| REQ-ID | 요구사항 설명 | Source | Priority | Acceptance Criteria |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-FUNC-030** | 진단 응답자의 정보(이름·전화·이메일·채널·상태)는 Supabase LEAD 테이블에 자동 적재되어야 한다. | F4 | Must | **Given** 고객이 리드 정보 입력 완료 **When** 제출 **Then** Supabase LEAD 테이블 INSERT 성공. 데이터 누락률 **0%** |
| **REQ-FUNC-031** | 브리프 납품 완료 후 7일이 경과하면 고객에게 5점 척도 팔로업 설문이 자동 발송되어야 한다. | AC-Out-6 | Should | **Given** 마스터 브리프 납품 완료 후 7일 경과 **When** 자동 팔로업 트리거 **Then** 고객에게 5점 척도 설문 발송. 설문 응답률 ≥ **70%**, 평균 점수 ≥ **4.0/5.0** 목표 |

---

#### F9 — Question Architecture Engine 관련 요구사항

| REQ-ID | 요구사항 설명 | Source | Priority | Acceptance Criteria |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-FUNC-040** | 시스템은 42문항 각각에 대해 파트(PART 1~4), Stage(1~4), 브랜딩 요소, 질문 의도, 연결 산출물, MVP 포함 여부를 메타데이터로 관리해야 한다. | F9, §4-1, §4-2 | Must | **Given** 질문 메타데이터 조회 요청 **When** API 호출 **Then** 42개 질문에 대해 PART·Stage·브랜딩 요소·의도·산출물·MVP 포함 여부 모두 반환. 누락 항목 **0건** |
| **REQ-FUNC-041** | MVP 축약 진단(16문항)에서도 PART 1→2→3→4 순서가 유지되어야 하며, 각 파트에서 핵심 문항만 선별 표시해야 한다. | §4-5 | Must | **Given** 고객이 MVP 진단 폼 접근 **When** 폼이 렌더링 **Then** Q1·Q2·Q4·Q6·Q7·Q8·Q9·Q11·Q13·Q15·Q26·Q28·Q33·Q40·Q41·Q42 순서로 표시. 순서 오류 **0건** |

---

#### F10 — Answer Pattern Classifier 관련 요구사항

| REQ-ID | 요구사항 설명 | Source | Priority | Acceptance Criteria |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-FUNC-050** | 시스템은 고객 답변을 P1~P10 10개 유형(직함 중심형·가치 중심형·자기축소형·회피형·타깃 과확장형·경험 나열형·방법론 보유형·채널 과욕형·실패 통합형·실패 회피형)으로 분류해야 한다. | F10, §5-1 | Must | **Given** 고객 답변 텍스트 입력 **When** F10 분류 처리 **Then** P1~P10 중 1개 이상의 분류 라벨 반환. 검수자 기준 분류 정확도 ≥ **85%** |
| **REQ-FUNC-051** | Q1 답변에서 직함·회사명·직위 중심 표현 2회 이상 + 가치·태도 형용사 0개 감지 시 P1(직함 중심형) 패턴 분류 및 후속 질문을 자동 생성해야 한다. | AC-Pat-1 | Must | **Given** Q1 자기소개에 직함·회사명 중심 답변 **When** AI가 답변 분석 **Then** P1 패턴 분류 + 후속 질문 "직함이 사라져도 남는 당신을 찾아봅시다" 생성. 분류 정확도 ≥ **85%**, 검수자 동의율 ≥ **80%** |
| **REQ-FUNC-052** | Q2·Q7 답변에서 "별로", "당연한", "대단한 건 아니", "그냥" 등 축소 표현 3회 이상 감지 시 P3(자기축소형) 패턴 분류 및 재프레이밍 메시지를 자동 생성해야 한다. | AC-Pat-2 | Must | **Given** Q2·Q7 답변에 자기축소 표현 ≥ 3회 **When** AI 분석 **Then** P3 분류 + 재프레이밍 메시지 생성. 감지 정밀도 ≥ **80%** |
| **REQ-FUNC-053** | Q9·Q26 답변에서 "모든 사람", "다양한 분", "누구나" 등 범용 표현 + 구체적 페르소나 정보 0개 감지 시 P5(타깃 과확장형) 분류 및 좁히기 코칭 질문을 자동 생성해야 한다. | AC-Pat-3 | Must | **Given** Q9·Q26에 범용 표현 + 구체 페르소나 0개 **When** AI 분석 **Then** P5 분류 + 좁히기 코칭 질문 생성. 감지 정밀도 ≥ **85%** |
| **REQ-FUNC-054** | Q15 답변 길이 < 50자 OR "없다"/"모르겠다"/"그냥 버텼다" 포함 시 P10(실패 회피형) 분류, 대안 질문 제공, 검수자에게 "사람 코치 개입 권장" 플래그를 자동 설정해야 한다. | AC-Pat-4, §11-2 | Must | **Given** Q15 답변 < 50자 OR 회피 표현 **When** AI 분석 **Then** P10 분류 + 대안 질문 + 코치 개입 플래그. 회피 감지 정밀도 ≥ **80%** |
| **REQ-FUNC-055** | CLASSIFY 동사를 포함한 15문항 처리 시 사전 정의 유형 집합 외의 분류 결과 발생률이 0%여야 한다. | AC-Logic-3 | Must | **Given** CLASSIFY 대상 15문항 답변 입력 **When** AI 분류 **Then** 사전 정의 유형 집합(예: Q1: IDENTITY_EXTERNAL·VALUES·SEARCHING) 외 결과 발생률 **0%** |
| **REQ-FUNC-056** | 동일 답변 텍스트를 재입력 시 핵심 필드(태그·분류·키워드 TOP3)가 3회 반복 실행 기준 80% 이상 일관되어야 한다. | AC-Logic-6 | Must | **Given** 동일 답변 텍스트 입력(재현성 테스트) **When** F10·F12·F15 처리 **Then** 핵심 필드 일관성 ≥ **80%** (3회 반복) |

---

#### F11 — Branding Output Mapper 관련 요구사항

| REQ-ID | 요구사항 설명 | Source | Priority | Acceptance Criteria |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-FUNC-060** | 시스템은 각 답변을 8개 브랜딩 구성 요소(정체성·핵심 가치·강점·스토리·이상적 고객·핵심 메시지·채널 전략·레거시) 중 하나 이상에 매핑해야 한다. | F11, AC-Map-1 | Must | **Given** 고객이 42문항 중 20문항 이상 응답 **When** 마스터 브리프 생성 요청 **Then** 각 답변을 8개 브랜딩 구성 요소 중 1개 이상에 매핑. 매핑률 ≥ **90%** |
| **REQ-FUNC-061** | 특정 브랜딩 구성 요소에 매핑된 답변이 0건이면 해당 영역에 대한 보완 질문을 자동 생성해야 한다. | AC-Map-2 | Must | **Given** 특정 브랜딩 요소 매핑 답변 0건 **When** 브리프 생성 전 검증 **Then** 해당 영역 보완 질문 자동 생성. 보완 질문 생성률 **100%** |
| **REQ-FUNC-062** | Q26(심리통계)과 Q33(인구통계) 답변을 통합한 페르소나 카드 1종을 자동 생성해야 한다. | AC-Map-4 | Must | **Given** Q26·Q33 답변 모두 수신 **When** AI 분석 **Then** 마음 상태·나이·직업·상황·고민·원하는 변화가 포함된 페르소나 카드 1종 생성. 통합 정확도 ≥ **85%**, 코치 동의율 ≥ **80%** |

---

#### F15 — Coach Session Brief Generator 관련 요구사항

| REQ-ID | 요구사항 설명 | Source | Priority | Acceptance Criteria |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-FUNC-070** | Stage 1(9문항) 제출 완료 시 시스템이 자동으로 코치 분석 노트 6항목을 생성해야 한다: ① Q1 정체성 분류 ② Q2 반복 감정어 추출 ③ Q6×Q20 가치 일관성 점수 ④ Q3 버팀목 분류 ⑤ Q32 추상도 평가 ⑥ 1차 세션 집중 탐색 질문 2개 추천 | US-2, AC-Sess-1 | Must | **Given** 고객이 Stage 1(9문항) 제출 완료 **When** AI 분석 완료 **Then** 6개 항목 생성률 **100%**, 코치 동의율 ≥ **85%** |
| **REQ-FUNC-071** | Stage 3(12문항) 제출 완료 시 시스템이 자동으로 코치 분석 노트 6항목을 생성해야 한다: ① Q41 vs Q1 정체성 변화 분석 ② Q26+Q33 페르소나 통합 ③ Q38 메시지 유형 분류 ④ Q29 장벽 유형 분류 ⑤ Q23 비전 구체성 등급 ⑥ 원라이너 초안 3종 자동 생성 | AC-Sess-3 | Must | **Given** 고객이 Stage 3(12문항) 제출 완료 **When** AI 분석 완료 **Then** 코치 동의율 ≥ **85%**, 원라이너 3종 생성률 **100%** |
| **REQ-FUNC-072** | 5060 특화 신호(직함 의존·자기축소·실패 회피·타깃 과확장 등) 1건 이상 감지 시 코칭 가이드의 실제 발언 스크립트(126 정본 기준, 168 풀 보조)를 노트에 첨부해야 한다. | US-3, AC-Sess-4 | Must | **Given** Stage 1·3 답변 중 5060 특화 신호 ≥ 1건 감지 **When** 코치 분석 노트 생성 **Then** 해당 신호별 실제 발언 스크립트 첨부. 스크립트 첨부율 **100%** |
| **REQ-FUNC-073** | Stage 1 + Stage 2 코치 메모 + Stage 3 답변이 통합된 데이터 기반으로, 2차 세션 24시간 전 원라이너 초안 3종(전문성형·공감형·결과형)을 자동 생성해야 한다. | US-5, AC-One-1 | Must | **Given** Stage 1·2·3 데이터 통합 **When** 2차 세션 24시간 전 자동 트리거 **Then** 3종 생성률 **100%**, 코치 채택률 ≥ **70%** |
| **REQ-FUNC-074** | 원라이너 초안 각 버전 옆에 원천 답변 인용(Q 번호 + 표현 출처)이 표시되어야 한다. | AC-One-2 | Must | **Given** 원라이너 초안 3종 생성 완료 **When** 코치 검수 **Then** 각 버전에 원천 답변 인용 표시. 인용 정확도 **100%** |
| **REQ-FUNC-075** | 코치 요청 시 원라이너 초안의 10글자 이하 압축 버전을 추가 생성해야 한다. | AC-One-3 | Should | **Given** 원라이너 초안에 단순화 옵션 활성화 **When** 코치 요청 **Then** 각 초안의 10글자 이하 압축 버전 생성. 압축 생성률 **100%**, 의미 보존율 ≥ **80%** |
| **REQ-FUNC-076** | Stage 1 코치 분석 노트 생성 최소 조건은 Stage 1 최소 6문항 이상 응답이며, 미충족 시 차단 메시지와 미응답 문항 목록을 표시해야 한다. | AC-Neg-4 | Must | **Given** 답변 데이터가 Stage 1 최소 기준(6문항) 미충족 **When** 노트 생성 시도 **Then** "Stage 1 최소 6문항 필요" 차단 메시지 + 미응답 문항 목록 표시. 차단 정확도 **100%** |
| **REQ-FUNC-077** | F15가 처리하는 의사 코드 MERGE/GENERATE 동사를 포함한 4문항(Q9·Q21·Q41·Q42)의 처리 결과는 반드시 다른 OUTPUT 변수들을 실제로 참조하여 생성해야 한다. | AC-Logic-7 | Must | **Given** GENERATE/MERGE 대상 문항(Q9·Q21·Q41·Q42) 처리 **When** AI 생성·머지 처리 **Then** 다중 변수 참조율 **100%**, 검수자 평가 ≥ **4.0/5.0** |

---

#### 답변 충분성 요구사항

| REQ-ID | 요구사항 설명 | Source | Priority | Acceptance Criteria |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-FUNC-080** | 고객 응답 문항이 20개 미만이면 마스터 브리프 생성을 차단하고 "응답 부족(최소 20문항 필요)" 경고를 출력해야 한다. | AC-Suf-1 | Must | **Given** 고객이 42문항 중 20문항 미만 응답 **When** 마스터 브리프 생성 요청 **Then** 경고 출력 + 생성 차단. 차단 정확도 **100%** |
| **REQ-FUNC-081** | 응답된 문항의 평균 답변 길이가 100자 미만이면 "답변 보충 필요" 알림과 해당 문항 목록을 표시해야 한다. | AC-Suf-2 | Must | **Given** 평균 답변 길이 < 100자 **When** AI 분석 시작 **Then** 알림 + 부족 문항 목록 표시. 부족 문항 식별 정확도 ≥ **95%** |
| **REQ-FUNC-082** | Q42 자동 트리거 발동 시 OUTPUT 변수 누락이 5개 이상이면 마스터 브리프 생성을 보류하고 추가 답변 필요 문항 목록을 표시해야 한다. | AC-Neg-7 | Must | **Given** Q42 자동 트리거 발동 시 OUTPUT 변수 누락 ≥ 5개 **When** F1 호출 **Then** 생성 보류 + 문항 목록 표시. 누락 검출 정확도 **100%** |

---

#### 교차 분석 요구사항

| REQ-ID | 요구사항 설명 | Source | Priority | Acceptance Criteria |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-FUNC-090** | Stage 1 Q1과 Stage 3 Q41 답변이 모두 수신되면 정체성 표현 변화 리포트(직함 의존 비율 변화·가치 표현 추가 개수·어휘 구체성 변화·코칭 변화 요약)를 자동 생성해야 한다. | US-4, AC-Cross-1 | Must | **Given** Q1 + Q41 답변 모두 수신 **When** AI 분석 **Then** 4개 지표 포함 변화 리포트 생성. 변화량 정확도 ≥ **90%** |
| **REQ-FUNC-091** | Q6·Q20 교차 검증으로 가치 일관성 점수(0~1)를 산출하고, 0.5 미만 시 "심화 탐색 필요" 플래그와 코치 알림을 자동 설정해야 한다. | AC-Cross-2 | Must | **Given** Q6·Q20 답변 수신 **When** AI 분석 **Then** 가치 일관성 점수 산출. 점수 < 0.5 시 플래그 + 코치 알림. 점수 정확도 ≥ **85%** |
| **REQ-FUNC-092** | Q1·Q21·Q41 3지점 정체성 일관성 점수를 계산하고 정체성 진화 시각화(Stage 1→2→3)를 생성해야 한다. | AC-Cross-3 | Should | **Given** Q1·Q21·Q41 답변 모두 수신 **When** AI 분석 **Then** 3지점 일관성 점수 + 진화 시각화 생성. 점수 정확도 ≥ **85%** |
| **REQ-FUNC-093** | Q32(레거시)·Q42(브랜드 WHY) 답변의 추상도 차이가 2단계를 초과하면 "WHY 재확인 필요" 플래그를 자동 설정해야 한다. | AC-Cross-4 | Should | **Given** Q32·Q42 답변 수신 **When** AI 분석 **Then** WHY 일관성 검증. 추상도 차이 > 2단계 시 플래그. 검출 정밀도 ≥ **80%** |

---

#### AI 처리 로직 정확도 요구사항

| REQ-ID | 요구사항 설명 | Source | Priority | Acceptance Criteria |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-FUNC-100** | 42문항 답변 처리 시 §10-3의 표준 OUTPUT 변수(42종)가 스키마(variable_name·구조)에 일치하여 누락 없이 생성되어야 한다. | AC-Logic-1 | Must | **Given** 42문항 답변 데이터 입력 **When** F1·F15 처리 **Then** 변수 생성률 ≥ **95%**, 스키마 일치율 **100%** |
| **REQ-FUNC-101** | EXTRACT 동사를 포함한 15문항에서 추출된 키워드·감정어는 답변 텍스트의 실제 표현에 근거해야 하며 환각을 포함하지 않아야 한다. | AC-Logic-2 | Must | **Given** EXTRACT 대상 15문항 입력 **When** AI 처리 **Then** 환각률 < **5%**, 검수자 동의율 ≥ **85%** |
| **REQ-FUNC-102** | §5-5 교차 검증 매트릭스의 9개 검증 항목에 대한 정합성 점수(0~1)를 산출해야 한다. | AC-Logic-4 | Must | **Given** CROSS-CHECK 대상 8문항 조합 입력 **When** AI 교차 검증 **Then** 9개 매트릭스 중 해당 검증 결과(통과/fail) + 정합성 점수 반환. 점수 산출 정확도 ≥ **85%** |

---

#### 오류 처리 요구사항

| REQ-ID | 요구사항 설명 | Source | Priority | Acceptance Criteria |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-FUNC-110** | LLM API 호출 응답 시간 초과(30초) 또는 500 에러 발생 시 최대 2회 자동 재시도 후, 실패 시 "AI 분석 지연 중, 최대 5분 소요" 안내 배너를 표시해야 한다. | AC-Neg-1 | Must | **Given** LLM API 응답 > 30,000ms 또는 500 에러 **When** 호출 **Then** 최대 2회 재시도. 재시도 성공률 ≥ **90%**, 실패 시 안내 배너 표시. API Timeout 임계치 **30,000ms** |
| **REQ-FUNC-111** | 원라이너 3종이 모두 의미적으로 동일(중복)할 경우 자동으로 재생성 요청을 수행하고 코치에게 "원천 답변 다양성 부족" 알림을 발송해야 한다. | AC-Neg-5 | Must | **Given** 원라이너 3종 생성 결과 모두 의미적 중복 **When** 검수 단계 **Then** 재생성 요청 + 코치 알림. 중복 검출 정확도 ≥ **90%** |

---

### 4.2 Non-Functional Requirements

#### 성능 (Performance)

| REQ-ID | 요구사항 설명 | Source | Priority | 측정 기준 |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-NF-001** | 일반 API(비LLM) 응답 시간은 P95 기준 200ms 미만이어야 한다. | §9-7 | Must | Datadog P95 지표. 2분간 임계치 초과 시 Slack Warning 알림 |
| **REQ-NF-002** | LLM 추론 API 응답 시간은 P95 기준 25초 미만이어야 한다. | §9-7 | Must | Datadog P95 지표. 2분간 임계치 초과 시 Slack Warning 알림 |
| **REQ-NF-003** | 진단 폼은 동시 100명 입력 시 지연 없이 처리되어야 한다. | §9-7 | Must | K6 부하 테스트 (런칭 전 수행) |
| **REQ-NF-004** | 진단 결과 리포트는 동시 500명 조회 시 P95 응답시간 500ms 이하를 유지해야 한다. | §9-7 | Must | K6 부하 테스트 |
| **REQ-NF-005** | Q42 완료 → F1 마스터 브리프 생성기 자동 호출은 5초 이내에 완료되어야 한다. | AC-Logic-5 | Must | API 호출 타임스탬프 측정 (Supabase `briefs.created_at` 기준) |
| **REQ-NF-006** | 마스터 브리프 초안 생성 소요시간은 건당 30분 이내이어야 한다. (북극성 보조 KPI 1) | §1-3 보조 KPI 1 | Must | `briefs.created_at` 타임스탬프 기준 측정 |

---

#### 가용성 (Availability)

| REQ-ID | 요구사항 설명 | Source | Priority | 측정 기준 |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-NF-010** | 핵심 시스템 월간 Uptime이 99.9% 이상(월 장애 허용 43.8분)이어야 한다. | §9-7 | Must | UptimeRobot 1분 단위 핑 테스트. 다운타임 발생 시 SMS 즉시 발송 |
| **REQ-NF-011** | HTTP 5xx 에러가 5분 내 5회 이상 스파이크 시 즉각 Slack Critical 알람을 발송해야 한다. | §9-7 | Must | Datadog 에러율 모니터링. 전체 API 에러율 < **1%** 유지 |

---

#### 보안 (Security)

| REQ-ID | 요구사항 설명 | Source | Priority | 측정 기준 |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-NF-020** | 모든 API 통신은 TLS 1.2 이상으로 암호화해야 한다. | §9-3 | Must | SSL/TLS 인증서 유효성 정기 점검 |
| **REQ-NF-021** | 고객의 경력 서사·실패 경험·개인 신념 등 자기서사 데이터는 일반 개인정보와 별도 보호 등급으로 관리해야 한다. | §9-3 | Must | Supabase Row Level Security (RLS) 정책 적용, 별도 필드 암호화 |
| **REQ-NF-022** | 고객 답변 데이터는 AI 학습용으로 재사용하지 않으며, 재사용 시 별도 동의를 수집해야 한다. | §9-3, C8 | Must | Claude API 이용 약관 준수 감사 로그 유지 |
| **REQ-NF-023** | 운영자·코치 기능은 RBAC(Role-Based Access Control)로 관리자 콘솔 접근을 제한해야 한다. | §9-3 | Must | 역할별 API 엔드포인트 접근 권한 테스트 |
| **REQ-NF-024** | 고객 미승인 상태의 최종 리포트 외부 전송이 시스템에서 차단되어야 한다. | §9-3 | Must | 차단율 **100%** — 자동화 테스트 |

---

#### AI 코칭 품질 (AI Coaching Quality)

| REQ-ID | 요구사항 설명 | Source | Priority | 측정 기준 |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-NF-030** | 답변 패턴 분류 정확도는 검수자 기준 85% 이상이어야 한다. | §9-6 | Must | 검수자 AI 분류 결과 승인/거부 태깅 → 월간 집계 |
| **REQ-NF-031** | 브랜드 요소 매핑 정확도는 검수자 기준 90% 이상이어야 한다. | §9-6 | Must | 매핑된 브랜딩 요소와 검수자 판단 일치율 월간 집계 |
| **REQ-NF-032** | AI 코칭 톤 적합도는 5060 고객 평가 4.3/5.0 이상이어야 한다. | §9-6 | Must | 브리프 검수 미팅 후 5점 척도 설문 |
| **REQ-NF-033** | AI 코칭 일반론·뻔한 조언 비율은 검수자 태깅 기준 10% 미만이어야 한다. | §9-6 | Must | 검수자 "일반론" 태깅 문장 수 / 전체 코칭 문장 수 |
| **REQ-NF-034** | 자기축소 재프레이밍 성공률은 고객 동의율 80% 이상이어야 한다. | §9-6 | Must | "AI 제시 재해석에 동의하십니까?" 설문 |
| **REQ-NF-035** | 최종 브랜드 문장의 "바로 활용 가능" 응답률은 80% 이상이어야 한다. | §9-6 | Must | 납품 후 설문: "이 문장을 수정 없이 사용할 수 있습니까?" |
| **REQ-NF-036** | 환각(Hallucination) 비율은 전체 AI 출력 기준 5% 미만이어야 한다. | AC-Neg-2, AC-Logic-2 | Must | 검수자 "거부(Reject)" 태깅 건수 / 전체 AI 출력 문장 수 |
| **REQ-NF-037** | 코치 분석 노트 6항목 적합도(수정 없이 사용 가능 응답)는 코치 동의율 85% 이상이어야 한다. | §9-6 | Must | F15 출력 노트 6개 항목별 "수정 없이 사용 가능" 응답 비율 |
| **REQ-NF-038** | 원라이너 3종 코치 채택률(원형 또는 부분 사용)은 70% 이상이어야 한다. | §9-6 | Must | 2차 세션에서 3종 중 1개 이상이 최종 원라이너 기반이 된 비율 |
| **REQ-NF-039** | F15 사용 시 코치 세션 준비 시간 단축률이 75% 이상이어야 한다. (F15 미사용 평균 60분 → 사용 시 ≤ 15분) | §9-6 | Must | 세션 준비 시간 측정 (코치 직접 기록 기반) |

---

#### 비즈니스 KPI (North Star & Supporting)

| REQ-ID | 요구사항 설명 | Source | Priority | 측정 기준 |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-NF-040** | 고객 1인당 분기 B2B 수주 건수가 2건 이상 달성되어야 한다. (북극성 KPI) | §1-3 북극성 | Must | Supabase `projects.outcome_count` 분기 집계 |
| **REQ-NF-041** | Option B(880만 원) 전환율이 월간 10% 이상이어야 한다. | §1-3 보조 KPI 2 | Should | Supabase 조인 쿼리 월간 집계 |
| **REQ-NF-042** | 고객 만족도(NPS)가 70 이상이어야 한다. | §1-3 보조 KPI 3 | Should | Typeform NPS 설문 (프로젝트 종료 시) |
| **REQ-NF-043** | 리테이너 전환율이 분기 30% 이상이어야 한다. | §1-3 보조 KPI 4 | Should | Supabase `retainers` 분기 집계 |
| **REQ-NF-044** | AI 진단 리포트 완독 → CTA 클릭율이 주간 10% 이상이어야 한다. | §1-3 보조 KPI 5 | Should | GA4 이벤트 `cta_click` / `diagnosis_complete` 주간 비율 |
| **REQ-NF-045** | 월간 신규 진단 리드 수가 50명 이상이어야 한다. | §1-3 보조 KPI 6 | Should | Supabase `leads` 월간 신규 INSERT 건수 |

---

#### 확장성 및 유지보수성 (Scalability & Maintainability)

| REQ-ID | 요구사항 설명 | Source | Priority | 측정 기준 |
| :--- | :--- | :--- | :---: | :--- |
| **REQ-NF-050** | MVP 단계에서 ANSWER_OUTPUT은 Supabase JSONB 단일 필드(`answer_outputs`)로 저장하며, V1.5 전환 시 정형화 테이블로 마이그레이션 가능한 구조를 유지해야 한다. | §10-3, C2 | Must | JSONB 필드 내 42개 표준 변수명 일관성 유지. 정규화 전환 스크립트 1주 내 작성 가능 |
| **REQ-NF-051** | Claude API System Prompt 업데이트(패턴 스크립트 교체 등)가 코드 배포 없이 설정 파일 변경으로 적용 가능해야 한다. | §9-6, C4 | Should | 설정 파일(또는 DB 기반 프롬프트 관리) 변경 후 재배포 없이 10분 이내 반영 |

---

## 5. Traceability Matrix

| Story / Feature | 요구사항 ID (REQ) | Test Case ID |
| :--- | :--- | :--- |
| US-1 (작성 동기 + 브랜드 자산 매핑 안내) | REQ-FUNC-011 | TC-011 |
| US-2 (코치 세션 준비 시간 단축) | REQ-FUNC-070, REQ-FUNC-020 | TC-070, TC-020 |
| US-3 (5060 특화 신호 → 스크립트 즉시 사용) | REQ-FUNC-051, REQ-FUNC-052, REQ-FUNC-053, REQ-FUNC-054, REQ-FUNC-072 | TC-051~054, TC-072 |
| US-4 (Stage 1 → 3 변화점 시각화) | REQ-FUNC-090 | TC-090 |
| US-5 (원라이너 초안 3종 자동 생성) | REQ-FUNC-073, REQ-FUNC-074 | TC-073, TC-074 |
| US-6 (마스터 브리프 원천 추적) | REQ-FUNC-003 | TC-003 |
| US-7 (일관성 충돌 자동 감지) | REQ-FUNC-091, REQ-FUNC-092, REQ-FUNC-093 | TC-091~093 |
| F1 (마스터 브리프 생성기) | REQ-FUNC-001~005, REQ-FUNC-100~102 | TC-001~005, TC-100~102 |
| F2 (AI 브랜드 진단 툴) | REQ-FUNC-010~013 | TC-010~013 |
| F3 (관리자 콘솔) | REQ-FUNC-020~023 | TC-020~023 |
| F4 (리드 DB) | REQ-FUNC-030~031 | TC-030~031 |
| F9 (Question Architecture Engine) | REQ-FUNC-040~041 | TC-040~041 |
| F10 (Answer Pattern Classifier) | REQ-FUNC-050~056 | TC-050~056 |
| F11 (Branding Output Mapper) | REQ-FUNC-060~062 | TC-060~062 |
| F15 (Coach Session Brief Generator) | REQ-FUNC-070~077 | TC-070~077 |
| AC-Suf-1~3 (답변 충분성) | REQ-FUNC-080~082 | TC-080~082 |
| AC-Neg-1~7 (오류 처리) | REQ-FUNC-110~111, REQ-FUNC-080~082 | TC-110~111 |
| §9-7 (성능·가용성) | REQ-NF-001~011 | TC-NF-001~011 |
| §9-3 (보안) | REQ-NF-020~024 | TC-NF-020~024 |
| §9-6 (AI 코칭 품질) | REQ-NF-030~039 | TC-NF-030~039 |
| §1-3 (비즈니스 KPI) | REQ-NF-040~045 | TC-NF-040~045 |
| §1-2 (성능·확장성) | REQ-NF-050~051 | TC-NF-050~051 |
| E11 (의사 코드 스펙 OUTPUT 정확도) | REQ-FUNC-100~102, REQ-NF-036 | TC-100~102, TC-NF-036 |
| PF-1 (코칭형 질문 → 전환율) | REQ-NF-044 | TC-NF-044 |
| PF-2 (42문항 패턴 추출) | REQ-NF-030 | TC-NF-030 |
| PF-6 (F15 코치 분석 노트 정확도) | REQ-NF-037, REQ-NF-039 | TC-NF-037, TC-NF-039 |
| PF-7 (원라이너 초안 효율) | REQ-NF-038 | TC-NF-038 |
| PF-8 (의사 코드 OUTPUT 정확도) | REQ-FUNC-100~102 | TC-100~102 |

---

## 6. Appendix

### 6.1 API Endpoint List

| Method | Endpoint | 설명 | 요청 주체 | 관련 REQ-ID |
| :---: | :--- | :--- | :--- | :--- |
| POST | `/api/leads` | 리드 정보 등록 (이름·이메일·전화) | 클라이언트 | REQ-FUNC-030 |
| POST | `/api/diagnosis/submit` | 12~16문항 답변 제출 + 리포트 생성 트리거 | 클라이언트 | REQ-FUNC-010, REQ-FUNC-012 |
| GET | `/api/reports/{diagnosis_id}` | 진단 리포트 웹뷰 조회 | 클라이언트 | REQ-FUNC-012 |
| POST | `/api/ai/classify-patterns` | F10 — 답변 패턴 분류 | 관리자 콘솔 | REQ-FUNC-050~056 |
| POST | `/api/ai/map-branding` | F11 — 브랜딩 요소 매핑 | 관리자 콘솔 | REQ-FUNC-060~062 |
| POST | `/api/ai/coach-brief` | F15 — Stage 1 또는 Stage 3 코치 분석 노트 자동 생성 | 시스템 자동 트리거 | REQ-FUNC-070~077 |
| POST | `/api/ai/master-brief` | F1 — 42 OUTPUT 변수 → 마스터 브리프 8개 섹션 생성 | 시스템 자동 트리거 (Q42) | REQ-FUNC-001~005 |
| PATCH | `/api/briefs/{id}/review` | 검수자 승인·수정·거부 처리 | 관리자 콘솔 | REQ-FUNC-021, REQ-FUNC-022 |
| GET | `/api/briefs/{id}` | 브리프 조회 (코치 분석 노트 포함) | 관리자 콘솔 | REQ-FUNC-020 |
| GET | `/api/clients/{id}/dashboard` | 고객 대시보드 (V1.5 이후) | 클라이언트 | F5 |
| GET | `/api/admin/projects` | 전체 프로젝트 현황 목록 조회 | 관리자 콘솔 | REQ-FUNC-023 |

---

### 6.2 Entity & Data Model

#### LEAD

| 컬럼명 | 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK | 리드 고유 식별자 |
| `name` | VARCHAR(100) | NOT NULL | 고객 이름 |
| `phone` | VARCHAR(20) | | 전화번호 |
| `email` | VARCHAR(255) | NOT NULL, UNIQUE | 이메일 |
| `title` | VARCHAR(200) | | 현재 직함·직위 |
| `company` | VARCHAR(200) | | 소속 기관·회사 |
| `channel` | VARCHAR(100) | | 유입 채널 (GA4 Source) |
| `status` | ENUM | NOT NULL | `new`, `contacted`, `consulting`, `contracted`, `completed` |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | 등록 시각 |

#### DIAGNOSIS

| 컬럼명 | 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK | 진단 고유 식별자 |
| `lead_id` | UUID | FK → LEAD | 연결 리드 |
| `answers` | JSONB | NOT NULL | 12~16문항 답변 원문 배열 |
| `report` | JSONB | | AI 생성 진단 리포트 |
| `coaching_insights` | JSONB | | AI 코칭 인사이트 메모 |
| `brand_score` | FLOAT | | AI 산출 브랜드 지수 (0~100) |
| `created_at` | TIMESTAMP | NOT NULL | 진단 생성 시각 |

#### CLIENT

| 컬럼명 | 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK | |
| `lead_id` | UUID | FK → LEAD | 연결 리드 |
| `name` | VARCHAR(100) | NOT NULL | |
| `package` | ENUM | NOT NULL | `option_a`, `option_b`, `retainer` |
| `paid_amount` | INT | | 결제 금액 (원) |
| `contract_date` | DATE | | 계약일 |

#### PROJECT

| 컬럼명 | 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK | |
| `client_id` | UUID | FK → CLIENT | |
| `status` | ENUM | NOT NULL | `stage1`, `session1`, `stage2`, `stage3`, `session2`, `stage4`, `brief_generated`, `delivered` |
| `target_delivery` | DATE | | 목표 납품일 |
| `actual_delivery` | DATE | | 실제 납품일 |
| `outcome_count` | INT | DEFAULT 0 | 고객 B2B 수주 건수 (북극성 KPI) |

#### BRIEF

| 컬럼명 | 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK | |
| `project_id` | UUID | FK → PROJECT | |
| `raw_input` | TEXT | | 인터뷰 Raw 텍스트 |
| `ai_output` | JSONB | | F1 마스터 브리프 8개 섹션 AI 출력 |
| `pattern_analysis` | JSONB | | F10 패턴 분류 결과 |
| `output_mappings` | JSONB | | F11 브랜딩 요소 매핑 결과 |
| `coach_note_stage1` | JSONB | | F15 Stage 1 코치 분석 노트 6항목 |
| `coach_note_stage3` | JSONB | | F15 Stage 3 코치 분석 노트 6항목 + 원라이너 3종 |
| `reviewed_output` | TEXT | | 검수자 확정 최종 출력 |
| `review_status` | ENUM | | `pending`, `approved`, `rejected`, `on_hold` |
| `cross_check_results` | JSONB | | §5-5 교차 검증 매트릭스 9개 결과 |
| `human_handoff_flags` | JSONB | | 사람 코치 핸드오프 플래그 목록 |
| `version` | INT | DEFAULT 1 | 브리프 버전 번호 |
| `created_at` | TIMESTAMP | NOT NULL | |
| `updated_at` | TIMESTAMP | | |

#### BRAND_PROFILE

| 컬럼명 | 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK | |
| `project_id` | UUID | FK → PROJECT | |
| `one_liner` | TEXT | | 브랜드 원라이너 |
| `core_values` | JSONB | | 핵심 가치 3개 + 행동 사례 |
| `strength_statement` | TEXT | | 강점 명제문 |
| `target_persona` | JSONB | | 타깃 페르소나 카드 |
| `brand_story` | TEXT | | 브랜드 스토리 핵심 (BTA 구조) |
| `core_message` | TEXT | | 핵심 메시지 |
| `channel_strategy` | JSONB | | 채널 전략 (1순위 + 보조) |
| `brand_why` | TEXT | | 브랜드 WHY 선언문 |
| `version` | INT | DEFAULT 1 | |
| `created_at` | TIMESTAMP | NOT NULL | |

#### ANSWER_OUTPUT

| 컬럼명 | 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| `output_id` | UUID | PK | |
| `answer_id` | UUID | FK → ANSWER | |
| `question_number` | INT | NOT NULL | 1~42 |
| `output_variable_name` | VARCHAR(100) | NOT NULL | 표준 변수명 (예: `identity_baseline`, `brand_why_final`) |
| `output_data` | JSONB | NOT NULL | OUTPUT 객체 직렬화 (§10-3 스키마) |
| `cross_check_results` | JSONB | | 교차 검증 결과 (§5-5 매트릭스) |
| `confidence_score` | FLOAT | | AI 신뢰도 0~1 |
| `flags` | VARCHAR[] | | `re_explore_needed`, `human_handoff_recommended` 등 |
| `created_at` | TIMESTAMP | NOT NULL | |
| `updated_at` | TIMESTAMP | | |

#### RETAINER

| 컬럼명 | 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK | |
| `client_id` | UUID | FK → CLIENT | |
| `monthly_fee` | INT | NOT NULL | 월 정액 (원) |
| `start_date` | DATE | NOT NULL | |
| `end_date` | DATE | | |
| `status` | ENUM | NOT NULL | `active`, `paused`, `terminated` |

---

#### 42개 표준 OUTPUT 변수 요약

| Stage | 질문 | 변수명 | 타입 |
| :--- | :--- | :--- | :--- |
| Stage 1 | Q1 | `identity_baseline` | object `{tag, top_words[3], next_difficulty}` |
| Stage 1 | Q2 | `candidate_values[]` | string[] (감정어 TOP3) |
| Stage 1 | Q3 | `story_turning_point_hint` | object `{period, support_type, keywords[]}` |
| Stage 1 | Q6 | `decision_pattern` | object `{type, key_principle}` |
| Stage 1 | Q7 | `confidence_statement_draft` | string |
| Stage 1 | Q10 | `core_message_seed` | string |
| Stage 1 | Q18 | `brand_consistency_basis` | object `{pattern_type, keywords[]}` |
| Stage 1 | Q20 | `brand_values_confirmed[]` | object[] `[{value, evidence}]` |
| Stage 1 | Q32 | `brand_why_draft` | string |
| Stage 2 | Q4 | `expertise_statement` | string |
| Stage 2 | Q5 | `external_brand_keywords[]` + `perception_gap_score` | object |
| Stage 2 | Q8 | `brand_story_chapter` | object `{type, period, keywords[]}` |
| Stage 2 | Q11 | `strength_portfolio` | object `{top3, type_classification}` |
| Stage 2 | Q12 | `natural_authority` | object `{domain, type}` |
| Stage 2 | Q13 | `methodology_draft` | object `{name_candidates[2~3], structure_3steps}` |
| Stage 2 | Q15 | `resilience_story_draft` | object `{before, crisis, learning}` |
| Stage 2 | Q16 | `passion_expertise_overlap` | object `{overlap_domain}` |
| Stage 2 | Q21 | `strength_statement_v1` | object `{draft, improvement_hints[]}` |
| Stage 2 | Q35 | `usp_statement_draft` | string |
| Stage 2 | Q37 | `brand_story_draft` | object `{before, turning, after}` |
| Stage 3 | Q23 | `vision_lifestyle_draft` | object `{key_elements[3], direction}` |
| Stage 3 | Q24 | `second_chapter_direction` | object `{direction, asset_link_hints[]}` |
| Stage 3 | Q26 | `persona_psychological_profile` | object `{mind_state, situation, desire}` |
| Stage 3 | Q27 | `brand_promise` | string |
| Stage 3 | Q29 | `barrier_map` | object `{type, removal_strategy}` |
| Stage 3 | Q31 | `brand_driver` | string |
| Stage 3 | Q33 | `persona_card` | object `{name_alias, age, situation, pain_language, desired_change}` |
| Stage 3 | Q34 | `customer_pain_language` | string[] |
| Stage 3 | Q38 | `core_message` | object `{confirmed_sentence, variants[2]}` |
| Stage 3 | Q40 | `channel_strategy` | object `{primary, frequency, format}` |
| Stage 3 | Q41 | `oneliner_draft_v1[]` | object[] `[{type, draft, source_questions[]}]` × 3 |
| Stage 3 | **Q42** | `brand_why_final` | string 🚨 마스터 브리프 자동 생성 트리거 |
| Stage 4 | Q9 | `persona_final` | object (Q26+Q33+Q9 머지) |
| Stage 4 | Q14 | `network_map` | object `{first_customer[], partner[], evangelist[]}` |
| Stage 4 | Q17 | `optimal_condition` | object `{type, channel_fit_recommendation}` |
| Stage 4 | Q19 | `expression_environment` | object `{environment_type, service_format}` |
| Stage 4 | Q22 | `gap_analysis` | object `{match_unmatch, message_correction}` |
| Stage 4 | Q25 | `unrealized_resource` | object `{desire, activation_direction}` |
| Stage 4 | Q28 | `contribution_style` | object `{method, channel_fit_final}` |
| Stage 4 | Q30 | `brand_editing` | string |
| Stage 4 | Q36 | `brand_vocabulary_final` | object `{words[5], type_classification, usage_context}` |
| Stage 4 | Q39 | `tone_and_manner` | object `{style_type, traits[3], forbidden_patterns[]}` |

---

### 6.3 Detailed Interaction Models

#### 시퀀스 4: Stage 3 제출 → 원라이너 3종 생성 → 2차 세션 준비 흐름

```mermaid
sequenceDiagram
    actor 고객
    actor 코치
    participant API as 백엔드 API
    participant Supabase
    participant ClaudeAPI as Claude API
    participant AdminConsole as 관리자 콘솔

    고객->>API: Stage 3 (12문항) 제출 완료
    API->>Supabase: INSERT ANSWER_OUTPUT (Stage 3 변수 12개)
    API->>ClaudeAPI: POST /api/ai/coach-brief {stage=3, answers[stage1+2+3]}
    Note over ClaudeAPI: COMPARE Q41 vs Q1 (정체성 변화)<br/>MERGE Q26+Q33 페르소나 통합<br/>CLASSIFY Q38 메시지 유형<br/>CLASSIFY Q29 장벽 유형<br/>CLASSIFY Q23 비전 구체성<br/>GENERATE 원라이너 3종 (전문성형/공감형/결과형)
    ClaudeAPI-->>API: coach_note_stage3 {6항목 + 원라이너 3종}
    API->>Supabase: UPDATE BRIEF (coach_note_stage3)

    Note over API: 2차 세션 24시간 전 자동 트리거
    API->>AdminConsole: 알림 — Stage 3 노트 + 원라이너 3종 생성 완료
    코치->>AdminConsole: 원라이너 3종 조회 (각 버전별 원천 답변 인용 포함)
    코치->>AdminConsole: 원라이너 선택/수정 후 승인
    AdminConsole->>API: PATCH /api/briefs/{id}/review {oneliner_confirmed}
    API->>Supabase: UPDATE BRIEF (reviewed_oneliner)
    코치->>고객: 2차 코칭 세션 진행 (원라이너 확정 + 브리프 방향)
```

#### 시퀀스 5: 교차 검증 매트릭스 처리 흐름

```mermaid
sequenceDiagram
    participant API as 백엔드 API
    participant ClaudeAPI as Claude API
    participant Supabase
    participant AdminConsole as 관리자 콘솔

    API->>API: 42 OUTPUT 변수 전체 수집 확인
    API->>ClaudeAPI: §5-5 교차 검증 9개 매트릭스 요청
    Note over ClaudeAPI: 검증 1: Q2+Q6+Q20 가치 일관성<br/>검증 2: Q1+Q21+Q41 정체성 진화<br/>검증 3: Q3+Q8+Q15+Q37 스토리 일관성<br/>검증 4: Q26+Q33+Q9 페르소나 정합<br/>검증 5: Q4+Q12 전문성 vs 자연 권위<br/>검증 6: Q5+Q11 외부/내부 강점 갭<br/>검증 7: Q1+Q22 인식 갭<br/>검증 8: Q31+Q32+Q42 WHY 통합<br/>검증 9: Q17+Q19+Q28+Q40 채널 적합성
    ClaudeAPI-->>API: cross_check_results {9개 점수 + pass/fail}
    API->>Supabase: UPDATE BRIEF (cross_check_results)

    alt 9개 모두 pass
        API->>API: F1 마스터 브리프 생성 진행
    else 1개 이상 fail
        API->>AdminConsole: fail 항목 목록 표시 + 사람 코치 핸드오프 권장
        AdminConsole-->>코치: 명시 승인 요청
    end
```

#### 시퀀스 6: 오류 처리 — LLM API 타임아웃 흐름

```mermaid
sequenceDiagram
    participant API as 백엔드 API
    participant ClaudeAPI as Claude API
    participant Client as 클라이언트 (고객/콘솔)

    API->>ClaudeAPI: LLM 추론 요청
    Note over ClaudeAPI: 응답 대기 중...

    alt 응답 시간 > 30,000ms 또는 500 에러
        ClaudeAPI-->>API: Timeout / 500 Error
        API->>API: 자동 재시도 #1
        alt 재시도 #1 실패
            API->>API: 자동 재시도 #2
            alt 재시도 #2 실패
                API-->>Client: "AI 분석 지연 중, 최대 5분 소요" 안내 배너 표시
                API->>Sentry: 에러 로그 기록
                API->>Slack: Warning 알림 발송
            else 재시도 #2 성공
                ClaudeAPI-->>API: 정상 응답
                API-->>Client: 결과 반환
            end
        else 재시도 #1 성공
            ClaudeAPI-->>API: 정상 응답
            API-->>Client: 결과 반환
        end
    else 정상 응답 (≤ 25초 P95)
        ClaudeAPI-->>API: 정상 응답
        API-->>Client: 결과 반환
    end
```

---

### 6.4 Validation Plan (검증 계획 요약)

| 실험 ID | 가설 | 성공 기준 | 관련 REQ-ID |
| :---: | :--- | :--- | :--- |
| E5 | 42문항 기반 AI 분석 ↔ 코치 분석 일치율 ≥ 80% | AI-코치 일치율 ≥ **80%** | REQ-NF-030 |
| E6 | 12문항 진단 CTA 클릭율 ≥ 5문항 대비 1.5배 | 12문항 그룹 CTA 클릭율 **≥ 1.5배** | REQ-NF-044 |
| E7 | 안내 문구 포함 완주율 +15%p | 안내 문구 그룹 완주율 **+15%p** | REQ-FUNC-011 |
| E8 | 패턴 기반 피드백 만족도 ≥ 4.3/5.0 | **≥ 4.3/5.0** | REQ-NF-032 |
| E9 | F15 코치 분석 노트 동의율 ≥ 85%, 세션 준비 시간 단축 ≥ 75% | 동의율 ≥ **85%**, 단축률 ≥ **75%** | REQ-NF-037, REQ-NF-039 |
| E10 | 원라이너 3종 초안으로 2차 세션 시간 ≥ 50% 단축 | 시간 단축 ≥ **50%** | REQ-NF-038 |
| E11 | §5-4 의사 코드 스펙 → 42 OUTPUT 변수 사양 준수 | 스키마 일치율 **100%**, 환각률 < **5%**, 분류 정확도 ≥ **85%**, 교차 검증 통과율 ≥ **80%** | REQ-FUNC-100~102, REQ-NF-036 |

---

*SRS-001 v1.0 — End of Document*
*Source of Truth: PRD_v0_4_2.md (2026-04-25)*
*Standard: ISO/IEC/IEEE 29148:2018*
