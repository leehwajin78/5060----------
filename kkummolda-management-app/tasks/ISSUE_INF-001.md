---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] INF-001: Next.js App Router 프로젝트 부트스트랩 + Tailwind CSS + shadcn/ui"
labels: 'feature, infra, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [INF-001] Next.js App Router 프로젝트 부트스트랩
- 목적: MVP-Free 전체 시스템의 기반이 되는 Next.js App Router 프로젝트를 생성하고, Tailwind CSS 및 shadcn/ui를 통합하여 이후 모든 태스크가 의존하는 프로젝트 골격을 확보한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#Appendix C Step 1~2`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md)
- 제약사항: SRS §1.2 Constraints — C-FREE-001 (1인 바이브코딩), C-FREE-004 (Vercel Hobby)
- 기술 참조: REF-08 (Next.js App Router), REF-14 (Tailwind CSS), REF-15 (shadcn/ui)
- 컴포넌트 다이어그램: SRS §3.2 Component Diagram

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `npx create-next-app@latest ./ --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"` 실행
- [ ] 프로젝트 구조 확인: `src/app/`, `src/lib/`, `src/components/` 디렉토리 존재 여부
- [ ] `npx shadcn@latest init` 실행 및 기본 설정 (New York style, Zinc palette 등)
- [ ] shadcn/ui 기본 컴포넌트 설치: `Button`, `Card`, `Input`, `Textarea`, `Label`, `Badge`, `Separator`
- [ ] `npm run dev` 로컬 실행 성공 확인 (http://localhost:3000)
- [ ] `npm run build` 빌드 성공 확인 (에러 0건)
- [ ] `.env.local.example` 파일 생성 — 향후 필요한 환경변수 키 목록 주석으로 기록
- [ ] `.gitignore` 점검 — `.env.local`, `node_modules/`, `.next/` 포함 확인

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 프로젝트 로컬 실행 성공**
- Given: Next.js App Router 프로젝트가 생성됨
- When: `npm run dev`를 실행함
- Then: http://localhost:3000 에서 기본 페이지가 정상 렌더링된다 (HTTP 200)

**Scenario 2: Tailwind CSS 적용 확인**
- Given: Tailwind CSS가 설정됨
- When: 임의의 컴포넌트에 `className="bg-blue-500 text-white p-4"`를 적용함
- Then: 브라우저에서 파란 배경, 흰 텍스트, 패딩이 정상 적용된다

**Scenario 3: shadcn/ui 컴포넌트 사용 가능**
- Given: shadcn/ui가 초기화되고 Button 컴포넌트가 설치됨
- When: `import { Button } from "@/components/ui/button"` 후 렌더링함
- Then: 스타일이 적용된 Button이 정상 표시된다

**Scenario 4: 프로덕션 빌드 성공**
- Given: 프로젝트 코드에 타입 에러나 린트 에러가 없음
- When: `npm run build`를 실행함
- Then: 빌드가 에러 없이 완료된다

## :gear: Technical & Non-Functional Constraints
- Node.js ≥ 18, TypeScript strict mode
- Vercel Hobby 배포 호환성 (Next.js App Router 기본 설정 유지)
- 월 인프라 비용 0원 (C-FREE-003) — 유료 플러그인/라이브러리 사용 금지
- ESLint 경고 0건 유지

## :checkered_flag: Definition of Done (DoD)
- [ ] `npm run dev` 로컬 실행 성공 (HTTP 200)
- [ ] `npm run build` 에러 0건
- [ ] shadcn/ui Button, Card, Input, Textarea 컴포넌트 import 가능
- [ ] Tailwind CSS 유틸리티 클래스 정상 적용
- [ ] `.env.local.example` 파일에 향후 환경변수 키 목록 기재
- [ ] ESLint / TypeScript 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** None (최초 태스크)
- **Blocks:** DB-001, DB-002~008, API-001~008, DATA-001~004, INF-002, INF-003, INF-005, 모든 FE/BE 태스크
