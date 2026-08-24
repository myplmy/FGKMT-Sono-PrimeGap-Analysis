# P007 — 유한범위 residue-state prime-gap count 인증

## 1. 상태

`G2_SUPPLIED_CERTIFICATE_EXPERIMENT_PASS / G3_WAITING_FOR_USER_APPROVAL`

첫 사용자 pilot `20260823T173316Z`는 runner 오류로 certificate audit 전에 중단됐지만, 교정판 실행 `20260823T185624Z_p007_pilot`은 preflight, 61 tests, 415,223 transition exact audit와 saved verification을 모두 통과했다. supplied certificate G2는 PASS이며 실제 prime enumeration/search는 없었다. 작은 modulus LP 비교 G3 full은 아직 실행하지 않았고 별도 사용자 승인이 필요하다.

## 2. 목적과 연구 질문

1. 제공된 modulus 2310 dual certificate가 모든 전이에서 exact integer arithmetic으로 성립하는가?
2. right-boundary crossing을 포함한 start-bounded count upper bound가 정확히 얼마인가?
3. nested modulus `30,210,2310`에서 발견·유리화한 exact certificate bound는 어떻게 변하는가?
4. modulus 30030 확장이 32 GiB 제한에서 안전한가?
5. 이 upper bound가 실제 `10^20`–`10^21` prime-gap 탐색의 후보 위치나 coverage를 제공하는가?

## 3. 비목적

- `10^20`–`10^21`의 소수를 생성하거나 gap을 exhaustive 탐색하지 않는다.
- global count upper bound를 후보 위치 목록으로 부르지 않는다.
- `C` normalization을 FGKMT/Sono 상수 또는 정리의 핵심 결론으로 부르지 않는다.
- modulus 30030 LP를 현재 full 실행기에서 풀지 않는다.
- GPU를 사용하지 않는다.
- 사용자 승인 없이 pilot/full을 실행하거나 새 패키지를 설치하지 않는다.

## 4. 수학 정의와 경계 계약

\[
N_{\ge H}(A,B)
=\#\{p:\ A\le p<B,\ \operatorname{nextprime}(p)-p\ge H\}.
\]

P007 고정값:

```text
A = 10^20 inclusive
B = 10^21 exclusive
H = 1856
boundary_mode = start-bounded count
```

이는 P003/P004의 canonical end-bounded

\[
G(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n)
\]

와 다른 보조 함수다. 두 결과를 같은 열이나 같은 부등식으로 결합하지 않는다.

내부 gap 수는 endpoints가 `(A,B)` 안에 모두 있는 경우

\[
M=\pi(B)-\pi(A)-1
\]

이고, start prime이 `B`보다 작지만 end prime이 `B` 이상인 gap은 최대 하나이므로 total bound에 `+1`을 더한다. 비교용 packing bound도

\[
\left\lfloor\frac{B-A}{H}\right\rfloor+1
\]

을 사용한다.

## 5. 입력과 고정값

- certificate: `ai_dev_tool/temp_prime_gap_count_algorithm/source/C2310_certificate.txt`
- certificate SHA-256: `44c6a9e51b5f99ef2f49f89c89cfc40604e83ce8fe20e802f21733109b1e92fb`
- reviewed generator SHA-256: `653ebc624b8245c8e10f707f667b08f46f11cc571a2b597681c206d79407f934`
- reviewed verifier SHA-256: `87fedc5141020ebdc35ab343188faeb8a92330550420e2270d59b89fc1cd9f6f`
- `pi(10^20)=2220819602560918840`
- `pi(10^21)=21127269486018731928`
- Python: `W:\miniforge3\envs\FGKMT\python.exe`
- packages: pinned `numpy`, `scipy`, `mpmath`
- GPU: disabled

prime-count 공개 교차확인: https://github.com/kimwalisch/primecount

## 6. 증명 산출물 계약

모든 허용 transition에 대해

\[
wD\le\lambda_{num}d+\mu_{num}+\phi_i-\phi_j,
\qquad \lambda_{num}\ge0,
\]

를 정수로 검사한다. LP solver는 candidate를 찾을 뿐 증명하지 않는다. accepted certificate는 다음을 모두 만족해야 한다.

1. denominator 양수, `lambda_num≥0`
2. potential 개수=`phi(modulus)`
3. `max|phi_i|≤t_num`
4. 모든 small/large representative transition slack≥0
5. 선언된 internal/total bound를 `Fraction`으로 재계산해 일치
6. saved artifact를 다시 읽고 SHA-256과 exact bound 재검증

## 7. 단계와 게이트

### G0 — 비판적 수학 검토 (`PASS`)

- start/end boundary를 분리함
- packing `+1` 오류를 교정함
- `gap≥1856 ⇒ p+1856 prime` 오류를 기각함
- finite-flow endpoint term을 명시함
- global count bound가 후보 위치를 주지 않음을 명시함

