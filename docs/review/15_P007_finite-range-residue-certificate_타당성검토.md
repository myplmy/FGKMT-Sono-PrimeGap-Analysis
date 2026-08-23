# P007 finite-range residue-state certificate 비판적 타당성 검토

## 결론

제안의 핵심인 **유한 범위 residue-state dual certificate**는 수학적으로 타당한 연구 대상이다. 제공된 modulus 2310 인증서는 정수 산술로 모든 전이 부등식을 검사할 수 있고, 올바른 경계 보정을 포함하면 다음을 인증한다.

\[
N_{\ge1856}(10^{20},10^{21})
\le 439{,}161{,}464{,}927{,}854{,}179.
\]

다만 이것은 `10^20`부터 `10^21` 사이에 큰 gap이 있을 **수 있는 위치 목록**이 아니다. 실제 큰 gap의 개수에 대한 전역 상한만 주므로, 이 숫자를 낮추는 것만으로 `prime-gap`이나 segmented sieve가 건너뛸 구간이 자동으로 생기지 않는다. 따라서 P007은 다음처럼 채택한다.

- 채택: exact certificate 검증, 작은 modulus 비교, 더 큰 modulus의 계산량·메모리 타당성 평가
- 보류: modulus 30030 LP의 직접 실행
- 기각: 현재 인증서만으로 `10^20`–`10^21` exhaustive 탐색이 직접 빨라진다는 주장
- 별도 필요: 누락 없는 후보 위치 집합 또는 block별 local certificate와 coverage ledger

## 검토 대상과 provenance

- `ai_dev_tool/temp_prime_gap_count_algorithm/C_1856_finite_range_research_memo(검토용).md`
- `ai_dev_tool/temp_prime_gap_count_algorithm/PrimeGap_FiniteRange_Theory_Nomenclature_and_Certification(검토용).md`
- `source/C2310_certificate.txt`, SHA-256 `44c6a9e51b5f99ef2f49f89c89cfc40604e83ce8fe20e802f21733109b1e92fb`
- `source/C_2310_certificate.py`, SHA-256 `653ebc624b8245c8e10f707f667b08f46f11cc571a2b597681c206d79407f934`
- `source/verify_C2310.py`, SHA-256 `87fedc5141020ebdc35ab343188faeb8a92330550420e2270d59b89fc1cd9f6f`

위 `source/` 경로는 모두 `ai_dev_tool/temp_prime_gap_count_algorithm/` 아래의 상대경로다.

## 정확한 연구 대상

P007의 함수는 canonical end-bounded `G(x)`와 다른 start-bounded count다.

\[
N_{\ge H}(A,B)
=\#\{p:\ A\le p<B,\ p\text{와 }p^+=\operatorname{nextprime}(p)
\text{가 연속 소수이고 }p^+-p\ge H\}.
\]

이 정의에서는 마지막 start prime `p<B`의 다음 소수가 `B` 이상일 수 있다. 그래서 내부 endpoint가 모두 `B` 미만인 gap 개수에 **최대 1개**의 right-boundary crossing gap을 더해야 한다. 이 경계 의미를 P003/P004의 end-bounded FGKMT 함수와 혼합하지 않는다.

## 타당한 증명 구조

`A=10^20`, `B=10^21`에서는 모든 대상 소수가 11보다 크므로 양 끝 소수는 modulus 2310의 unit residue다. residue 전이를 `r→s`, 실제 gap을 `d`, 큰-gap 지시자를 `w`라 하고 다음 exact 부등식을 모든 허용 전이에 대해 확인한다.

\[
wD\le \lambda_{num}d+\mu_{num}+\phi_{num}(r)-\phi_{num}(s),
\qquad \lambda_{num}\ge0.
\]

