# Sono/FMT DEP-R09 explicit PNT-in-AP 대체자료 감사

- 작성일: 2026-09-13 KST
- 단계: `DEP-R09 REPLACEMENT-SOURCE AUDIT / COEFFICIENT CAPACITY GATE`
- 선행 정본: [Theory 57](57_Sono_FMT_DEPR09_Gallagher_Maier_McCurley_source_recovery.md)
- 기계 원장: [replacement source audit v1](data/Sono_FMT_DEPR09_explicit_PNT_AP_replacement_v1.json)
- 판정: `NO_DROP_IN_NUMERICAL_PAP_REPLACEMENT_FOUND / FIXED_COEFFICIENT_PATH_OPEN`
- 비목적: 저자에게 문의하기, Sono 정리 전체의 반증, 새 계수 채택, numerical
  \(X_{\mathrm{cert}}\) 계산

## 1. 결론부터

2026-09-13 현재 공개된 Sono의 최신 arXiv v4와 journal 판에는 Theory 57에서 발견한
Section 5 정규화 문제가 그대로 남아 있다. 공개 arXiv record와 journal article page에서
별도 correction 또는 erratum도 식별하지 못했다. 이는 **공개적으로 찾은 자료의 범위**에
한정한 판정이며, 저자에게 비공개 설명이 있는지는 확인하지 않았다.

현대 명시적 PNT-in-AP·zero-density·Deuring--Heilbronn 결과도 검토했지만, 다음 계약을
그대로 충족하는 drop-in theorem은 찾지 못했다.

\[
 \pi(u;q,a)\ge C_{\rm PAP}\frac{u}{\varphi(q)\log u},
 \qquad q\le u^{1/160},
 \qquad C_{\rm PAP}=1-e^{-2},
\tag{58.1}
\]

여기서 한 exceptional modulus의 제외, 모든 필요한 reduced residue, prime-power와 endpoint
보정, 그리고 하나의 공통 numerical cutoff까지 포함해야 한다.

가장 중요한 새 수치 판정은 다음이다.

1. 현재 Sono downstream 계수식을 그대로 두면 \(D=160\)에서 필요한 최소 PAP 계수는
   \(0.8638312615226712472\ldots\)다.
2. 따라서 허용되는 총 상대오차는 \(0.1361687384773287528\ldots\)이고, Sono 인쇄값의
   \(e^{-2}\)를 제외하고 남는 추가 오차 여유는
   \(0.0008334552407160609\ldots\)뿐이다.
3. PAP 계수를 낙관적으로 1까지 올려도, 같은 downstream 식에서 fixed
   \(2\times10^{-17}\)을 유지하는 최대 정수 \(D\)는 186이다. \(D=187\)부터 실패한다.

> 쉬운 설명: 새 정리가 단순히 “효과적으로 계산 가능하다”고 말하는 것만으로는 부족하다.
> 현재 최종계수에는 여유가 약 0.2%밖에 없어서, 중간 정리의 숨은 배수와 작은 보정도
> 실제 숫자로 알아야 한다. 더 느슨한 정리를 가져와 \(D\)를 크게 만들면 마지막 계수는
> 빠르게 작아진다.

`DEP-R09`, `PAP-11`, fixed \(2\times10^{-17}\), \(X_{\mathrm{cert}}\)는 계속 OPEN이다.

## 2. 이번 감사의 actual target

Sono Assumption 3.2의 asymptotic 표기를 finite certificate로 바꾸려면 최소한 다음 interface가
필요하다. \(B_0\)는 허용되는 하나의 exceptional prime/modulus 정보를 대표한다.

\[
\begin{aligned}
&u\ge u_{\rm PAP},\quad q\le u^{1/D_{\rm PAP}},\quad (a,q)=1,
   \quad B_0\nmid q,\\
&\pi(u;q,a)\ge
 \left(1-\eta_{\rm pr}-\eta_{\rm np}-\eta_{\psi\to\pi}\right)
 \frac{u}{\varphi(q)\log u}.
\end{aligned}
\tag{58.2}
\]

고정 목표에서는

