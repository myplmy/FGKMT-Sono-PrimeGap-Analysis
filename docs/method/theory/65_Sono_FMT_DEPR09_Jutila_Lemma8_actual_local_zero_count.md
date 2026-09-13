# Sono/FMT DEP-R09 Jutila Lemma 8 actual 국소 영점 개수

- 작성일: 2026-09-13 KST
- 단계: **DEP-R09 / JL8 ACTUAL NEAR-ONE LOCAL ZERO COUNT**
- 선행 정본: [Theory 64](64_Sono_FMT_DEPR09_Jutila_Lemma6_actual_common_budget.md)
- 기계 원장: [Jutila Lemma 8 local count v1](data/Sono_FMT_DEPR09_Jutila_Lemma8_local_count_v1.json)
- 판정: **JL8-ACTUAL-NEAR-ONE ACTUAL_APPLICATION_EXPLICIT_SOURCE_REPLACEMENT /**
  **PRINTED GENERAL JL8·TERMINAL DENSITY OPEN**
- 비목적: Jutila Lemma 8의 모든 \(\alpha\) 범위 재증명, Jutila Theorem 1-prime 종단
  multiplier 확정, PAP-11·DEP-R09·fixed \(2\times10^{-17}\) 또는 \(X_{\rm cert}\) 인증

## 1. 결론

Jutila 1977 Lemma 8은 필요한 국소 정사각형의 영점 수를
`≪ (1-alpha) log(q(T+1))+1`로 적지만 multiplier를 주지 않는다. Prachar·Turan·Gallagher
계보도 같은 구조만 확인하고 exact 숫자는 주지 않는다. 그러나 McCurley 1984의 명시적
로그미분 공식과 Lemmas 1--4를 직접 조합하면 actual near-one branch에 충분한 다음
명제를 얻는다.

비주인(nonprincipal) Dirichlet character \(\chi\pmod q\)와

\[
 0<r\le\frac1{21}
\tag{65.1}
\]

에 대해, 중복도를 포함하여

\[
 \boxed{
 N_{\square}(r,t_0,\chi)
 :=\#\{\rho=\beta+i\gamma:
       1-r\le\beta\le1,\ |\gamma-t_0|\le r/2\}
 <3+r\log\!\bigl(q(1+|t_0|)\bigr).}
\tag{65.2}
\]

따라서 `JL8-ACTUAL-NEAR-ONE`은
`ACTUAL_APPLICATION_EXPLICIT_SOURCE_REPLACEMENT`로 닫힌다. 이 값은 최소 multiplier가
아니라 원문에서 재현하기 쉬운 보수적 상계다.

> 쉬운 설명: 작은 상자 하나에 영점이 몇 개까지 들어갈 수 있는지 원 논문은 “어떤
> 상수배 이하”라고만 말했다. McCurley의 숫자가 적힌 공식들을 다시 조립하니, 우리가
> 실제로 쓰는 얇은 상자에서는 `3 + 상자폭 × 로그크기`보다 적다는 명시식이 나왔다.

이 진전만으로 전체 density estimate가 끝나지는 않는다. Jutila Lemma 7과 식 (3.6)의
모든 계수, finite 로그 보정 및 Theorem 1-prime 종단 합성이 남으므로 PAP-11, DEP-R09,
fixed \(2\times10^{-17}\), numerical \(X_{\rm cert}\)는 계속 OPEN이다.

## 2. 원문과 판독 방식

| source | 확인 위치 | 판독 방식 | 판정·역할 |
|---|---|---|---|
| Jutila 1977 | printed pp.51--52, Lemma 8·(3.1) | native text 18 bytes로 비어 OCR locator 뒤 원페이지 대조 | target square, \(\Delta\)-strip, even/odd system |
| McCurley 1984 | printed pp.10--16, (5), Lemmas 1--4, (13) | native text 우선, 수식·부등호를 렌더링 페이지 대조 | actual explicit replacement의 주 source |
| Turan 1961 | printed p.166, (1.2.2) | native text 수식이 깨져 원페이지 대조 | 같은 square 구조; `about 1/2`는 exact 값으로 미채택 |
| Gallagher 1970 | printed p.333 | native text 우선, 원페이지 대조 | 반지름 \(r\) 원판의 `≪ r log T`; multiplier 숨음 |
| Bennett et al. 2021 | Theorem 1.1 | native text·원페이지 대조 | explicit global \(N(T,\chi)\); local drop-in 아님 |

Prachar, *Primzahlverteilung* (1957) p.331은 Jutila·Turan·Gallagher가 공통으로 인용한다.
공개 Internet Archive 항목은 access-restricted라 해당 페이지의 exact scan을 확보하지
못했다. 공개 Google Books snippet은 disk-covering 계보를 확인하지만 Lemma 2.1의 exact
multiplier를 노출하지 않았다. 아래 증명은 이 미확보 숫자를 임의로 채우지 않고, 저장소에
영구 보존된 `article/McCurley 1984.pdf`의 peer-reviewed 명시식으로 대체한다.

2026년 peer-reviewed Linnik-lemma 재진술도
\(N_\chi(r;s)\ll r\log(q(|t|+3))\) 형태에서 implied constant를 숨긴다. 반면 Bennett et
al.의 explicit global count를 두 높이에서 차분하면 양 끝의 absolute remainder 두 개가
남아 \(r\)이 작을 때 \(r\log qT\) 이득이 사라진다. 따라서 둘 다 식 (65.2)의 직접
대체 source로 사용하지 않았다.

## 3. McCurley의 명시식

\(\chi^*\)가 conductor \(k\)인 primitive nonprincipal character라 하자. McCurley의
표기를 따라

\[
 \sigma=1+r,\qquad
 \sigma_1=\frac{1+\sqrt{1+4\sigma^2}}2,\qquad
 \kappa=\frac{5-\sqrt5}{10}<\frac3{10},
\tag{65.3}
\]

\[
 F(s,z)=\Re\!\left(\frac1{s-z}+\frac1{s-1+\bar z}\right),
\qquad
 f(t,\chi^*)=\Re\!\left{
 \frac1{\sqrt5}\frac{L'}L(\sigma_1+it,\chi^*)
 -\frac{L'}L(\sigma+it,\chi^*)\right}.
\tag{65.4}
\]

McCurley 식 (5)의 절대수렴 Dirichlet series를 펼치면

\[
 f(t,\chi^*)=
 \sum_{n\ge2}\Lambda(n)
 \left(n^{-\sigma}-\frac1{\sqrt5}n^{-\sigma_1}\right)
 \Re\!\left(\chi^*(n)n^{-it}\right).
\tag{65.5}
\]

\(\sigma_1>\sigma\), \(1/\sqrt5<1\)이므로 괄호 안 coefficient는 양수다. 따라서
\(\chi_0\)를 modulus \(k\)의 principal character라 하면

\[
 f(t,\chi^*)\ge-f(0,\chi_0).
\tag{65.6}
\]

McCurley Lemma 3은 \(1<\sigma<1.15\)에서

\[
 f(0,\chi_0)<\frac1{\sigma-1}-0.8973-s(k)<\frac1r,
 \qquad s(k)\ge0,
\tag{65.7}
\]

를 준다. 식 (65.6)--(65.7)에서 \(-f(t,\chi^*)<1/r\)다. 별도의
\(-\zeta'/\zeta\) 추정이나 숨은 상수는 필요하지 않다.

McCurley 식 (13)과 Stechkin Lemma 4를 모든 local zero에 유지하면

\[
 \sum_{\rho}'\left{
 F(\sigma+it_0,\rho)
 -\frac1{\sqrt5}F(\sigma_1+it_0,\rho)\right}
 =\kappa\log\frac{k}{\pi}+G(t_0)-f(t_0,\chi^*).
\tag{65.8}
\]

여기서 \(\beta=1/2\)인 항만 반 가중치다. 식 (65.1)의 local zero는
\(\beta\ge1-r>1/2\)이므로 전부 가중치 1이다. McCurley Lemmas 1--2와 표의 반올림된
상계를 함께 쓰고 음의 \(t_0\)는 공액 대칭으로 환원하면 모든 실수 \(t_0\)에서

\[
 G(t_0)<\kappa\log\max(1,|t_0|)+\frac{1959}{5000}.
\tag{65.9}
\]

따라서 \(k\le q\)와 \(\pi>1\)을 사용해 식 (65.8)의 오른쪽을

\[
 \sum_{\rho}'(\cdots)
 <\frac1r+\kappa\log\!\bigl(q(1+|t_0|)\bigr)
   +\frac{1959}{5000}
\tag{65.10}
\]

으로 상계할 수 있다.

## 4. local kernel의 명시 하한

local zero에 대해

\[
 a:=\sigma-\beta\in[r,2r],\qquad
 y:=t_0-\gamma,\quad |y|\le r/2.
\tag{65.11}
\]

\((a-2r)(8a-r)\le0\)을 정리하면

\[
 \frac{a}{a^2+y^2}\ge\frac8{17r}.
\tag{65.12}
\]

또 \(\sigma_1>3/2\), \(1-r\le\beta\le1\)에서

\[
 0<F(\sigma_1+it_0,\rho)
 \le\frac1{\sigma_1-\beta}
    +\frac1{\sigma_1-1+\beta}<3.
\tag{65.13}
\]

\(r\le1/21\), \(1/\sqrt5<1/2\)와 식 (65.12)--(65.13)을 합치면

\[
 \begin{aligned}
 F(\sigma+it_0,\rho)-\frac1{\sqrt5}F(\sigma_1+it_0,\rho)
 &>\frac1r\left(\frac8{17}-\frac32r\right)\\
 &\ge\frac3{8r},
 \end{aligned}
 \qquad
 \frac8{17}-\frac3{42}-\frac38=\frac{23}{952}>0.
\tag{65.14}
\]

식 (65.10)과 local zero마다의 식 (65.14)에서

\[
 \frac3{8r}N_{\square}
 <\frac1r+\kappa L+\frac{1959}{5000},
 \qquad L=\log\!\bigl(q(1+|t_0|)\bigr).
\tag{65.15}
\]

즉

\[
 N_{\square}
 <\frac83+\frac{8\kappa}{3}rL
   +\frac83\frac{1959}{5000}r
 <3+rL.
\tag{65.16}
\]

마지막 strict inequality는 \(8\kappa/3<4/5<1\)과

\[
 3-\frac83-\frac83\frac{1959}{5000}\frac1{21}>0
\tag{65.17}
\]

에서 나온다. 이것이 식 (65.2)다.

## 5. imprimitive character와 Jutila strip으로의 전달

비주인(nonprincipal) \(\chi\pmod q\)가 primitive \(\chi^*\pmod k\)에서 유도되면

\[
 L(s,\chi)=L(s,\chi^*)
 \prod_{\substack{p\mid q\\p\nmid k}}
 (1-\chi^*(p)p^{-s}).
\tag{65.18}
\]

추가 Euler factor의 영점은 \(\Re s=0\)에만 있다. 따라서
\(\beta\ge1-r>0\)인 actual square의 영점은 \(L(s,\chi^*)\)의 영점과 중복도까지
같다. \(k\le q\)이므로 식 (65.2)는 원 modulus \(q\)로 안전하게 올라간다. principal
character의 zeta zero는 Jutila p.51에서 별도 known-results branch로 제외되므로 이번
replacement의 대상이 아니다. 식 (65.2)의 닫힌 경계 \(\beta=1\)은 비주인 Dirichlet
\(L\)-함수의 고전적 \(\Re s=1\) 비소멸 정리로 영점을 추가하지 않는다. 이 analytic
source 사실도 Lean local axiom으로 바꾸지 않는다.

이제 \(D=qT\), \(\Delta=1/\log D\), \(\delta=1-\alpha\)이고

\[
 0<\theta\le\frac1{21},\qquad
 0<\delta\le\theta,\qquad
 \log D\ge\theta^{-2},\qquad
 r:=\max(\delta,\Delta)
\tag{65.19}
\]

라 하자. 그러면 \(\Delta\le\theta^2\le\theta\)라서 \(r\le\theta\le1/21\)이다.
Jutila의 높이 \(\Delta\)인 각 clipped strip은 그 중점을 중심으로 하는 radius \(r\)
square 하나에 포함된다. 또 \(|t_0|\le T\), \(T\ge1\)이면

\[
 \log\!\bigl(q(1+|t_0|)\bigr)
 \le\log(q(1+T))\le\log(2D).
\tag{65.20}
\]

각 nonempty `(character, strip)`에서 영점 하나를 고르고 strip index의 짝·홀을 나눈 뒤,
더 큰 well-spaced system의 크기를 \(J\)라 하면 nonempty cell 수는 \(2J\) 이하이다.
따라서 nonprincipal part에 대해

\[
 \boxed{
 N_{\rm nonprin}(\alpha,T,q)
 \le2J\{3+r\log(2D)\}.}
\tag{65.21}
\]

이는 Jutila p.52의 “Lemma 8에 의해 \(J\)만 추정하면 충분하다”를 actual branch에서
숫자로 바꾼 식이다. 다음 종단 합성에서는 이 factor를 버리거나 multiplier 1로 바꾸지
말고 그대로 흡수해야 한다.

## 6. source 비교의 비판적 판정

- **Turan의 `about 1/2`를 숫자 \(1/2\)로 쓰지 않았다.** 문장은 유효상수의 규모를
  알려 주지만 directed numerical certificate가 아니다.
- **Bennett et al. global count를 억지로 차분하지 않았다.** explicit하다는 사실과
  필요한 local scaling을 보존한다는 것은 다른 조건이다.
- **Prachar p.331 미확보가 이번 actual replacement를 막지 않는다.** 최종 채택 경로는
  permanent local PDF인 McCurley의 인쇄식에서 독립적으로 재구성된다.
- **McCurley의 zero-free region 결론만 가져온 것이 아니다.** 그 proof 중 explicit
  identity·gamma table·principal bound·Stechkin positivity를 local count 목적에 맞게
  다시 합성했다.
- **Lean 경계:** source analytic identity, Dirichlet series와 zero sum을 project-local
  axiom으로 옮기지 않는다. 식 (65.12)--(65.17), (65.19)--(65.21)의 유한 실수대수만
  source premise를 받는 형태로 커널 검증한다.

## 7. 기계검증과 증거 수준

- evaluator:
  [dep_r09_jutila_jl8_local_count.py](../../../source/dep_r09_jutila_jl8_local_count.py)
- fail-closed tests:
  [test_dep_r09_jutila_jl8_local_count.py](../../../tests/test_dep_r09_jutila_jl8_local_count.py)
- machine ledger:
  [Sono_FMT_DEPR09_Jutila_Lemma8_local_count_v1.json](data/Sono_FMT_DEPR09_Jutila_Lemma8_local_count_v1.json)
- numerical dense-grid check는 식 (65.14)의 경계·내부값을 점검하는 회귀검사일 뿐 증명이
  아니다. 증명은 위 유리 부등식이고, dependency-critical 유한 대수는 Lean이 검사한다.
- `sorry`, `admit`, project-local `axiom`은 사용하지 않는다.
- Theory 65 뒤 전수 inventory는 theory 문서 66개, display 1,163식이고, 이 batch에서
  dependency-critical finite algebra 10식이 `KERNEL_PASS` 또는
  `CONDITIONAL_KERNEL_PASS`로 연결됐다. 전체 declaration은 161개, 금지 proof escape는 0건이다.

## 8. 상태와 다음 gate

| ID | 이번 판정 | 남은 일 |
|---|---|---|
| `JL5` | `EXPLICIT_SOURCE_REPLACEMENT` | Theory 61 유지 |
| `JL6-ACTUAL` | `ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT` | Theory 64 유지 |
| `JL8-ACTUAL-NEAR-ONE` | `ACTUAL_APPLICATION_EXPLICIT_SOURCE_REPLACEMENT` | 식 (65.21)을 종단 budget에 보존 |
| `JL8-PRINTED-GENERAL` | `OPEN` | unrestricted \(\alpha\)·모든 source 범위는 미복원 |
| `JL7 / (3.6) TERMINAL` | `OPEN` | finite multiplier·log correction·density exponent 합성 |
| `PAP-11 / DEP-R09` | `OPEN` | Jutila 종단 뒤 Gallagher/Maier bridge까지 필요 |
| fixed \(2\times10^{-17}\) / \(X_{\rm cert}\) | `OPEN` | calculator 제작 금지 유지 |

다음 우선순위는 `JL7/(3.6)-TERMINAL`이다. 식 (65.21), Theory 64의 detector lower
bound와 Theory 60의 Barban--Vehov coefficient를 Jutila 식 (3.6)에 실제로 넣어, 남은
Halasz 합과 \(\log D\) factor가 얼마의 multiplier·cutoff를 요구하는지 분해한다.

## 9. 참고문헌

- M. Jutila, [*On Linnik's constant*](https://doi.org/10.7146/math.scand.a-11701),
  Math. Scand. 41 (1977), 45--62.
- K. S. McCurley,
  [*Explicit Zero-Free Regions for Dirichlet L-functions*](https://doi.org/10.1016/0022-314X(84)90089-1),
  J. Number Theory 19 (1984), 7--32.
- P. Turan, *On a Density Theorem of Yu. V. Linnik*, 1961, printed (1.2.2).
- P. X. Gallagher,
  [*A Large Sieve Density Estimate near sigma=1*](https://doi.org/10.1007/BF01403187),
  Invent. Math. 11 (1970), 329--339.
- M. A. Bennett, G. Martin, K. O'Bryant and A. Rechnitzer,
  [*Counting Zeros of Dirichlet L-Functions*](https://doi.org/10.1090/mcom/3599),
  Math. Comp. 90 (2021), 1455--1482; [arXiv:2005.02989](https://arxiv.org/abs/2005.02989).
