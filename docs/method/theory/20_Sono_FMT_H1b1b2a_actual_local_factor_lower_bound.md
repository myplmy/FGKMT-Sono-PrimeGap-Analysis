# Sono/FMT H1b-1b-2a Maynard actual-call local-factor·제외모듈 하한 정식화

- 작성일: 2026-09-07
- 상위 obligation: `H1B1B2-CMIN-*`, `H1B1B2-ROUTE-DECISION`, `SIV-07`
- 상위 원장:
  [H1b-1b-2 오류 정규화·Lemma 8.4 보정](19_Sono_FMT_H1b1b2_cgamma_error_normalization_ledger.md)
- 기계 계약:
  [Sono_FMT_H1b1b2a_actual_local_factor_lower_bound_v1.json](data/Sono_FMT_H1b1b2a_actual_local_factor_lower_bound_v1.json)
- application 전수감사:
  [H1b-1b-2a.1 actual application-exclusion inventory](21_Sono_FMT_H1b1b2a1_application_exclusion_inventory.md)
- 검증 구현: `source/h1b1b2_local_factor_lower_bound.py`

## 1. 판정부터 요약

Maynard Lemma 8.4의 추상 가정 (g(p)=p+O(k))만으로는 각 비제외 소수의
local factor를 아래에서 1로 누를 수 없다. 그러나 Maynard Section 8에서 **실제로
Lemma 8.3·8.4를 호출하는 분모**를 원정의까지 추적하면 네 가지 대수형으로 덮이며,
그 네 형식은 모두

\[
0<g(p)\le p-a(p)
\]

를 만족한다. 여기서 (a(p))는 해당 호출의 전체 허용 좌표 수를 지배하는
\(\omega(p)\) 또는 \(\omega^*(p)\)다. 이 사실로 비제외 local factor는 정확히 1 이상이다.

한 번의 Lemma 8.4 적용에서 제외된 소수는 유효 제외 정수

\[
Q_j=\widetilde W_{j+1}\prod_{i=j+2}^{r}e_i
\]

의 소인수이므로 그 손실 전체는

\[
c_{\gamma,j}\ge\prod_{p\mid Q_j}\left(1-\frac1p\right)
=\frac{\varphi(Q_j)}{Q_j}
\]

