---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-004: 관리자 리포트 승인/거부/재생성 Action 연동 및 UI 처리"
labels: 'feature, frontend, admin, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-004] 관리자 리포트 승인/거부/재생성 Action 연동
- 목적: 관리자 상세 페이지(Q-004)에서 리포트를 승인(고객 공개), 거부, 또는 AI 재생성 요청할 수 있는 액션 버튼들을 구현하고 관련된 Server Action(C-008, C-010)과 연동한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- UI: Q-004 (관리자 상세 페이지)
- Server Actions: C-008 (reviewReportStatus), C-010 (regenerateReport)
- 요구사항: REQ-FREE-FUNC-033 (상태 전이)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 상세 페이지 하단에 액션 버튼 그룹 추가 ("승인하기", "거부하기", "재생성하기")
- [ ] 승인/거부 동작 (`ReviewActionGroup` 컴포넌트):
  - 버튼 클릭 시 확인 모달 표시 (예: "이 리포트를 승인하고 고객에게 공개하시겠습니까?")
  - (선택) Review Note 입력 필드 (Textarea) 모달 내에 제공
  - `reviewReportStatus({ action: "approve" | "reject" })` 호출
  - 로딩 상태 처리 및 성공 시 `router.refresh()`
- [ ] 재생성 동작 (`RegenerateButton` 컴포넌트):
  - 재생성 허용 횟수(1회) 안내 및 확인 모달 표시
  - (선택) 재생성 사유(reason) 입력 폼 제공
  - `regenerateReport()` 호출
  - 로딩 상태 처리 및 결과 토스트 표시
- [ ] 현재 상태(status)에 따른 버튼 비활성화/숨김 처리:
  - 이미 승인된 리포트: 승인 버튼 비활성화
  - 재생성 한도 초과 시: 재생성 버튼 비활성화

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 승인 동작 성공**
- Given: draft 상태의 리포트를 보는 중임
- When: "승인하기" 클릭 -> 확인 모달 "확인" 클릭
- Then: 리포트 상태가 approved로 변경되고 화면이 갱신된다

**Scenario 2: 거부 동작 성공**
- Given: draft 상태의 리포트를 보는 중임
- When: "거부하기" 클릭 (Review Note 입력) -> 확인 모달 "확인" 클릭
- Then: 리포트 상태가 rejected로 변경되고 화면이 갱신된다

**Scenario 3: 재생성 동작 성공**
- Given: 재생성 이력이 없는 진단의 상세 화면
- When: "재생성하기" 클릭 -> 확인 모달 "확인" 클릭
- Then: 약 10~20초 로딩 후 새 리포트가 화면에 갱신된다

**Scenario 4: 로딩 및 중복 클릭 방지**
- Given: 비동기 액션이 진행 중임
- When: 사용자가 버튼을 확인함
- Then: 버튼들이 disabled 상태이고 로딩 스피너가 표시된다

## :gear: Technical & Non-Functional Constraints
- 승인은 데이터의 외부 공개를 의미하므로 반드시 사용자 확인 모달을 거친다.
- AI 재생성(C-010)은 시간이 오래 걸릴 수 있으므로(Gemini API 대기), 충분한 로딩 피드백을 제공한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 액션 버튼 UI 및 확인 모달 구현 완료
- [ ] C-008, C-010 Server Action 연동 완료
- [ ] 상태에 따른 버튼 활성/비활성 제어 확인
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** Q-004 (상세 화면), C-008 (승인/거부), C-010 (재생성)
- **Blocks:** 테스트(관리자 검수 플로우)
