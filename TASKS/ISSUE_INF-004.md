---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] INF-004: Supabase 연결 및 Prisma Connection Pooling 최적화"
labels: 'feature, infrastructure, priority:critical'
assignees: ''
---

## :dart: Summary
- 기능명: [INF-004] Supabase 데이터베이스 연결 설정
- 목적: 서버리스 환경(Vercel)에서 DB(Supabase)에 접근할 때 Connection 개수가 초과되어 서버가 다운되는 것을 막기 위해, Prisma Client 인스턴스 싱글톤 유지 및 Supabase PgBouncer/Connection Pooling 설정을 명시한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: `src/lib/prisma.ts`
- 요구사항: REQ-NF-FREE-010, REQ-NF-FREE-021 (Supabase Free Tier 제약)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/lib/prisma.ts` 파일 생성 및 싱글톤 패턴 적용 (Next.js HMR(핫 리로딩) 시 DB Connection 고갈 방지):
  ```typescript
  import { PrismaClient } from '@prisma/client'

  const prismaClientSingleton = () => {
    return new PrismaClient()
  }

  type PrismaClientSingleton = ReturnType<typeof prismaClientSingleton>

  const globalForPrisma = globalThis as unknown as {
    prisma: PrismaClientSingleton | undefined
  }

  export const prisma = globalForPrisma.prisma ?? prismaClientSingleton()

  if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
  ```
- [ ] `.env`의 `DATABASE_URL` 형식이 Supabase의 Connection Pooling URL (보통 포트 6543)인지 확인.
- [ ] `.env`의 `DIRECT_URL` 형식이 Supabase의 직접 접근 URL (보통 포트 5432)인지 확인 (`prisma db push` / 마이그레이션 용도).

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: 개발 모드에서 Connection 보존**
- Given: Next.js 개발 서버(`npm run dev`) 구동 중
- When: 코드를 수정하여 HMR(Hot Module Replacement)이 여러 번 발생함
- Then: DB Connection이 중복 생성되어 터지지 않고 싱글톤 객체가 재사용된다.

**Scenario 2: DB 쿼리 정상 동작**
- Given: `prisma.ts`에서 가져온 인스턴스
- When: 임의의 쿼리(예: `prisma.lead.count()`)를 실행함
- Then: 정상적으로 쿼리가 수행된다.

## :gear: Technical & Non-Functional Constraints
- 서버리스 환경에서는 인스턴스가 계속 생성/소멸될 수 있으므로 Connection Pooling은 필수불가결하다. Prisma와 Supabase 조합의 공식 가이드라인을 엄수한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `prisma.ts` 싱글톤 패턴 작성
- [ ] `.env.example`에 DATABASE_URL / DIRECT_URL 분리 주석 기입
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** 전체 DB 액션 모듈
- **Blocks:** Vercel 프로덕션 라이브
