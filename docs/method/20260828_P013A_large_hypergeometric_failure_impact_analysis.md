# P013-A 대규모 hypergeometric 실패 교정 영향도 분석

## 1. 결론

P013-A r1 실패는 prime sieve·record 범위·P012 통계 정의의 오류가 아니라 NumPy 난수 API의
명시적 크기 제한을 preflight가 검사하지 못한 구현 결함이다. r1은 `[10^10,10^11)`의
`3,663,002,302` gap starts와 오른쪽 boundary prime까지 세는 내부 invariant를 통과했지만, 첫
Monte Carlo inference에서
`ngood` 또는 `nbad`가 `10^9` 이상인 component를 NumPy에 넘겨 중단됐다.

교정 r2는 연구 질문, range, records, bin, cohort, forced-record removal, seed `20260828`,
100,000 replications, stage별 alpha `0.025`를 바꾸지 않는다. 작은 parameter에서는 기존 NumPy
호출과 난수열을 bit-for-bit 유지하고, API 한계를 넘는 component만 같은 유한모집단
hypergeometric 분포의 exact sequential symmetry sampler로 바꾼다. binomial 근사는 사용하지
않는다.

## 2. 원본 증거

- log: `test_result/logs/run_20260827T163052Z_p013a_recurrence_extension_1e11.log`
- log SHA-256: `5CCD6E2997123A99120512AF9D36A4B5AC50CFB4A3E24D6833E5B48EAEEBE79C`
- 실행 시간: 2026-08-28 01:30:52–02:14:53 KST, 약 44분
- 마지막으로 로그에 찍힌 100-chunk progress: `last_prime=99999999977`, `sieve_chunks_completed=1800`,
  `primes_emitted_including_possible_boundary=3663002302`
- 첫 actual FAIL: `ValueError: both ngood and nbad must be less than 1000000000`
- 이 progress 뒤의 boundary-only chunk는 100배수 로그 대상이 아니지만, 코드가 inference까지
  진입했으므로 `gap_count=3,663,002,302`와 `prime_count=3,663,002,303` 내부 검사는 통과
- terminal PASS: 없음
- 표시된 partial result directory: 실제로 생성되지 않음
- 분석표·manifest·figure: 생성되지 않음

따라서 r1에서 과학적으로 해석할 recurrence p-value나 figure는 없다. 유효한 것은 범위 sweep가
끝까지 진행됐다는 실행 진단뿐이며, saved full recomputation도 시작되지 않았다.

## 3. 수학적 교정의 타당성

원래 component의 난수를

\[
X\sim\operatorname{Hypergeom}(N,K,n)
\]

이라고 하자. 이는 크기 `N`인 모집단의 `K`개 marked item 중 크기 `n`인 표본에 들어온 개수다.
반대로 `K`개의 marked item 위치를 모집단에서 비복원 추출하고, 그중 고정된 `n`개 sample
position 안에 든 수를 세어도 같은 `X`를 얻는다. j개 marked position을 이미 노출했고 그중
`Y_j`개가 sample position이었다면 다음 indicator의 조건부 확률은

\[
\Pr(I_{j+1}=1\mid Y_j)=\frac{n-Y_j}{N-j}.
\]

이 조건부 확률로 순차 추출하면 모든 크기 `K`의 위치 부분집합이 균등하므로 결과는 원래
hypergeometric law와 같다. 같은 방식으로 `K`, `N-K`, `n`, `N-n` 중 가장 작은 쪽을 노출하고
필요하면 `n-Y` 또는 `K-Y`로 되돌린다. 이는 계산량을 줄이는 분포 대칭이며 근사가 아니다.

구현 근거:

- NumPy 공식 API는 `ngood`, `nbad`가 각각 `10^9` 미만이어야 한다고 명시한다.
- Kachitvichyanukul–Schmeiser의 hypergeometric variate 연구:
  DOI `10.1080/00949658508810839`.
- r2의 sequential sampler는 signed-int64 population만 허용하고 P013 범위는 `2^53`보다 훨씬
  작아 double 조건부 확률에서 정수 자체의 표현 손실이 없다.
- reviewed sequential draw cap은 component당 `2,000,000`; 초과 시 근사로 몰래 바꾸지 않고
  중단한다.

