---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-008: AdminUser 테이블 스키마 (환경변수 단순 인증 대체 가능)"
labels: 'feature, backend, database, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-008] AdminUser 테이블 스키마 작성
- 목적: 관리자 인증 정보를 저장하는 AdminUser 모델을 정의한다. MVP-Free 단계에서는 환경변수 기반 단순 패스워드 인증(FE-007)으로 대체 가능하므로, 이 테이블은 **선택 사항**이다. V1.5에서 복수 관리자 지원 시 활성화한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`SRS_v1.md#Appendix A — 필수 엔터티`](file:///e:/%EA%BF%88%EB%AA%B0%EB%8B%A4/%EC%99%B8%EB%B6%80%EC%82%AC%EC%97%85/2026/%EB%AA%A8%EB%91%90%EC%9D%98%EC%97%B0%EA%B5%AC%EC%86%8C/5060%20%EB%B8%8C%EB%9E%9C%EB%93%9C%20%EB%A7%A4%EB%8B%88%EC%A7%80%EB%A8%BC%ED%8A%B8/SRS_v1.md) — Line 504 (AdminUser: 선택)
- 제약사항: C-FREE-010 (단일 관리자 운영), O10 (복잡한 RBAC V2 이동)
- 관련 이슈: OI-009 (단일 관리자 인증 보안 수준 미흡 가능성)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/schema.prisma`에 AdminUser 모델 추가 (주석 처리 또는 선택 활성화):
  ```prisma
  // MVP-Free: 환경변수 ADMIN_PASSWORD로 대체 가능. V1.5에서 활성화.
  model AdminUser {
    id           String   @id @default(cuid())
    email        String   @unique
    passwordHash String   // bcrypt 해시
    name         String?
    isActive     Boolean  @default(true)
    createdAt    DateTime @default(now())
    updatedAt    DateTime @updatedAt
  }
  ```
- [ ] MVP-Free에서는 주석 처리 상태로 유지하거나, 마이그레이션만 실행하되 사용하지 않음을 문서화
- [ ] 환경변수 대체 방식 문서화: `ADMIN_PASSWORD` 환경변수로 인증 (FE-007에서 구현)

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: AdminUser 모델 정의 (선택)**
- Given: AdminUser 모델이 schema.prisma에 정의됨
- When: `npx prisma validate`를 실행함
- Then: 스키마 유효성 검사를 통과한다

**Scenario 2: MVP-Free에서 AdminUser 없이 동작**
- Given: AdminUser 테이블이 비활성화(주석 처리)됨
- When: 관리자 인증을 환경변수 ADMIN_PASSWORD로 수행함
- Then: 관리자 기능이 정상 동작한다

## :gear: Technical & Non-Functional Constraints
- MVP-Free 단계: 환경변수 `ADMIN_PASSWORD` 기반 단순 인증 (FE-007)
- AdminUser는 V1.5에서 복수 관리자/RBAC 도입 시 활성화
- passwordHash: bcrypt 해시 (V1.5에서 구현)
- email: unique 제약 (V1.5에서 로그인 ID로 사용)

## :checkered_flag: Definition of Done (DoD)
- [ ] AdminUser 모델이 schema.prisma에 정의됨 (활성화 또는 주석 처리)
- [ ] MVP-Free 환경변수 대체 방식이 문서화됨
- [ ] `npx prisma validate` 에러 0건
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** DB-001 (Prisma 초기화)
- **Blocks:** None (MVP-Free에서는 환경변수 인증으로 대체)
