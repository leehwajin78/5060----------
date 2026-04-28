---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-001: Prisma 프로젝트 초기화 및 datasource 설정"
labels: 'feature, backend, database, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-001] Prisma 프로젝트 초기화 및 datasource 설정
- 목적: MVP-Free의 단일 진실 공급원(SSOT)인 Prisma ORM을 초기화하고, 로컬 개발(SQLite)과 운영(Supabase PostgreSQL)을 환경변수로 분기하는 datasource를 설정하여, 이후 모든 DB 모델 정의의 기반을 마련한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#Appendix A — Prisma Schema 초안`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md)
- 제약사항: SRS §1.2 — C-FREE-005 (Supabase Free PostgreSQL)
- ERD: SRS Appendix E
- 기술 참조: REF-13 (Prisma Documentation)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `npm install prisma @prisma/client` 의존성 설치
- [ ] `npx prisma init` 실행 — `prisma/schema.prisma` 파일 생성
- [ ] `schema.prisma`에 generator 설정: `provider = "prisma-client-js"`
- [ ] `schema.prisma`에 datasource 설정: `provider = env("DATABASE_PROVIDER")`, `url = env("DATABASE_URL")`
- [ ] `.env.local`에 로컬 개발용 환경변수 추가:
  - `DATABASE_PROVIDER="sqlite"`
  - `DATABASE_URL="file:./dev.db"`
- [ ] `.env.local.example` 업데이트 — DATABASE_PROVIDER, DATABASE_URL 키 추가
- [ ] `src/lib/prisma.ts` Prisma Client 싱글턴 인스턴스 생성 (Next.js HMR 대응 global 캐싱 패턴 적용)
- [ ] Prisma Client import 정상 동작 확인 (`import { prisma } from '@/lib/prisma'`)

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: Prisma 초기화 성공**
- Given: `prisma init`이 실행됨
- When: `prisma/schema.prisma` 파일을 확인함
- Then: generator와 datasource 블록이 올바르게 정의되어 있다

**Scenario 2: 로컬 SQLite datasource 동작**
- Given: `.env.local`에 `DATABASE_PROVIDER="sqlite"`, `DATABASE_URL="file:./dev.db"`가 설정됨
- When: `npx prisma validate`를 실행함
- Then: 스키마 유효성 검사를 통과한다 (에러 0건)

**Scenario 3: Prisma Client 싱글턴 동작**
- Given: `src/lib/prisma.ts`에 싱글턴 패턴이 구현됨
- When: Next.js 개발 서버에서 HMR이 발생함
- Then: Prisma Client 인스턴스가 중복 생성되지 않고 global 캐시에서 재사용된다

**Scenario 4: 운영 환경 PostgreSQL 분기**
- Given: `.env.local`의 `DATABASE_PROVIDER`를 `"postgresql"`로, `DATABASE_URL`을 Supabase 연결 문자열로 변경함
- When: `npx prisma validate`를 실행함
- Then: PostgreSQL datasource로 유효성 검사를 통과한다

## :gear: Technical & Non-Functional Constraints
- Prisma ≥ 5.x, @prisma/client 동일 버전 매칭
- `env("DATABASE_PROVIDER")` 분기로 SQLite(로컬) ↔ PostgreSQL(운영) 동일 스키마 사용 (SRS Appendix A)
- Next.js App Router 환경의 HMR에서 Prisma Client 커넥션 누수 방지 (globalThis 패턴)
- 이 시점에서는 모델을 정의하지 않음 (모델 정의는 DB-002~DB-008에서 수행)

## :checkered_flag: Definition of Done (DoD)
- [ ] `prisma/schema.prisma` 파일에 generator + datasource 블록이 존재
- [ ] `npx prisma validate` 에러 0건 (SQLite 모드)
- [ ] `src/lib/prisma.ts` 싱글턴 파일 생성 완료
- [ ] `.env.local.example`에 DATABASE_PROVIDER, DATABASE_URL 키 문서화
- [ ] `npm run build` 에러 0건 유지

## :construction: Dependencies & Blockers
- **Depends on:** INF-001 (Next.js 프로젝트 생성 완료)
- **Blocks:** DB-002, DB-003, DB-004, DB-005, DB-006, DB-007, DB-008, API-001~008, 모든 Command/Query 태스크
