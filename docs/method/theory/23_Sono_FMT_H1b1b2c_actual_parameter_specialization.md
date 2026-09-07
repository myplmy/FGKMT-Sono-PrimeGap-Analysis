# Sono/FMT H1b-1b-2c 실제 Section 8 입력 상수 특수화

- 작성일: 2026-09-08
- 상위 obligation: `H1B-L83`, `H1B-L84`, `H1B1-PACKAGE`, `SIV-07`
- 선행 정식화:
  - [actual local factor](20_Sono_FMT_H1b1b2a_actual_local_factor_lower_bound.md)
  - [11개 application inventory](21_Sono_FMT_H1b1b2a1_application_exclusion_inventory.md)
  - [교정된 kappa=1 multiplier](22_Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier.md)
- 기계 계약:
  [Sono_FMT_H1b1b2c_actual_parameter_specialization_v1.json](data/Sono_FMT_H1b1b2c_actual_parameter_specialization_v1.json)
- 구현: `source/h1b1b2c_actual_parameter_package.py`

## 1. 판정부터 요약

Maynard Section 8에서 추적한 11개 analytic subapplication의 Lemma 8.3 입력은
다음 하나의 공통 package로 덮을 수 있다.

\[
\boxed{
 a=\frac12,\qquad A_2=8,\qquad
 L=L_*:=5+\log\Lambda_*
}
\]

여기서 Maynard의 표기는

\[
0\le \frac{\gamma(p)}p\le1-a
\]

이고, GGPY의 대응 표기에서는 `A1=1/a=2`다. 또한

\[
\Lambda_*=
2k^2\log(2k^2)+k(k-1)\log2+
\left\{
\frac{10\alpha(2k^2-k+1)}{\theta}+k
\right\}\log R
\]

는 theory 21에서 인증한 11개 적용의 공통
\(\log\operatorname{rad}(Q)\) 상계다.

정식 판정은 다음과 같다.

~~~text
actual four-family local density bound              PROJECT FINITE THEOREM
common Maynard a / GGPY A1                          1/2 / 2
common upper prime-sum discrepancy A2               8
common lower discrepancy magnitude L                5+log(Lambda_star)
corrected one-step Lemma 8.3 input package           PARAMETERIZED EXPLICIT
corrected Lemma 8.4 r-fold composition               OPEN
SIV-07 / numerical X_cert                            HARD_BLOCKER / OPEN
~~~

따라서 이번 단계는 이전의 `actual a,A2,L OPEN`을 닫는다. 다만 \(L_*\)가
전역 매개변수 \(k,\alpha,\theta,R\)에 의존하고, Lemma 8.4의 반복오차와 smooth
function norm이 아직 합성되지 않았으므로 최종 numerical threshold를 계산할 수 있다는
뜻은 아니다.

## 2. 쉬운 설명

Lemma 8.3을 계산 가능한 형태로 쓰려면 세 종류의 안전장치가 필요하다.

1. 각 소수의 국소 밀도가 1에 너무 가까워지지 않는다는 여유 `a`.
2. 소수들을 구간별로 더했을 때 기준값보다 위로 벗어나는 양 `A2`.
3. 아래로 벗어나는 양 `L`.

Maynard 원문은 이 값들을 “충분히 큰 \(k\)”에서 고정할 수 있다고만 설명한다.
이번 작업은 실제 Section 8에서 쓰는 네 종류의 식만 대상으로 잡아, 모든 11개 호출에
동시에 쓸 수 있는 보수적인 숫자와 공식을 만들었다. 비유하면 부품 하나의 허용오차표를
완성한 것이다. 아직 그 부품을 여러 번 연결한 완성 기계의 누적오차표는 만들지 않았다.

## 3. 문헌 우선 조사와 직접 증명의 경계