상세 근거: `docs/review/15_P007_finite-range-residue-certificate_타당성검토.md`

### G1 — 로컬 코드 사전검증 (`PASS — 2026-08-24`)

- `py_compile`
- P007 toy unittest
- 전체 unittest
- supplied certificate exact audit를 test 함수로 재검산
- 두 edge builder를 toy modulus에서 집합 대조
- PowerShell parser와 두 BAT approval-denial 경로 검사

하나라도 실패하면 실제 P007 실행을 중단한다.

실제 검증 증거:

- targeted P007 tests: 8/8 PASS
- 최종 전체 repository tests: 61/61 PASS, 4.411초
- supplied verifier: 480 states, 415,223 constraints, minimum slack 0, PASS
- P007 preflight: 고정 Python·input hash·resource guard 모두 PASS
- PowerShell parser와 pilot/full BAT approval-denial: PASS
- 교정 검증 보고서: `test_result/202608240329_P005_P006_P007_runner_fix_local_validation.md`

### G2 — supplied certificate pilot (`EXPERIMENT_PASS — 20260823T185624Z`)

- 입력 hash 고정
- modulus 2310, 480 states, 415,223 constraints exact 검증
- corrected packing bound, internal/total bound, heuristic `C`를 분리 저장
- prime enumeration/search는 0건

실행 감사:

- log: `test_result/logs/run_20260823T173316Z_p007_pilot.log`, SHA-256 `2E0E831DF50361F965EF22E95594ADB80BFF7E5173670366FCA8FD5EE76F8C1B`
- preflight PASS, 61-test Python process exit 0
- 정상 빈 stderr 줄의 parameter binding 오류로 certificate audit·result·verification은 NOT RUN
- 상세: `test_result/202608240315_P007_pilot_failure_analysis.md`

교정판 성공 실행:

- log: `test_result/logs/run_20260823T185624Z_p007_pilot.log`, SHA-256 `6d1bb5e777b367d223f5d200b35d08e2b90a1ac2b65860118d3cb29e80456e82`
- 61 tests PASS, 480 states, 415,223 constraints, minimum slack 0
- saved-artifact verification issue 0
- actual prime search false, direct acceleration false
- 상세: `test_result/202608240432_P007_pilot_certificate_result_analysis.md`
- 실행 BAT 보존: `test_done/run_P007_finite_gap_certificate_pilot-20260823T185624Z-done.bat`, SHA-256 `7BC4524C945C4081EA93F1D50BB8E8FD3D8457F30F32703609F3504BA5A952EC`

### G3 — 작은 modulus 비교 full phase A (`WAITING_FOR_USER_APPROVAL`)

- modulus `30,210,2310`에 대해 SciPy HiGHS로 candidate 탐색
- denominator `10^15`로 유리화
- 가장 작은 negative slack만큼 `mu_num`을 exact integer repair
- 모든 edge exact 재검증
- nested modulus의 bound가 실제 산출물에서 non-increasing인지 확인
- modulus 30030은 resource estimate만 생성

사용자 승인 후 명령:

```bat
run_P007_finite_gap_certificate_full.bat --confirm-p007
```

예상시간: 약 5–30분, 메모리 약 2 GiB 이하를 목표로 한 사전 추정이다. 실제 시간·메모리는 pilot/full 로그로만 확정한다.

### G4 — modulus 30030 (`BLOCKED_BY_RESOURCE_DESIGN`)

- states 5,760
- large ordered transitions 33,177,600개와 additional small transitions
- 현재 1,000,000-constraint guard가 실행 전 차단

다음 중 하나가 구현·toy 검증되기 전에는 실행하지 않는다.

1. cutting-plane/constraint generation
2. residue product 구조를 이용한 dynamic or shortest-path separation oracle
3. compiled streaming exact verifier와 명시적인 peak-memory proof

32 GiB RAM 한계 중 실제 사용 상한은 30 GiB 이하로 잡는다.

### G5 — P005 탐색과 연결 (`BLOCKED_BY_MISSING_CONSTRUCTIVE_COVER`)

global upper bound만으로는 탐색 block을 건너뛸 수 없다. 다음이 있어야 탐색 개선으로 승격한다.

1. false negative가 없는 candidate-location generator
2. block별 local no-gap 또는 survivor certificate
3. 경계 overlap과 모든 block을 기록한 coverage ledger
4. endpoint primality와 interior compositeness verification

## 8. 실행기와 산출물

구현:

- `source/finite_gap_certificate.py`
- `source/finite_gap_certificate_cli.py`
- `tests/test_finite_gap_certificate.py`
- `run_finite_gap_certificate.ps1`
- `run_P007_finite_gap_certificate_pilot.bat`
- `run_P007_finite_gap_certificate_full.bat`

승인 실행 산출물:

- `test_result/logs/run_<UTC>_p007_<mode>.log`
- `test_result/run_<UTC>_p007_<mode>/manifest.json`
- pilot: copied input certificate와 `verification_report.json`
- full: modulus별 exact certificate와 `comparison_report.json`

