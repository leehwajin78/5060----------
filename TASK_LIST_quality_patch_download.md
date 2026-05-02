# TASK_LIST_v1 품질 검토 및 보강본

**대상 파일:** TASK_LIST_v1(2).md  
**검토 기준:** 개발 실행 가능성, Task 단위 명확성, API/DB/로직/예외/테스트 구체성, 보안·운영 반영도  
**작성 목적:** 기존 TASK LIST 중 품질이 부족한 항목을 식별하고, 개발자가 바로 구현 가능한 수준으로 보강하기 위한 패치 문서  
**작성일:** 2026-05-02

---

## 1. 핵심 결론

기존 TASK_LIST_v1은 **82개 태스크를 단계별로 분해한 WBS 문서로는 양호**합니다.  
다만 실제 개발자가 이 문서만 보고 바로 구현하기에는 일부 태스크가 **제목 중심**으로 작성되어 있어, 다음 보강이 필요합니다.

| 구분 | 판정 |
|---|---|
| 전체 구조 | 양호 |
| 구현 지시 수준 | 보강 필요 |
| API 명세 수준 | 부족 |
| DB 제약조건 명세 | 부족 |
| AI 호출·실패 처리 | 부족 |
| 개인정보·보안 기준 | 보강 필요 |
| 테스트 기준 | 일부 부족 |
| 운영·배포 체크리스트 | 보강 필요 |

**최종 판단:**  
현재 문서는 “Task 목록”으로는 사용할 수 있으나, “GitHub Issue 또는 AI 개발 지시서”로 사용하려면 본 보강본을 함께 적용해야 합니다.

---

## 2. 기존 TASK_LIST의 강점

| 항목 | 긍정 평가 |
|---|---|
| 단계 구분 | DB → API → Mock → Query → Command → FE → Test → Infra 순서가 명확함 |
| 총량 관리 | 총 82개 태스크로 MVP-Free 범위를 관리 가능하게 분해함 |
| 의존성 표시 | 선행 태스크가 포함되어 있어 구현 순서 설계에 유리함 |
| CQRS 분리 | Read/Write 태스크가 구분되어 있어 로직 구조화에 도움 됨 |
| 테스트 분리 | 별도 테스트 태스크 15개를 둔 점은 실무적으로 유용함 |
| MVP 범위 통제 | V1.5/V2 Deferred 항목을 제외한다고 명시해 범위 확산을 막음 |

---

## 3. 품질 부족 항목 식별 기준

아래 중 2개 이상에 해당하는 태스크는 “보강 필요”로 분류했습니다.

| 기준 | 설명 |
|---|---|
| 입력값 불명확 | 어떤 데이터가 들어오는지 명시되지 않음 |
| 출력값 불명확 | 성공 시 무엇을 반환하거나 저장해야 하는지 모호함 |
| 검증 조건 부족 | 필수값, 길이, 형식, 상태값 제한 등이 빠짐 |
| 예외 처리 부족 | 실패 상황과 에러 응답 방식이 없음 |
| 상태 전이 불명확 | submitted, draft, approved 등 상태 변경 규칙이 명확하지 않음 |
| 테스트 가능성 부족 | 완료 여부를 자동 테스트로 검증하기 어려움 |
| 보안 기준 부족 | 개인정보, 인증, 접근 제어, AI payload 익명화 기준이 약함 |
| 운영 기준 부족 | 배포, 장애 대응, 로그, 롤백 기준이 부족함 |

---

## 4. 보강 우선순위 요약

| 우선순위 | 대상 | 이유 |
|---|---|---|
| P0 | API-001~008 | 프론트·백엔드·테스트의 계약 기준이므로 가장 먼저 확정 필요 |
| P0 | DB-001~007 | 모든 기능의 데이터 기반이므로 제약조건과 관계 설정 필요 |
| P0 | C-001~010 | 핵심 비즈니스 로직이며 상태 전이와 예외 처리가 중요함 |
| P0 | SEC-001~003, DPR-001~002 | 개인정보와 외부 리포트 접근 제어는 MVP에서도 필수 |
| P1 | T-001~015 | 테스트 케이스가 있으나 fixture, 예상 결과, 실패 조건 보강 필요 |
| P1 | INF-002~005 | 무료 인프라 제약과 환경변수 기준 보강 필요 |
| P2 | MOCK-001~003 | 개발 초기에는 유용하나 실제 구현 전 스키마 정합성 보강 필요 |
| P2 | OPS-001~002 | MVP 후반 배포 전 체크리스트로 확장 필요 |