\[
D_{\rm PAP}=160,
\qquad
1-\eta_{\rm pr}-\eta_{\rm np}-\eta_{\psi\to\pi}
\ge C_{\rm PAP,min}(160)
\tag{58.3}
\]

이어야 한다. 다음은 대체할 수 없다.

- 평균 modulus 합인 Bombieri--Vinogradov 명제를 각 modulus의 pointwise lower bound로 사용
- \(\psi\) 또는 \(\theta\) 상계를 prime count \(\pi\)의 lower bound로 보정 없이 사용
- “effectively computable” implied constant를 1로 사용
- fixed-modulus 정리를 \(q=u^{1/160}\)까지 uniform하다고 사용
- exceptional zero를 제거하지 않고 main term을 1로 사용

## 3. Sono 공식 공개판과 correction 상태

| 항목 | 확인 결과 |
|---|---|
| arXiv | `2404.06951v4`, last revised 2024-06-05 |
| journal | DOI `10.4418/2025.80.2.2`, 2025 publication |
| 관련 위치 | Assumption 3.2, Section 5, equations (5.2)--(5.7) |
| 공개 correction/erratum | 2026-09-13 검색에서 식별되지 않음 |
| 저자 문의 | 수행하지 않음 |

최신 arXiv v4와 journal PDF 모두 다음 연결을 인쇄한다.

\[
c_1=3c_{\rm ZFR},\qquad
a=\frac{3}{10}c_{\rm ZFR}=\frac1{80},\qquad
D_{\rm PAP}=160,\qquad C_{\rm PAP}=1-e^{-2}.
\tag{58.4}
\]

Theory 57에서 확인했듯이 Proposition 5.3의 분모
\(\log(Q(1+|t|))\)에서 Gallagher의 \(\log T\) 정규화로 직접 옮길 때 안전한 방향은
\(c_{\rm ZFR}/3\)이다. 이번 version 감사는 그 문제가 후속 공개판에서 교정되지 않았음을
확인한 것이지, Sono 정리 전체가 거짓임을 증명한 것이 아니다.

## 4. 기존 explicit 후보의 적용성 재검토

### 4.1 Bennett--Martin--O'Bryant--Rechnitzer 2018

Theorem 1.1은 모든 \(q\ge3\)에 대해 explicit bound를 주지만, \(q>10^5\)에서 시작점은

\[
x_0(q)=\exp\!\left(0.03\sqrt q\,(\log q)^3\right)
\tag{58.5}
\]

이다. Corollary 1.8의 더 단순한 uniform 식도
\(x\ge\exp(8\sqrt q(\log q)^3)\)를 요구한다. \(q=x^{1/160}\)을 넣으면
우변의 로그가 \(e^{(\log x)/320}\)을 포함하므로 충분히 큰 \(x\)에서 \(\log x\)보다
훨씬 빨리 증가한다. 따라서 이 theorem은 고정되거나 작은 \(q\)에는 강하지만
PAP의 전체 polynomial modulus 경계를 덮지 않는다.

판정: `EXPLICIT_BUT_NOT_UNIFORM_ON_Q_EQ_U_POW_1_OVER_160`.

### 4.2 Bordignon 2021

Theorems 2--3은 \(q\le(\log x)^{\alpha_1}\) 범위이고, 완전한 explicit exceptional-zero
제거를 쓰는 Theorem 3은 \(\alpha_1<2\)를 요구한다. 이는 \(q\le x^{1/160}\)보다
훨씬 좁다.

판정: `POLYLOG_MODULUS_ONLY`.

### 4.3 Yamada 2014

주요 결과는 exceptional modulus를 제외한 Bombieri--Vinogradov형 **modulus 평균합**이다.
FMT/Sono PAP가 요구하는 각 \(q,a\)의 pointwise lower bound와 논리형이 다르다.

판정: `AVERAGED_MODULI_NOT_POINTWISE_PAP`.

### 4.4 Kadiri의 explicit zero-free region

Theorem 1.1의 \(R=5.60\) zero-free region은 \(3\le q\le400000\)이고, 큰 \(q\)는
후속연구 대상으로 명시돼 있다. 이는 유한 small-modulus branch에는 유용하지만
무한히 증가하는 \(q\le u^{1/160}\) 전체를 대신하지 않는다.

