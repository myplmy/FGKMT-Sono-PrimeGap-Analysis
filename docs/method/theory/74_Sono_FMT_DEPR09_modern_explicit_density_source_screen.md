# Sono/FMT DEP-R09 현대 명시적 zero-density 대체자료 선별

- 작성일: 2026-09-14 KST
- 단계: **DEP-R09 / MODERN EXPLICIT DENSITY SOURCE SCREEN**
- 선행 정본: [Theory 72](72_Sono_FMT_DEPR09_Gallagher_Maier_PAP_density_integral_split.md),
  [Theory 73](73_Sono_FMT_DEPR09_CJ_loss_tree_structural_audit.md)
- 기계 원장: [modern density source screen v1](data/Sono_FMT_DEPR09_modern_density_source_screen_v1.json)
- 판정: **선별한 공개 후보 중 (d\le186) PAP gate에 그대로 대입 가능한 수치 정리는 없음**
- 비목적: 모든 관련 문헌의 불가능성 증명, source analytic theorem의 Lean 재증명,
  `PAP-11`·`DEP-R09`·fixed (2\times10^{-17}) 또는 numerical
  (X_{\rm cert}) 인증, actual prime 계산

## 1. 결론

Theory 73의 다음 질문은 “현재 (C_J)를 더 다듬을 것인가”가 아니라
“더 좋은 현대 정리를 넣으면 (d\le186)에서 PAP가 수치적으로 닫히는가”였다.
이번에는 다음 여덟 갈래를 같은 변수로 비교했다.

1. Ramaré 2016의 완전 수치 averaged density,
2. Thorner--Zaman 2024의 explicit Bombieri density,
3. Thorner--Zaman 2024의 uniform PNT in progressions,
4. Kaneko--Thorner 2025의 highly uniform PNT,
5. Thorner--Zhang 2026의 Chebotarev relative-error route,
6. Friedlander--Iwaniec 2023의 density를 우회하는 sieve route,
7. Chen--Gupta--Li 2026 arXiv 원고의 개선된 density exponent,
8. Bellotti--Castillo의 아직 공개되지 않은 in-preparation 결과.

선별 결과는 다음과 같다.

\[
 \boxed{\text{이번에 식별·감사한 공개 후보 중 numerical drop-in 통과 후보는 0개다.}}
\tag{74.1}
\]

이는 “그런 정리가 세상에 존재할 수 없다”는 전수 불가능성 정리가 아니다. 검색하고
원문을 확보한 후보 집합에 대한 fail-closed 판정이다. 따라서 fixed Sono coefficient와
(X_{\rm cert})의 상태를 올리지 않는다.

> **쉬운 설명:** 최신 논문의 제목이나 지수가 더 좋아 보여도, 계산기에 넣을 숫자가
> 모두 적혀 있어야 한다. 이번 후보들은 (a) 숫자는 있지만 우리 식에 넣으면 너무 크거나,
> (b) 구조는 좋지만 숨은 상수와 시작점이 없거나, (c) 아직 미심사·미공개였다. 그러므로
> 지금 큰 소수를 더 계산한다고 마지막 증명 구멍이 메워지지는 않는다.

## 2. 통과해야 하는 실제 계약

현재 downstream 증명이 요구하는 pointwise PAP 입력은 좋은 modulus에 대해

\[
 \pi(u;q,a)\ge
 C_{\rm PAP}\frac{u}{\varphi(q)\log u},
 \qquad q\le u^{1/D}
\tag{74.2}
\]

형태다. Theory 58의 coefficient capacity를 바꾸지 않으면 낙관적으로도
(D\le186)이어야 한다. (D=160)에서는

\[
 C_{\rm PAP}\ge
 0.8638312615226712472\ldots
\tag{74.3}
\]

가 필요하고, Gallagher--Maier branch의 현재 positive error budget은 추가 유한 손실 전에
적어도 (e^{-2}) 이하여야 한다. 따라서 source 후보는 다음을 모두 제공해야 한다.

- 실제 primitive character family와 modulus·height 범위,
- numerical multiplier와 numerical finite cutoff,
- principal·exceptional character 처리,
- averaged zero count에서 식 (74.2)의 pointwise prime count로 가는 수치 전달.

지수만 개선되거나 “effectively computable”, (O(\cdot)), (o(1))이 남으면
(X_{\rm cert}) 계산기의 인증 입력으로 승격하지 않는다.

## 3. 원문 판독과 기존 고전 source의 위치

사용자가 추가한 Gallagher 1970, Maier 1981, McCurley 1984 원문은 이미
Theory 57·65·72에서 hash와 printed page/equation 단위로 감사했다. 이 세 논문은
현재 PAP proof architecture의 baseline이며, 이번 단계에서 “현대 대체자료”인 것처럼
중복 등록하지 않았다.

