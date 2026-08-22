# P001 — FGKMT 정규화 maximal-gap empirical envelope

> 상태: **⏸ WAITING_FOR_USER_APPROVAL**  
> 이 문서는 실행 전에 고정한 계획이다. 데이터 취득·검증·본 계산·그래프 생성은 아직 수행하지 않았다.

## 1. 목적

검증된 maximal prime-gap records로

\[
G(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n)
\]

를 end-bounded 계단함수로 복원하고,

\[
F(x)=\frac{\log x\,\log_2x\,\log_4x}{\log_3x},\qquad
H(x)=\frac{G(x)}{F(x)}
\]

를 계산한다. 여기서 \(\log_k\)는 자연로그를 \(k\)회 반복한 함수다. 실제 \(H(x)\), record 사이 감소, 새 record에서의 회복, interval minima, global running minimum 및 interval-minimum log-log descriptive trend를 정량화한다.

이 계산은 FGKMT/Sono의 무한 범위 정리를 재증명하거나 유한 범위에서 검증하기 위한 것이 아니다.

## 2. 연구 질문

1. 계산 범위에서 \(H(x)\)의 interval별 변화와 장기 추세는 어떠한가?
2. 새 maximal-gap record 직전과 직후의 \(H\) 및 recovery factor는 어떠한가?
3. interval minimum과 global running minimum은 어떻게 변화하는가?
4. Wolf 계열 경험적 참고선 \(H=1\)과 어느 정도 일치하는가?
5. Sono의 explicit constant \(2\times10^{-17}\)와 실제 값의 배수 차이는 얼마이며, 그 격차는 어떻게 변화하는가?
6. Cramér형 \(G(x)/\log^2x\) 보조 정규화와 비교할 때 특이 구조가 있는가?

## 3. 입력과 출처 고정

- 데이터 정본: `https://github.com/primegap-list-project/prime-gap-list`
- 입력 파일: 같은 commit으로 고정한 allgaps.sql과 schema.sql
- 참고 웹 표: `prime-gaps-high-watermarks` (입력으로 사용하지 않음)
- exhaustive 범위 출처: `fully-analyzed`
- 준비 시 확인한 master: `1a112a1387052d9ad360686313f501c01fe46b68`
- 실행 시점에는 master를 다시 resolve하고 실제 40자 commit, raw URL, 취득 UTC, SHA-256을 기록한다.
- 현재 문서화된 분석 상한: \(10^{20}\) (2026-05-08)

최신 발견 record와 exhaustive 검증범위는 별개다. 실제 \(G(x)\)라는 표현은 명시된 exhaustive 범위 안에서만 사용한다.

## 4. 단계와 gate

| 단계 | 작업 | 성공 기준 | 실패/중단 기준 |
|---|---|---|---|
| P0 | 반복로그 및 코드 정적 preflight | 모든 단위시험 PASS, base-\(k\) 호출 0 | 하나라도 FAIL |
| P1 | master resolve 및 commit-pinned raw 취득 | 40자 commit, non-empty data/schema, 파일별 SHA-256 metadata | 네트워크/해시/원본 충돌 |
| P2 | SQL schema parse 및 record 검증 | `ismax`와 독립 high-watermark 일치, 연속 소수·증가성 PASS | 불일치 또는 미해석 row가 범위 내 record에 영향 |
| P3 | end-bounded \(G/F/H\) 및 envelope 계산 | 마지막 interval이 정확히 분석 상한에서 종료 | exhaustive 범위 초과·interval 공백·비양의 scale |
| P4 | 표·그래프·요약 생성 | provenance, 범위, 정의, code/input hash 포함 | 덮어쓰기 또는 필수 metadata 누락 |
| P5 | 문헌과 비교 후 해석 | theorem/heuristic/finite observation 구분 | 먼저 결론을 정한 해석 또는 과잉 일반화 |

P1 이후는 사용자의 명시적 허가 없이는 시작하지 않는다.

## 5. 계산 계약

- Python: `W:\miniforge3\envs\FGKMT\python.exe`
- 정밀도: `mpmath` 50 decimal digits 이상
- 분석 최소 정수: `X_SCALE_POSITIVE_MIN = 3_814_280`
- canonical boundary: `end_prime <= x`
- interval: `[end_i, end_{i+1}-1]`, 분석 시작점과 상한으로 clip
- exact interval minimum: `gap_i / F(interval_right)`
- global running minimum: interval minimum의 누적 최소; 정의상 단조 비증가
- 큰 정수: Python `int` 및 CSV 10진 문자열; float64 정수 열 금지

## 6. 승인 후 실행 명령

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -B -m unittest discover -s tests -v
.\run_experiment.ps1 -Approved
```

재현성을 더 강하게 고정하려면 승인 시 확인한 commit을 직접 지정한다.

```powershell
.\run_experiment.ps1 -Approved -Commit '<40-character-commit>'
```

## 7. 예상 산출물

```text
datas/raw/prime-gap-list-project/<commit>/allgaps.sql
datas/raw/prime-gap-list-project/<commit>/schema.sql
datas/raw/prime-gap-list-project/<commit>/metadata.json
datas/validated/prime-gap-list-project/<commit>/maximal_gap_records.csv
datas/validated/prime-gap-list-project/<commit>/validation_report.json
test_result/run_<run-id>/tables/end_bounded_intervals.csv
test_result/run_<run-id>/tables/end_bounded_jumps.csv
test_result/run_<run-id>/figures/*.png
test_result/run_<run-id>/figures/*.pdf
test_result/run_<run-id>/summary.json
```

## 8. 해석 한계

- 유한 계산은 무한 범위 정리의 증명이나 반증이 아니다.
- Sono 정리의 “sufficiently large” 수치 임계값을 이 데이터가 제공하지 않는다.
- \(2\times10^{-17}\)은 empirical limit가 아니라 explicit lower-bound constant다.
- \(H=1\)은 Wolf 계열의 empirical reference이며 정리가 아니다.
- 원 데이터의 completeness는 endpoint primality 검사가 아니라 exhaustive-search provenance에 의존한다.
- running minimum 자체는 증가하거나 요동할 수 없다. 장기적인 변화는 interval minima 궤적과 descriptive log-log trend로 보고, 필요하면 log-bin·rolling 지표를 후속 민감도 분석으로 분리한다.

## 9. 실행 이력

- 2026-08-23: 코드·출처 registry·승인 gate 준비. **실제 데이터 미취득, 본 실험 미실행.**
