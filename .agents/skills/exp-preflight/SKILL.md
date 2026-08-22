---
name: exp-preflight
description: FGKMT-Sono 실제 maximal-gap dataset 취득이나 분석을 시작하기 전에 수학 정의, 원천 provenance, 환경, 검증 게이트와 산출물 충돌을 점검한다. 실제 실험 실행 직전에는 반드시 사용한다.
---

# Experiment preflight

이 점검은 알려진 설계 오류를 거르는 절차이며 연구 가설이나 이론을 확인하는 판정이 아니다.

## 필수 입력

- AGENTS.md
- 현재 연구 작업지시서
- docs/METHODS.md
- 해당 test_plan 문서
- datas/source_registry.json

## 게이트

1. 사용자에게 목적·정의·범위·방법을 설명했고 명시적 실행 허가를 받았는가.
2. Python이 정확히 W:\miniforge3\envs\FGKMT\python.exe인가.
3. log_k가 밑 k 로그가 아니라 k회 반복 자연로그이며 독립 테스트를 통과했는가.
4. canonical 경계가 오직 p_(n+1) <= x인가.
5. 원천이 primegap-list-project/prime-gap-list의 pin한 40자리 commit과 allgaps.sql인가.
6. 웹페이지를 dataset으로 스크레이핑하지 않는가.
7. raw hash, 취득 시각, URL, commit, schema를 기록하며 raw를 덮어쓰지 않는가.
8. SQL을 실행하지 않고 허용된 INSERT 문법만 제한 파싱하는가.
9. first occurrence, confirmed prime category, high-watermark 재도출, 순서·gap, 선택적 consecutive-prime 검증이 있는가.
10. 큰 소수는 문자열 또는 임의정밀도 정수로 보존되는가.
11. 분석 상한이 검증된 exhaustive coverage를 넘지 않는가.
12. interval minimum, running minimum, record jump, Sono ratio, Wolf 비교의 정의가 문서와 코드에서 일치하는가.
13. 입력·코드·환경 hash와 버전이 기록되는가.
14. 기존 raw/validated/result 경로를 덮어쓰지 않는가.

하나라도 핵심 게이트가 실패하면 BLOCKED로 보고하고 실제 실행을 시작하지 않는다. 모두 통과하면 READY, 승인 자체가 없으면 WAITING_FOR_USER_APPROVAL로 보고한다.