이번에 새로 확보한 Ramaré, Friedlander--Iwaniec, Chen--Gupta--Li,
Thorner--Zhang PDF는 모두 usable native text layer가 있었다. 텍스트로 먼저 위치와
수식을 찾고 해당 렌더 페이지를 원문과 대조했으며 OCR은 쓰지 않았다. 따라서 수식의
첨자·지수는 OCR 추정값이 아니다.

## 4. 후보별 판정표

| 후보 | 공개 상태 | 장점 | 현재 gate에서 막힌 이유 | 판정 |
|---|---|---|---|---|
| Ramaré 2016, Theorem 1.1 | peer-reviewed | 범위·상수·가중 평균이 모두 수치 | direct 적분에서 log power와 (32Q^2L^2) additive term이 남음 | direct insertion `FAIL` |
| Thorner--Zaman explicit Bombieri | peer-reviewed | 전 구간 explicit, near exponent 99/170 | (10^{88},10^{93}) prefactor와 PAP 전달 예산 미폐쇄; exceptional all-sigma exponent 198 | `HOLD` |
| Thorner--Zaman uniform PNT | peer-reviewed | 점별 PNT 구조가 목표와 가장 가까움 | relevant decay multiplier와 공통 cutoff가 unnamed | 최우선 구조 후보, numerical `HOLD` |
| Kaneko--Thorner highly uniform PNT | peer-reviewed | 넓은 uniformity | 수치 Dirichlet pointwise package가 인쇄되지 않음 | `HOLD` |
| Thorner--Zhang Chebotarev | peer-reviewed/online | cyclotomic specialization 가능 | (c_i)가 effectively computable이나 숫자로 주어지지 않음 | `HOLD` |
| Friedlander--Iwaniec sieve | peer-reviewed | log-free density·DH를 우회하는 다른 구조 | (x\ge q^{52600}), coefficient (1/210000), smoothing·sister-source 조건 | numerical `FAIL` |
| Chen--Gupta--Li density | arXiv v2, 미검증 | exponent (7/3), smooth modulus (30/13) | ((qT)^{o(1)})와 cutoff가 비수치 | 승격 금지 |
| Bellotti--Castillo Dirichlet density | in preparation | 제목상 missing component와 직접 일치 | 공개 statement·formula·multiplier가 없음 | watchlist only |

## 5. Ramaré 정리의 direct insertion 계산

Ramaré Theorem 1.1은 (T\ge2000), (T\ge Q\ge10),
(\sigma\ge0.52)에서

\[
 \sum_{q\le Q}\frac q{\varphi(q)}
 \sum_{\chi\bmod^{*}q}N(\sigma,T,\chi)
 \le
 20(56Q^5T^3)^{1-\sigma}
 \log^{5-2\sigma}(Q^2T)
 +32Q^2\log^2(Q^2T)
\tag{74.4}
\]

를 준다. (q/\varphi(q)\ge1)이므로 필요한 unweighted primitive 평균도 제어한다.


\[
 \delta=1-\sigma,\qquad
 Q=X^{1/d},\qquad T=Q^5,\qquad
 L=\log(Q^2T)=\frac7d\log X
\tag{74.5}
\]

로 놓고 Gallagher kernel (X^{-\delta})를 곱하면 두 source term은

\[
 B_{\rm main}(\delta)
 =20\,56^\delta L^{3+2\delta}
 \exp\!\left[-\left(1-\frac{20}{d}\right)\delta\log X\right],
\tag{74.6}
\]

\[
 B_{\rm add}(\delta)
 =32L^2\exp\!\left[\left(\frac2d-\delta\right)\log X\right].
\tag{74.7}
\]

현재 McCurley 보수 폭 (c_1=1/24)에서 (T=Q^5)의 zero-free edge는

\[
 \eta\log X=\frac{c_1d}{5}.
\tag{74.8}
\]

Gallagher의 바깥 (\log X)와 정확히 상쇄되는 한 unit slice
(\delta\in[\eta,\eta+1/\log X])만 보아도, source RHS를 그대로 적분해 얻는
upper-certificate에는 다음 양의 하한이 생긴다.

\[
 \mathcal C_{\rm main}^{\rm slice}\ge
 20L^3\exp\!\left[-\left(1-\frac{20}{d}\right)
 \left(\frac{c_1d}{5}+1\right)\right],
\tag{74.9}
\]

\[
 \mathcal C_{\rm add}^{\rm slice}\ge
 32L^2\exp\!\left[\frac{2\log X}{d}
 -\left(\frac{c_1d}{5}+1\right)\right].
\tag{74.10}
\]

(d=186,c_1=1/24)에서는 exact하게

\[
 1-\frac{20}{d}=\frac{83}{93},\qquad
 \frac2d=\frac1{93},\qquad
 \frac{c_1d}{5}=\frac{31}{20}.
\tag{74.11}
\]

