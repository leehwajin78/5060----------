---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] OPS-004: 수동 장애 복구 Runbook 작성"
labels: 'feature, ops, priority:high'
assignees: ''
---

# [OPS-004] 수동 장애 복구 Runbook 작성

## 1. 목적
- 1인 개발/운영 환경에서 발생할 수 있는 주요 장애 상황(Gemini API 한도 초과, Supabase 연결 지연 등)에 대한 신속한 대응 메뉴얼을 작성한다.

## 2. 구현 범위
- `RUNBOOK.md` 문서 작성

## 3. 처리 로직
다음 시나리오에 대한 조치 방법을 기재한다.
1. Gemini API Rate Limit / Quota Exceeded 에러 발생 시
2. Prisma DB Connection Pool 고갈 시
3. Vercel Serverless Function Timeout 다량 발생 시
4. 특정 진단 건에 대한 관리자의 리포트 수동 재생성 플로우 안내

## 4. 완료 기준
- [ ] `RUNBOOK.md` 문서 작성이 완료됨

## 5. 관련 태스크
- 선행: LOG-001, LOG-002
- 후행: None
