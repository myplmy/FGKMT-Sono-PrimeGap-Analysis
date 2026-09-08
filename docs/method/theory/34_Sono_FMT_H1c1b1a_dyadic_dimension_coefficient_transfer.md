# Sono/FMT H1c-1b.1a dyadic dimension·coefficient transfer

- 작성: 2026-09-09 KST
- 증거 수준: `SOURCE-LEVEL NORMALIZATION AUDIT / PROJECT FINITE LEMMA`
- 판정:
  `DYADIC_DIMENSION_R_SCALE_TRANSFER_CLOSED / SUCCESSOR_SIV_03_EXPLICIT`
- H1c-1b.1a:
  `CLOSED_FOR_ASYMPTOTIC_COEFFICIENT_AND_PARAMETERIZED_FINITE_SIGMA_GATE`
- `SIV-03`: 후속 H1c-1b.1a.1에서 `EXPLICIT`
- `SIV-07/08`: `HARD_BLOCKER` 유지
- numerical theorem threshold \(X_{\mathrm{cert}}\): `OPEN`
- 기계 판독 정본:
  [`data/Sono_FMT_H1c1b1a_dimension_coefficient_transfer_v1.json`](data/Sono_FMT_H1c1b1a_dimension_coefficient_transfer_v1.json)
- exact 보조검산:
  [`source/h1c1b1a_dimension_coefficient_transfer.py`](../../../source/h1c1b1a_dimension_coefficient_transfer.py)
- 비판적 검토:
  [`docs/review/40_20260909_H1c1b1a_dyadic_coefficient_transfer_타당성검토.md`](../../review/40_20260909_H1c1b1a_dyadic_coefficient_transfer_타당성검토.md)

## 1. 결론

직전 H1c-1b.1에서 발견한 \(x\) 대 \(x/2\) dimension 불일치는 다음 선택으로 고칠 수 있다.

\[
T=\frac x2,\qquad
r=r_T:=\left\lfloor(\log T)^{1/5}\right\rfloor.
\]

이 선택은 Maynard의 인쇄된 \(r\le(\log T)^{1/5}\) 조건을 정확히 만족한다. 더 중요한
질문은 \(r\)이 원래 선택보다 때때로 하나 작아져 Sono의 최종 계수가 줄어드는지였다.

이번 감사의 답은 다음과 같다.

1. \(r\ge36\)에서 차원 보정으로 인한 정규화 손실은 명시적으로 작다.
2. FGKMT가 실제로 쓰는 \(R=(x/4)^{\theta/3}\)의 유한 손실까지 포함해도 전체 factor는
   \(39/40\)보다 크다.
3. Sono가 \(\varepsilon_0\) 분모를 150 대신 160으로 택하면서 만든 여유는 \(16/15\)이다.
4. 따라서
   \[
   \sigma y\le\frac{26}{25}\,80cx\log_2x
   \]
   만 확보되면 hypergraph가 요구하는
   \(C\ge(5/4)\log5\)를 같은 \(c=\theta c_{I,J}/(12800\log5)\)로 유지한다.
5. 원문의 \(o(1)\)은 결국 위 \(26/25\) gate에 들어가므로 **충분히 큰 \(x\)**라는
   asymptotic 정리 수준에서는 Sono의 최종 \(2\times10^{-17}\) 계수를 줄일 필요가 없다.

후속 H1c-1b.1a.1은 Rosser--Schoenfeld Theorem 7로
\(x\ge2\exp(36^5)\)에서 더 강한 \(1001000/998001<26/25\) 상계를 증명했다. 그러므로
이 문서의 conditional finite gate는 현재 닫혔다. 그래도 이는 “dimension repair 때문에
계수를 낮출 필요가 없다”는 한 하위 증명이지, “Sono 부등식이 어느 숫자부터 성립한다”는
\(X_{\mathrm{cert}}\) 계산이 아니다.

## 2. 쉬운 설명

Sono의 증명에는 통과선보다 약간 높은 예비 점수가 있었다.

