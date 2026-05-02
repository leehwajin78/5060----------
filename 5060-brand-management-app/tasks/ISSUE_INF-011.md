---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] INF-011: 프로젝트 README 작성 및 Vibe-Coding 프롬프트 템플릿 구성"
labels: 'feature, documentation, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [INF-011] 리드미 및 Vibe-Coding 프롬프트 템플릿 작성
- 목적: 1인 개발자(또는 AI 에이전트)가 프로젝트의 구조, 로컬 실행 방법, 환경변수 설정을 쉽게 파악할 수 있도록 최상단 `README.md`를 정리한다. 또한 AI 에디터(Cursor/Copilot) 환경에서 일관된 코드 품질을 뽑아낼 수 있는 프롬프트 템플릿(가이드)을 프로젝트 루트에 적재한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 파일: `README.md`, `prompt-rules.md` (또는 `.cursorrules`)
- 프로젝트 전반적인 아키텍처 및 요구사항

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `README.md` 작성:
  - 프로젝트 개요 (5060 프리미엄 브랜드 매니지먼트 MVP)
  - 기술 스택 (Next.js, Tailwind, Prisma, Supabase, Gemini)
  - 로컬 환경 설정 및 실행 방법 (`npm install`, `.env` 세팅, `npm run dev`)
  - Vercel 배포 가이드라인 요약
- [ ] `.cursorrules` (또는 `system-prompt.md`) 작성:
  - AI에게 지시할 프로젝트 컨텍스트: "이 프로젝트는 5060 세대를 위한 프리미엄 서비스를 타겟팅하므로, UI는 크고 명확하게 작성하고 심미성을 중시할 것"
  - 코딩 규칙 강제: "Server Component 우선, Zod 검증 필수, 서버리스 Vercel 타임아웃 고려, PII(개인정보) 마스킹 강제"
  - 컴포넌트 명명 규칙 및 폴더 구조 컨벤션 명시

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: README 문서 검토**
- Given: 개발자가 저장소를 클론함
- When: `README.md`를 확인함
- Then: 별도의 구두 설명 없이도 로컬 서버 구동과 DB 스키마 푸시가 가능하다.

**Scenario 2: AI 에이전트 컨텍스트 주입**
- Given: Cursor 에디터에서 프로젝트를 염
- When: 새로운 파일을 생성하거나 코드 수정 프롬프트를 입력함
- Then: `.cursorrules`가 반영되어 5060 타겟의 폰트 크기와 Server Component 지침이 포함된 코드가 생성된다.

## :gear: Technical & Non-Functional Constraints
- Vibe-coding의 생산성은 룰 기반 컨텍스트 주입에 크게 의존하므로, 이 문서는 단순한 가이드가 아니라 **AI의 뇌**를 세팅하는 작업이다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `README.md` 작성 완료
- [ ] `.cursorrules` 작성 완료
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** 전체 프로젝트 아키텍처 확정
- **Blocks:** 다른 개발자나 AI 에이전트의 효율적 온보딩
