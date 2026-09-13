# Sono/FMT DEP-R09 Jutila \(C_J\) loss tree 구조 감사

- 작성일: 2026-09-14 KST
- 단계: **DEP-R09 / JUTILA TERMINAL COEFFICIENT LOSS TREE**
- 선행 정본: [Theory 72](72_Sono_FMT_DEPR09_Gallagher_Maier_PAP_density_integral_split.md)
- 기계 원장: [C_J loss tree v1](data/Sono_FMT_DEPR09_CJ_loss_tree_v1.json)
- 판정: **같은 source 안의 finite-safe 개선은 약 343배 가능하지만,**
  **\(d\le186\) PAP gate에는 여전히 약 \(4.62\times10^{11}\)배 부족**
- 비목적: 모든 Jutila형 증명의 불가능성 증명, 새 zero-density theorem 증명,
  `PAP-11`·`DEP-R09`·fixed \(2\times10^{-17}\) 또는 numerical
  \(X_{\rm cert}\) 인증, actual prime 계산

## 1. 결론

Theory 70--72에서 사용한 한 parity selected-system coefficient는

\[
 C_J(\theta)=\frac{884000}{9(1-\theta)^2\theta^6}.
\tag{73.1}
\]

이번 감사는 이 숫자를 source 식까지 거꾸로 분해했다. 정확한 baseline loss tree는

\[
 \boxed{
 C_J=
 \underbrace{2}_{\text{half margin}}
 \underbrace{52}_{\text{residue}}
 \underbrace{5}_{\text{denominator}}
 \underbrace{\frac{34}{\theta^2}}_{\text{weighted sum}}
 \underbrace{\underline c_g^{-2}}_{\text{detector}}
 \underbrace{(\theta^2/2)^{-1}}_{\text{area}},
 \qquad
 \underline c_g=\frac35(1-\theta)\theta .}
\tag{73.2}
\]

\(\theta=1/21\)에서 이는 exact하게

\[
 C_J=9{,}287{,}613{,}243{,}090
     =108{,}290\cdot21^6.
\tag{73.3}
\]

같은 analytic source를 바꾸지 않고 각 유한 상계를 다시 조이면 다음 endpoint-specific
coefficient를 얻는다.

\[
 \boxed{
 C_{J,{\rm tight}}
 =\frac{11503697604450072}{425315}
 =27047476821.7675\ldots .}
\tag{73.4}
\]

이는 baseline보다

\[
 \frac{C_J}{C_{J,{\rm tight}}}
 =\frac{2304222695775}{6710379548}
 =343.3818727081\ldots
\tag{73.5}
\]

배 작다. 유효한 개선이지만 \(d=186\)에서 Theory 72의 near budget
\(e^{-2}\)가 허용하는 값은

\[
 C_J\le0.0585042942822\ldots
\tag{73.6}
\]

뿐이다. 따라서 개선 뒤에도

\[
 \frac{C_{J,{\rm tight}}}{C_{J,{\rm cap}}}
 =4.62316094119\ldots\times10^{11}
\tag{73.7}
\]

배 부족하다.

> **쉬운 설명:** 기존 계산서에는 여러 안전 여유가 겹쳐 있었다. 그것들을 실제로
> 고쳐 보니 비용이 약 343분의 1로 줄었다. 하지만 필요한 합격선까지는 다시 약
> 4,620억 배를 줄여야 한다. 나사를 조금 더 조이는 수준으로는 부족하고, 기계의 핵심
> 방식인 영점밀도 정리나 detector 구조를 바꿔야 한다.

## 2. source-first 대조

| source·정본 | 확인 위치 | 역할 | 판독·판정 |
|---|---|---|---|
| Jutila, *On Linnik's constant* | printed pp.52--53, (3.2)--(3.7) | detector, weighted terminal inequality, contour/residue 분리 | native text layer가 사실상 비어 OCR은 locator만 사용하고 rendered page 직접 대조 |
| Ramaré--Zuniga Alterman, *An \(L^2\)-bound for the Barban--Vehov weights* | Corollary 1.3, printed p.2 | weighted square의 exact source coefficient | native text 우선, rendered formula 대조 |
| Theory 66 | (66.3)--(66.14) | RZ 특수화, denominator, area | actual parameterized explicit |
| Theory 69 | (69.13)--(69.22) | Gamma row, Rankin harmonic, residue 52 | actual-input parameterized explicit |
| Theories 70--71 | (70.9)--(70.18), (71.20)--(71.23) | strict absorption과 averaged normalization | actual primitive nonprincipal near-one only |
| Theory 72 | (72.14)--(72.15) | PAP near integral과 coefficient capacity | pointwise PAP 전체는 OPEN |