---

# 5. 품질 부족 태스크 상세 식별 및 보강 방향

## 5-1. DB 태스크 보강 필요 항목

### 대상 태스크

- DB-001: Prisma 프로젝트 초기화 및 datasource 설정
- DB-002: Lead 테이블 스키마·마이그레이션
- DB-003: Diagnosis 테이블 스키마·마이그레이션
- DB-004: Answer 테이블 스키마·마이그레이션
- DB-005: Report 테이블 스키마·마이그레이션
- DB-006: AiRun 테이블 스키마·마이그레이션
- DB-007: ReviewLog 테이블 스키마·마이그레이션
- DB-008: AdminUser 테이블 스키마

### 부족한 점

| 항목 | 문제 |
|---|---|
| 필드 타입 | 각 필드의 자료형, nullable 여부, 기본값이 없음 |
| 관계 설정 | FK onDelete, cascade 여부가 명시되지 않음 |
| 인덱스 | leadId, diagnosisId, status, createdAt 기준 조회 최적화 기준 없음 |
| enum 연동 | Diagnosis/Report/AiRun 상태값 enum과 DB 필드 연결 기준 부족 |
| 개인정보 보호 | Lead.contact 저장 방식, 삭제 정책, 보존 기간 기준 없음 |

### 보강 방향

DB 태스크는 아래 기준까지 확장해야 합니다.

```md
## DB-XXX 상세 명세

### 목적
- 해당 테이블이 어떤 기능을 지원하는지 설명한다.

### Prisma Model 필드
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|---|---|---|---|---|

### 관계
- FK 관계
- onDelete 정책
- unique/index 설정

### 제약조건
- nullable 여부
- enum 제한
- 문자열 길이 제한
- 중복 허용 여부

### 완료 기준
- prisma migrate dev 성공
- prisma generate 성공
- seed/mock 데이터 생성 가능
- 관련 query/command에서 타입 에러 없음
```

---

## 5-2. API·DTO 태스크 보강 필요 항목

### 대상 태스크

- API-001: createLead Server Action DTO 정의
- API-002: submitDiagnosis Server Action DTO 정의
- API-003: POST /api/ai/generate-report DTO 정의
- API-004: AI 진단 리포트 Zod Schema 작성
- API-005: reviewReport Server Action DTO 정의
- API-006: regenerateReport Server Action DTO 정의
- API-007: GET /api/reports/[id] Response DTO 정의
- API-008: 공통 에러 응답 코드 정의

### 부족한 점

| 항목 | 문제 |
|---|---|
| 요청 필드 | 필수/선택 필드가 구분되지 않음 |
| 응답 구조 | success, data, error 형태의 표준 응답이 없음 |
| 에러 코드 | 400/404/500만 있고 401/403/409/422가 없음 |
| Validation | Zod schema 기준이 상세하지 않음 |
| 보안 | AI payload에서 PII 제거 여부가 API 계약에 명시되지 않음 |

### 보강 방향

API 태스크는 아래 형식을 적용해야 합니다.

```md
## API-XXX 상세 명세

### 목적
- 이 API 또는 Server Action이 해결하는 문제를 설명한다.

### Request DTO
| 필드 | 타입 | 필수 | 검증 조건 | 설명 |
|---|---|---|---|---|

### Response DTO
```ts
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

### Validation Rule
- 필수값 검증
- 길이 검증
- enum 검증
- 배열 개수 검증

### Error Case
| 상황 | HTTP/Action Error | 메시지 |
|---|---|---|

