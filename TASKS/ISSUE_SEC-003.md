---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] SEC-003: 로봇/크롤러 접근 차단 (robots.txt & meta 태그)"
labels: 'feature, security, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [SEC-003] 검색엔진 및 크롤러 차단
- 목적: 리포트 웹뷰(`/report/[id]`) 등 개인의 브랜드 자산이 담긴 페이지가 구글 등 검색엔진에 무단 노출(인덱싱)되지 않도록 설정한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 타겟 코드: `src/app/robots.ts` 또는 정적 `public/robots.txt`, 웹뷰의 SEO 메타 데이터
- 요구사항: REQ-NF-FREE-033 (미승인/개인 리포트 비공개)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `src/app/robots.ts` (Next.js App Router 방식) 생성:
  ```typescript
  import { MetadataRoute } from 'next'
  
  export default function robots(): MetadataRoute.Robots {
    return {
      rules: {
        userAgent: '*',
        allow: '/',
        disallow: ['/admin/', '/report/'], // 관리자 및 리포트 페이지 크롤링 차단
      },
    }
  }
  ```
- [ ] `src/app/report/[id]/page.tsx` 메타데이터에 `robots: "noindex, nofollow"` 속성 추가:
  ```typescript
  export const metadata: Metadata = {
    title: '나다운 브랜딩 | 브랜드 진단 리포트',
    robots: {
      index: false,
      follow: false,
    },
  }
  ```

## :test_tube: Acceptance Criteria (BDD/GWT)

**Scenario 1: robots.txt 생성 확인**
- Given: Next.js 서버 구동
- When: `/robots.txt`에 접근함
- Then: `Disallow: /report/` 규칙이 표시된다.

**Scenario 2: 리포트 웹뷰 메타 태그 확인**
- Given: 승인 리포트 페이지 접속
- When: 페이지 소스(head)를 확인한다
- Then: `<meta name="robots" content="noindex, nofollow">` 태그가 존재한다.

## :gear: Technical & Non-Functional Constraints
- 고객 프라이버시를 지키는 가장 기본적이고 수동적인 방어선. MVP 단계의 법적/심리적 안정감을 제공한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] robots.txt 라우트 설정 완료
- [ ] 리포트 웹뷰 noindex 메타 태그 추가
- [ ] `npm run build` 에러 0건

## :construction: Dependencies & Blockers
- **Depends on:** Q-005
- **Blocks:** None