별도의 선행 lemma를 찾지 않고 직접 고친 부분은 exponential quotient의 단조성,
finite log-ratio, rational factor composition뿐이다. 이들은 외부 analytic theorem을 새로
가정하는 것보다 직접 증명하는 편이 짧고 검증 가능하다. Ramaré--Zuniga의 Corollary 자체와
Jutila의 generalized Halász inequality는 원문 source premise로 남기며 Lean local axiom으로
바꾸지 않는다.

## 3. baseline에서 실제로 큰 항

\(\theta=1/21\)에서 식 (73.2)의 숫자는 다음과 같다.

| component | baseline 값 | 역할 |
|---|---:|---|
| half-margin | \(2\) | \(E\le A/2\) 뒤 \((A-E)^{-1}\) |
| residue | \(52\) | same-character height row와 diagonal \(r\)-sum |
| denominator | \(5\) | Lemma 7의 \(b_n^{-1}\) quotient |
| weighted square | \(14994\) | \(34/\theta^2\) |
| detector inverse square | \(21609/16=1350.5625\) | \(\underline c_g^{-2}\) |
| area inverse | \(882\) | \((\theta^2/2)^{-1}\) |

세 \(\theta^{-2}\) 항이 합쳐져 \(\theta^{-6}\)이 된다.

1. weighted mean-value가 \(\asymp\theta^{-2}\),
2. detector를 제곱한 뒤 나누어 \(\asymp\theta^{-2}\),
3. integration area로 나누어 \(\asymp\theta^{-2}\)

가 생긴다. 이 power structure는 숫자 52나 5를 조금 줄이는 것과 다른 종류의 손실이다.

## 4. denominator 5를 \(8/5\)로 줄이는 초등 lemma

식 (66.10)에서

\[
 W(n;M,N,x)=
 \frac{e^{-2n/x}}{e^{-n/N}-e^{-n/M}}.
\]

\(\rho=x/z_1\ge4\), \(t=n/x\in[1/\rho,1]\), \(N\ge x\),
\(M\le z_1\)이다. 분모 방향을 보존하면

\[
 W(n;M,N,x)
 \le f_\rho(t):=
 \frac{e^{-t}}{1-e^{-(\rho-1)t}}.
\tag{73.8}
\]

고정 \(\rho\)에서

\[
 \frac{d}{dt}\log f_\rho(t)
 =-1-\frac{(\rho-1)e^{-(\rho-1)t}}
              {1-e^{-(\rho-1)t}}<0.
\tag{73.9}
\]

따라서 최대는 \(t=1/\rho\)에서 생긴다. \(a=1/\rho\in(0,1/4]\)로 두고
미분하거나 양의 분모를 제거하면 이 endpoint 함수는 \(a\)가 증가할수록 감소한다.
그 결과

\[
 f_\rho(1/\rho)
 \le\lim_{a\downarrow0}
 \frac{e^{-a}}{1-e^{-1+a}}
 =\frac e{e-1}<\frac85.
\tag{73.10}
\]

마지막 부등식은 \(e>8/3\)에서 나온다. 그러므로 5 대신 \(8/5\)를 쓸 수 있다.

## 5. weighted square의 exact endpoint 계수

Theory 66 식 (66.4)를 \(\theta=1/21\)에 exact하게 대입하면

\[
 K_{\rm BV}(1/21)=\frac{921495783}{3500000}
 =263.2845094285\ldots .
\tag{73.11}
\]

또

\[
 \frac{\log x}{\log(z_2/z_1)}
 =33+42\frac{\log L}{L}.
\tag{73.12}
\]

\(L\ge441\)에서 \(\log L/L\)은 감소하고, \(441<e^8\)이므로

\[
 42\frac{\log L}{L}
 \le42\frac{\log441}{441}<\frac{16}{21}<1.
\tag{73.13}
\]

따라서 finite-safe upper는

\[
 C_{\rm WS}\le34K_{\rm BV}(1/21)
 =\frac{15665428311}{1750000}.
\tag{73.14}
\]

식 (73.10)과 합친 preterminal upper는

\[
 C_{{\rm pre},{\rm tight}}
 =\frac85 C_{\rm WS}
 =\frac{15665428311}{1093750}.
\tag{73.15}
\]

## 6. averaged residue 52를 \(710/171\)로 줄이기

Theory 69 식 (69.15)의 \(40/19\)를 3으로 올리지 않고 보존하면 height row는

\[
 C_{\rm row}(\theta)
 =\frac{280}{19}\theta^2+\frac{2800}{57}\theta.
\tag{73.16}
\]

\(0<\theta\le1/21\)에서 증가하므로

\[
 C_{\rm row}(\theta)\le C_{\rm row}(1/21)
 =\frac{2840}{1197}.
\tag{73.17}
\]