### 완료 기준
- Zod schema 작성
- TypeScript type export
- 실패 케이스 테스트 가능
```

---

## 5-3. Command 태스크 보강 필요 항목

### 대상 태스크

- C-001: createLead
- C-002: submitDiagnosis 답변 유효성 검증
- C-003: Answer 16건 + Diagnosis 생성
- C-004: AI 리포트 생성 요청 payload 구성
- C-005: Gemini 호출 + Zod 검증 + Report 저장
- C-006: AI 리포트 생성 실패 처리
- C-007: reviewReport 리포트 수정 저장
- C-008: 승인/거부 상태 변경
- C-009: ReviewLog 생성
- C-010: regenerateReport
- C-011: CTA 클릭 이벤트 기록

### 부족한 점

| 항목 | 문제 |
|---|---|
| 트랜잭션 | Lead, Diagnosis, Answer 저장 시 transaction 기준 없음 |
| 상태 전이 | Diagnosis.status와 Report.status 변경 순서가 불명확함 |
| 실패 처리 | AI 실패 시 사용자에게 무엇을 보여줄지 불명확함 |
| 재생성 제한 | 진단당 1회 제한 기준을 어디에서 검증할지 없음 |
| 감사 로그 | beforeJson/afterJson 저장 범위와 개인정보 포함 여부가 없음 |

### 보강 방향

Command 태스크는 아래 형식으로 보강해야 합니다.

```md
## C-XXX 상세 명세

### 목적
- 사용자의 어떤 행동을 처리하는지 설명한다.

### 입력
- DTO 이름
- 필수 필드
- 인증 필요 여부

### 처리 절차
1. 입력값 검증
2. 권한 검증
3. DB 조회
4. 상태 검증
5. DB 변경
6. 로그 기록
7. 응답 반환

### Transaction 범위
- 하나의 transaction 안에서 처리해야 하는 DB 작업을 명시한다.

### 예외 처리
| 상황 | 처리 방식 | 반환 메시지 |
|---|---|---|

### 완료 기준
- 성공 케이스 통과
- 실패 케이스 통과
- DB 상태 전이 검증
- 로그 기록 검증
```

---

## 5-4. AI 리포트 관련 태스크 보강 필요 항목

### 대상 태스크

- API-003
- API-004
- C-004
- C-005
- C-006
- C-010
- SEC-001
- LOG-001
- T-005
- T-006
- T-007
- T-014

### 부족한 점

| 항목 | 문제 |
|---|---|
| AI 입력 | 질문코드+답변만 보내야 한다고 되어 있으나 payload 구조가 없음 |
| AI 출력 | DiagnosisReport JSON의 세부 필드와 필수값이 불명확함 |
| 검증 실패 | Zod 검증 실패 시 재시도 여부, draft 저장 여부가 없음 |
| timeout | 60초 초과 처리 기준이 UI/서버 양쪽에서 불명확함 |
| 개인정보 제거 | 이름, 연락처, 이메일, 전화번호 제거 기준이 정규식 수준까지 없음 |
| 비용 제한 | Free Tier 초과나 rate limit 대응 기준이 없음 |

### AI 리포트 태스크 보강안

```md
## AI-REPORT 공통 명세

### AI 입력 Payload 원칙
- lead.name 전송 금지
- lead.contact 전송 금지
- 이메일, 전화번호, 실명 추정 문자열 제거
- questionCode와 answerText만 전송
- answerText는 trim 처리 후 전송

### 예시 Payload
```json
{
  "diagnosisId": "diag_123",
  "answers": [
    {
      "questionCode": "Q01",
      "answerText": "오랜 현장 경험을 바탕으로 중장년 전문가를 돕고 싶습니다."
    }
  ]
}
```

### AI 출력 Report JSON 필수 구조
```json
{
  "summary": "string",
  "brandCore": {
    "keywords": ["string"],
    "positioning": "string",
    "oneLiner": "string"
  },
  "assets": {
    "lectureTopics": ["string"],
    "consultingThemes": ["string"],
    "proposalAngles": ["string"]
  },
  "recommendations": [
    {
      "title": "string",
      "description": "string",
      "sourceQuestionCodes": ["Q01", "Q02"]
    }
  ],
  "nextActions": ["string"]
}
```

