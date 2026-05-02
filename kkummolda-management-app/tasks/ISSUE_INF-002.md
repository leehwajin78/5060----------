---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] INF-002: Vercel 자동 배포 파이프라인 및 환경변수 템플릿 구성"
labels: 'feature, infrastructure, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [INF-002] Vercel 배포 환경 구성
- 목적: Github 저장소와 Vercel을 연동하여 CI/CD 파이프라인을 구축하고, MVP 동작에 필수적인 `.env.example` 템플릿을 정의하여 환경변수 누락에 의한 배포 실패를 방지한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 인프라 요구사항: REQ-NF-FREE-010 (Vercel 배포)
- 관련 태스크: INF-003, INF-004, SEC-002, FE-006

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Vercel 프로젝트 생성 및 GitHub Repository 연동
- [ ] 루트 디렉토리에 `.env.example` 파일 생성 및 필수 환경변수 목록화:
  ```env
  # Database (Supabase)
  DATABASE_URL="postgresql://..."
  DIRECT_URL="postgresql://..."

  # AI Service (Gemini)
  GEMINI_API_KEY="AIzaSy..."

  # Security / Admin
  ADMIN_PASSWORD="your-strong-password"

  # CTA Settings
  NEXT_PUBLIC_CTA_LINK="https://forms.gle/..."
  NEXT_PUBLIC_CTA_LABEL="상담 신청하기"
  ```
- [ ] Vercel 대시보드 (Settings > Environment Variables)에 해당 변수들 등록
- [ ] `next.config.mjs`에 기본 빌드 설정 최적화 확인 (기본값 유지하되, 필요 시 strict mode 유지)
- [ ] (선택) `package.json`의 빌드 스크립트에 prisma db push/generate 연동 확인 (`"build": "prisma generate && next build"`)

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 환경변수 템플릿 검증**
- Given: 프로젝트 클론 직후
- When: `.env.example` 파일을 확인함
- Then: DB, Gemini, Admin 인증, CTA 설정에 대한 모든 키가 주석과 함께 명시되어 있다.

**Scenario 2: Vercel 자동 배포 연동**
- Given: `main` 브랜치에 코드가 푸시됨
- When: Vercel CI가 트리거됨
- Then: Prisma generate 및 Next 빌드가 성공하고 프로덕션 URL에 접근 가능하다.

## :gear: Technical & Non-Functional Constraints
- 프리티어를 최대한 활용하는 구조이므로, 빌드 타임을 줄이고 DB Connection 수(Supabase pool)를 방어하는 환경 설정이 중요하다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `.env.example` 작성 완료
- [ ] `package.json` 빌드 스크립트 Prisma 통합 확인
- [ ] Vercel 배포 성공 확인

## :construction: Dependencies & Blockers
- **Depends on:** 전체 소스 코드 (빌드 통과용)
- **Blocks:** 실제 프로덕션 라이브