세 source 조건을 동시에 만족시키는 충분 하한은

\[
 \log X\ge
 \max\!\left\{d\log10,\frac d5\log2000,
 \frac{c_1d/5+1}{1-0.52}\right\}
 =186\log10.
\tag{74.12}
\]

이 시작점에서 100자리 진단값은

\[
 \mathcal C_{\rm main}^{\rm slice}>8602.03,
 \qquad
 \mathcal C_{\rm add}^{\rm slice}>64912.22,
 \qquad e^{-2}<0.136.
\tag{74.13}
\]

두 식의 오른쪽은 이 범위에서 (\log X)와 함께 증가한다. 그러므로 이 source RHS만
비음수로 direct 적분하는 방식은 (X)를 더 크게 해도 (e^{-2}) 예산을 인증하지 못한다.

중요한 논리 경계는 다음과 같다.

- 식 (74.9)--(74.13)은 **실제 prime-distribution error의 하한이 아니다.**
- 이는 Ramaré 정리가 거짓이거나 쓸모없다는 뜻이 아니다.
- 다른 upper bound와의 minimum, cancellation, smoothing 또는 transfer 재설계는 배제하지 않는다.
- 증명한 것은 “이 theorem RHS를 현재 Gallagher 적분에 그대로 넣는 certificate”의 실패뿐이다.

## 6. Thorner--Zaman 두 갈래

explicit Bombieri 논문의 relevant source shape는 Theory 58에서 감사한

\[
 10^{88}(10^{421}Q^{99})^{1-\sigma},
 \qquad
 10^{93}\min\{1,(1-\beta_1)\log Q\}
 (10^{466}Q^{170})^{1-\sigma}
\tag{74.14}
\]

이다. 지수 비교만 하면

\[
 99\le186,\qquad170\le186,\qquad198>186.
\tag{74.15}
\]

near exponent 두 개는 형식상 capacity 안에 있지만, 큰 고정 prefactor와 exceptional
factor, 식 (74.2)로의 numerical transfer를 한 공통 budget에서 닫지 못했다. 반대로
*Refinements to the prime number theorem for arithmetic progressions*는 구조상 식 (74.2)에
가장 가까운 published 후보지만 핵심 상수와 cutoff가 “effectively computable” 수준이다.
따라서 어느 쪽도 현재 계산기에 바로 넣을 수 없다.

## 7. 개선된 exponent와 Chebotarev 결과를 승격하지 않은 이유

Chen--Gupta--Li Theorem 1.2가 주는 대표 요약은

\[
 \sum_{\chi\bmod q}N(\sigma,T,\chi)
 \le(qT)^{\frac73(1-\sigma)+o(1)}
\tag{74.16}
\]

이고 smooth modulus에서는 (30/13) exponent가 나타난다. 그러나 (o(1))의 multiplier와
finite cutoff가 숫자가 아니며, 2026-09-14 현재 arXiv v2 원고로 분류했다. 이 결과는
미래 proof design에는 중요하지만 현 numerical certificate에는 넣지 않는다.

Thorner--Zhang과 Kaneko--Thorner는 effective 구조를 제공한다. 그러나 “계산 가능하다”는
존재 명제와 실제 계산기에 넣을 숫자가 인쇄되었다는 명제는 다르다. 각 (c_i), 공통 cutoff,
Dirichlet specialization과 pointwise transfer를 별도로 복원하기 전에는 `HOLD`다.

## 8. Friedlander--Iwaniec 우회 경로

Friedlander--Iwaniec Lemma 7.1의 수치 결과는 조건부 세 branch 아래

\[
 x\ge q^{52600},\qquad
 \varphi(q)\pi_f(x;q,a)\ge
 \frac{\widehat f(0)x}{210000\log x}.
\tag{74.17}
\]

이다. Theorem 7.2의 마지막 exponent는

\[
 80\cdot18\cdot52600=75{,}744{,}000.
\tag{74.18}
\]

이 갈래는 density/DH 구조를 우회한다는 점에서 연구 아이디어로는 가치가 있다. 하지만
(52600>186), (1/210000<4/5)이고 (\pi_f)가 smoothed count이며 일부 branch가
sister source를 사용한다. 현재 fixed coefficient를 보존하는 drop-in은 아니다.

## 9. 판정과 다음 gate

이번 source screen 뒤 상태는 다음과 같다.

| 항목 | 상태 |
|---|---|
| 식별한 modern 후보의 source·publication·수식 범위 감사 | `DONE` |
| Ramaré direct nonnegative insertion | `FAILS CURRENT BUDGET` |
| Thorner--Zaman uniform PNT | `BEST STRUCTURAL CANDIDATE / NUMERICAL HOLD` |
| 미심사·미공개 결과의 certificate 승격 | `NOT DONE` |
| 모든 가능한 문헌·hybrid proof의 불가능성 | `NOT CLAIMED` |
| `PAP-11`, `DEP-R09` | `OPEN` |
| fixed (2\times10^{-17}), numerical (X_{\rm cert}) | `OPEN` |
| threshold calculator·장시간 prime 계산 | `NOT READY / NOT RUN` |