### 실패 처리
| 실패 상황 | 처리 기준 |
|---|---|
| Gemini API 실패 | AiRun.status=failed 저장, Report 생성하지 않음 |
| Zod 검증 실패 | AiRun.status=failed 저장, errorMessage에 schema error 요약 저장 |
| 60초 초과 | 사용자 화면에는 처리 중 안내, 관리자 화면에는 실패/재시도 가능 표시 |
| 재생성 1회 초과 | 409 Conflict 성격의 에러 반환 |

### 완료 기준
- PII 제거 테스트 통과
- Zod schema 통과 테스트 통과
- 실패 시 Answer 데이터 보존
- AiRun 로그에 provider, taskType, status, errorMessage 저장
```

---

## 5-5. 보안·개인정보 태스크 보강 필요 항목

### 대상 태스크

- SEC-001: AI payload 익명화 파이프라인
- SEC-002: 관리자 인증 미들웨어
- SEC-003: 미승인 리포트 외부 URL 접근 차단
- DPR-001: 고객 동의 체크박스 UI
- DPR-002: 무료 AI API 데이터 처리 약관 검토 체크리스트

### 부족한 점

| 항목 | 문제 |
|---|---|
| 동의 범위 | 개인정보 수집 동의와 AI 처리 동의가 분리되지 않음 |
| 관리자 인증 | 세션 유지 방식, 만료 시간, 실패 횟수 제한 없음 |
| 외부 URL 접근 | approved 여부 외에 추측 가능한 report id 문제 대응 없음 |
| AI 약관 | 검토 체크리스트가 어떤 항목을 포함해야 하는지 없음 |

### 보강 방향

```md
## 보안·개인정보 공통 기준

### 개인정보 수집 동의
- 이름
- 연락처
- 진단 답변
- 상담 안내 목적
- 보관 기간

### AI 처리 동의
- 답변 내용이 AI 분석에 사용될 수 있음
- 이름/연락처는 AI에 전송하지 않음
- AI 결과는 관리자가 검수 후 제공됨

### 관리자 인증
- ADMIN_PASSWORD 환경변수 기반 1차 구현
- 세션 쿠키 httpOnly 적용
- 운영 배포 전 비밀번호 변경 필수
- 잘못된 접근 시 관리자 페이지 내용 노출 금지

### 리포트 접근 제어
- Report.status=approved인 경우만 외부 웹뷰 노출
- draft/rejected/regeneration_requested 상태는 404 또는 준비 중 메시지
- report id는 UUID 또는 추측 어려운 식별자 사용 권장
```

---

## 5-6. 테스트 태스크 보강 필요 항목

### 대상 태스크

- T-001~T-015 전체

### 부족한 점

| 항목 | 문제 |
|---|---|
| 테스트 유형 | unit/integration/e2e 구분이 없음 |
| fixture | 정상/실패 데이터 샘플이 없음 |
| expected result | 어떤 DB 상태나 응답을 검증해야 하는지 부족함 |
| 보안 테스트 | 관리자 인증, PII 제거, 미승인 접근 차단은 더 구체화 필요 |

### 보강 방향

```md
## T-XXX 테스트 명세

### 테스트 유형
- Unit / Integration / E2E 중 선택

### Given
- 사전 데이터 조건

### When
- 실행 행동

### Then
- 예상 결과

