---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] OPS-003: 배포 전 환경변수 체크리스트"
labels: 'feature, ops, priority:high'
assignees: ''
---

# [OPS-003] 배포 전 환경변수 체크리스트

## 1. 목적
- Vercel 프로덕션 배포 시 필수 환경변수가 누락되어 애플리케이션이 크래시되는 것을 방지하기 위한 안전 장치

## 2. 구현 범위
- `src/lib/env.ts` 환경변수 검증 스크립트 작성 (선택적)
- 배포 전 수동 체크리스트 문서화

## 3. 처리 로직
1. 필수 환경변수 목록 정의
   - `DATABASE_URL`, `DIRECT_URL` (Supabase)
   - `GEMINI_API_KEY` (AI 생성)
   - `ADMIN_PASSWORD` (관리자 인증)
2. (코드 구현 시) 앱 시작 시점에 `process.env` 검사 및 누락 시 Error throw
3. 문서화

## 4. 완료 기준
- [ ] `.env.example` 최신화
- [ ] Vercel 프로젝트 설정에 환경변수 100% 등록 완료 확인

## 5. 관련 태스크
- 선행: INF-005
- 후행: INF-004