| 항목 | 우선 사용한 선행 결과 | 적용성 판정 | 이번 프로젝트의 보충 |
|---|---|---|---|
| 실제 \(\gamma(p)\)와 가정 | Maynard Lemmas 8.3--8.4, source 531--604행 | 직접 대상 | 11개 적용·네 family 전수 대응 |
| \(\sum_{p\le x}\log p/p\) | Rosser--Schoenfeld Theorem 6, (3.21), (3.24) | 모든 실수 \(x>1\)에 직접 적용 | 양 끝 포함 구간으로 변환하는 endpoint 보정 |
| 교정된 합 공식 | Ford Theorem 4.4 | \(\kappa=1\)에 적용 | 보수적 explicit multiplier는 theory 22에서 정식화 |
| 인쇄 오류항 경고 | Castillo et al. Lemma 2.5와 직후 Remark | 반드시 반영 | 누락된 \(c_\gamma(L+1)\) 항을 보존 |
| 더 최신한 소수합 추정 | Dusart 2010 | 사용 가능하지만 불필요 | 모든 작은 \(w\ge2\)를 한 번에 덮는 Rosser--Schoenfeld를 선택 |

표적 검색에서 이 11개 실제 적용의 공통 \(a,A_2,L\)을 완성된 수치 package로
제시한 논문은 확인하지 못했다. 이는 전 세계 문헌에 그런 결과가 없다는 novelty 주장이
아니다. 선행 결과가 직접 주는 부분을 먼저 사용하고, 실제 family 특수화와 endpoint·제외소수
연결부만 아래에서 직접 증명한다.

## 4. actual local density의 공통식

비제외 소수에서 theory 20--21의 source tracing은

\[
\rho_p:=\frac{\gamma(p)}p
=\frac{1}{1+n+g(p)},
\qquad 0\le n\le b-1,quad 1\le b\le k+1,quad p>2k^2
\]

를 준다. 여기서 \(b\)는 해당 소수에서의 root count이며, 실제 네 family는

\[
g_0=p-b,
\quad g_1=\frac{(p-b)^2}{p-1},
\quad g_2=\frac{(p-b)^2}{p+b-2},
\quad g_3=p-b-\frac{b-1}{p-1}
\]

이다. 제외 소수 \(p\mid Q\)에서는 \(\rho_p=0\)이다.

## 5. 국소 보조정리: \(a=1/2\)와 positive correction

### Lemma H1B1B2C-LF

§4의 비제외 입력에 대해 \(D_p=1+n+g(p)\)라 두면

\[
0\le p-D_p\le3(b-1)\le3k.
\]

### 증명

\(n\ge0\)이므로 각 family에서 \(p-1-g(p)\)만 상계하면 충분하다.

\[
\begin{array}{c|c|c}
g & p-1-g & \text{상계}\\ \hline
p-b & b-1 & b-1\\
(p-b)^2/(p-1) & (b-1)(2p-b-1)/(p-1) & 2(b-1)\\
(p-b)^2/(p+b-2) & (b-1)(3p-b-2)/(p+b-2) & 3(b-1)\\
p-b-(b-1)/(p-1) & (b-1)+(b-1)/(p-1) & 2(b-1)
\end{array}
\]

theory 20의 \(g+n\le p-1\)에 의해 \(D_p\le p\)이므로 왼쪽 부등식도 성립한다. □

\(p>2k^2\ge4k\)와 위 정리로

\[
D_p\ge p-3k>\frac p4>2.
\]

따라서

\[
0\le\rho_p-\frac1p
=\frac{p-D_p}{pD_p}
\le\frac{12k}{p^2},
\qquad
\rho_p<\frac12.
\]

즉 Maynard의 공통 gap parameter로 \(a=1/2\), GGPY 표기로 `A1=2`를 쓸 수 있다.

## 6. 비제외 소수 correction의 전역 상계

\[
C_k:=\sum_{p>2k^2}\left(\rho_p-\frac1p\right)\log p
\]

라 하자. 모든 \(k\ge2\)에서

\[
\boxed{C_k<4}.
\]

### \(k\ge3\)

이때 \(p>2k^2\ge6k\)이므로 \(D_p>p/2\)이고

\[
C_k\le6k\sum_{n>2k^2}\frac{\log n}{n^2}
\le\frac{3\{\log(2k^2)+1\}}k<4.
\]

마지막 식은 \(k=3\)에서 4보다 작고 이후 감소한다.

