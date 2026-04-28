---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-002: 진단 폼 제출 로직 (Server Action 연동) 및 완료 화면 처리"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-002] 진단 폼 제출 로직 (Server Action 연동)
- 목적: 클라이언트 검증을 통과한 데이터를 `submitDiagnosis`(C-003) Server Action으로 전송하고, 성공/실패/로딩 상태를 처리하여 사용자에게 적절한 피드백과 완료 모달(또는 페이지 이동)을 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- UI: Q-002 (진단 폼)
- 클라이언트 검증: FE-001
- Server Action: C-003 (submitDiagnosis)
- SRS 요구사항: REQ-FREE-FUNC-005 (제출 완료 화면 제공)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `useTransition` 훅을 사용하여 제출 중 로딩 상태(pending) 관리
- [ ] 폼의 `onSubmit` 핸들러에서 `submitDiagnosis` Server Action 호출:
  ```typescript
  import { useTransition } from "react"
  import { submitDiagnosis } from "@/lib/actions/diagnosis.actions"

  // ...
  const [isPending, startTransition] = useTransition()

  const onSubmit = (data: SubmitDiagnosisInput) => {
    startTransition(async () => {
      const result = await submitDiagnosis(data)
      if (result.success) {
        // 성공 처리 (완료 모달 표시 또는 페이지 이동)
        showSuccessModal(result.message)
      } else {
        // 에러 처리 (Zod 에러면 필드 맵핑, 서버 에러면 토스트 알림)
        handleActionError(result)
      }
    })
  }
  ```
- [ ] 제출 중일 때 "제출하기" 버튼을 비활성화하고 스피너 표시
- [ ] 제출 완료 시 성공 모달(Dialog 컴포넌트) 또는 별도의 `/diagnose/complete` 페이지 표시
  - 모달 내용: "제출 완료! AI 분석 및 검수 후 기재해주신 연락처로 리포트 링크를 보내드립니다." (result.message 활용)
- [ ] 에러 발생 시 Toast 알림(`sonner` 또는 `useToast` 활용) 표시

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 성공적인 폼 제출**
- Given: 모든 필드가 유효하게 채워진 상태
- When: "제출하기" 버튼을 클릭함
- Then: 로딩 스피너가 표시되고 잠시 후 제출 성공 안내 모달(또는 페이지)이 나타난다

**Scenario 2: 서버 검증 실패 시 에러 표시**
- Given: 클라이언트를 우회하여 유효하지 않은 데이터가 전송됨
- When: Server Action이 fieldErrors를 반환함
- Then: 해당 필드 하단에 서버에서 반환된 에러 메시지가 표시된다

**Scenario 3: 서버 내부 오류 시 토스트 알림**
- Given: DB 연결 오류 등 서버 측 에러 발생
- When: 폼을 제출함
- Then: "진단 제출에 실패했습니다" 토스트 알림이 표시되고 입력 데이터는 유지된다

**Scenario 4: 제출 중 중복 클릭 방지**
- Given: 폼 제출이 진행 중임
- When: "제출하기" 버튼을 다시 클릭 시도함
- Then: 버튼이 비활성화(disabled) 상태여서 클릭되지 않는다

## :gear: Technical & Non-Functional Constraints
- `useTransition`을 활용한 비차단(non-blocking) UI 업데이트
- AI 처리(C-005)가 비동기로 진행되므로, 제출 완료 응답은 즉각적으로 반환됨 (Timeout 걱정 없음)
- 에러 응답 형식(API-008 ActionError)에 맞춰 필드 에러와 일반 에러를 구분하여 처리

## :checkered_flag: Definition of Done (DoD)
- [ ] Server Action 호출 연동 완료
- [ ] 로딩 상태(isPending) UI 처리 완료
- [ ] 성공 모달/페이지 전환 동작 확인
- [ ] 서버 에러/Toast 알림 연동 완료
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** FE-001 (클라이언트 검증), C-003 (Server Action)
- **Blocks:** 테스트(E2E 진단 제출 플로우)