### 검증 항목
- 응답값
- DB 저장값
- 상태값
- 로그 기록
- 에러 메시지
```

---

# 6. 우선 보강해야 할 핵심 태스크 상세 명세

## 6-1. API-002 submitDiagnosis DTO 상세 보강

### 목적
리드 정보와 16문항 답변을 받아 Diagnosis와 Answer를 생성하기 위한 입력 계약을 정의한다.

### Request DTO

| 필드 | 타입 | 필수 | 검증 조건 | 설명 |
|---|---|---|---|---|
| leadInfo.name | string | Y | 1자 이상 50자 이하 | 신청자 이름 |
| leadInfo.contact | string | Y | 이메일 또는 전화번호 형식 | 연락처 |
| leadInfo.channel | string | N | 100자 이하 | 유입 채널 |
| answers | array | Y | 정확히 16개 | 진단 답변 목록 |
| answers[].questionCode | string | Y | Q01~Q16 | 질문 코드 |
| answers[].answerText | string | Y | 3단어 이상, 공백만 입력 불가 | 답변 내용 |

### 처리 기준

1. leadInfo 검증
2. answers 배열 개수 검증
3. questionCode 중복 여부 검증
4. answerText 공백 제거 후 3단어 미만 여부 검증
5. transaction으로 Lead, Diagnosis, Answer 16건 저장
6. Diagnosis.status=submitted 또는 report_pending으로 저장

### 예외 처리

| 상황 | 처리 |
|---|---|
| 연락처 없음 | 400 validation error |
| 답변 16개 미만 | 422 validation error |
| questionCode 중복 | 422 validation error |
| 3단어 미만 답변 | 422 validation error |
| DB 저장 실패 | 500 internal error |

### 완료 기준

- 정상 입력 시 Diagnosis 1건, Answer 16건 생성
- 실패 입력 시 DB에 부분 저장 없음
- 테스트 T-002, T-004 통과

---

## 6-2. C-003 submitDiagnosis 저장 로직 상세 보강

### 목적
진단 제출 시 리드, 진단, 답변을 하나의 트랜잭션으로 안전하게 저장한다.

### 처리 절차

1. submitDiagnosis DTO 검증
2. Lead 생성 또는 저장
3. Diagnosis 생성
4. Answer 16건 bulk insert
5. Diagnosis.status를 report_pending으로 설정
6. 저장 성공 응답 반환

### Transaction 범위

아래 작업은 반드시 하나의 transaction으로 처리한다.

- Lead 생성
- Diagnosis 생성
- Answer 16건 생성

### 예외 처리

| 상황 | 처리 |
|---|---|
| Answer 저장 중 일부 실패 | 전체 rollback |
| 중복 questionCode | 저장 전 차단 |
| DB 연결 실패 | 사용자에게 “제출 처리 중 문제가 발생했습니다” 안내 |

### 완료 기준

- Answer 16건이 모두 저장되어야 성공
- 하나라도 실패하면 Lead/Diagnosis/Answer 모두 저장되지 않아야 함
- T-004 통과

---

## 6-3. C-005 AI 리포트 생성 상세 보강

### 목적
제출된 진단 답변을 기반으로 AI 진단 리포트 초안을 생성하고 Report(draft)로 저장한다.

### 입력

- diagnosisId
- answers: questionCode + answerText

### 처리 절차

1. Diagnosis 존재 여부 확인
2. Answer 16건 존재 여부 확인
3. AI payload 익명화
4. AiRun.status=processing 생성
5. Gemini API 호출
6. 응답 JSON 파싱
7. DiagnosisReportSchema로 Zod 검증
8. Report.status=draft 저장
9. AiRun.status=completed 변경
10. Diagnosis.status=report_generated 변경

### 예외 처리

| 상황 | 처리 |
|---|---|
| Diagnosis 없음 | 404 |
| Answer 16건 미만 | 422 |
| Gemini API 실패 | AiRun.status=failed |
| JSON 파싱 실패 | AiRun.status=failed |
| Zod 검증 실패 | AiRun.status=failed |
| timeout | 처리 중 안내 또는 실패 기록 |

### 완료 기준

- 성공 시 Report.status=draft 저장
- 실패 시 Answer 데이터 보존
- 실패 시 AiRun.errorMessage 저장
- T-005, T-006, T-007 통과

---

## 6-4. C-008 관리자 승인/거부 상태 변경 상세 보강

### 목적
관리자가 AI 리포트를 검수한 뒤 승인 또는 거부 상태로 변경한다.

### 입력

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| reportId | string | Y | 대상 리포트 ID |
| status | enum | Y | approved 또는 rejected |
| reviewNote | string | N | 검수 메모 |

### 상태 전이 규칙

| 현재 상태 | 변경 가능 상태 |
|---|---|
| draft | approved, rejected |
| rejected | approved, regeneration_requested |
| approved | rejected 가능하나 이력 기록 필수 |
| regeneration_requested | draft |

### 처리 절차

1. 관리자 인증 확인
2. Report 조회
3. 변경 가능한 상태인지 검증
4. Report.status 변경
5. ReviewLog 생성
6. 성공 응답 반환

### 완료 기준

- Report.status 정상 변경
- ReviewLog에 beforeJson, afterJson, action 저장
- T-010 통과

---

## 6-5. SEC-001 AI payload 익명화 상세 보강

### 목적
AI API에 개인정보가 전송되지 않도록 payload에서 실명, 연락처, 이메일, 전화번호를 제거한다.

### 제거 대상

| 대상 | 예시 | 처리 |
|---|---|---|
| 이메일 | test@example.com | `[EMAIL_REMOVED]` |
| 전화번호 | 010-1234-5678 | `[PHONE_REMOVED]` |
| lead.name | 홍길동 | payload에 포함 금지 |
| lead.contact | 이메일/전화번호 | payload에 포함 금지 |

### 처리 기준

- AI payload에는 questionCode와 answerText만 포함한다.
- leadInfo 전체 객체는 AI payload에 포함하지 않는다.
- answerText 내부에 이메일/전화번호가 포함된 경우 정규식으로 마스킹한다.

### 완료 기준

- T-007 통과
- payload snapshot에 name/contact/email/phone 미포함

---

# 7. 추가 생성이 필요한 태스크

기존 82개 태스크 외에 아래 태스크를 추가하는 것이 좋습니다.

| Task ID | Epic | Feature | 우선순위 | 이유 |
|---|---|---|---|---|
| DB-009 | Infra/DB | 주요 FK 및 status/createdAt 인덱스 추가 | P0 | 관리자 목록·상세 조회 성능 안정화 |
| DB-010 | Infra/DB | seed 데이터 및 개발용 fixture 구성 | P1 | 테스트·UI 개발 속도 향상 |
| DB-011 | Infra/DB | 개인정보 보존·삭제 기준 필드 검토 | P1 | 운영 전 개인정보 리스크 완화 |
| API-009 | Contract | 공통 ApiResponse 타입 정의 | P0 | API 응답 일관성 확보 |
| API-010 | Contract | 공통 ValidationError 타입 정의 | P0 | 프론트 에러 표시 기준 확보 |
| AI-001 | AI | AI 프롬프트 템플릿 파일 분리 | P0 | 유지보수 및 결과 품질 관리 |
| AI-002 | AI | AI 응답 파싱 실패 복구 로직 | P1 | JSON 파싱 실패 대응 |
| SEC-004 | Security | 관리자 세션 만료 및 로그아웃 처리 | P1 | 단순 패스워드 인증의 위험 완화 |
| DPR-003 | DataProtection | 개인정보 처리 안내 문구 작성 | P0 | 실제 사용자 제출 전 필수 |
| DPR-004 | DataProtection | AI 분석 동의 문구 작성 | P0 | AI 처리 투명성 확보 |
| T-016 | Test | submitDiagnosis transaction rollback 테스트 | P0 | 부분 저장 방지 검증 |
| T-017 | Test | AI 응답 Zod 실패 테스트 | P0 | 리포트 품질 안정성 검증 |
| T-018 | Test | 관리자 승인 후 외부 리포트 접근 가능 테스트 | P1 | 공개 조건 검증 |
| T-019 | Test | 관리자 미인증 접근 차단 E2E 테스트 | P1 | 보안 검증 |
| T-020 | Test | 개인정보 마스킹 snapshot 테스트 | P0 | AI payload 안전성 검증 |
| OPS-003 | Ops | 배포 전 환경변수 체크리스트 | P0 | Vercel 배포 실패 방지 |
| OPS-004 | Ops | 수동 장애 복구 Runbook 작성 | P1 | MVP 운영 안정성 확보 |

---

# 8. 보강 후 권장 Milestone 구조

## Milestone 0. 프로젝트 기반 구축

| 포함 태스크 |
|---|
| INF-001 |
| DB-001 |
| INF-002 |
| INF-005 |
| DB-009 |
| API-009 |
| API-010 |

### 완료 기준

- Next.js 프로젝트 실행 가능
- Prisma 연결 가능
- 환경변수 템플릿 완성
- 공통 응답 타입 정의 완료

---

## Milestone 1. 데이터 계약 및 스키마 확정

| 포함 태스크 |
|---|
| DB-002~008 |
| DATA-001~004 |
| API-001~008 |
| DB-010 |

### 완료 기준

- 모든 Prisma model 작성
- enum 정의 완료
- Zod schema 작성
- seed/mock 데이터 생성 가능

---

## Milestone 2. 진단 제출 기능 구현

| 포함 태스크 |
|---|
| Q-001 |
| Q-002 |
| FE-001 |
| DPR-001 |
| DPR-003 |
| DPR-004 |
| C-001~003 |
| FE-002 |
| T-001~004 |
| T-016 |

### 완료 기준

- 사용자가 진단 폼 제출 가능
- Lead/Diagnosis/Answer 정상 저장
- 답변 검증 및 rollback 테스트 통과

---

## Milestone 3. AI 리포트 생성 기능 구현

| 포함 태스크 |
|---|
| INF-003 |
| AI-001 |
| AI-002 |
| SEC-001 |
| C-004~006 |
| LOG-001 |
| T-005~007 |
| T-017 |
| T-020 |

### 완료 기준

- Gemini 호출 가능
- AI payload에 개인정보 미포함
- Report draft 저장 가능
- 실패 로그 저장 가능

---

## Milestone 4. 관리자 검수 콘솔 구현

| 포함 태스크 |
|---|
| FE-007 |
| SEC-002 |
| SEC-004 |
| Q-003~004 |
| Q-006~007 |
| FE-003~004 |
| C-007~010 |
| T-008~010 |
| T-014~015 |
| T-019 |

### 완료 기준

- 관리자 로그인 가능
- 진단 목록/상세 조회 가능
- 리포트 수정·승인·거부·재생성 가능
- ReviewLog 기록 가능

---

## Milestone 5. 승인 리포트 웹뷰 및 CTA 구현

| 포함 태스크 |
|---|
| Q-008 |
| SEC-003 |
| Q-005 |
| FE-005~006 |
| C-011 |
| T-011~013 |
| T-018 |

### 완료 기준

- approved 리포트만 외부 노출
- draft/rejected 접근 차단
- CTA 링크 정상 작동
- CTA 이벤트 기록 가능

---

## Milestone 6. 배포·운영 안정화

| 포함 태스크 |
|---|
| INF-004 |
| PERF-001~003 |
| LOG-002 |
| OPS-001~004 |
| DPR-002 |

### 완료 기준

- Vercel 배포 완료
- 환경변수 체크 완료
- 성능 기준 검증
- 장애 복구 체크리스트 작성

---

# 9. GitHub Issue Template 권장 형식

각 태스크를 실제 Issue로 전환할 때는 아래 템플릿을 사용합니다.

```md
# [Task ID] 제목