### \(k=2\)

\(p=11\) 항은 \(24\log11/11^2<1/2\)다. \(p\ge13\)에서는
\(D_p>p/2\)이므로

\[
\sum_{p\ge13}\left(\rho_p-\frac1p\right)\log p
\le12\sum_{n\ge13}\frac{\log n}{n^2}
\le\log12+1<\frac72.
\]

두 항을 합치면 4보다 작다. 여기에는 \(\log11<5/2\),
\(\log12<5/2\)라는 초등 약화만 사용했다.

## 7. Rosser--Schoenfeld 누적합을 양 끝 포함 구간으로 변환

\[
S(x)=\sum_{p\le x}\frac{\log p}{p}
\]

라 하자. Rosser--Schoenfeld Theorem 6의 (3.21), (3.24)는 모든 \(x>1\)에서

\[
\log x+E-\frac1{2\log x}<S(x)<\log x
\]

를 준다. 논문의 상수는

\[
E=-\gamma-\sum_p\frac{\log p}{p(p-1)}.
\]

다음 초등 상계로 소수 전체를 직접 계산할 필요가 없다.

\[
\begin{aligned}
\sum_p\frac{\log p}{p(p-1)}
&\le\sum_{n=2}^{\infty}\frac{\log n}{n(n-1)}\\
&=\log2+\sum_{n=2}^{\infty}\frac{\log(1+1/n)}n\\
&<\log2+\sum_{n=2}^{\infty}\frac1{n^2}
<\frac7{10}+\frac34=\frac{29}{20}.
\end{aligned}
\]

\(0<\gamma<1\)이므로 \(E>-49/20\)이다.

Maynard의 합은 \(w\le p\le z\)로 양 끝을 포함한다. \(w\)가 소수이면
누적합을 뺄 때 \(\log w/w\) 한 항을 되돌려야 한다. \(w\ge2\)에서
\(1/(2\log w)<1\), \(\log w/w<1/2\)이므로 모든 실수
\(2\le w\le z\)에 대해

\[
\boxed{
-\frac72<
\sum_{w\le p\le z}\frac{\log p}{p}-\log(z/w)
<4
}.
\]

이 endpoint 보정은 작은 범위까지 포함하는 공통 상수를 쓰기 위해 필요하다.

## 8. 제외 소수의 손실

\(Q\)를 한 application·iteration의 effective excluded radical이라 하고
\(\log Q\le\Lambda\), \(\Lambda\ge\log210\)라 하자. 제외 소수를
\(p\le\Lambda\)와 \(p>\Lambda\)로 나누면 (3.24)에 의해

\[
\begin{aligned}
\sum_{p\mid Q}\frac{\log p}{p}
&<\sum_{p\le\Lambda}\frac{\log p}{p}
+\frac1\Lambda\sum_{\substack{p\mid Q\\p>\Lambda}}\log p\\
&<\log\Lambda+1.
\end{aligned}
\]

theory 21은 모든 11개 적용에서 \(\Lambda\le\Lambda_*\)와
\(Q\ge210\)을 이미 인증했다.

## 9. 세 입력의 결합

§6--§8을 합치면

\[
\begin{aligned}
\sum_{w\le p\le z}\rho_p\log p-\log(z/w)
&<4+4=8,\\
\sum_{w\le p\le z}\rho_p\log p-\log(z/w)
&>-\frac72-(\log\Lambda_*+1)\\
&>-(5+\log\Lambda_*).
\end{aligned}
\]

따라서 §1의 공통 \(a,A_2,L_*\)이 Maynard Lemma 8.3의 모든 구간
\(2\le w\le z\)와 추적된 11개 subapplication에서 성립한다.

## 10. 11개 적용의 실제 family 대응

