# P008 — local residue-state certificate 탐색 가속 연결 타당성 실험

## 1. 상태

`IMPLEMENTED / LOCALLY_VERIFIED / ACTUAL_RUN_NOT_AUTHORIZED`

P008 검토용 문서의 핵심 방향은 채택하되, unresolved right-boundary가 있는 block을 zero로 인증할 수 없다는 보정을 최우선 게이트로 둔다. 현재 구현은 feasibility phase A까지만 준비하며 candidate cover나 실제 prime-gap speedup을 주장하지 않는다.

## 2. 연구 질문

1. P007 modulus-2310 인증서를 임의 `[A,B)` block에 exact하게 적용할 수 있는가?
2. worst-case endpoint potential `2t`에서 internal large-gap count upper bound가 0까지 내려가는 길이가 있는가?
3. 내부 상한이 0일 때 unresolved right-boundary `+1`을 해결하는 비용은 어느 정도인가?
4. exact `pi(B-1)-pi(A-1)` 입력 생성비가 baseline search보다 이미 비싼가?
5. 이 결과가 나중의 candidate cover·coverage ledger 연구로 진행할 근거가 되는가?

## 3. 비목적

- `[10^20,10^21)`의 large gap 부재를 증명하지 않는다.
- 대표 block을 전체 범위 coverage라고 부르지 않는다.
- residue state만으로 candidate 위치가 생성된다고 주장하지 않는다.
- `prime-gap`의 `m·P#/d` 작업단위와 임의 x-block 사이의 mapping을 가정하지 않는다.
- modulus 30030/510510 LP를 실행하지 않는다.
- GPU를 사용하지 않는다.
- 사용자의 새 승인 없이 pilot, primecount input 생성, full을 실행하지 않는다.

## 4. 수학 계약

대상은 start-bounded count다.

\[
N_{\ge H}(A,B)=\#\{p:\ A\le p<B,\ p^+-p\ge H\}.
\]

임의 endpoint에서 block 안 start-prime 수는

\[
K=\pi(B-1)-\pi(A-1)
\]

이고 내부 gap 수는 `max(K-1,0)`이다. 내부 path의 dual 합으로 `N_internal≤q`를 얻으면 tight integer bound는 `floor(q)`다.

endpoint primes를 모를 때:

\[
q_{worst}=\frac{\lambda_{num}(B-A)+\mu_{num}(K-1)+2t_{num}}{D}.
\]

endpoint primes를 exact하게 알 때는 `(B-A)` 대신 `last-first`, `2t` 대신 `phi(first)-phi(last)`를 쓴다. nonempty block의 right crossing을 모르면 total에 1을 더한다. 따라서

```text
right_boundary_status=UNRESOLVED => certified_zero=false
```

를 불변식으로 둔다.

## 5. 입력과 환경

- certificate: `ai_dev_tool/temp_prime_gap_count_algorithm/source/C2310_certificate.txt`
- SHA-256: `44c6a9e51b5f99ef2f49f89c89cfc40604e83ce8fe20e802f21733109b1e92fb`
- modulus: 2310
- threshold: 1856
- bound Python: `W:\miniforge3\envs\FGKMT\python.exe`
- exact prime counts: WSL Ubuntu `primecount 7.10`, Gourdon과 Deleglise–Rivat 결과 일치
- CPU: Ryzen 7 9700X, 최대 8 threads
- hard virtual-memory cap: 30 GiB
- GPU: disabled

## 6. 구현

- `source/local_residue_certificate.py`: local exact bound, toy inputs, future ledger geometry
- `source/local_residue_verification.py`: 별도 direct Fraction 재계산, artifact hash, prime-count metadata/CSV hash 검사
- `source/local_residue_certificate_cli.py`: preflight/run/verify 승인 게이트
- `tests/test_local_residue_certificate.py`: boundary, floor, zero, ledger, non-overwrite tests
- `run_local_residue_certificate.ps1`: 공통 Windows FGKMT runner
- `run_P008_local_residue_certificate_pilot.bat`: toy pilot
- `prepare_P008_local_primecounts.sh`: WSL exact prime-count input 준비
- `run_P008_local_residue_certificate_full.bat`: READY 입력을 읽는 phase-A full

## 7. 단계와 게이트

### G0 — 비판적 검토 (`PASS`)

- global/local/coverage 구분은 채택
- right-boundary unresolved zero 주장은 보정
- arbitrary endpoint prime-count 식 보정
- integer `floor` 보정
- endpoint integer residue와 endpoint prime state를 구분
- full grid를 5 unique endpoint의 staged check로 축소

근거: `docs/review/16_P008_local-residue-state-certificate_타당성검토.md`

### G1 — 로컬 정적·toy 검증 (`PASS — 20260824T0440 KST`)

1. `py_compile`
2. P008 targeted unittest
3. 전체 unittest
4. PowerShell parser
5. BAT approval-denial
6. WSL `bash -n`
7. primecount toy `pi(100)=25`를 Gourdon/Deleglise–Rivat로 대조

하나라도 실패하면 사용자 실행을 요청하지 않는다.

검증 결과: targeted 7/7, 전체 68/68 tests, py_compile, PowerShell parser, BAT approval-denial, WSL `bash -n`, failure-manifest toy, 합성 gaps DB import, primecount Gourdon/Deleglise–Rivat `pi(100)=25` 대조가 모두 PASS했다. full 입력 메타데이터의 CSV hash·thread·memory·GPU/search 계약과 고정 4-block grid도 사전 및 독립 재검증에 추가했다. canonical raw SQL의 실제 DB 변환은 승인 심사에서 차단되어 수행하지 않았다. 상세: `test_result/202608240440_P005_P008_local_validation.md`.