## 1. 목적
- 이 태스크가 해결하는 문제를 작성한다.

## 2. 구현 범위
- 포함할 작업
- 제외할 작업

## 3. 입력/출력
### Input
- 

### Output
- 

## 4. 처리 로직
1. 
2. 
3. 

## 5. 예외 처리
| 상황 | 처리 방식 | 사용자 메시지 |
|---|---|---|

## 6. 완료 기준
- [ ] 타입 에러 없음
- [ ] 정상 케이스 동작
- [ ] 실패 케이스 처리
- [ ] 관련 테스트 통과
- [ ] 보안/개인정보 기준 충족

## 7. 관련 태스크
- 선행:
- 후행:

## 8. 테스트
- Unit:
- Integration:
- E2E:
```

---

# 10. AI 개발 도구에 넣을 수 있는 보강 프롬프트

아래 프롬프트를 Cursor, Claude Code, ChatGPT, Gemini 등에 입력해 기존 TASK_LIST를 구현용 명세로 확장할 수 있습니다.

```md
첨부된 TASK_LIST_v1.md를 기반으로 각 태스크를 개발자가 바로 구현 가능한 GitHub Issue 수준으로 확장하라.

[목표]
- 기존 82개 Task의 ID와 구조는 유지한다.
- 각 Task에 목적, 구현 범위, 입력값, 출력값, 처리 로직, 예외 처리, 완료 기준, 테스트 기준을 추가한다.
- API/DB/Command/AI/Security/Test 태스크는 특히 상세히 보강한다.
- MVP-Free 범위를 벗어나는 기능은 Deferred로 분리한다.

