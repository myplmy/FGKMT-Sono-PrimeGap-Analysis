# P011 — P006 maximal-gap plateau recurrence null-model 파일럿

## 1. 상태

`EXPERIMENT_PASS / STATIONARY_NULL_INADEQUACY_INDICATED / USER_FIGURE_QA_PENDING`

P006은 record gap이 다음 record 전까지 몇 번 다시 나타났는지 exact하게 셌다. P011은
그 재발 횟수가 단순히 “그 gap 길이 자체가 전체 범위에서 흔하기 때문”으로 설명되는지
보는 경험적 진단이다. 소수 gap의 독립성이나 정상성을 주장하지 않으며 새로운 수론
정리를 검증하는 실험이 아니다.

## 2. 입력과 hash

- P006 full range: `[2,10^9]`
- complete plateaus:
  `test_result/run_20260824T065339Z_p006_full_1000000000/tables/complete_plateaus.csv`
- SHA-256:
  `4675e8b6e7284b31c61ad66f3f98ffa34114553d49ab32878c609608530daca6`
- gap histogram:
  `test_result/run_20260824T065339Z_p006_full_1000000000/tables/gap_histogram.csv`
- SHA-256:
  `ef68d47588b492a5747ff54a58634be5d5c4a339a0599bf5273dd43949ed9ecb`
- total gaps: 50,847,533
- complete/right-censored plateaus: 29/1; censored plateau는 제외

## 3. null 정의

plateau `i`에서 record gap을 `g_i`, 전체 gap-start 수를 `N_i`, 같은 gap의 총 발생을
`M_i`, 첫 record 발생 뒤 재발을 `C_i=M_i-1`이라 한다. 전체 P006 histogram에서
`g_i`의 빈도를 `K_i`, 전체 gap 수를 `T`라 하면 plateau 자체를 뺀 확률을

\[
\hat p_i^{(-i)}=\frac{K_i-M_i}{T-N_i}
\]

로 둔다. 진단 null은

\[
C_i\sim \operatorname{Binomial}(N_i-1,\hat p_i^{(-i)})
\]

이다. plateau 자료를 그 plateau의 null 추정에서 제외해 가장 직접적인 자기포함은
줄이지만, 같은 전체 dataset을 재사용한다는 한계는 남는다.

## 4. 분석

- plateau별 기대값 `(N_i-1)p_i`, variance, standardized residual
- exact binomial one-sided enrichment p-value와 two-sided p-value
- 전체 eligible plateau one-sided p-value의 Benjamini-Hochberg q-value
- 20,000회, seed `20260826` Monte Carlo
- aggregate recurrence total의 upper-tail 진단
- cohort 내 maximum absolute z의 family-level 진단

cohort:

- primary: `start_prime >= 1,000`
- sensitivity 1: gap 1을 뺀 모든 eligible complete plateau
- sensitivity 2: `start_prime >= 100,000`

초기 작은 수의 특수성과 유일한 odd gap 1은 primary 해석에서 분리한다.

## 5. 해석 제한

- maximal record를 본 뒤 선택했으므로 post-selection이다.
- 연속 소수 gap은 iid가 아니며 분포가 `x`에 따라 변한다.
- global gap frequency 하나는 local nonstationarity를 반영하지 못한다.
- p/q 값은 탐색적 진단이며 정리 또는 새로운 법칙의 증거가 아니다.
- 유의성이 나와도 더 큰 독립 범위와 위치 의존 null에서 재검증해야 한다.

## 6. 산출물

- `test_result/logs/run_<UTC>_p011_recurrence_null_pilot.log`
- `analysis.json`
- `plateau_null_statistics.csv`
- `cohort_summary.json`
- 입력 table 사본과 SHA-256 manifest
- 관측/기대 비교 PNG·PDF
- standardized residual PNG·PDF

## 7. 성공·중단 기준

성공:

- 입력 hash와 P006 `N/M/C` invariant PASS
- 고정 seed 재계산이 saved `analysis.json`과 exact 일치
- 3개 cohort 결과와 20,000회 MC 완료
- 모든 artifact hash PASS
- terminal `[PASS] P011 recurrence null-model pilot completed.`

중단:

- 입력 hash 변경
- histogram count보다 plateau occurrence가 큼
- RNG seed/replication 누락
- 결과 폴더 덮어쓰기
- 10분 또는 RAM 4 GB 초과

## 8. 사용자 실행 절차

환경: Windows PowerShell 또는 FGKMT Conda Prompt

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\experiments\p011\run_p011_recurrence_null_pilot.ps1 -ConfirmP011
```

예상시간: 1–3분. 예상 RAM: 1 GB 미만. 예상 disk: 100 MB 미만.

완료 후 다음을 회신한다.

- 마지막 `[PASS]` 또는 첫 `[FAIL]` 줄
- `test_result/logs/run_<UTC>_p011_recurrence_null_pilot.log`
- 결과 폴더 경로
- PNG 두 장의 축·점·글자가 정상인지 시각 확인 결과

## 9. 실제 결과와 다음 판정

- run: `test_result/run_20260826T100938Z_p011_recurrence_null_pilot`
- log: `test_result/logs/run_20260826T100938Z_p011_recurrence_null_pilot.log`
- deterministic saved verification: PASS, issue 0
- primary cohort: 관측 재발 9, stationary-null 기대 109.079
- all eligible: 관측 20, 기대 119.432
- `start>=100000`: 관측 5, 기대 43.734
- all-eligible enrichment BH 최소 q: gap 6의 약 0.105; 0.05 기준 유의하지 않음

따라서 “record gap이 일반적인 빈도보다 유난히 자주 재발한다”는 방향은 지지되지 않았다.
반대로 gap 72 등에서 null이 과도하게 많이 예측했다. 이는 곧바로 수론적 반발 현상을
뜻하지 않고, 전체 `[2,10^9]` 빈도를 모든 위치에 동일하게 쓰는 stationary null이
초기 plateau에 부적합하다는 진단이다. 후속 P012는 local/log-x matched null을 사전
고정한 뒤에만 실행한다.

## 10. 선행연구와 통계 근거

1. Gallagher, P. X., *On the distribution of primes in short intervals*,
   Mathematika 23 (1976), DOI: https://doi.org/10.1112/S0025579300016442
2. Goldston, D. A. and Ledoan, A. H., *On the differences between consecutive
   prime numbers, I*, arXiv:0910.2960, https://arxiv.org/abs/0910.2960
3. Goldston, D. A. and Ledoan, A. H., *On the differences between consecutive
   prime numbers, II*, arXiv:1102.4879, https://arxiv.org/abs/1102.4879
4. Benjamini, Y. and Hochberg, Y., *Controlling the false discovery rate*,
   JRSS B 57 (1995), DOI: https://doi.org/10.1111/j.2517-6161.1995.tb02031.x

이 문헌은 Poisson형 간격 heuristic과 탐색적 다중비교의 배경이다. P011의
leave-plateau-out binomial을 소수 gap 정리로 만들어 주지는 않는다.
