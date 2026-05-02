---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] INF-007: UI 컴포넌트 프레임워크 (Tailwind CSS & shadcn/ui) 설정"
labels: 'feature, infrastructure, ui, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [INF-007] UI 컴포넌트 프레임워크 초기 설정
- 목적: 1인 개발 환경에서 고품질의 UI를 빠르게 구현하기 위해 Tailwind CSS 기반의 `shadcn/ui` 컴포넌트 라이브러리를 초기화하고 필수 컴포넌트들을 설치한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- UI 프레임워크: Next.js + Tailwind CSS 기반
- 요구사항: REQ-NF-FREE-010, REQ-FREE-FUNC-002 (심미성 높은 UI)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Tailwind CSS 최적화 (`tailwind.config.ts` 기본 설정 확인)
- [ ] `shadcn/ui` CLI 초기화 실행 (`npx shadcn-ui@latest init` 상당의 설정 적용):
  - `components.json` 설정 파일 구성
  - `src/lib/utils.ts` (cn 헬퍼 함수) 세팅
- [ ] 기본 필수 컴포넌트 설치 및 구성:
  - Button, Input, Textarea, Label
  - Card (Header, Title, Content, Footer)
  - Dialog (모달용)
  - Toast 또는 Sonner (알림용)
  - Badge (상태 표시용)

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: shadcn/ui 초기화**
- Given: 프로젝트 루트
- When: `src/components/ui/button.tsx` 등 기본 컴포넌트가 생성됨을 확인함
- Then: Tailwind 클래스와 `class-variance-authority`를 통해 버튼 컴포넌트가 올바르게 렌더링된다.

**Scenario 2: cn 유틸리티 작동**
- Given: `src/lib/utils.ts`
- When: `cn('bg-red-500', conditional && 'text-white')` 함수를 호출함
- Then: Tailwind 클래스 충돌 없이 깔끔하게 병합된 문자열이 반환된다.

## :gear: Technical & Non-Functional Constraints
- `shadcn/ui`는 npm 패키지로 설치되는 것이 아니라 코드가 프로젝트 내로 복사되는 형태이므로, 커스터마이징(INF-008 브랜드 테마)에 매우 유리하다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `components.json` 및 `utils.ts` 설정 완료
- [ ] 필수 컴포넌트 코드 (`/components/ui/*`) 적재 완료
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** Next.js 초기화 (INF-001)
- **Blocks:** 모든 프론트엔드 UI 컴포넌트 개발 (FE-001 ~ FE-006)