Theory 71의 averaged scale에서는 \(q\le Q\),
\(L=\log(Q^2T)\), \(T\ge1\)이므로

\[
 \frac{\log q}{L}\le\frac12.
\tag{73.18}
\]

Theory 69의 Rankin 계산을 이 더 강한 정보로 다시 쓰면

\[
 \frac{S_q(R)}{(\varphi(q)/q)L}
 \le e^{\theta+1/2}\left(1+\frac1L\right).
\tag{73.19}
\]

\(\theta\le1/21\), \(L\ge441\)에서 오른쪽은

\[
 e^{23/42}\frac{442}{441}<\frac74.
\tag{73.20}
\]

이다. Mathlib의 여섯 항 exponential remainder bound는

\[
 e^{23/42}\le
 \frac{5857471148617}{3387516733440},
\]

이고 \(442/441\)을 곱한 뒤 \(7/4\)와의 차이는 exact하게

\[
 \frac{12656895671803}{746947439723520}>0
\]

이다. 식 (73.17)--(73.20)을 합치면 residue upper는

\[
 \boxed{
 C_{{\rm RES},{\rm tight}}
 =\frac74\frac{2840}{1197}
 =\frac{710}{171}.}
\tag{73.21}
\]

이 개선은 fixed-modulus의 \(\log q\le L\)보다 강한 averaged-scale 관계를 쓰므로,
Theory 71과 그 뒤 PAP branch에만 적용한다.

## 7. exact area와 더 작은 absorption slack

\(\theta=1/21\), \(L\ge1\)에서 식 (70.6)은

\[
 A_{\rm int}
 \ge\theta^2\left(\frac12+7\theta\right)(1+12\theta)
 =\frac{55}{18522}.
\tag{73.22}
\]

detector lower \(\underline c_g=4/147\)는 그대로 둔다. 또 임의 정수
\(m>1\)에 대해 \(E\le A/m\)이면

\[
 A-E\ge\frac{m-1}{m}A,\qquad
 J\le\frac{m}{m-1}\frac BA Y.
\tag{73.23}
\]

이는

\[
 L\ge\frac1\gamma\log\left(
 \frac{36mC_{{\rm pre},{\rm tight}}\overline C_{\rm CL3}}
      {\underline c_g^2}\right)
\tag{73.24}
\]

로 달성할 수 있다. \(m=10^6\),
\(\overline C_{\rm CL3}=136224\), \(\gamma=29/5292\)에서 이 cutoff의
120-dps 진단값은

\[
 L\ge8394.0173339360\ldots .
\tag{73.25}
\]

이다. decimal은 directed interval certificate가 아니며, 엄밀한 충분조건은 식 (73.24)다.
식 (73.14)--(73.24)을 합치면 식 (73.4)가 나온다.

## 8. 각 개선의 크기

| 개선 항목 | 개선 배수 |
|---|---:|
| half-margin | \(999999/500000=1.999998\) |
| residue | \(4446/355=12.52394\ldots\) |
| denominator | \(25/8=3.125\) |
| weighted source specialization | \(514500000/307165261=1.67499\ldots\) |
| exact area | \(55/21=2.61904\ldots\) |
| detector rationalization | 이번 finite-safe package에서는 그대로 유지 |
| 전체 | \(343.3818727081\ldots\) |

actual detector \((1-\theta)(6/\pi^2)\theta\)를 직접 유지하면 detector 제곱에서 약
2.7%를 더 얻을 수 있지만, 식 (73.7)의 열한 자릿수 격차를 바꾸지 않는다.

## 9. 왜 contour 45408·Lemma 3·phase 36이 우선 개선 대상이 아닌가

Theory 70--71의 normalized terminal inequality는

\[
 AJ^2\le BJY+EJ^2.
\]

여기서 contour·Lemma 3와 phase 36은 \(E\)에만 들어간다. \(L\)을 충분히 키워
\(E/A\)를 작게 만들면 최종 coefficient는 \(B/A\)로 수렴한다. 따라서 이 항들을
줄이면 식 (73.24)의 finite cutoff는 줄지만, Theory 72의 asymptotic near coefficient는
줄지 않는다.

이는 해당 항들이 수학적으로 불필요하다는 뜻이 아니다. 단지 **현재 처음 실패하는
coefficient gate를 고치는 우선순위가 아니다.**

## 10. \(d=186\) PAP capacity와 구조적 진단

\(d=186\), \(c_1=1/24\), \(\theta=1/21\)이면

\[
 \lambda=\frac{82}{93},\qquad
 \lambda\frac{c_1d}{5}=\frac{1271}{930},qquad
 \lambda\frac d7=\frac{164}{7}.
\tag{73.26}
\]

Theory 72 식 (72.15)의 unit-\(C_J\) kernel은

