---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] SEC-002: 단순 환경변수 기반 관리자 인증 (MVP-Free)"
labels: 'feature, security, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [SEC-002] 단순 환경변수 기반 관리자 인증
- 목적: 복잡한 회원가입이나 RBAC 없이, 환경변수에 지정된 단일 패스워드만으로 관리자 페이지(`/admin/*`) 접근을 제어하여 개발 공수를 최소화하고 빠른 MVP 런칭을 달성한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: `src/middleware.ts` 또는 `src/app/admin/layout.tsx`
- 요구사항: O10 (복잡한 인증/RBAC 제거), C-FREE-010 (단일 관리자)
- 관련 스키마: DB-008 (AdminUser 엔터티는 보류됨)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `.env.local`에 `ADMIN_PASSWORD` 환경변수 추가.
- [ ] Next.js Middleware (`src/middleware.ts`) 작성:
  - `/admin/:path*` 경로에 대한 접근을 인터셉트
  - 쿠키(예: `admin_token`) 확인
  - 쿠키가 없거나 유효하지 않으면 `/admin/login` 페이지로 리다이렉트
- [ ] `src/app/admin/login/page.tsx` 라우트 생성:
  - 비밀번호 입력 폼 구현
  - 제출 시 Server Action을 통해 입력된 비밀번호와 `process.env.ADMIN_PASSWORD` 비교
  - 일치 시 `admin_token` 쿠키를 HttpOnly로 설정 후 `/admin`으로 리다이렉트
- [ ] (선택) `admin_token`을 단순 평문이 아닌 JWT 또는 단방향 해시로 구성하여 보안성 강화. MVP 수준에서는 고정된 비밀키 기반의 서명 토큰 정도로 충분.

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 미인증 관리자 접근 차단**
- Given: 쿠키 없이 브라우저에서 `/admin/diagnoses` 접속
- When: Middleware가 동작함
- Then: `/admin/login` 화면으로 리다이렉트된다.

**Scenario 2: 올바른 비밀번호로 로그인**
- Given: `/admin/login` 페이지
- When: 환경변수와 일치하는 올바른 비밀번호를 입력하고 제출함
- Then: 인증 쿠키가 생성되고 `/admin` 대시보드로 이동한다.

**Scenario 3: 잘못된 비밀번호 입력**
- Given: `/admin/login` 페이지
- When: 틀린 비밀번호를 입력하고 제출함
- Then: 로그인에 실패하며 에러 메시지가 표시된다.

## :gear: Technical & Non-Functional Constraints
- 완전한 보안 시스템이 아닌 MVP 수준의 "빠른 차단벽" 역할.
- Next.js의 Edge 환경(Middleware)에서 동작하므로 Node.js 종속성이 없는 방법(예: Web Crypto API 또는 단순 서명)으로 구현한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] Middleware 인증 로직 적용
- [ ] 로그인 페이지 및 쿠키 설정 액션 구현
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** Q-003, Q-004 (관리자 페이지)
- **Blocks:** None
