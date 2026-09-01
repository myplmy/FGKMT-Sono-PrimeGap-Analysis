---
name: research-status-synthesis
description: FGKMT-Sono 연구의 현재 정의, 이론, 가설, actual 결과와 열린 문제를 증거 수준별로 종합해 비전문 사용자용 진행현황 리뷰를 작성한다.
---

# Research status synthesis

현재 상태를 재구성할 때 다음 정본을 이 순서로 읽는다.

1. 최신 `handoff/YYYYMMDDHHmm_HANDOFF.md`
2. `test_result/00_실험결과_분석보고서_색인.md`
3. `docs/METHODS.md`와 `docs/method/theory/00_이론_가설_방법론_색인.md`
4. 현재 active plan과 관련 정본 result report
5. 필요한 문헌 review

## 증거 등급

각 주장을 `DEFINITION`, `THEOREM`, `EXACT_FINITE`, `EMPIRICAL`,
`HYPOTHESIS`, `OPEN`, `REJECTED_AS_STATED` 중 하나로 분류한다. 실행 성공과 과학적 개선,
상한 감소와 위치 coverage, 계산 결과와 무한범위 정리를 합치지 않는다.

과거 handoff·계획의 “다음 우선순위”가 현재와 다르면 오류로 덮어쓰지 말고 historical snapshot으로
표시하고 최신 정본을 제시한다. 미실행 runner는 결과처럼 쓰지 않는다.

## 설명 방식

- 먼저 연구 질문을 일상어 한 문단으로 설명한다.
- 각 축마다 무엇을 물었는지, 무엇을 실행했는지, 무엇을 알았는지, 아직 모르는지를 쓴다.
- 전문 용어에는 지도·계단·상자처럼 구조가 맞는 짧은 비유를 붙인다.
- 관련 파일명과 정확한 section 제목을 함께 적는다.
- negative result와 LOW_INFORMATION을 숨기지 않는다.
- figure는 사용자 visual QA 여부를 분리한다.

## threshold 필수 구분

Sono 부등식의 시작점을 다룰 때 다음을 반드시 분리한다.

- 검증 상한까지의 finite observed persistent threshold
- 증명이 제공하는 numerical threshold
- 실제 전역 최소 threshold

`X_SCALE_POSITIVE_MIN`을 theorem threshold라고 부르지 않는다. Sono가 직접 explicit화한 FMT
chain theorem과 FGKMT scale의 계보도 구분한다.

## 산출물

`docs/review/<date>_...종합리뷰.md`에 상태표, 쉬운 결론, 파일·section 참조, 권장 연구 순서와
승인 경계를 쓴다. 확인하지 않은 전 세계 novelty나 미래 계산 결과를 추정으로 채우지 않는다.
