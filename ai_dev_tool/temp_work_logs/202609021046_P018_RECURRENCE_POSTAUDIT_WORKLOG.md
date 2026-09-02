# P018 recurrence 설계 사후감사·전체 시각화 가능성 작업로그

- 시작: 2026-09-02 10:46 KST
- 사용자 승인: P018 설계 사후감사 착수
- 범위: P006·P011–P013·P018 recurrence 결과 종합, 저장 데이터 수준 감사, 전체 분량 시각화 가능성·비용·정밀도 검토, 리뷰 문서 작성
- 현재 금지: 새 actual prime sweep, P018-B/P019/P013-C 실행, observed recurrence 사후 unblinding, 새 그래프 본생성, 외부 데이터 다운로드, commit/push/PR

## 영향도 사전판정

| 축 | 판정 | 근거 |
|---|---|---|
| iterated-log·end-bounded 수학 정의 | 영향 없음 | recurrence 사후감사는 F/H 계산을 바꾸지 않음 |
| dataset provenance·coverage | 읽기 전용 영향 | 기존 commit-pinned records와 actual artifact만 사용 |
| 큰 정수·정밀도 | 확인 필요 | 전체 점 대신 exact streaming aggregate 여부를 구분해야 함 |
| 사용자 승인 경계 | 영향 있음 | feasibility 검토만 승인; 새 full sweep·그래프 생성은 별도 gate 필요 |
| 통계 재현성 | 영향 있음 | development/holdout, stationary/stratified, blinded margin을 섞지 않아야 함 |
| 그래프 재현성 | 영향 있음 | 저장 raw 수준·aggregation schema·해상도·누락 여부를 명시해야 함 |
| 정리와 경험적 결론 | 영향 있음 | LOW_INFORMATION과 구조 부재를 동일시하면 안 됨 |
| 문서·handoff | 영향 있음 | 신규 review와 최신 상태 연결 필요 |

## 단계 현황

1. **완료 — 최신 handoff·결과 색인·METHODS·이론 정본 확인**
2. **완료 — P006·P011–P013·P018 run별 artifact·schema·범위 inventory**
3. **완료 — recurrence 질문·모형·결과·한계 종합**
4. **완료 — 전체 분량 시각화 3개 접근의 정확성·비용·위험 비교**
5. **완료 — docs/review 사후감사 보고서 작성**
6. **완료 — 정적검증·문서 정합성 확인**
7. **완료 — 신규 handoff와 사용자 보고 준비**

## 재개 규칙

- 첫 미완료 단계부터 재개한다.
- 저장되지 않은 raw prime/gap stream을 존재한다고 추정하지 않는다.
- P018-A의 blinded margin에서 허용된 정보만 사용하고 p/q/z를 사후 생성하지 않는다.
- 서로 다른 null·범위·cohort를 하나의 p-value나 단일 curve로 임의 pooling하지 않는다.

## 2026-09-02 artifact inventory 중간 결론

- P006 full, P012-B, P013-A, P013-B, P018-A의 보고된 gap-start 처리량을 중복 제거해 합하면
  `72,178,455,399`다. P006 pilot·P011·P012-A·P017·P018-P0는 각각 앞선 범위의 재사용,
  검증 또는 부분집합이므로 다시 더하지 않는다.
- 이 합은 처리량 회계값이지 721억 행 raw file이 아니다. 실제 result directory에는 plateau,
  log-bin, gap-count, exposure 같은 exact 충분통계만 보존됐다.
- P006은 `10^9` 오른쪽 boundary prime을 붙이지 않았고 이후 range stream은 붙였다. 따라서
  `999,999,937 -> 1,000,000,007`의 gap 70 한 건은 이어 붙인 raw stream 관점에서 비어 있다.
  종합 그림은 이 경계 차이를 주석 처리해야 한다.
- P018-A만 해도 x 한 열을 64-bit 정수로 전부 저장하면 약 `257.57 GiB`, x와 gap을 최소
  16 bytes/점으로 잡으면 약 `515.14 GiB`다. 전체 721억 점은 각각 약 `537.77 GiB`와
  `1,075.54 GiB`라 100 GB 제약을 넘고 점 중첩 때문에 직접 산점도 가치도 낮다.
- 기존 artifact를 이용한 plateau·model-row·information-gate 전수 종합 그림은 가능하다.
  임의의 새 x-bin 또는 모든 occurrence 위치 그림은 raw가 없으므로 새 streaming actual이 필요하다.
- P018의 `gap_counts` margin은 `exposure_equal_counts`를 읽지 않지만 conditioned count가 0이면
  recurrence 0을 논리적으로 드러낸다. 따라서 강한 의미의 outcome blinding보다는
  `allocation-blinded / margin-only`가 정확한 명칭인지 사후감사에서 판정한다.

## 완료 산출물

- 정본 리뷰:
  `docs/review/21_20260902_P018_recurrence_설계사후감사_전체시각화_타당성검토.md`
- 최신 handoff: `handoff/202609021101_HANDOFF.md`
- METHODS·이론 문서·색인·P018 계획·AGENTS 동기화 완료
- local reference 12개 존재 확인, missing 0, `git diff --check` whitespace issue 0
- 새 actual·figure·prime sweep·commit은 수행하지 않음