### G2 — P008 toy pilot (`WAITING_FOR_USER_APPROVAL`)

```bat
run_P008_local_residue_certificate_pilot.bat --confirm-p008
```

- 환경: Windows CMD, 시작 경로 `Z:\FGKMT-Sono-PrimeGap-Analysis`
- 예상시간: 약 1–3분
- 실제 `10^20` prime count/search: 없음
- 성공: 전체 tests, toy exact sieve, right-boundary resolved/unresolved 비교, saved verification 모두 PASS

### G3 — exact local prime-count input (`WAITING_FOR_G2_AND_USER_APPROVAL`)

```bash
cd /mnt/z/FGKMT-Sono-PrimeGap-Analysis
bash ./prepare_P008_local_primecounts.sh --confirm-p008
```

- 환경: WSL Ubuntu
- grid: `x=10^20`, `L=10^3,10^6,10^9,10^12`
- unique endpoint: 5개
- 각 endpoint: Gourdon과 Deleglise–Rivat exact integer result 일치 필요
- 예상시간: 약 20–90분; 설치된 7.10과 8-core 실측 전 넓은 추정
- 산출물: `tmp/p008-primecounts/<UTC>/`, prep log, `READY.txt`
- 실제 prime-gap 탐색: 없음

### G4 — phase-A full local bound (`WAITING_FOR_G3_AND_USER_APPROVAL`)

```bat
run_P008_local_residue_certificate_full.bat --confirm-p008
```

- 환경: Windows CMD, 시작 경로 `Z:\FGKMT-Sono-PrimeGap-Analysis`
- 예상시간: 약 1–3분
- READY의 exact counts를 Windows FGKMT Python이 재검사·적용
- 모든 block의 internal floor, historic ceil, right-boundary status, total bound 저장
- representative blocks는 coverage ledger가 아님을 manifest에 고정

### G5 — endpoint/crossing resolver (`BLOCKED_BY_MISSING_PROOF_AND_BENCHMARK`)

G4에서 internal upper bound 0인 block이 있어야만 설계한다. 필요 조건:

1. last start prime과 next consecutive prime의 exact 결정
2. endpoint primality 및 crossing gap `<1856` 증거
3. certificate+boundary 비용이 baseline보다 작은 실측
4. block 경계 gap의 중복·누락 없는 담당 규칙

### G6 — candidate cover와 exhaustive integration (`BLOCKED`)

다음이 증명·toy 검증되기 전에는 구현하지 않는다.

1. 모든 실제 large-gap start가 candidate set에 포함된다는 theorem
2. arbitrary x-block과 `m·P#/d` 작업단위의 sound mapping
3. 전체 `[A,B)` partition ledger
4. zero/candidate/exact 상태별 artifact hash
5. survivor endpoint primality와 interior compositeness certificate

## 8. 산출물 계약

각 P008 run은 다음을 non-overwrite로 만든다.

- `test_result/logs/run_<UTC>_p008_<mode>.log`
- `test_result/run_<UTC>_p008_<mode>/input_certificate.txt`
- `input_prime_counts.csv`
- full이면 `input_count_metadata.txt`
- `local_block_bounds.csv`
- `summary.json`
- `verification_report.json`
- `manifest.json`

각 local row에는 A/B, exact pi endpoints, K, internal gaps, potential contract, rational numerator/denominator, floor/ceil, boundary status, total bound, zero flag, heuristic C를 저장한다.

## 9. 성공·중단 기준

성공:

- supplied certificate exact audit PASS
- fixed Python/hash/schema PASS
- 두 primecount 알고리즘 일치
- prime-count metadata의 CSV SHA-256·최대 8 threads·30 GiB·GPU/search 미사용 계약 PASS
- independent Fraction recomputation issue 0
- unresolved boundary zero flag 0건
- manifest artifact hash issue 0

즉시 중단:

- `pi(B-1)<pi(A-1)`
- endpoint prime state를 정수 block residue로 대체
- negative exact slack 또는 inconsistent negative local bound
- unresolved boundary인데 `certified_zero=true`
- representative blocks를 complete coverage로 표시
- READY path가 project root 밖을 가리킴
- output overwrite
- 30 GiB limit 초과

## 10. 다음 단계 판정

- internal zero candidate 0개: supplied 2310 certificate direct local skipping은 negative result; expanded sweep 중단
- internal zero candidate 존재, crossing 비용 큼: 수학적으로 가능하지만 실용 가속 실패
- internal zero + cheap crossing: G5 endpoint resolver 구현 검토
- candidate cover theorem과 runtime break-even까지 통과: 그때만 P005 계열 알고리즘 개선 후보

## 11. 참고문헌

1. Oliveira e Silva, Herzog, Pardi, DOI https://doi.org/10.1090/S0025-5718-2013-02787-1
2. Ziller, Morack, arXiv:1611.03310, https://arxiv.org/abs/1611.03310
3. Costello, Watts, DOI https://doi.org/10.1090/S0025-5718-2014-02896-2
4. primecount official repository and benchmarks, https://github.com/kimwalisch/primecount
5. Seth Troisi prime-gap official repository, https://github.com/sethtroisi/prime-gap
6. Ford–Green–Konyagin–Maynard–Tao, DOI https://doi.org/10.1090/jams/876
7. Banks–Ford–Tao, DOI https://doi.org/10.1007/s00222-023-01199-0, arXiv:1908.08613