로 합쳐진다. 정본의 기본 (W_i) 구성에 대해서는 숨은 (R^{O(k^2)})를
명시적 상계 (Lambda^{\rm base}_j)로 바꿨다. 이어진 H1b-1b-2a.1 감사는
(dW_i), (W'_i), (a_mWBr), (rW_m), (W_0=DV\Delta_L)를 포함한
11개 actual subapplication을 원문에서 전수 고정하고, 각 추가 로그 비용
(eta_{\rm app,j})가 0 또는 (log R)임을 증명했다. 따라서

\[
\log Q_j\le
\Lambda^{\rm app}_j:=\Lambda^{\rm base}_j+\eta_{\rm app,j}
\]

이며, 모든 호출·iteration에 공통인 상계는

\[
\Lambda_*=
2k^2\log(2k^2)+k(k-1)\log2+
\left\{
\frac{10\alpha(2k^2-k+1)}{\theta}+k
\right\}\log R
\]

이다. Rosser--Schoenfeld로 이제 추적된 actual call 전체에서

\[
\boxed{
c_{\gamma,j}>
\frac{1}{3\{1+\log \Lambda_*\}}
}
\]

를 결론낼 수 있다. 따라서 `uniform c_gamma lower-bound route`는 주요 후보 단계를
넘어 **추적된 actual call 전체에 대해 parameterized explicit 경로로 선택됐다**.
그 뒤에도 절대오차의 기본 상수
\(C_{3,\mathrm{abs}}(A_1,A_2)\), 그 유효범위, (L)의 수치 multiplier와 수정된
(r)-회 합성이 필요하므로 `SIV-07`과 (X_{\mathrm{cert}})는 계속 `OPEN`이다.

## 2. 1차 자료와 provenance

### 2.1 Maynard

James Maynard,
[*Dense Clusters of Primes in Subsets*](https://doi.org/10.1112/S0010437X16007296),
arXiv:1405.2593.

- 검토본: `tmp/pdfs/h1b1b/maynard_source/Subsets.tex`
- 핵심 위치: 366, 376--407, 413--421, 531--604행
- actual-call 위치: 620--622, 723--739, 750--760, 883--910,
  995--1019, 1096--1098, 1112--1141, 1228--1237행

### 2.2 Rosser--Schoenfeld

J. Barkley Rosser and Lowell Schoenfeld,
[*Approximate Formulas for Some Functions of Prime Numbers*](https://doi.org/10.1215/ijm/1255631807),
*Illinois Journal of Mathematics* 6 (1962), 64--94.

- 검토 위치: PDF page 9, 인쇄면 p.72, Theorem 15, (3.41)--(3.42)
- 증명 위치: 인쇄면 pp.88--89
- 로컬 PDF SHA-256:
  `8e37b06f82e09421bceb2502578c47b61469141f0287e6acedb70e01765ab556`
- (3.41)의 일반 계수 (5/2) 대신 유일한 예외에 쓰인 (2.50637)을 전 범위에
  적용하면 모든 정수 (n\ge3)에 유효한 안전한 약화가 된다.

### 2.3 Dusart 대체 경로

Pierre Dusart,
[*Estimates of Some Functions Over Primes without R.H.*](https://arxiv.org/abs/1002.0442),
Theorem 6.12.

- 검토 위치: PDF page 11
- 로컬 PDF SHA-256:
  `3f11eca84613ad00e6a447f99b318d5c3d76e360283efcc6d3eebdda25ff3923`
- (x\ge2973)에서

\[
\frac{e^{-\gamma}}{\log x}
\left(1-\frac{0.2}{\log^2x}\right)
<\prod_{p\le x}\left(1-\frac1p\right)
\]

을 준다. 임의 (Q\le Q_{\max})에 모든 (p\le Q_{\max})를 추가한 곱으로
하한을 만들 수 있지만 크기가 (1/\log Q_{\max}) 수준이라,
(1/\log\log Q_{\max}) 수준인 Rosser--Schoenfeld 경로보다 훨씬 약하다.
따라서 검산·fallback으로만 보존한다.

두 PDF는 2026-09-07T04:48:29Z에 공식 arXiv·DOI 연결에서 다시 취득했고,
텍스트 추출과 해당 page render를 함께 확인했다. Rosser--Schoenfeld 파일은 H1b-1a에서
이미 취득한 동일 hash의 PDF와 일치한다.

## 3. actual-call 분모 분류

아래 표의 (a)는 (omega(p)) 또는 (omega^*(p))다. `availability`는 실제 합에서
소수 (p)를 받을 수 있는 전체 좌표 수이며 항상 (m(p)\le a)다.

| Maynard 위치 | 원래 합의 prime 분모 | 본 문서 family | availability 상계 |
|---|---|---|---:|
| 620--622 | \(\phi_\omega(p)=p-\omega(p)\) | (p-a) | \(\omega(p)\) |
| 723--739 | \(\phi_\omega(p)^2/\phi(p)\) | \((p-a)^2/(p-1)\) | \(\omega(p)\) |
| 750--760 | \(\phi_\omega(p)\) | (p-a) | \(\omega(p)\) |
| 883--888 | \(\phi_\omega(p)^2/\phi(p)\) | \((p-a)^2/(p-1)\) | \(\le\omega(p)\) |
| 903--910 | \(\phi_\omega(p)\) | (p-a) | \(\le\omega(p)\) |
| 995--999 | \(\phi_\omega(p)\) | (p-a) | 1, 비제외이면 (a\ge1) |
| 1015--1019 | \(\phi_\omega(p)[p/(p-1)-1/\phi_\omega(p)]\) | (p-a-(a-1)/(p-1)) | 1 |
| 1096--1098 | \(\phi(p)=p-1\) | (p-a, a=1) | 1 |
| 1112--1141 | \((p-\omega^*(p))^2/(p+\omega^*(p)-2)\) | \((p-a)^2/(p+a-2)\) | \(\le\omega^*(p)\) |
| 1228--1237 | \((p-\omega(p))^2/(p+\omega(p)-2)\) | \((p-a)^2/(p+a-2)\) | \(\omega(p)\) |

885행과 1135행 근처에서 논문은 분모를 (p+O(k))로 다시 축약한다. 본 감사는 그
축약을 역으로 임의 복원하지 않고, 바로 앞의 exact rational expression을 사용했다.

### 3.1 실제 제외 모듈은 동일하지 않다

분모 family가 같아도 Lemma 8.3·8.4에 들어가는 제외 모듈은 호출마다 다르다.

| Maynard 위치 | 확인된 유효 제외인자 | 현재 판정 |
|---|---|---|
| 620 | (dW_i), (d\le R) | 추가 (log R) 후보; 반복 단계별 통합 미완료 |
| 737, 752, 1232 | 정본 (W_i) | §6의 base 식 적용 가능 |
| 885, 905 | (W_i'=\operatorname{rad}(W_i(a_i b_m-a_m b_i))) | 판별식 support와의 포함관계 재검증 필요 |
| 995 | (a_mWBr) | (a_m,r) 범위와 적용 차원 통합 필요 |
| 1015 | (rW_m) | (r) 범위와 one-variable (Q) 통합 필요 |
| 1096 | (W_0=DV\Delta_L) | 별도 (W_0) 상계 필요 |
| 1135 | (W_0) 합과 정본 (W_i) 합 | 두 적용을 분리해 각각 상계해야 함 |

이 목록은 source에서 인자를 **찾은 결과**이지 아직 모든 호출의 uniform 상계를
증명한 결과가 아니다. 특히 같은 문자 (D,r,W)가 문맥마다 다른 역할로 쓰이므로,
각 호출의 support·크기·Lemma 8.4 차원을 따로 고정해야 한다.

## 4. 비제외 local-factor 보조정리

### 정리 H1B1B2A-LF

정수 (1\le a<p), (0\le n\le a-1)에 대해 (g)가 다음 중 하나라 하자.

\[
g_0=p-a,
\quad
g_1=\frac{(p-a)^2}{p-1},
\quad
g_2=\frac{(p-a)^2}{p+a-2},
\quad
g_3=p-a-\frac{a-1}{p-1}.
\]

그러면 (0<g\le p-a)이고

\[
\left(1-\frac1p\right)
\left(1+\frac1{g+n}\right)\ge1.
\]

### 증명

네 함수의 (p-a)에 대한 여유는 각각

\[
0,
\quad
\frac{(p-a)(a-1)}{p-1},
\quad
\frac{2(p-a)(a-1)}{p+a-2},
\quad
\frac{a-1}{p-1}
\]

이므로 모두 음이 아니다. 또한 (a<p)에서 네 분모는 양수다. 따라서

\[
d:=g+n\le(p-a)+(a-1)=p-1.
\]

직접 정리하면

\[
\left(1-\frac1p\right)\left(1+\frac1d\right)-1
=\frac{p-1-d}{pd}\ge0.
\]

Maynard iteration에서 비제외 (p\nmid W_{j+1}\prod_{i>j+1}e_i)이면 현재 좌표
(j+1)도 (p)를 받을 수 있다. 그러므로 이전 좌표의 허용 개수 (n_j(p))는 전체
상계 (a)보다 적어 (n_j(p)\le a-1)이고 정리를 적용할 수 있다. □

### 적용 범위 경고

`g(p)=p+O(k)`라는 기호만으로는 (g(p)\le p-a)를 얻지 못한다. 따라서 이 보조정리는
추상 Lemma 8.4 전체가 아니라 §3에서 원식이 확인된 actual call에만 적용한다.

## 5. 제외 소수의 정확한 합성

한 단계에서

\[
Q_j=\widetilde W_{j+1}\prod_{i=j+2}^{r}e_i
\]

로 둔다. (p\mid Q_j)이면 (gamma_j(p)=0)이므로 local factor는 (1-1/p)다.
§4에 의해 나머지 factor는 모두 1 이상이므로

\[
\boxed{
c_{\gamma,j}\ge
\prod_{p\mid Q_j}\left(1-\frac1p\right)
=\frac{\varphi(Q_j)}{Q_j}
}.
\]

이 식은 작은 제외 소수와 큰 제외 소수를 하나의 유한 정수로 묶는다. 원문의
\(W=\prod_{p\le2k^2,\,p\nmid B}p\) 정의상 작은 소수 \(p\)는
\(p\nmid B\)이면 \(W\)에, \(p\mid B\)이면 \(B\)에 들어간다. 따라서 \(WB\), 그리고
그 배수인 모든 유효 \(\widetilde W_i\)가 \(p\le2k^2\)인 소수를 전부 포함한다는
호출 가정을 확인한 경우, \(k\ge2\)이므로

\[
Q_j\ge2\cdot3\cdot5\cdot7=210.
\]

## 6. 정본 base (W_i)의 숨은 지수 제거

Maynard 385행에서

\[
D=\prod_{i=1}^{k}|a_i|
\prod_{i\ne\ell}|a_i b_\ell-b_i a_\ell|
\]

의 소인수를 제외하면 (omega(p)=k)다. 396--407행의 (W_i) 구성상 모든
(W_i)의 소인수는 (WBD)의 소인수 안에 있다. (W_i)는 square-free이므로

\[
W_i\le W B D.
\]

계수 가정 (|a_i|,|b_i|\le x^\alpha)에서

\[
D\le
2^{k(k-1)}x^{\alpha(2k^2-k)}.
\]

또한 (W=\prod_{p\le2k^2,p\nmid B}p\le(2k^2)^{2k^2}),
(B\le x^\alpha), (R\ge x^{\theta/10})이므로

\[
W_i\le
(2k^2)^{2k^2}2^{k(k-1)}
R^{10\alpha(2k^2-k+1)/\theta}.
\]

각 (e_i\le R)이므로, **유효 모듈이 정본 (W_i) 자체인 호출에 한해** 다음 식은
(log Q_j)의 명시적 상계다.

\[
\boxed{
\begin{aligned}
\Lambda^{\rm base}_j={}&2k^2\log(2k^2)+k(k-1)\log2\\
&+\left\{
\frac{10\alpha(2k^2-k+1)}{\theta}
+r-j-1
\right\}\log R.
\end{aligned}
}
\]

이는 날카로운 상계가 아니라 base (W_i)의 hidden (O(k^2))를 없애기 위한
안전한 상계다. §3.1의 확대 모듈에는 자동으로 적용하지 않고, H1b-1b-2a.1에서
각 호출을 별도로 인증했다.

호출별로

\[
\widetilde W_i\mid A_{\rm app,i}W_i,
\qquad
\eta_{\rm app,i}\ge\log A_{\rm app,i}
\]

를 증명한 뒤에만

\[
\Lambda^{\rm app}_j=
\Lambda^{\rm base}_j+\eta_{\rm app,j}
\]

를 사용한다. 구현도 일반 함수에서는 `application_log_overhead`를 필수 인수로
요구하여 미감사 호출에서 0을 자동 대입하지 않는다. 이름이 고정된 11개 actual
application만 전수감사 spec을 통해 0 또는 (log R)을 가져온다.

## 7. Rosser--Schoenfeld의 조건부 (c_{\min}) 변환

Theorem 15의 예외안전형은 모든 정수 (N\ge3)에서

\[
\frac{N}{\varphi(N)}
<e^\gamma\log\log N+
\frac{2.50637}{\log\log N}
\]

이다. 호출별 감사로 (210\le Q_j\le e^{\Lambda^{\rm app}_j})를 얻었다면
(loglog Q_j>1)이고

\[
\frac{Q_j}{\varphi(Q_j)}
<e^\gamma\log\Lambda^{\rm app}_j+2.50637.
\]

따라서 더 날카로운 explicit 식은

\[
c_{\gamma,j}>
\frac{1}{e^\gamma\log\Lambda^{\rm app}_j+2.50637}.
\]

또한 (0<\gamma<1), (e<3), (2.50637<3)이라는 초등 약화를 쓰면

\[
\boxed{
c_{\gamma,j}>
c_{\min,j}:=
\frac{1}{3(1+\log\Lambda^{\rm app}_j)}
}.
\]

이 변환 자체는 explicit하다. 그러나 모든 (j=0,\ldots,r-1)에 하나의 하한을 쓰려면
각 호출의 (eta_{\rm app,j})를 먼저 닫고 그 최대값을 사용해야 한다. 현재는
base 식의 (j=0)이 최악이라는 사실만으로 실제 전체 호출의 최악값을 정할 수 없다.

## 8. 교정된 GGPY 절대오차에 미치는 영향

H1b-1b에서 얻은 안전한 절대오차 전달은

\[
C_{4,\mathrm{abs}}\le2C_{3,\mathrm{abs}}
\]

이다. 호출별 (Lambda^{\rm app}_j)를 인증한 뒤에는 상대 multiplier를

\[
\boxed{
C_{4,\mathrm{rel},j}
\le6C_{3,\mathrm{abs}}(1+\log\Lambda^{\rm app}_j)
}.
\]

로 둘 수 있다. H1b-1b-2a.1은 모든 추적 호출에 대해
(\Lambda^{\rm app}_j\le\Lambda_*)를 닫았다. 따라서 actual-call 제외모듈 때문에
추가되던 불확실성은 사라졌다. 다만 아직 숫자가 없는 (C_{3,\mathrm{abs}}),
(A_1,A_2,L), finite range와 모든 multiplier를 넣어 (r)-회 귀납을 다시 써야
finite theorem으로 승격할 수 있다.

## 9. 상태 변화와 남은 blocker

| obligation | 이전 | 현재 | 설명 |
|---|---|---|---|
| `CMIN-NONEXCLUDED` | `RATE_MISSING` | `PROJECT_FINITE_COMPONENT_CLOSED_FOR_ACTUAL_CALLS` | actual 네 family factor \(\ge1\) |
| `CMIN-SMALL-EXCLUDED` | `RATE_MISSING` | `PRIMARY_EXPLICIT_BOUND_AVAILABLE` | totient 식에 통합 |
| `CMIN-LARGE-EXCLUDED` | `RATE_MISSING` | `PROJECT_PARAMETERIZED_EXPLICIT_FOR_ALL_TRACED_APPLICATIONS` | 11개 subapplication에서 \(\Lambda^{\rm app}_j\le\Lambda_*\) |
| `CMIN-COMPOSE` | `PARAMETERIZED_EXPLICIT` | `PROJECT_PARAMETERIZED_EXPLICIT_FOR_ALL_TRACED_APPLICATIONS` | 공통 \(c_{\min}>1/[3(1+\log\Lambda_*)]\) |
| `ROUTE-DECISION` | `HARD_BLOCKER` | `PRIMARY_EXPLICIT_LOWER_BOUND_ROUTE_SELECTED` | lower-bound normalization 경로 선택 완료 |
| `RFOLD-COMPOSITION` | `HARD_BLOCKER` | `HARD_BLOCKER` | 새 손실을 포함한 재합성 필요 |
| `SIV-07` | `HARD_BLOCKER` | `HARD_BLOCKER` | base constant와 나머지 moment 상수 미복원 |
| (X_{\mathrm{cert}}) | `OPEN` | `OPEN` | threshold 계산 금지 유지 |

남은 핵심은 다음과 같다.

1. Kuperberg/HR recurrence에서 (C_{3,\mathrm{abs}}(A_1,A_2))와 최초 유효범위를 복원한다.
2. Maynard 575--579행의 (A_1,A_2,L)을 actual call 전부에 대해 수치화한다.
3. 인증된 공통 (Lambda_*)를 넣어 Lemma 8.4의 (r)-회
   binomial error를 다시 합성한다.
4. 그 뒤에만 Lemmas 8.5--8.6과 Propositions 9.1--9.5의 moment error budget으로 진행한다.

## 10. 자동 검증 계약

`tests/test_h1b1b2a_local_factor_lower_bound.py`는 다음을 확인한다.

- 네 family의 exact rational (g\le p-a)
- 모든 시험 (0\le n\le a-1)에서 local factor가 1 이상
- 극단 (g=p-a,n=a-1)에서 factor가 정확히 1
- 제외 소수 \(2,3,5,7\)의 곱이 \(\varphi(210)/210=8/35\)
- base (\Lambda^{\rm base}_j)가 (j)에 따라 감소하는지
- `application_log_overhead`가 누락되거나 음수이면 fail-closed하는지
- Rosser--Schoenfeld 식이 초등 약화보다 강한지
- 기계 원장이 abstract (p+O(k)), `SIV-07`, (X_{\mathrm{cert}})를 닫지 않는지

별도 `tests/test_h1b1b2a1_application_exclusion_inventory.py`는 10개 source call,
11개 analytic subapplication, 세 개의 (log R) overhead, (W_0) 지수 지배와
공통 (Lambda_*) 최댓값을 검증한다.

수치 grid는 대수 증명의 대체물이 아니라 구현 회귀검사다. 본 보조정리의 증명은 §4--§7이다.

## 11. 사용자 수행사항

별도 수행절차 필요없음. 이 단계는 문헌·대수 감사와 데이터 비의존 단위시험이다.
Lean이나 새 Python 라이브러리는 필요하지 않다.