다음 합리적 갈래는 둘이다.

1. Bellotti--Castillo 공개 원고 또는 다른 fully numerical pointwise PNT가 나타나는지
   source watch를 유지한다.
2. 현재 averaged density를 단순 비음수 적분하지 않고 smoothing·hybrid minimum·
   cancellation을 보존하는 PAP transfer가 가능한지 작은 proof-design 감사를 한다.

두 번째도 먼저 기호 구조와 coefficient gate를 통과해야 한다. 그 전망이 없는데 사용자
CPU로 소수 범위를 더 계산하는 것은 (X_{\rm cert}) 증명 병목을 줄이지 않는다.

## 10. Lean과 계산 증거 경계

Python은 식 (74.11)--(74.13), source range와 단조 진단을 100자리로 재계산한다.
Lean은 외부 analytic theorem을 axiom으로 넣지 않고 다음 유한 대수만 검사한다.

- 식 (74.11)의 exact rational identities,
- 식 (74.15)의 integer exponent gate,
- 식 (74.18)과 (1/210000<4/5).

Ramaré·Thorner--Zaman·Friedlander--Iwaniec 등의 analytic theorem 자체는
`SOURCE_THEOREM_UNFORMALIZED`로 남는다. `sorry`, `admit`, project-local `axiom`은 쓰지 않는다.

## 11. 참고문헌

- P. X. Gallagher, *A large sieve density estimate near \(\sigma=1\)*,
  Invent. Math. 11 (1970), 329--339, DOI
  [10.1007/BF01403187](https://doi.org/10.1007/BF01403187).
- H. Maier, *Chains of Large Gaps between Consecutive Primes*,
  Adv. Math. 39 (1981), 257--269, DOI
  [10.1016/0001-8708(81)90003-7](https://doi.org/10.1016/0001-8708(81)90003-7).
- K. S. McCurley, *Explicit Zero-Free Regions for Dirichlet L-Functions*,
  J. Number Theory 19 (1984), 7--32, DOI
  [10.1016/0022-314X(84)90089-1](https://doi.org/10.1016/0022-314X(84)90089-1).
- O. Ramaré, *An explicit density estimate for Dirichlet L-series*,
  Math. Comp. 85 (2016), 325--356, DOI
  [10.1090/mcom/2991](https://doi.org/10.1090/mcom/2991).
- J. Thorner and A. Zaman, *An explicit version of Bombieri's log-free density estimate and
  Sárközy's theorem for shifted primes*, Forum Math. 36 (2024), 1059--1080,
  arXiv [2208.11123](https://arxiv.org/abs/2208.11123), DOI
  [10.1515/forum-2023-0091](https://doi.org/10.1515/forum-2023-0091).
- J. Thorner and A. Zaman, *Refinements to the prime number theorem for arithmetic progressions*,
  Math. Z. 306 (2024), Paper 54, arXiv
  [2108.10878](https://arxiv.org/abs/2108.10878), DOI
  [10.1007/s00209-023-03414-3](https://doi.org/10.1007/s00209-023-03414-3).
- I. Kaneko and J. Thorner, *Highly Uniform Prime Number Theorems*,
  Ann. Inst. Fourier (2025), arXiv [2203.09515](https://arxiv.org/abs/2203.09515),
  DOI [10.5802/aif.3698](https://doi.org/10.5802/aif.3698).
- J. Thorner and Z. Zhang, *A new bound on the relative error in the Chebotarev density theorem*,
  Forum Math. (online 2026), arXiv [2412.01802](https://arxiv.org/abs/2412.01802),
  DOI [10.1515/forum-2025-0281](https://doi.org/10.1515/forum-2025-0281).
- J. B. Friedlander and H. Iwaniec, *Sifting for small primes from an arithmetic progression*,
  Sci. China Math. 66 (2023), 2715--2730, arXiv
  [2303.06122](https://arxiv.org/abs/2303.06122), DOI
  [10.1007/s11425-022-2123-2](https://doi.org/10.1007/s11425-022-2123-2).
- B. Chen, V. Gupta and Y. C. Li, *Large value estimates for Dirichlet polynomials, and the
  density of zeros of Dirichlet's L-functions*, unverified arXiv v2
  [2507.08296](https://arxiv.org/abs/2507.08296).
- C. Bellotti and C. Castillo, *An explicit log-free zero density estimate for Dirichlet
  L-functions*, in preparation; status source:
  [Cruz Castillo research page](https://ccasti30.web.illinois.edu/research.html).