```text
hypergraph 통과선       = (5/4) log 5
Sono가 겨냥한 극한 하한 = (4/3) log 5
예비 여유의 비율        = (4/3)/(5/4) = 16/15
```

\(x/2\)에 맞춰 내부 후보 수를 한 개 줄이면 점수가 조금 내려간다. 실제 \(R\)도
\(x^{\theta/3}\)이 아니라 \((x/4)^{\theta/3}\)이라 아주 조금 더 내려간다. 두 손실을
합쳐도 원래 점수의 \(39/40\)보다 크다.

Mertens 곱의 남은 오차가 위쪽으로 4% 이하, 즉 \(26/25\) 이하라면

\[
\frac{39/40}{26/25}=\frac{15}{16}
\]

이고, 원래 \(16/15\) 여유와 정확히 상쇄된다. 실제 부등식은 모두 엄격하므로 경계에
딱 걸리는 것이 아니라 통과선보다 크다.

## 3. 선행연구 우선 조사

직접 lemma를 쓰기 전에 다음 원문을 실제 적용식과 대조했다.

- [FMT, *Chains of Large Gaps Between Primes*](https://arxiv.org/abs/1511.04468),
  Theorem 4의 (5.4), Theorem 6의 (6.1), (6.3), (6.8).
- [FGKMT, *Long Gaps Between Primes*](https://arxiv.org/abs/1412.5029),
  Theorem 6과 Section 8의 \(R=(x/4)^{\theta/3}\), (8.3), \(x/2\) 호출.
- [Sono](https://doi.org/10.4418/2025.80.2.2),
  Proposition 6.2의 (6.5)와 pp.541--542의 150 대 160 선택.
- [H1a project theorem](13_Sono_FMT_H1a_finite_r_integral_lemma.md),
  모든 정수 \(r\ge36\)에서
  \(J_r/I_r>\log r/(4r)\).

arXiv metadata와 표적 검색에서 이 dyadic floor 보정, 실제 \(R\), Sono의 explicit
coefficient를 한꺼번에 다룬 erratum이나 후속 lemma는 찾지 못했다. 따라서 원문의
정리와 식은 그대로 채택하고, 원문 사이에 빠진 초등 부등식만 아래 project lemma로
증명한다. 이 검색 결과는 전 세계 문헌의 완전탐색이나 novelty 주장이 아니다.

## 4. Source 식의 정확한 복원

### 4.1 Sono의 원래 slack

Sono Proposition 6.2는

\[
\frac{\theta c_{I,J}}{9600c}(1+o(1))
\le C\le
\frac{\theta c_{I,J}}{4800c}(1+o(1))
\tag{S6.5}
\]

를 쓴다. Proposition 6.3은

\[
C\ge\frac54\log5
\tag{S6.11}
\]

를 요구한다. Sono는 허용식의 분모 150보다 보수적인 160을 택해

\[
c=\frac{\theta c_{I,J}}{12800\log5}
\]

로 둔다. 그러면 lower limiting value는

\[
\frac{\theta c_{I,J}}{9600c}
=\frac43\log5.
\]

따라서 요구치와의 비율 여유는 정확히

\[
\frac{(4/3)\log5}{(5/4)\log5}=\frac{16}{15}.
\tag{H1c1b1a.1}
\]

### 4.2 FGKMT actual weight

FGKMT Section 8은

\[
R=(x/4)^{\theta/3}
\]

를 쓰므로

\[
\frac{\log R}{\log x}
=\frac{\theta}{3}
\left(1-\frac{\log4}{\log x}\right).
\tag{H1c1b1a.2}
\]

또

\[
u=\frac{\varphi(B)}B\frac{\log R}{\log x}
\frac{rJ_r}{2I_r}.
\]

\(B=1\) 또는 prime이므로 \(\varphi(B)/B\ge1/2\)이고, H1a가
\(J_r/I_r>\log r/(4r)\)를 주므로

\[
u>
\frac{\theta}{48}
\left(1-\frac{\log4}{\log x}\right)\log r.
\tag{H1c1b1a.3}
\]

Sono p.542의 \(R=x^{\theta/3}\)는 asymptotic main term에는 맞지만 finite 식에서는
(H1c1b1a.2)의 factor를 버린 표기다. numerical threshold 감사에서는 이 factor를
반드시 보존한다.

## 5. Project Lemma — exact normalization transfer

### 5.1 명제

실수 \(x\)와 정수 \(r\)가

\[
r=\left\lfloor(\log(x/2))^{1/5}\right\rfloor\ge36
\tag{H1c1b1a.4}
\]

을 만족한다고 하자. 그러면

\[
\boxed{
\frac{5\log r}{\log_2x}
\left(1-\frac{\log4}{\log x}\right)>\frac{39}{40}.
}
\tag{H1c1b1a.5}
\]

### 5.2 dimension factor

\(L=\log x\)라 쓰면

\[
r^5\le L-\log2<(r+1)^5.
\]

\(\log2<1\)이므로

\[
L<(r+1)^5+1<(r+2)^5.
\]

따라서

\[
\frac{5\log r}{\log L}>
\frac{\log r}{\log(r+2)}.
\]

\(t\log t\)가 \(t\ge36\)에서 증가하므로
\(\log r/\log(r+2)\)도 증가한다. 최소 endpoint에서

\[
36^{64}>38^{63}
\]

이므로

\[
\frac{\log36}{\log38}>\frac{63}{64}.
\tag{H1c1b1a.6}
\]

### 5.3 actual \(R\) factor

\(L>r^5\ge36^5\), \(\log4<2\), \(210<36^5\)이므로

\[
1-\frac{\log4}{L}
>
1-\frac{2}{36^5}
>
\frac{104}{105}.
\tag{H1c1b1a.7}
\]

(H1c1b1a.6)과 (H1c1b1a.7)을 곱하면

\[
\frac{63}{64}\frac{104}{105}
=\frac{39}{40},
\]

이므로 (H1c1b1a.5)가 증명된다. 정수 거듭제곱과 유리수 항등식은 보조 모듈이
exact arithmetic으로 검사한다.

## 6. Hypergraph coefficient로의 전달

식 (H1c1b1a.3)과 (H1c1b1a.5)에서

\[
u>
\frac{\theta}{240}\frac{39}{40}\log_2x.
\tag{H1c1b1a.8}
\]

이제 finite Mertens target을

\[
\boxed{
\sigma y\le\frac{26}{25}\,80cx\log_2x
}
\tag{H1c1b1a.9}
\]

로 둔다. \(C=ux/(2\sigma y)\)이므로, \(c_{I,J}=1/4\)와
\(c=\theta/(51200\log5)\)를 넣으면

\[
\begin{aligned}
C
&>
\frac43\log5\,
\frac{39/40}{26/25}\\
&=
\frac43\log5\cdot\frac{15}{16}
=\frac54\log5.
\end{aligned}
\tag{H1c1b1a.10}
\]

따라서 (H1c1b1a.9)가 성립하는 범위에서는 dimension 보정과 actual \(R\) factor가
Sono의 \(c\)를 낮추지 않는다. 원문의

\[
\sigma y=(1+O(\log_2^{-10}x))80cx\log_2x
\]

는 asymptotically (H1c1b1a.9)를 만족한다. 후속 문서
[`35_Sono_FMT_H1c1b1a1_sigma_y_explicit_cutoff.md`](35_Sono_FMT_H1c1b1a1_sigma_y_explicit_cutoff.md)는
이 \(O\)-항의 숨은 상수를 추측하지 않고 published explicit Mertens theorem으로 우회해
\(x\ge2\exp(36^5)\)에서 (H1c1b1a.9)를 증명했다. 따라서 `SIV-03`은 현재 `EXPLICIT`이다.

## 7. 정정한 기존 기계 원장 오류

T1 JSON의 `SIV-03`은 한때

```text
sigma*y = ... * 80c*x*log_2(x)/log(x)
```

라고 기록돼 있었다. FMT (6.12), FGKMT (6.11), Sono p.542를 대조하면 정확한 식은

```text
sigma*y = ... * 80c*x*log_2(x)
```

이다. `/log(x)`는 prime survivor count
\(\sigma y/\log x\)에 붙는다. 이번에 기계 원장을 교정한다. 기존 actual empirical
산출물에는 이 JSON 식을 사용하지 않았으므로 계산 결과 오염은 없다.

## 8. 닫힌 항목과 열린 항목

| 항목 | 상태 | 의미 |
|---|---|---|
| \(r_T=\lfloor(\log(x/2))^{1/5}\rfloor\) admissibility | `CLOSED` | 반복 transition strip 제거 |
| \(r\ge36\) H1a integral ratio | `EXPLICIT` | 기존 project theorem 사용 |
| dimension normalization \(>63/64\) | `CLOSED` | exact integer endpoint certificate |
| actual \(R\) factor \(>104/105\) | `CLOSED` | \(R=(x/4)^{\theta/3}\) 반영 |
| combined factor \(>39/40\) | `CLOSED` | 위 두 손실의 합성 |
| \(\sigma y\) target \(26/25\) 아래 coefficient | `CLOSED_PARAMETERIZED` | \(C>(5/4)\log5\) |
| asymptotic Sono coefficient 보존 | `CLOSED` | dimension repair가 새 계수 손실을 강제하지 않음 |
| \(26/25\) sufficient cutoff | `EXPLICIT` | 후속 H1c-1b.1a.1에서 \(x\ge2\exp(36^5)\) |
| common exceptional \(B\) | `OPEN` | H1c-1b.2 |
| endpoint·\(\psi\to\pi\)·recentring | `OPEN` | H1c-1b.3 |
| density·full Bordignon error·common cutoff | `OPEN` | H1c-1b.4 |
| P9.2, Hypothesis 1(2), `SIV-07/08` | `OPEN / HARD_BLOCKER` | 승격 없음 |
| \(X_{\mathrm{cert}}\) | `OPEN` | calculator 작성 금지 유지 |

### 최소 dimension gate의 정확한 뜻

이번 lemma의 시작조건은

\[
\log(x/2)\ge36^5,
\qquad\text{즉}\qquad
\log x\ge36^5+\log2.
\]

이는 coefficient-transfer lemma의 충분조건일 뿐 전체 Sono 정리의 시작점이 아니다.
다른 root blocker의 cutoff가 훨씬 클 수 있다.

## 9. 선행연구 전략의 평가

“기존 lemma를 먼저 찾고 없을 때만 직접 증명한다”는 전략은 이번에도 타당했다.

- 원문이 결정하는 \(C,u,R,r,c\)는 직접 재발명하지 않고 source 그대로 사용했다.
- H1a가 이미 닫은 \(J_r/I_r\)를 재증명하지 않았다.
- 새로 증명한 것은 source 사이의 floor endpoint와 네 개 유리 slack의 연결뿐이다.

다만 표적 검색에서 선행 lemma가 보이지 않았다는 이유만으로 새 결과의 세계적 novelty를
주장하지 않는다. 또한 이 초등 transfer가 어려운 소수분포 blocker를 대신하지 않는다.

## 10. 다음 gate

직접 후속 H1c-1b.1a.1은 완료됐다. 현재 다음 gate는 H1c-1b.2의 한 common exceptional
conductor/prime \(B\)와 full quantitative distribution composition이다.

actual prime sweep, P018-B, threshold calculator, 장시간 runner, Lean 또는 새 Python
package는 이번 단계에 필요하지 않았다.

```text
H1c-1b.1a elementary transfer              = CLOSED
dimension repair forces smaller Sono c     = NO
Sono 2e-17 coefficient preserved           = YES, ASYMPTOTICALLY
finite coefficient gate                    = CLOSED
explicit cutoff for the 26/25 gate         = x >= 2*exp(36^5)
SIV-07 / SIV-08                            = HARD_BLOCKER
threshold calculator                       = NOT READY
X_cert                                     = OPEN
```