판정: `FINITE_MODULUS_COMPONENT_ONLY`.

## 5. 현대 후보 1: Thorner--Zaman uniform PNT-in-AP

Thorner--Zaman의 Theorem 1.1은 no-exception case에서 \(\theta=7/12\)이고, \(h=x\)인
경우 \(q=x^{1/160}\)에서도 main-term 크기 조건에는 큰 여유가 있다. 또한 exceptional
zero가 있으면 그 효과를 \(\lambda\)라는 secondary main term으로 보존한다.

그러나 결론의 implied constant와 decay constant \(c_1(\varepsilon)\)는
`effectively computable`이라고만 적혀 있고 수치가 인쇄되지 않았다. fixed \(D=160\)에서는
오차가 대략

\[
K_{\varepsilon}\exp(-160c_1(\varepsilon))
\tag{58.6}
\]

형태로 남으므로, \(K_{\varepsilon}\)와 \(c_1(\varepsilon)\)를 실제 숫자로 복원하기 전에는
식 (58.3)을 검사할 수 없다. exceptional branch에서는 \(\lambda\)를 PAP의 uniform
one-sided constant와 연결하는 별도 finite lower bound도 필요하다.

판정: `BEST_STRUCTURAL_REPLACEMENT_CANDIDATE / NUMERICAL_CONSTANTS_NOT_PRINTED`.

## 6. 현대 후보 2: fully explicit log-free density

Thorner--Zaman의 explicit Bombieri density theorem은 \(Q\ge3\), \(\sigma\ge39/40\)에서

\[
N(\sigma,Q)\le10^{88}\left(10^{421}Q^{99}\right)^{1-\sigma},
\tag{58.7}
\]

\[
N^*(\sigma,Q)\le10^{93}\min\{1,(1-\beta_1)\log Q\}
\left(10^{466}Q^{170}\right)^{1-\sigma}
\tag{58.8}
\]

를 준다. Corollary 6.1은 모든 \(\sigma\ge0\)로 확장하면서 exponent를 각각 127과
198로 키운다.

이 결과의 장점은 multiplier와 범위가 실제 숫자라는 것이다. 단점은 다음과 같다.

1. density estimate이지 PAP pointwise lower bound가 아니다.
2. \(10^{88},10^{421},10^{93},10^{466}\)의 비용을 prime-sum transfer에서 흡수해야 한다.
3. exceptional branch의 exponent 198은 현재 fixed-coefficient capacity와 긴장한다.

특히 “density exponent \(c\)를 쓰면 반드시 \(D=c\)”라는 정리는 없다. transfer 설계에 따라
관계가 달라진다. 다만 어떤 구성에서 \(D\ge198\)이 필요해진다면, 아래 §8의 capacity gate에
의해 **현재 downstream 식 그대로는** fixed \(2\times10^{-17}\)을 유지할 수 없다.

판정: `FULLY_EXPLICIT_DENSITY_COMPONENT / NEW_TRANSFER_REQUIRED`.

## 7. 현대 후보 3: explicit Deuring--Heilbronn

Benli--Goel--Twiss--Zaman Corollary 1.1은 \(q>400000\), \(T\ge4\)에서 possible
Landau--Siegel zero가 있을 때 다른 zero의 반발을

\[
c_1=10,\quad c_2=1,\quad c_3=107,\quad c_4=1/16
\tag{58.9}
\]

으로 완전 명시한다. 이는 Theory 57의 exceptional branch를 개선할 중요한 구성요소다.
하지만 이 corollary만으로는 prime count의 pointwise lower bound, density-to-prime-sum
transfer, \(\psi\to\pi\), 공통 cutoff가 나오지 않는다. Corollary 1.2의 더 좋은 asymptotic
상수는 cutoff \(C(\varepsilon)\)가 ineffective이므로 numerical certificate에 사용할 수 없다.

판정: `EXPLICIT_EXCEPTIONAL_BRANCH_COMPONENT / NOT_A_PAP_THEOREM`.

## 8. fixed \(2\times10^{-17}\)의 수치 capacity gate