## 4. 재현성·기존 결과 영향

| 대상 | 영향 | 판정 |
|---|---|---|
| P012-A/B 기존 결과 | 두 category가 모두 `10^9` 미만이면 기존 NumPy backend와 RNG call을 그대로 사용 | 불변 |
| P013 frozen 통계 계약 | range/bin/cohort/seed/replications/alpha 불변 | 불변 |
| P013 output schema | sampler·sufficient-statistics provenance 추가 | v2로 갱신 |
| P013-A r1 | terminal/saved verification 없음 | USER_RUN_FAILED 유지 |
| P013-A r2 | 새 BAT·새 run id로만 실행 | 사용자 실행 대기 |
| P013-B | 같은 large-parameter 교정 적용 | actual 미실행 |

단위검증은 native safe path의 10,000개 draw가 raw NumPy와 bit-for-bit 같은지, 네 가지 symmetry의
support·평균, 작은 exact PMF와 300,000회 표본빈도의 6-sigma 합치, 10억 초과 parameter path와
determinism을 각각 검사한다.

## 5. 계산 손실 방지 checkpoint

r1에서는 충분통계를 memory에만 유지해 예외 시 44분 sweep 결과가 남지 않았다. r2는 full sieve
직후 다음 compact checkpoint를 exclusive-write한다.

```text
tmp/p013-checkpoints/p013a_sufficient_statistics_v2.json
tmp/p013-checkpoints/p013b_sufficient_statistics_v2.json
```

checkpoint에는 input hash, stage/range, exact prime·gap count, selected plateaus와 bin components가
들어간다. contract·plateau identity·N/M/C·scheme별 exposure 합이 모두 맞아야 재사용한다. final
PASS에는 checkpoint만 믿지 않고 기존대로 별도의 두 번째 full range recomputation을 수행해
저장 analysis와 일치해야 한다. 따라서 checkpoint는 실패 복구 시간을 줄일 뿐 독립 saved gate를
약화하지 않는다.

## 6. CPU core 영향

호스트 실측은 AMD Ryzen 7 9700X, 물리 8코어·논리 16프로세서다.

- r1 P013: affinity·thread 환경 변수를 지정하지 않았고 알고리즘도 single Python stream이다.
  따라서 동시에 주로 1개 compute thread를 썼으며 Windows가 16 logical processor 사이에서
  이동시킬 수 있었다. 8개 core 병렬 계산은 아니었다.
- 기존 P014(미실행): exact scan은 single stream이고, HiGHS solver thread 수는 명시적으로
  제한하지 않았다.
- 교정 후 P013/P014: Windows physical-core topology에서 첫 4개 core와 그 SMT sibling 8개를
  합친 affinity mask `0xff`를 process에 적용한다. OMP/OpenBLAS/MKL/NumExpr/BLIS ceiling도 8이다.
  P013 sieve와 P014 exact scan은 여전히 single stream이라 실제 사용률은 보통 1 logical CPU이고,
  P014 HiGHS 같은 내부 병렬 구간만 최대 8 logical CPU를 사용할 수 있다.

즉 “4물리/8논리”는 허용 상한과 배치 범위이며 항상 8개를 100% 쓰겠다는 뜻은 아니다. P013을
실제로 8-way 병렬화하려면 chunk별 boundary/order와 exact totals를 보존하는 별도 설계·회귀검증이
필요하므로 이번 오류 교정에 섞지 않는다.

## 7. 시간 추정과 다음 gate

r1 first sweep 실측 44분을 기준으로 A의 두 full sweeps는 약 88분이다. sampler·artifact·figure를
합쳐 r2 중심 예상은 1.5–2시간, hard timeout은 기존 4시간이다. B는 exact gap-start count가 A의
약 9.14배이므로 두 sweep 중심 12–16시간, hard timeout 20시간을 유지한다. P014는 3–16시간 예상,
child timeout 22시간이다.

권장 gate는 P013-A r2 terminal·saved full recomputation PASS를 먼저 확인한 뒤 P013-B를 여는
것이다. P014는 통계 코드와 독립이므로 P013 실패 여부와 무관하게 수행할 수 있다. unattended
실행에서는 교정된 P015 queue가 이 분기를 자동 처리한다.