`lambda≥0`이므로 같은 residue 전이·같은 small/large 분류에서는 가장 작은 양의 대표 gap만 검사해도 더 큰 대표를 자동으로 덮는다. 내부 prime path에 부등식을 합하면 potential이 망원합으로 사라지고 양 끝 차이만 남는다.

\[
N_{internal}
\le \lambda(B-A)+\mu\{\pi(B)-\pi(A)-1\}+2t.
\]

여기서 사용한 값은 다음과 같다.

\[
\pi(10^{20})=2{,}220{,}819{,}602{,}560{,}918{,}840,
\]

\[
\pi(10^{21})=21{,}127{,}269{,}486{,}018{,}731{,}928.
\]

제공 인증서는 480 states, 415,223 transition constraints에서 최소 정수 slack 0을 가지며, 내부 upper bound `439161464927854178`과 right-boundary 1개를 합쳐 총 `439161464927854179`를 준다. LP의 부동소수점 해는 증명이 아니며 이 전수 정수 검사가 증명 산출물이다.

## 반드시 고쳐야 하는 주장

### 1. 단순 packing의 경계 보정

start-bounded 전체 count에 대한 안전한 비교 기준은

\[
N_{\ge H}(A,B)\le
\left\lfloor\frac{B-A}{H}\right\rfloor+1
\]

이다. 마지막 gap이 `B`를 가로지를 수 있으므로 `+1` 없는 식은 전체 start-bounded 함수의 일반적 상한으로는 부족하다. 현재 인증서 계산은 마지막에 `+1`을 실제로 더했으므로 최종 인증값은 이 오류의 영향을 받지 않는다.

### 2. `gap≥1856`과 prime pair `(p,p+1856)`는 동치가 아님

gap이 정확히 1856일 때만 `p+1856`이 다음 소수다. gap이 1858 이상이면 `p+1856`은 보통 gap 내부의 합성수다. 따라서

\[
N_{\ge1856}\le\#\{p:p,p+1856\text{ prime}\}
\]

라는 문서의 prime-pair 비교는 성립하지 않는다. Selberg prime-pair sieve를 이 방식으로 직접 적용하는 부분은 폐기해야 한다.

### 3. finite path의 flow conservation에는 경계가 있음

유한 prime path는 시작 state와 끝 state에서 flow imbalance가 난다. primal LP에서 모든 state에 exact conservation을 강제하면 원래 finite path와 다른 모델이 된다. dual telescope의 `2t` boundary term처럼 끝점 불균형을 명시해야 한다.

### 4. 기존 verifier의 독립성은 제한적임

`verify_C2310.py`는 generator와 분리된 파일이지만 residue/edge 생성 공식과 상수를 다시 복제한다. 부동소수점 solver 없이 exact arithmetic을 확인한다는 점에서는 독립적이나, 같은 모델링 오류를 공유하지 않는 완전한 독립 구현은 아니다. P007에서는 ordered-pair builder와 offset builder를 toy modulus에서 대조하고, 수식·경계는 별도로 감사한다.

### 5. `C`는 설명용 정규화이지 정리의 핵심 상수가 아님

메모의

\[
\mathcal T=\frac{B-A}{\log B}\exp(-H/\log B),\qquad C=U/\mathcal T
\]

는 bound 크기를 비교하는 heuristic normalization이다. 엄밀한 결론은 정수 `U`이며 `C`를 FGKMT/Sono 상수나 관측된 large-gap count로 해석하면 안 된다.

## 사용자의 알고리즘 개선 가설 판정

사용자 의견 중 “상한이 충분히 낮아지면 후속 검사를 줄일 가능성이 있다”는 방향성은 **조건부로** 맞다. 그러나 다음 연결고리가 추가로 필요하다.

1. 모든 실제 큰 gap start를 포함하는 구체적인 후보 집합을 생성한다.
2. 후보가 아닌 block을 건너뛰어도 된다는 local certificate를 만든다.
3. 모든 block의 포함·경계를 추적하는 coverage ledger를 만든다.
4. survivor마다 양 끝 소수성과 내부 합성수를 인증한다.