Sono Theorem 3.6에서 이 감사와 직접 관계있는 부분을 함수

\[
\widehat c(C,D,M)=
\frac{C^2\,(1/3)(1/4)e^{4\gamma}}
{737280000\log5\,C_{\rm UB}\,M(1+1/D)^4
 (25C_{\rm UB}+20e^\gamma M)},
\qquad C_{\rm UB}=8e^{2\gamma}
\tag{58.10}
\]

로 둔다. 현재 package는 \(M=D\)를 사용한다.

### 8.1 \(D=160\)에서 필요한 최소 PAP 계수

\[
C_{\min}(160)
=\sqrt{\frac{2\times10^{-17}}{\widehat c(1,160,160)}}
=0.863831261522671247201665369608\ldots
\tag{58.11}
\]

따라서 총 상대오차 budget은

\[
1-C_{\min}(160)
=0.136168738477328752798334630392\ldots
\tag{58.12}
\]

이고, Sono 인쇄 main error \(e^{-2}\)를 먼저 사용하면 추가로 남는 양은

\[
1-C_{\min}(160)-e^{-2}
=0.000833455240716060904335135419\ldots
\tag{58.13}
\]

이다. 이는 total coefficient의 상대 0.0965% 정도의 PAP headroom이다. finite
principal·nonprincipal·prime-power 보정이 이 안에 들어가야 한다는 뜻이지, 각 보정이
자동으로 이보다 작다는 뜻은 아니다.

### 8.2 \(D\)의 절대적인 낙관 상한

\(C=1\), \(M=D\)라는 가장 낙관적인 값을 넣어도

\[
\widehat c(1,186,186)=2.01845486839327\ldots\times10^{-17},
\tag{58.14}
\]

\[
\widehat c(1,187,187)=1.99808701863747\ldots\times10^{-17}.
\tag{58.15}
\]

그러므로 현재 downstream 식의 fixed-coefficient capacity는

\[
\boxed{D\le186}
\tag{58.16}
\]

이다. 이는 새 PAP 정리가 \(D=186\)에서 존재한다는 뜻이 아니라, \(D\ge187\)을 요구하는
경로는 downstream 상수도 함께 개선해야 한다는 **필요조건 감사**다.

## 9. 두 repair branch

### Branch S — sharp fixed-coefficient 주축

- 목표: \(D=160\) 유지
- 필요한 것: Gallagher--Jutila--Huxley 또는 Thorner--Zaman transfer의 실제
  multiplier, decay constant, exceptional branch와 cutoff
- 통과조건: 식 (58.2)의 총 coefficient가 식 (58.11) 이상
- 장점: 현재 fixed \(2\times10^{-17}\) 목표와 호환 가능
- 위험: 매우 작은 finite slack 때문에 정량 재증명이 길어질 수 있음

### Branch E — fully explicit 보수 경로

- 입력 후보: explicit 127/198 density와 explicit Deuring--Heilbronn
- 필요한 것: 새로운 pointwise PNT transfer와 공통 cutoff
- 장점: 숨은 상수 대신 인쇄된 큰 숫자에서 출발
- 위험: \(D\)나 multiplier 비용이 커져 fixed coefficient를 잃을 가능성이 높음
- 현재 역할: 독립 cross-check 또는 더 작은 인증계수 후보; 주 연구목표를 자동 변경하지 않음

현재 권장은 Branch S를 먼저 진행하고, Branch E는 source component를 잃지 않도록 병렬 원장에
보존하는 것이다.

## 10. 다음 최소 proof obligations

