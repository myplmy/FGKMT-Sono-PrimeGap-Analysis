# P010 — P010A count upper bound / P010B search acceleration 상위 계획

## 1. 상태

`SPLIT_APPROVED / G3_EXPERIMENT_PASS / G4_STRICT_BOUND_IMPROVEMENT_PASS / G5_BLOCKED`

사용자 제안에 따라 P010을 다음 두 축으로 분리한다.

- [P010A](P010A_P007_count-upper-bound.md): residue-state certificate와 count upper bound
- [P010B](P010B_search-acceleration.md): 누락 없는 candidate cover와 실제 탐색 가속

이 문서는 memory-safe separation oracle의 공통 설계 기록으로 유지한다. 실제 실행 게이트,
입력 hash, 성공·중단 기준은 두 하위 계획서가 정본이다.

P007 작은 modulus 비교는 30, 210, 2310에서 exact PASS했지만 modulus 30030은
5,760 states와 35,224,647 transition constraints 때문에 기존 monolithic sparse LP
구축을 중단했다. P010은 전체 행렬을 만들지 않고 위반 제약만 찾는 separation oracle을
먼저 검증하는 준비 단계다.

## 2. 연구 질문

1. 한 candidate dual solution의 모든 transition을 source-state chunk로 누락 없이
   훑을 수 있는가?
2. chunked 결과가 작은 modulus의 독립 brute-force 결과와 일치하는가?
3. 32 GB보다 충분히 작은 메모리로 most-violated constraints만 보존할 수 있는가?
4. 이 oracle을 cutting-plane LP와 exact streaming verifier로 확장할 가치가 있는가?

## 3. 비목적과 승인 경계

- Codex 로컬검증에서는 modulus 30030 transition 전체 scan을 실행하지 않는다.
- modulus 30030 LP를 풀지 않는다.
- 새 rational certificate 또는 더 낮은 `C_max`를 주장하지 않는다.
- `[10^20,10^21)` prime search를 실행하지 않는다.
- GPU를 사용하지 않는다.

## 4. 설계

unit residue를 `r_i`, `r_j`라 하고

\[
d_0=(r_j-r_i)\bmod M,
\]

zero residue는 `M`으로 대표한다. small constraint가 있으면 `d_0<H`에서 검사하고,
large representative는

\[
d_{large}=d_0+M\max\left(0,\left\lceil\frac{H-d_0}{M}\right\rceil\right)
\]

로 계산한다. floating discovery candidate `(lambda,mu,phi)`의 slack을 source row
`c`개씩 계산하고 음수 slack 상위 `K`개만 남긴다.

이 방식의 working memory는 대략 `O(c phi(M))`이고 전체 constraint matrix를 저장하지
않는다. 64 rows, 5,760 states, top 1,000 설정의 현재 보수적 배열 추정은 약
34.24 MiB다. 이는 solver 전체 메모리 보장이 아니라 oracle 한 chunk의 상한 추정이다.

## 5. exactness 계약

floating slack은 제약 발견에만 사용한다. 최종 certificate가 생기면 다음을 별도 수행한다.

1. coefficient를 고정 denominator 정수로 변환
2. 모든 transition을 다시 streaming
3. Python integer 또는 overflow가 증명된 정수형으로 slack exact 검사
4. minimum integer slack `>=0` 확인
5. certificate·입력·코드 hash 저장

floating oracle PASS만으로 exact certificate라고 부르지 않는다.

## 6. 구현과 로컬 검증

- `source/finite_gap_separation.py`
- `source/finite_gap_separation_cli.py`
- `tests/test_finite_gap_separation.py`
- `scripts/experiments/p007/run_mod30030_separation_toy.ps1`

2026-08-26 targeted test 5개 PASS:

- modulus 30 chunked top violations와 brute-force 일치
- modulus 30 scanned constraint count와 exact edge count 일치
- chunk size가 달라도 deterministic top-K 일치
- modulus 30030 chunk memory estimate가 1 GiB 미만
- 별도 승인 없는 modulus 30030 scan은 resource guard로 거부

fixed FGKMT Python preflight도 PASS했고 실제 modulus 30030 scan·LP solve는 0건이다.

## 7. 후속 gate

### G1 — separation oracle toy (`PASS`)

현재 단계다.

### G2 — modulus 2310 replay (`EXPERIMENT_PASS`)

`20260826T100715Z` run에서 기존 exact solution을 입력해 oracle 위반 0, 두 exact
builder 415,223개, saved issue 0을 확인했다. 상한은 P007과 동일하다.

### G3 — modulus 30030 one-candidate scan·exact lift (`EXPERIMENT_PASS`)

lifted modulus-2310 potential을 고정한 실제 실행은 35,224,647 constraints에서
floating/exact 위반 0이었다. 핵심 scan은 각각 약 0.77초, strict 상한 개선은 0이다.
결과는 `test_result/202608270005_P009_P010_bounded_queue_result_analysis.md`에 기록한다.

### G4 — cutting-plane prototype (`EXPERIMENT_PASS`)

사용자 실행 `20260826T155918Z`은 20,123-row working set에서 4회 solve 뒤 full floating
scan 위반 0으로 수렴했다. 저장 certificate는 35,224,647 exact constraints에서 위반 0,
minimum slack 0이며 total upper bound를 `436001550591586306`으로 약 0.7195% 낮췄다.
core elapsed는 20.919초였다. count 개선은 PASS지만 absolute 위치는 생기지 않았다.

### G5 — algorithm benefit (`BLOCKED`)

더 작은 count upper bound만으로 prime-gap 위치가 정해지지 않는다. P008/P009 같은
local coverage mapping과 baseline 대비 총비용 감소가 별도로 증명돼야 한다.

## 8. 현재 사용자 수행절차

P010A replay·exact lift·G4는 완료됐다. 완료 runner는 `test_done/` provenance이며 재실행하지
않는다. 현재 P010B는 absolute candidate-cover mapping이 생기기 전 사용자 수행절차가 없다.