전역 명제 `N≤U`는 실제 위치를 알려주지 않는다. 예를 들어 `U≤10^9`여도 “검사할 후보 파일이 10억 행 이하”라는 뜻은 아니다. 따라서 P007의 bound가 P005 탐색시간을 줄였다고 기록하려면 위 네 가지 중 적어도 후보 cover와 coverage proof가 구현되어야 한다.

## modulus 확대 타당성

modulus가 divisibility chain `30|210|2310|30030`을 이루면 coarse certificate를 finer state에 lift할 수 있으므로 exact 최적값은 이론상 나빠질 필요가 없다. 하지만 부동소수점 solver, rationalization, 제한된 formulation 때문에 실제로 찾은 인증값은 개선되지 않거나 탐색에 실패할 수 있다.

- `M=2310`: 480 states, 415,223 constraints로 현재 환경에서 sparse LP 후보 탐색이 가능
- `M=30030`: 5,760 states, large transition만 33,177,600개이고 small transition이 추가됨
- `M=510510`: 92,160 states, ordered-pair large transition만 약 84.9억 개

30030은 “작은 sparse LP”가 아니다. Python COO 배열, CSR 변환, HiGHS presolve/basis가 동시에 존재할 수 있어 32 GiB 제한 안에서 안전하다고 보장할 수 없다. 준비한 코드는 transition 100만 개 상한으로 30030 solve를 실행 전에 차단하고 resource estimate만 낸다. 30030을 실제 연구하려면 constraint generation/cutting-plane, 구조를 이용한 동적계획, compiled streaming verifier 중 하나가 먼저 필요하다.

## 선행연구와의 관계

- Ford–Green–Konyagin–Maynard–Tao, *Long gaps between primes*, JAMS 31 (2018), DOI https://doi.org/10.1090/jams/876 — 점근적 large-gap lower bound이며 이 유한 count certificate와 목적이 다르다.
- Ford–Maynard–Tao, *Chains of large gaps between primes*, arXiv:1511.04468 — FGKMT scale과 effective constant의 이론적 배경이며 finite search cover를 제공하지 않는다.
- Banks–Ford–Tao, *Large prime gaps and probabilistic models*, Invent. Math. 233 (2023), DOI https://doi.org/10.1007/s00222-023-01199-0, arXiv:1908.08613 — 확률 모델과 heuristic 범위를 다루므로 P007 exact 인증의 대체물이 아니다.
- Oliveira e Silva–Herzog–Pardi, *Empirical verification ... and computation of prime gaps up to 4×10^18*, DOI https://doi.org/10.1090/S0025-5718-2013-02787-1 — exhaustive block sieving과 검증 산출물의 중요한 계산 선례다.
- Nicely, *New maximal prime gaps and first occurrences*, DOI https://doi.org/10.1090/S0025-5718-99-01065-0 — first occurrence/maximal gap 탐색은 exhaustive coverage가 핵심임을 보여준다.
- Ziller–Morack, *Algorithmic concepts for the computation of Jacobsthal's function*, arXiv:1611.03310 — primorial residue 구조의 exhaustive 계산과 pruning 참고문헌이다.
- Erdős, *On the Integers Relatively Prime to n and a Number-Theoretic Function Considered by Jacobsthal*, DOI https://doi.org/10.7146/math.scand.a-10523.
- Costello–Watts, *An upper bound on Jacobsthal's function*, DOI https://doi.org/10.1090/S0025-5718-2014-02896-2.
- Montgomery–Vaughan, *Multiplicative Number Theory II: Primes and Sieves*, DOI https://doi.org/10.1017/9781009445030 — Selberg/upper-bound sieve의 일반 참고문헌이다.
- `primecount` 공식 표: https://github.com/kimwalisch/primecount — 위 두 exact prime-count 값의 공개 교차확인 원천이다.