\[
 K_{\rm unit}=2\left\{
 \frac{4e^{-1271/930}}{82/93}
 +\frac{7}{186}\frac{e^{-164/7}}{(82/93)^2}
 \right\}
 =2.3132538371250\ldots .
\tag{73.27}
\]

따라서 \(K_{\rm unit}C_J\le e^{-2}\)에는 식 (73.6)이 필요하다. baseline과
finite-safe tightening의 near upper는 각각

\[
 2.1484606972311\ldots\times10^{13},qquad
 6.2567679542504\ldots\times10^{10}.
\tag{73.28}
\]

이다.

현재 proof architecture의 \(\theta^{-6}\)만 남기고 모든 dimensionless cost를 1로
놓는 counterfactual에서도

\[
 \theta^{-6}=21^6=85{,}766{,}121
\tag{73.29}
\]

이고 PAP budget보다 약 \(1.466\times10^9\)배 크다. 식 (73.29)는 **불가능성 정리**가
아니다. 다른 증명은 \(\theta^{-6}\)을 없애거나 상쇄할 수 있다. 다만 현 구조를 유지한
채 52, 5, 2 같은 숫자만 개선하는 방향은 연구 투자 대비 전망이 없다는 강한 설계
진단이다.

## 11. 판정

| 항목 | 판정 | 이유 |
|---|---|---|
| exact baseline loss tree | `KERNEL/EXACT ALGEBRA` | 식 (73.2)--(73.3) |
| finite-safe local tightening | `PROJECT PARAMETERIZED EXPLICIT` | 식 (73.8)--(73.25) |
| local tightening으로 PAP gate 통과 | **FAIL** | 식 (73.7) |
| contour/Lemma 3 추가 최적화 | `CUTOFF-ONLY FOR THIS GATE` | asymptotic \(B/A\)에 불포함 |
| current architecture의 전역 최적성 | `NOT PROVED` | 재배열·새 weight·새 density theorem 배제 불가 |
| structural proof change 또는 source replacement 필요 | **YES** | 최소 \(10^{11}\) 이상 잔여 격차 |
| `PAP-11`, `DEP-R09` | `OPEN` | 새 density package와 남은 PAP component 필요 |
| fixed \(2\times10^{-17}\), \(X_{\rm cert}\) | `NOT CERTIFIED / OPEN` | threshold calculator 금지 유지 |

## 12. Python·Lean 증거 경계

- [exact/high-precision evaluator](../../../source/dep_r09_cj_loss_tree.py)는 baseline,
  source-tightened coefficient, absorption cutoff와 PAP budget ratio를 계산한다.
- [fail-closed tests](../../../tests/test_dep_r09_cj_loss_tree.py)는 exact fractions,
  denominator grid, source hash, status false gate와 coefficient gap을 검사한다.
- Lean 단일 파일에는 baseline factorization, endpoint source coefficient,
  exponential \(7/4\) envelope, residue composition, arbitrary absorption margin와
  tightened exact coefficient를 추가한다.
- generalized Halász inequality와 Ramaré--Zuniga analytic Corollary 자체는
  `SOURCE_THEOREM_UNFORMALIZED`; project-local axiom으로 대체하지 않는다.
- `sorry`, `admit`, project-local `axiom`을 사용하지 않는다.

Lean PASS는 외부 density theorem 전체의 독립 증명이 아니라, source premise 이후의
dependency-critical 유한 대수와 이번 loss-tree 결론을 검증한다.

## 13. 다음 권장 gate

다음은 ordinary constant polishing이 아니라 **modern explicit near-one zero-density source
비교**다. 후보 정리는 최소한 다음 정보를 동시에 제공해야 한다.

1. primitive nonprincipal family \(q\le Q=X^{1/d}\), \(T=Q^5\)에 적용 가능할 것,
2. \(1-\alpha\asymp1/\log X\)까지 uniform한 numerical multiplier와 finite cutoff가 있을 것,
3. \(d\le186\)에서 integrated near error가 \(e^{-2}\) budget 아래로 내려갈 것,
4. exceptional/principal branch와 결합할 수 있는 conductor normalization을 보존할 것.

이 네 조건을 만족하는 후보가 없으면 fixed \(2\times10^{-17}\)의 독립 인증 경로 자체를
재검토해야 한다. 이 source 비교 전에는 장시간 계산이나 threshold calculator를 만들지 않는다.

## 14. 참고문헌

- M. Jutila, *On Linnik's constant*, *Mathematica Scandinavica* 41 (1977),
  45--62, DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- O. Ramaré and S. Zuniga-Alterman,
  *An \(L^2\)-bound for the Barban--Vehov weights*,
  DOI [10.7169/facm/241018-19-5](https://doi.org/10.7169/facm/241018-19-5),
  arXiv [2405.12662](https://arxiv.org/abs/2405.12662).