| application ID | source | family | root count |
|---|---|---|---|
| `L620_dW` | 620--622 | \(p-b\) | \(\omega(p)\) |
| `L737_canonical` | 723--739 | \((p-b)^2/(p-1)\) | \(\omega(p)\) |
| `L752_canonical` | 750--760 | \(p-b\) | \(\omega(p)\) |
| `L885_W_prime` | 883--888 | \((p-b)^2/(p-1)\) | \(\omega(p)\) |
| `L905_W_prime` | 903--910 | \(p-b\) | \(\omega(p)\) |
| `L995_a_m_W_B_r` | 995--999 | \(p-b\) | \(\omega(p)\) |
| `L1015_r_W_m` | 1015--1019 | \(p-b-(b-1)/(p-1)\) | \(\omega(p)\) |
| `L1096_W0` | 1096--1098 | \(p-b\) | 1 |
| `L1135_W0_factor` | 1112--1141, \(r_0\) | \((p-b)^2/(p+b-2)\) | \(\omega^*(p)\) |
| `L1135_canonical_factor` | 1112--1141, r-vector | \((p-b)^2/(p+b-2)\) | \(\omega^*(p)\) |
| `L1232_canonical` | 1228--1237 | \((p-b)^2/(p+b-2)\) | \(\omega(p)\) |

1135행의 두 factor는 cutoff와 차원이 다르므로 계속 별도 analytic application으로 유지한다.

## 11. 교정 multiplier에 넣은 값과 크기

theory 22의 교정된 one-step multiplier에 \(a=1/2,A_2=8\)을 넣으면

\[
\Delta=\frac{14801}{69},\qquad T=264,
\]

\[
\log C_{\rm sum}=279.9886947801533187\ldots
\]

이고, weighted Lemma 8.3 multiplier는

\[
\boxed{
C_{8.3}\approx7.91726413329524\times10^{121}
}
\]

이다. 따라서 한 번의 적용에서 보수적 절대오차 계수는

\[
C_{8.3}\{6+\log\Lambda_*\}
\]

가 된다. 이 값이 큰 이유는 증명을 빠짐없이 explicit하게 만드는 과정에서 여러 번
거친 약화를 사용했기 때문이다. 이것이 실제 현상의 오차가 이만큼 크다는 뜻은 아니지만,
향후 \(X_{\rm cert}\)가 매우 커질 수 있음을 미리 보여 준다.

## 12. 닫힌 것과 닫히지 않은 것

| obligation | 이전 | 현재 |
|---|---|---|
| `H1B-L83` actual inputs | `PARAMETERIZED_EXPLICIT_INPUTS_OPEN` | `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT` |
| common \(a,A_2,L\) | `OPEN` | `1/2, 8, 5+log(Lambda_star)` |
| `H1B-L84` corrected r-fold composition | `RATE_MISSING` | `RATE_MISSING` |
| `H1B1-PACKAGE` | `HARD_BLOCKER` | `HARD_BLOCKER` |
| `SIV-07` | `HARD_BLOCKER` | `HARD_BLOCKER` |
| \(X_{\rm cert}\) | `OPEN` | `OPEN` |

이번 결과로 실제 입력의 불명확성은 제거됐다. 다음 gate는 smooth function norm과
각 단계의 \(L_j\)을 보존한 **교정된 Lemma 8.4 r-fold 합성**이다. 그 뒤에도
Lemmas 8.5--8.6, Propositions 9.1--9.5, H1c/PAP와 arbitrary-X 전달이 남는다.

## 13. 자동 검증과 비목표

`tests/test_h1b1b2c_actual_parameter_package.py`는 다음을 검증한다.

- 11개 ID와 네 family가 기존 전수 inventory와 정확히 일치
- \(2\le k\le14\)의 작은 exact-rational grid에서 defect·density 부등식
- \(2\le k\le1000\)에서 §6의 analytic correction majorant가 4 미만인지 회귀 확인
- 공통 상수와 \(\Lambda_*\) 결합식
- source SHA-256과 기계 계약
- r-fold, `SIV-07`, \(X_{\rm cert}\)가 자동 승격되지 않는 fail-closed 상태

수치 grid는 위 대수 증명의 대체물이 아니다. 이번 단계에서는 maximal-gap 데이터,
소수 sweep, empirical graph, threshold calculator를 실행하지 않았다.

## 14. 사용자 수행사항

별도 수행절차 필요없음. Lean이나 새 Python 라이브러리도 필요하지 않다.