이 문헌들은 residue-state certificate라는 명칭이나 현재 2310 인증값의 선행 출판을 입증하지 않는다. 별도의 체계적 novelty search 전에는 “새 정리”라고 주장하지 않는다.

## 최종 판정

P007을 **finite-range upper-bound certificate의 재현·개선 가능성 실험**으로 진행하는 것은 타당하다. 제공된 인증값은 exact 검증 가능한 결과지만 탐색 위치를 주지 않으므로 P005의 직접 가속기로 연결하지 않는다. P007 phase A는 `30,210,2310` 비교까지만 승인 가능한 크기로 준비하고, 30030과 Buchstab/Type-I·II 주장은 후속 수학·알고리즘 설계 항목으로 남긴다.


## 2026-08-24 사용자 질문에 대한 쉬운 판정

다음처럼 범위를 정확히 붙이면 사용자가 요약한 문장은 맞다.

> modulus 2310 residue-state dual certificate를 사용해, start prime `p`가 `[10^20,10^21)`에 있는 consecutive-prime gap 중 길이 1856 이상인 것의 개수에 대해, 추측을 쓰지 않는 계산적 상한 `439161464927854179`를 얻었고 모든 certificate 부등식을 exact integer arithmetic으로 검사했다.

구성은 480 states, 415,223 constraints, minimum integer slack 0이다. 내부 path 상한 `439161464927854178`에 `10^21` 오른쪽 경계를 가로지를 수 있는 gap 최대 1개를 더했다. “무조건적”은 리만가설 같은 미증명 추측을 쓰지 않는다는 뜻이다. 다만 이것은 현재 모델·경계 유도·exact prime-count 값·검증 프로그램을 함께 감사한 **유한 계산 인증**이며, failed P007 pilot이 새로 만든 결과나 실제 gap을 센 관측 결과는 아니다.

`C_max≤1.102803437542279×10^15`도 반올림값으로 맞지만, 엄밀한 정리의 핵심은 정수 `U`다. `C=U/T`, `T≈398.2227929091105`는 상한의 크기를 보기 위한 heuristic normalization이다. 현재 값은 corrected packing bound `484913793103448276`보다 약 9.435% 낮을 뿐이므로, 실제 탐색량을 크게 줄였다고 볼 수 없다.

연구 결과가 좋으면 알고리즘 개선으로 발전할 가능성은 있다. 그러나 전역 count 상한만 낮추는 연구와 실제 탐색 가속 사이에는 다음 한 단계가 더 필요하다.

1. 큰 gap이 있을 수 있는 위치를 빠짐없이 출력하는 candidate cover
2. 후보가 없는 block을 건너뛰어도 된다는 local certificate
3. 전체 범위와 경계를 빠짐없이 처리했다는 coverage ledger
4. certificate 생성·검증 비용까지 포함한 실제 break-even benchmark

양의 상한 `U`에는 자동 가속 임계값이 없다. `U≤10^9`나 심지어 `U≤1`도 위치를 알려 주지 않으므로 전체 범위를 훑어야 할 수 있다. `U=0`이면 해당 범위에 threshold 이상 gap이 없음을 바로 인증하므로 그 질문에 대한 탐색을 생략할 수 있다. 양의 `U`에서 도움 여부는 count `U`가 아니라 실제 후보 수 `K`를 만들 수 있는지와

\[
T_{certificate}+K T_{verify}+T_{coverage}<T_{baseline}
\]

를 실측해 판정해야 한다.

따라서 P007의 다음 연구 목표는 단순히 `C`를 낮추는 것만이 아니라, certificate가 block별 no-gap 판정이나 실제 candidate 위치를 내도록 구조를 바꾸는 것이다. 그 연결이 성공하면 P005 계열 exhaustive 탐색의 일부 block을 안전하게 건너뛰는 알고리즘으로 발전할 수 있다.