[보강 기준]
1. DB Task
- Prisma model 필드 타입, nullable, default, relation, index, onDelete를 명시한다.

2. API/DTO Task
- Request DTO, Response DTO, Zod validation, Error code를 명시한다.

3. Command Task
- 처리 순서, transaction 범위, 상태 전이, 실패 처리, 로그 기록을 명시한다.

4. AI Task
- AI payload에서 개인정보를 제거한다.
- questionCode와 answerText만 전송한다.
- AI 응답은 DiagnosisReportSchema로 검증한다.
- 실패 시 AiRun에 로그를 남기고 Answer 데이터는 보존한다.

5. Security/DataProtection Task
- 관리자 인증, 미승인 리포트 접근 차단, 개인정보 수집 동의, AI 처리 동의를 명시한다.

6. Test Task
- Given/When/Then 형식으로 작성한다.
- Unit/Integration/E2E 테스트 유형을 구분한다.

[출력 형식]
- Markdown
- Task ID별 섹션 구조
- 표와 체크리스트 적극 활용
- 기존 Task ID 변경 금지
- 누락된 필수 태스크가 있으면 “추가 권장 Task”로 별도 제안
```

---

# 11. 최종 적용 순서

| 순서 | 작업 | 설명 |
|---|---|---|
| 1 | API-009, API-010 추가 | 공통 응답·에러 타입부터 확정 |
| 2 | DB-002~007 상세화 | 데이터 구조를 먼저 고정 |
| 3 | API-001~008 상세화 | 프론트/백엔드 계약 확정 |
| 4 | C-001~010 상세화 | 핵심 비즈니스 로직 구현 기준 확정 |
| 5 | SEC/DPR 태스크 상세화 | 개인정보와 접근 제어 기준 확정 |
| 6 | T-001~020 재작성 | 구현 완료 여부를 테스트로 검증 가능하게 변경 |
| 7 | Milestone 기준으로 재정렬 | 실제 개발 순서에 맞게 Issue 배치 |

---

# 12. 최종 판단

기존 TASK_LIST_v1은 MVP 개발을 위한 큰 골격은 충분히 갖추고 있습니다.  
그러나 현재 상태 그대로 AI 개발 도구나 개발자에게 넘기면 다음 문제가 발생할 가능성이 큽니다.

1. API 응답 형식이 제각각 구현될 수 있음
2. DB 관계와 제약조건이 개발자마다 다르게 해석될 수 있음
3. AI 리포트 생성 실패 상황에서 데이터 정합성이 깨질 수 있음
4. 개인정보가 AI payload에 포함될 위험이 있음
5. 테스트가 “무엇을 검증해야 하는지” 모호해질 수 있음
6. 관리자 인증과 외부 리포트 접근 제어가 약하게 구현될 수 있음

따라서 본 보강본을 기준으로 기존 TASK_LIST를 다음 단계로 전환하는 것이 적절합니다.

> **기존 TASK_LIST_v1 = MVP 개발 WBS**  
> **본 보강본 = 구현 가능 Issue 명세로 전환하기 위한 품질 패치 문서**