| ID | 의무 | 현재 상태 | 닫힘 조건 |
|---|---|---|---|
| R09-RS01 | 최신 공개 Sono correction 상태 | `PUBLIC_SEARCH_COMPLETE_NO_CORRECTION_IDENTIFIED` | 저자 답변은 별도 외부행동 |
| R09-RS02 | sharp density multiplier | `OPEN` | 사용할 density theorem의 모든 숫자·범위 |
| R09-RS03 | density-to-prime-sum transfer | `HARD_BLOCKER` | pointwise, all residue, explicit \(K\)·cutoff |
| R09-RS04 | exceptional branch | `PARTIAL` | explicit DH를 actual \(B_0\) 제외와 합성 |
| R09-RS05 | principal term | `OPEN` | one-sided numerical rate와 endpoint |
| R09-RS06 | \(\psi\to\pi\) | `OPEN` | prime powers·partial summation·closed/open endpoint |
| R09-RS07 | common \(u_{\rm PAP}\) | `HARD_BLOCKER` | RS02--06의 최대 cutoff |
| R09-RS08 | coefficient capacity | `EXPLICIT_DIAGNOSTIC` | 실제 PAP package를 (58.10)에 대입 |

`R09-RS08`은 source analytic theorem을 닫지 않는다. 수치 대수만 검증된 gate다.

## 11. Lean·검증 경계

이번 단계에서는 외부 analytic theorem을 project-local axiom으로 옮기지 않는다. 새로 얻은
핵심 결과는 source applicability 판정과 고정밀 coefficient 계산이며, 이 둘은 각각 원문
감사와 Python exact/high-precision unittest로 검증한다.

식 (58.10)--(58.16)을 최종 proof DAG의 상위 결론에 실제로 사용할 때는 필요한 단조성·유리
budget을 `lean/FGKMTSono/TheoryVerification.lean`에 추가한다. 지금 즉시 형식화하지 않는 이유는
선택할 PAP source와 \(D,C\)가 아직 고정되지 않았기 때문이다. 이 보류는
`KERNEL_PASS`가 아니며 source theorem의 증명으로 기록하지 않는다.

## 12. 엄밀한 현재 판정

```text
latest public Sono Section 5 corrected     = NOT IDENTIFIED
drop-in explicit PAP at D=160              = NOT FOUND
modern structural PNT candidate            = FOUND, NUMERICAL CONSTANTS OPEN
fully explicit density / DH components     = FOUND, NEW TRANSFER REQUIRED
fixed-coefficient optimistic D capacity    = D <= 186
PAP-11 / DEP-R09                           = HARD_BLOCKER / OPEN
fixed 2e-17                                = NOT INDEPENDENTLY CERTIFIED
X_cert                                     = OPEN
actual prime computation                   = NOT RUN
```

## 13. 참고문헌

- Keiju Sono, [*An Explicit Lower Bound for Large Gaps Between Some Consecutive Primes*](https://doi.org/10.4418/2025.80.2.2), Section 5; [arXiv:2404.06951v4](https://arxiv.org/abs/2404.06951v4).
- Michael A. Bennett, Greg Martin, Kevin O'Bryant, Andrew Rechnitzer,
  [*Explicit Bounds for Primes in Arithmetic Progressions*](https://arxiv.org/abs/1802.00085),
  Theorem 1.1 and Corollary 1.8.
- Matteo Bordignon,
  [*Medium-sized values for the Prime Number Theorem for primes in arithmetic progressions*](https://arxiv.org/abs/2101.08610), Theorems 2--3.
- Tomohiro Yamada,
  [*Explicit formulae for primes in arithmetic progressions, II*](https://arxiv.org/abs/1309.5798), Theorems 1.1--1.2.
- Habiba Kadiri,
  [*Explicit zero-free regions for Dirichlet L-functions*](https://arxiv.org/abs/math/0510570), Theorem 1.1.
- Jesse Thorner and Asif Zaman,
  [*Refinements to the Prime Number Theorem for Arithmetic Progressions*](https://doi.org/10.1007/s00209-023-03414-3), Theorems 1.1, 2.1, 2.3.
- Jesse Thorner and Asif Zaman,
  [*An Explicit Version of Bombieri's Log-Free Density Estimate and Sárközy's Theorem for Shifted Primes*](https://doi.org/10.1515/forum-2023-0091), Theorem 1.2 and Corollary 6.1.
- Kübra Benli, Shivani Goel, Henry Twiss, Asif Zaman,
  [*Explicit Deuring--Heilbronn Phenomenon for Dirichlet L-functions*](https://doi.org/10.1090/proc/17450), Corollaries 1.1--1.2; [arXiv:2410.06082v3](https://arxiv.org/abs/2410.06082v3).
