---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-003: 관리자 AI 리포트 수정 편집기 UI 및 연동"
labels: 'feature, frontend, admin, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-003] 관리자 AI 리포트 수정 편집기 UI 및 연동
- 목적: 관리자가 상세 페이지(Q-004)에서 AI 리포트 JSON 데이터를 직접 수정할 수 있는 편집기를 제공하고, `modifyReport`(C-007) Server Action과 연동한다. Form 또는 JSON Editor 형태로 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- UI: Q-004 (관리자 상세 페이지)
- Server Action: C-007 (modifyReport)
- DTO: API-004 (DiagnosisReportSchema), API-005 (ReviewReportInput)
- 요구사항: REQ-FREE-FUNC-032 (관리자 리포트 수정 기능)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 상세 페이지(Q-004) 내 "리포트 수정" 모드 진입 버튼 추가
- [ ] 폼 기반 편집기 컴포넌트(`ReportEditor`) 구현:
  - `reportJson` 데이터를 React Hook Form의 `defaultValues`로 매핑
  - Summary 입력용 Textarea
  - Strengths/Weaknesses 배열 조작(추가/삭제/수정)용 `useFieldArray` 활용
  - BrandDirection (oneSentence, description) 입력용 Input/Textarea
  - CTA 및 Warnings 입력 필드
- [ ] 편집 완료 시 `modifyReport` Server Action 호출 (`action: "modify"`)
- [ ] 저장 중(isPending) UI 처리 및 에러/성공 토스트 알림 표시
- [ ] 수정 사유(reviewNote) 입력 필드 (선택 입력) 제공
- [ ] 저장 완료 시 읽기 모드로 전환하고 업데이트된 데이터 반영 (router.refresh() 활용)

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 편집 모드 진입**
- Given: 관리자 상세 페이지의 리포트 섹션
- When: "수정하기" 버튼을 클릭함
- Then: 리포트 내용이 폼(Input, Textarea) 형태로 변환된다

**Scenario 2: 배열 필드 조작 (강점 추가)**
- Given: 편집 모드 상태
- When: 강점(Strengths) 섹션의 "항목 추가" 버튼을 클릭함
- Then: 빈 강점 입력 필드 그룹이 추가된다

**Scenario 3: 정상 수정 및 저장**
- Given: Summary 내용을 일부 수정한 상태
- When: "저장" 버튼을 클릭함
- Then: Server Action이 호출되고, 성공 시 토스트 알림과 함께 읽기 모드로 복귀한다

**Scenario 4: Zod 스키마 위반 에러 처리**
- Given: Summary 필드를 지워버림 (30자 미만)
- When: "저장" 버튼을 클릭함
- Then: 클라이언트/서버 검증에 실패하여 저장되지 않고 에러 메시지가 표시된다

## :gear: Technical & Non-Functional Constraints
- 완전한 JSON Text Editor(monaco 등)를 쓸지, 구조화된 Form UI를 쓸지 결정 (MVP-Free의 1인 개발 제약상 **구조화된 Form(react-hook-form)**이 안전하고 구현이 빠름)
- Client Component(`"use client"`)로 구현하여 상태 관리
- 수정 완료 후 화면 데이터 최신화를 위해 `router.refresh()` 활용

## :checkered_flag: Definition of Done (DoD)
- [ ] 폼 기반 리포트 편집기 UI 구현 완료
- [ ] React Hook Form + useFieldArray 연동
- [ ] `modifyReport` Server Action 성공/실패 처리 확인
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** Q-004 (상세 화면), C-007 (수정 로직), API-004 (리포트 타입)
- **Blocks:** 테스트(관리자 검수 플로우)