기존 파일과 run ID를 덮어쓰지 않는다. PowerShell runner는 Python stdout/stderr를 임시 파일로 분리 수집하여 Windows PowerShell 5.1 `NativeCommandError` 오판을 피하고, 빈 줄·traceback·nonzero exit·PowerShell 전체 ErrorRecord를 같은 run log에 보존한다.

## 9. 성공·경고·중단 기준

성공:

- preflight 전 항목 PASS
- 전체 unittest exit 0
- certificate 모든 slack≥0
- declared/recomputed bound 일치
- saved artifact hash와 재검증 PASS
- GPU/search 미사용이 manifest와 로그에 표시

경고:

- 작은 modulus에서 bound 개선이 0일 수 있음
- floating candidate가 solver 옵션에 따라 달라질 수 있음
- heuristic `C`는 설명용이며 rigorous claim이 아님

즉시 중단:

- 입력 hash 불일치
- negative exact slack
- right-boundary `+1` 누락
- modulus 30030 solve 요청
- 100만 constraints 초과
- output path 충돌
- 승인 flag 누락
- Python 또는 dependency pin 불일치

## 10. 해석 제한

- supplied modulus 2310 인증값은 현재 입력·수식에 대한 exact computational certificate다.
- `N≤U`는 실제 `N`, 후보 위치, maximal gap의 존재/부재를 알려주지 않는다.
- bound가 작아져도 P005 runtime 감소율로 환산하지 않는다.
- `N=0`을 인증하지 못하면 해당 범위에서 gap 1856 이상이 없다고 결론 내리지 않는다.
- P007 start-bounded count를 P003/P004 end-bounded `G(x)` 산출물과 직접 합치지 않는다.

### 10.1 상한 크기와 알고리즘 연결 기준

현재 인증의 정규화 분모는 `T≈398.2227929091105`이고 `C=U/T`다. 정수 `U`가 엄밀한 결론이며 `C`는 크기 비교용이다.

| 수준 | count upper bound `U` | 대응 `C` | 전역 bound만으로 P005 직접 가속? |
|---|---:|---:|---|
| 현재 | `439161464927854179` | `1.102803437542279e15` | 아니오 |
| `C=1e14` | 약 `3.982227929091105e16` | `1e14` | 아니오 |
| `U≤10^9` | `1000000000` | 약 `2.5111571e6` | 아니오; 위치 목록이 아님 |
| `U≤1` | `1` | 약 `0.0025111571` | 아니오; 한 곳의 위치도 모름 |
| `U=0` | `0` | `0` | 예; 해당 threshold 질문에는 탐색 불필요 |

양의 `U`에서 계산 개선을 주장하려면 실제 후보 cover 크기 `K` 또는 건너뛴 block의 local certificate가 필요하다. 실측 break-even은

\[
T_{certificate}+K T_{verify}+T_{coverage}<T_{baseline}
\]

으로 판정한다. `K`를 주지 않는 전역 `U`에는 “얼마 이하이면 자동으로 빨라진다”는 단일 임계값이 없다.

## 11. 참고문헌

1. Ford, Green, Konyagin, Maynard, Tao, *Long gaps between primes*, JAMS 31 (2018), DOI https://doi.org/10.1090/jams/876
2. Ford, Maynard, Tao, *Chains of large gaps between primes*, arXiv:1511.04468, https://arxiv.org/abs/1511.04468
3. Banks, Ford, Tao, *Large prime gaps and probabilistic models*, DOI https://doi.org/10.1007/s00222-023-01199-0, arXiv:1908.08613
4. Oliveira e Silva, Herzog, Pardi, *Empirical verification ... and computation of prime gaps up to 4×10^18*, DOI https://doi.org/10.1090/S0025-5718-2013-02787-1
5. Nicely, *New maximal prime gaps and first occurrences*, DOI https://doi.org/10.1090/S0025-5718-99-01065-0
6. Ziller, Morack, *Algorithmic concepts for the computation of Jacobsthal's function*, arXiv:1611.03310
7. Erdős, *On the Integers Relatively Prime to n and a Number-Theoretic Function Considered by Jacobsthal*, DOI https://doi.org/10.7146/math.scand.a-10523
8. Costello, Watts, *An upper bound on Jacobsthal's function*, DOI https://doi.org/10.1090/S0025-5718-2014-02896-2
9. Montgomery, Vaughan, *Multiplicative Number Theory II: Primes and Sieves*, DOI https://doi.org/10.1017/9781009445030
10. `primecount` exact prime-count table, https://github.com/kimwalisch/primecount

## 12. 다음 승인 결정

사용자가 원하면 교정판 G2 pilot을 다시 실행한다. 새 log와 saved artifact를 Codex가 검토한 뒤에만 G3 full phase A 실행 여부를 결정한다. G4/G5는 현재 실행 승인을 요청하지 않는다.
