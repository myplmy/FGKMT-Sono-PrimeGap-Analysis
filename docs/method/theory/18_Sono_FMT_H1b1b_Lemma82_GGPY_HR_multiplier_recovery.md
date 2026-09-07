# Sono/FMT H1b-1b Maynard Lemma 8.2·GGPY/HR multiplier 복원과 오류항 교정

- 작성일: 2026-09-06
- 대상: Maynard, *Dense Clusters of Primes in Subsets*, Lemma 8.2와
  GGPY, *Small Gaps Between Products of Two Primes*, Lemmas 3–4,
  Kuperberg arXiv:2210.09775v2, Castillo et al. arXiv:1403.5808
- 상위 obligation: SIV-07
- 기계 계약:
  docs/method/theory/data/Sono_FMT_H1b1b_Lemma82_GGPY_HR_multiplier_v1.json
- 후속 proof-obligation 원장:
  [H1b-1b-2 c_gamma 오류 정규화·Lemma 8.4 보정](19_Sono_FMT_H1b1b2_cgamma_error_normalization_ledger.md)
- actual-call local-factor·제외모듈 후속 정식화:
  [H1b-1b-2a local-factor·제외모듈 하한](20_Sono_FMT_H1b1b2a_actual_local_factor_lower_bound.md)
  및 [H1b-1b-2a.1 application 전수감사](21_Sono_FMT_H1b1b2a1_application_exclusion_inventory.md)
- 판정:

~~~text
Maynard Lemma 8.2 multiplier       = 89 (PROJECT FINITE COMPONENT CLOSED)
GGPY Lemma 3 -> Lemma 4 transfer  = C4_abs <= 2 C3_abs (PARAMETERIZED)
printed c_gamma-relative error     = NOT JUSTIFIED BY STATED HYPOTHESES
modern HR structural reproduction = REVIEWED; NUMERICAL RATE/CUTOFF OPEN
Maynard Lemma 8.4 composition      = OPEN
SIV-07 / X_cert                    = OPEN
~~~

## 1. 쉬운 요약

이번 작업은 두 종류의 “숨은 상수”를 구분했다.

첫째, Maynard Lemma 8.2의 \(O(\cdot)\) 안에 숨어 있던 수는 선택한 cutoff를 직접 미분하고
부등식을 다시 전개해 **89**라는 안전한 숫자로 바꿨다. 이는 원문의 정성적 “어떤 상수가
존재한다”를 이 프로젝트에서 실제로 사용할 수 있는 유한 부등식으로 바꾼 것이다.

둘째, GGPY Lemma 4의 부분적분 자체는 바로 아래 Lemma 3의 **절대오차** 상수를
\(C_{3,\mathrm{abs}}(A_1,A_2)\)라고 부르면 최대
\(2C_{3,\mathrm{abs}}(A_1,A_2)\)로 전달된다. 그러나 Castillo et al.이 지적했듯이 GGPY와
Maynard에 인쇄된 오류항의 \(c_\gamma\) 인자는 원래 가정만으로 따라오지 않는다. 따라서
기존 문서가 가정했던
\(\lvert E\rvert\le C_3c_\gamma(L+1)\) 계약을
\(\lvert E\rvert\le C_{3,\mathrm{abs}}(L+1)\)로 교정했다.

셋째, Kuperberg는 HR Lemma 5.4를 따라가는 현대적 증명을 공개해 구조적 source blocker를
상당 부분 해소한다. 하지만 그 증명도 \(B_L,B_k\)와 여러 \(O\)-상수를 숫자로 주지 않고,
특수한 prime-tuple sieve function을 다룬다. 그러므로 Maynard Lemma 8.4 전체에 쓸 수 있는
숫자 \(C_{3,\mathrm{abs}}\)와 공통 시작점은 아직 없다.

비유하면, 첫 기어의 배율 89는 확정됐다. 둘째 기어는 절대오차를 두 배 이하로 전달한다.
그런데 원래 도면은 이 오차에 작은 할인율 \(c_\gamma\)가 자동 적용된 것처럼 적었다.
그 할인은 공짜가 아니며 별도 조건이나 \(c_\gamma\) 하한 증명이 필요하다. 따라서 전체 기계의
최종 배율과 작동 시작점은 여전히 계산할 수 없다.

## 2. 1차 출처와 provenance

| 출처 | 확인 위치 | 이번 판정 |
|---|---|---|
| James Maynard, *Dense Clusters of Primes in Subsets*, DOI 10.1112/S0010437X16007296, arXiv 1405.2593 | Section 8의 \(F,F_2\), Lemma 8.2, 식 (8.6)–(8.8), 출판본 16–18쪽 | 출판 PDF와 arXiv TeX를 식 단위로 대조 |
| Goldston–Graham–Pintz–Yıldırım, *Small Gaps Between Products of Two Primes*, DOI 10.1112/plms/pdn046, arXiv math/0609615 | Lemmas 3–4, PDF 9–10쪽; TeX 803–882행 | 조건, norm, 부분합 공식을 직접 대조 |
| GGPY corrigendum, DOI 10.1112/plms/pds053 | 서지·수정 대상 metadata | 출판사 PDF 접근 제한으로 본문은 미검토 |
| Halberstam–Richert, *Sieve Methods* | Lemma 5.3: 인쇄 144쪽; Lemma 5.4: 인쇄 147–152쪽 | Google Books 검색으로 위치 확인, 전체 proof는 제한되어 수치 복원 불가 |
| Vivian Kuperberg, *Sums of singular series with large sets and the tail of the distribution of primes*, DOI 10.1093/qmath/haad030, arXiv:2210.09775v2 | Lemma 4.3과 proof, PDF 16–19쪽 | HR 5.4 구조 재현 확인; \(B_L,B_k,O\)-상수와 일반화는 비명시적 |
| Castillo–Hall–Lemke Oliver–Pollack–Thompson, *Bounded gaps between primes in number fields and function fields*, DOI 10.1090/S0002-9939-2015-12554-3, arXiv:1403.5808 | Lemma 2.5와 직후 Remark·proof, PDF 11쪽 | GGPY/Maynard 오류항의 \(c_\gamma\) 문제 확인 |

로컬 hash와 취득시각은 기계 계약의 source_registry에 고정했다. GGPY arXiv source 응답은
파일명이 .tar였지만 실제 형식은 **단일 TeX를 gzip으로 압축한 payload**였다. 처음 이를 tar로
해제하려 한 시도는 잘못된 0-byte 항목들을 만들며 실패했다. 원본 hash를 유지한 채 gzip stream으로
다시 풀었고, 이후 감사에는 SHA-256
e58cc895e8b44f6369741f184bd81b595ed177463cf09cee8d0ad74558efce45인 TeX만 사용했다.
이는 도구 처리 실패이며 논문의 오류가 아니다. 2026-09-06 추가 PDF·source의 URL, 취득 UTC,
SHA-256과 TeX 행 범위도 기계 계약에 고정했다.

## 3. Maynard Lemma 8.2의 명시적 상수

### 3.1 고정된 함수

H1b-1a에서 다음 cutoff를 고정했다.

\[
0\le\psi\le1,\qquad
\psi(t)=1\ (0\le t\le9/10),\qquad
\operatorname{supp}\psi\subset[0,1],\qquad
\|\psi'\|_\infty<50.
\]

Maynard의 표기를 따라

\[
T_k=k\log k,\qquad U_k=k^{-1/2},
\]

\[
F(\mathbf t)=\psi\!\left(\sum_i t_i\right)
\prod_i\frac{\psi(t_i/U_k)}{1+T_kt_i},
\]

\[
F_2(\mathbf t)=\sum_j
\frac{\psi(t_j/2)}{1+T_kt_j}
\prod_{i\ne j}\frac{\psi(t_i/U_k)}{1+T_kt_i}
\]

로 둔다.

### 3.2 한 좌표를 움직일 때의 직접 부등식

\(\mathbf v=\mathbf u+\delta\mathbf e_j\), \(\delta\ge0\)라 하자. \(u_j\ge U_k\)이면
\(\psi(u_j/U_k)=0\)이고 단조성 때문에 \(F(\mathbf u)=F(\mathbf v)=0\)이다.

이제 \(u_j<U_k\), \(0\le\delta\le1\)인 경우를 본다. \(j\) 이외 좌표의 곱을

\[
P=\prod_{i\ne j}\frac{\psi(u_i/U_k)}{1+T_ku_i}
\]

로 쓰고, 전체합 cutoff·좌표 cutoff·분모의 차이를 각각 한 번씩 삼각부등식으로 분리하면

\[
|F(\mathbf v)-F(\mathbf u)|
\le
\delta\left[T_k+50\left(1+\frac1{U_k}\right)\right]
\frac{P}{1+T_ku_j}.
\]

\(u_j<U_k\le1/\sqrt2\)이므로 \(\psi(u_j/2)=1\)이고, 마지막 항은 \(F_2(\mathbf u)\)의
\(j\)번째 항 이하이다. 따라서

\[
|F(\mathbf v)-F(\mathbf u)|
\le
T_k\delta\left[1+\frac{50(1+\sqrt k)}{k\log k}\right]F_2(\mathbf u).\tag{H1b-1b.1}
\]

이 전개는 원문의 \(1+O(T_k\delta)\)를 곱해 펼치는 대신 분모 차이를 정확히 계산했기 때문에,
숨은 교차항이나 “\(\delta\)가 충분히 작다”는 추가 가정을 만들지 않는다.

### 3.3 \(k\ge2\)에서 89로 통일

양의 항만 취한 급수와 유리수 비교로

\[
\log2
=2\sum_{n\ge0}\frac{1}{(2n+1)3^{2n+1}}
>2\left(\frac13+\frac1{81}\right)
=\frac{56}{81}>\frac{69}{100},
\]

\[
\frac1{\sqrt2}<\frac{71}{100}
\]

이다. 모든 정수 \(k\ge2\)에서

\[
\frac{1/k+1/\sqrt{k}}{\log k}
<\frac{1/2+71/100}{69/100}
=\frac{121}{69}.
\]

그러므로 (H1b-1b.1)의 대괄호는

\[
1+50\frac{121}{69}=\frac{6119}{69}<89.
\]

\(\delta>1\)이면 \(F(\mathbf u)\le F_2(\mathbf u)\)이고
\(89T_k\delta>1\)이므로 같은 부등식이 더 쉽게 성립한다. 따라서 Lemma 8.2(i)를

\[
\boxed{
|y_{\mathbf s}-y_{\mathbf r}|\le
89T_kY_{\mathbf r}\frac{\log A}{\log R}\qquad(k\ge2)
}\tag{H1b-1b.2}
\]

로 명시할 수 있다.

### 3.4 Lemma 8.2(ii)

\(t_i=[r_i,s_i]\)로 두고 각 좌표에 (H1b-1b.2)를 순서대로 적용한다. \(F_2\), 따라서
\(Y\)는 각 좌표에 대해 단조 비증가하므로 중간 단계의 \(Y\)를 출발점의 \(Y\)로 상계할 수 있다.
\(\mathbf s\to\mathbf t\)와 \(\mathbf r\to\mathbf t\)의 두 부등식을 삼각부등식으로 더하면

\[
\boxed{
|y_{\mathbf s}-y_{\mathbf r}|\le
89T_k(Y_{\mathbf r}+Y_{\mathbf s})\frac{\log A}{\log R}\qquad(k\ge2)
}.\tag{H1b-1b.3}
\]

두 경로의 오차가 이미 \(Y_{\mathbf r}+Y_{\mathbf s}\) 안에 따로 들어가므로 multiplier를 178로
다시 곱하지 않는다.

## 4. GGPY Lemma 3–4 오류항 감사

### 4.1 GGPY와 Maynard에 인쇄된 형태

GGPY Lemma 3은 multiplicative \(\gamma\)가 \((\Omega_1)\),
\((\Omega_2(\kappa,L))\)을 만족할 때 누적합을

\[
G(u)=c_\gamma\frac{(\log u)^\kappa}{\Gamma(\kappa+1)}+E(u)
\]

로 쓴다. GGPY Lemma 4와 Maynard Lemma 8.3에 인쇄된 오류항은
\(c_\gamma L\) 또는 \(c_\gamma(1+L)\)을 포함한다. Maynard가 Lemma 8.4에서 쓰는
경우는 \(\kappa=1\)이다.

### 4.2 peer-reviewed correction의 판정

Castillo et al. Lemma 2.5(PDF 11쪽)는 정수의 경우 \(c_A=1\)로 두면 주항에
\(c_\gamma\)가 있으나 안전한 오류항은

\[
O_{A_1,A_2,\kappa}
\left(L\,G_{\max}(\log z)^{\kappa-1}\right)
\tag{H1b-1b.4}
\]

처럼 \(c_\gamma\)를 포함하지 않는 형태로 제시한다. 직후 Remark는 GGPY와 Maynard가 더
강한 \(c_\gamma\)-포함 오류항을 썼지만, 그 증명은 \(z\)가 \(L\)에 비해 더 크다는 추가
가정 아래에서만 그 형태를 지지한다고 명시한다. 저자들은 자신들의 정성적 응용에서는 다른
더 큰 오류항에 흡수되므로 문제가 없다고 설명한다.

따라서 다음 두 문장은 동시에 참이다.

- 이 지적은 실제이며 \(\kappa=1\)에도 적용된다.
- 이것만으로 GGPY나 Maynard의 최종 정성적 정리가 틀렸다고 결론낼 수는 없다.

Maynard 출판본이 Lemma 8.3 뒤에 추가한 “일반 \(\kappa\)에서는
\(c_\gamma(L+1)^\kappa\)가 필요하지만 \(\kappa=1\) 응용에는 영향 없다”는 주석은 다른
문제다. 그 주석은 이번에 확인한 “오류항 앞 \(c_\gamma\)가 원 가정만으로 나오는가”를
해결하지 않는다.

### 4.3 교정된 절대오차에서 factor 2

어떤 명시적 \(C_{3,\mathrm{abs}}(A_1,A_2)>0\)와 공통 범위에서

\[
|E(u)|\le C_{3,\mathrm{abs}}(A_1,A_2)(L+1)
\qquad(1\le u\le z)\tag{H1b-1b.5}
\]

를 얻었다고 가정한다. Stieltjes 부분적분과

\[
M(F)=\sup_{0\le x\le1}\bigl(|F(x)|+|F'(x)|\bigr)
\]

을 사용하면 경계항 한 번과 미분 적분항 한 번으로

\[
\left|\int_{1^-}^{z}F\!\left(\frac{\log(z/u)}{\log z}\right)dE(u)\right|
\le 2C_{3,\mathrm{abs}}(L+1)M(F).\tag{H1b-1b.6}
\]

따라서 안전하게 닫힌 것은

\[
\boxed{C_{4,\mathrm{abs}}\le2C_{3,\mathrm{abs}}}.\tag{H1b-1b.7}
\]

이라는 **절대오차 전달계수 2**다. \(C_{3,\mathrm{abs}}\)의 숫자와 범위는 여전히
미복원이다.

Maynard에 인쇄된 상대오차 형태로 되돌리려면 모든 호출에서
\(c_\gamma\ge c_{\min}>0\)을 별도로 증명해야 한다. 그러면

\[
2C_{3,\mathrm{abs}}(L+1)M(F)
\le
\frac{2C_{3,\mathrm{abs}}}{c_{\min}}\,
c_\gamma(L+1)M(F).\tag{H1b-1b.8}
\]

즉 상대 multiplier는 \(2C_{3,\mathrm{abs}}/c_{\min}\)이다. \(c_{\min}=1\)을 임의로
넣거나 오류항에 \(c_\gamma\)를 다시 붙이는 것은 금지한다.

## 5. Kuperberg arXiv:2210.09775가 제공하는 것

Kuperberg Lemma 4.3(PDF 17쪽)는 HR Lemma 5.4를 따라 특수한 prime-tuple sieve
function \(\nu_{\mathcal H}\)에 대해

\[
\frac1{G(z)}
=W(z)e^{\gamma\kappa}\Gamma(\kappa+1)
\left(1+O\!\left(\frac{L+\kappa^4}{\log z}\right)\right)
\tag{H1b-1b.9}
\]

형태를 재현한다. 적용 가정에는 어떤 충분히 큰 \(B_L,B_\kappa\)에 대해

\[
L\le\frac{\log z}{B_L},
\qquad
\kappa^2\le\frac{\log z}{B_\kappa}
\tag{H1b-1b.10}
\]

가 들어간다. proof는 HR 5.2–5.4의 recurrence와 Euler product tail을 상당히 자세히
재현한다. 이는 Castillo et al.의 “\(z\) 대 \(L\) 추가 크기조건 아래 더 강한 상대오차를
구제할 수 있다”는 설명과 구조적으로 일치한다.

그러나 다음 때문에 현재 목표를 닫지는 못한다.

1. \(B_L,B_\kappa\)와 \(O(k)\), \(O(k^3/\log a)\), \(O(k^4)\)의 multiplier가 숫자가 아니다.
2. \(\nu_{\mathcal H}\)라는 특수 함수에 대한 결과이지, Maynard Lemma 8.4에서 좌표마다 생기는
   모든 \(\gamma\)에 대한 uniform theorem이 아니다.
3. “나머지는 HR proof와 동일”한 단계에 원 HR 상수 의존성이 남는다.
4. Lemma 8.4의 \(r\)회 반복에서 같은 조건과 같은 error budget이 유지되는지 증명하지 않는다.

따라서 HR 원문만이 유일한 blocker였다는 과거 설명은 고친다. 현대의 접근 가능한 구조적
재현은 확보했지만, blocker는 이제 **수치 multiplier·유효범위·일반화·오류 정규화**다.
원 HR 140–153쪽은 여전히 계보와 누락된 상수 확인에 유용하지만, 그것만 확보한다고 자동으로
\(X_{\mathrm{cert}}\)가 계산되지는 않는다.

## 6. Maynard Lemma 8.4에 생긴 새 proof obligation

Maynard Lemma 8.4 proof는 Lemma 8.3을 좌표별로 \(r\)회 적용한다. 인쇄된 전개는 각 단계
오류항에도 해당 단계의 Euler product \(c_{\gamma,j}\)가 붙는 것을 이용해 모든 주항 곱과
같은 공통 인자를 꺼낸 뒤 \(O(r\varepsilon)\)로 모은다.

교정된 절대오차에서는 이 인수분해가 자동이 아니다. 다음 셋 중 하나를 새로 증명해야 한다.

1. **크기조건 경로:** 모든 단계에서 명시적인 \(z\)-대-\(L\) 조건을 만족시켜
   \(c_{\gamma,j}\)-포함 오류항 자체를 복원한다.
2. **Euler 곱 하한 경로:** 모든 단계의 \(c_{\gamma,j}\ge c_{\min,j}>0\)를 명시적으로
   증명하고, \(\prod_j c_{\gamma,j}\)에 대한 상대 손실을 전부 추적한다.
3. **직접 다변수 경로:** 절대오차들을 공통 주항에 대해 다시 합성해 더 나은 전역 경계를
   직접 증명한다.

2026-09-07 H1b-1b-2a.1은 두 번째 경로를 추적된 actual call 전체에서 선택했다. 네 prime-local denominator
family에서 비제외 local factor가 1 이상임을 증명하고, 유효 제외 소수를
\(Q_j=\widetilde W_{j+1}\prod_{i=j+2}^{r}e_i\)에 합치면

\[
c_{\gamma,j}\ge\frac{\varphi(Q_j)}{Q_j}
>
\frac{1}{3(1+\log\Lambda_*)}
\]

가 된다. 실제 호출의 \(dW_i,W_i',a_mWBr,rW_m,W_0\)를 11개
analytic subapplication으로 분해했고, 모든 호출·iteration에서
\(\Lambda^{\rm app}_j\le\Lambda_*\)를 인증했다. 따라서 절대오차 상수가 복원되면
상대오차 multiplier를

\[
C_{4,\mathrm{rel},j}
\le 6C_{3,\mathrm{abs}}(1+\log\Lambda_*)
\]

로 parameterize할 수 있다. 현재 \(C_{3,\mathrm{abs}}(A_1,A_2)\),
공통 finite range, 실제 \(A_1,A_2,L\), 그리고 이 손실을 포함한 \(r\)-회 합성은 열려 있다.
추상 조건 \(g(p)=p+O(k)\) 전체에도 이 하한을 일반화하지 않는다. 그러므로 local
normalization route는 진전했지만 Lemma 8.4는 계속 RATE_MISSING이고 SIV-07과
\(X_{\mathrm{cert}}\)도 OPEN이다.

## 7. 상태 변경과 바뀌지 않은 것

| obligation | 과거 상태 | 현재 상태 | 의미 |
|---|---|---|---|
| H1B1-L82-LIPSCHITZ | RATE_MISSING | PROJECT_FINITE_COMPONENT_CLOSED | multiplier 89, \(k\ge2\), 영향 없음 |
| H1B-L82 | RATE_MISSING | PROJECT_FINITE_COMPONENT_CLOSED | Lemma 8.2 자체는 닫힘 |
| H1B1-L83-GGPY4 | PARAMETERIZED_EXPLICIT | PARAMETERIZED_EXPLICIT | 절대오차에 한해 \(C_{4,\mathrm{abs}}\le2C_{3,\mathrm{abs}}\) |
| H1B1-L83-GGPY3 | SOURCE_ACCESS_BLOCKED | RATE_MISSING | 현대 구조 재현은 확보, 숫자·범위·일반화는 open |
| H1B1B2-CMIN-COMPOSE | PARAMETERIZED_EXPLICIT | PROJECT_PARAMETERIZED_EXPLICIT_FOR_ALL_TRACED_APPLICATIONS | 공통 \(\Lambda_*\) 인증 |
| H1B1B2-ROUTE-DECISION | HARD_BLOCKER | PRIMARY_EXPLICIT_LOWER_BOUND_ROUTE_SELECTED | actual 제외모듈 전수감사 완료 |
| H1B-L83 | RATE_MISSING | RATE_MISSING | \(C_{3,\mathrm{abs}},A_1,A_2,L\), finite range 필요 |
| H1B1-L84-ITERATION | RATE_MISSING | RATE_MISSING | 새 \(O(\log\log R)\) normalization 손실을 넣어 \(r\)회 합성 재증명 필요 |
| H1B1-PACKAGE | HARD_BLOCKER | HARD_BLOCKER | 공통 cutoff와 multiplier 없음 |
| SIV-07 | HARD_BLOCKER | HARD_BLOCKER | 변화 없음 |
| \(X_{\mathrm{cert}}\) | OPEN | OPEN | 계산 불가 |

Lemma 8.2에서 \(T_k\)와 \(Y\)가 기호로 남는 것은 숨은 상수가 남았다는 뜻이 아니다.
반면 \(C_{3,\mathrm{abs}}\), \(c_{\min}\), \(B_L,B_\kappa\)는 실제 숫자와 공통 범위가
필요한 입력이다.

## 8. 기계검증 계약

source/h1b1b_multiplier_recovery.py와 tests/test_h1b1b_multiplier_recovery.py는 다음을
확인한다.

- \(\log2>69/100\), \(1/\sqrt2<71/100\), \(6119/69<89\)의 exact rational chain
- 여러 \(k\), support 경계, 작은·큰 \(\delta\)에서 \(F,F_2\) 회귀검사
- 교정된 절대오차 전달 \(C_{4,\mathrm{abs}}=2C_{3,\mathrm{abs}}\)
- actual-call 네 family의 비제외 local factor와 11개 application 제외모듈 상계 회귀검사
- 일반 함수는 application overhead가 없으면 실패하고, 이름이 고정된 actual call만 감사값을 사용하는 회귀검사
- 추상 \(g(p)=p+O(k)\), 숫자 없는 \(C_{3,\mathrm{abs}}\), 미합성 \(r\)-fold
  error가 parent를 닫지 못하도록 하는 negative regression
- Maynard Lemma 8.2 child만 닫고 Lemma 8.4, package, SIV-07,
  \(X_{\mathrm{cert}}\)를 fail-closed로 유지하는지
- 문헌 source hash와 기계 원장 상태의 일치

수치 grid는 구현 회귀검사이고 §3의 전 구간 증명을 대신하지 않는다. 이번 gate에는 Lean이나
새 Python 라이브러리가 필요하지 않다.

## 9. 다음 권장 순서

1. **H1b-1b-2b base multiplier 복원:** Kuperberg/HR recurrence에서
   \(C_{3,\mathrm{abs}}(A_1,A_2)\)와 최초 유효범위를 숫자로 복원한다.
   8–24시간 이상이며 하위 \(O\)-상수가 새로 갈라지면 수일 이상 걸릴 수 있다.
2. **actual-call 입력 수치화:** Maynard 575–579행의 \(A_1,A_2,L\)을 모든 실제 호출에
   대해 하나의 공통 식과 범위로 고정한다. 6–16시간 이상.
3. **Lemma 8.4 재합성:** 위 입력에
   \(6C_{3,\mathrm{abs}}(1+\log\Lambda_*)\) 손실을 넣어 \(\Omega_G\)와 \(r\)-fold
   error를 한 공통 범위에 묶는다. 8–24시간 이상.
4. **H1c-1 병렬 이론축:** quantitative character/Bombieri–Vinogradov package를 복원한다.
5. 모든 root dependency가 숫자와 공통 범위로 닫힌 뒤에만 threshold calculator와
   \(X_{\mathrm{cert}}\) 계산을 설계한다.

현재 CPU actual 실험이나 장시간 runner를 돌릴 단계가 아니다. 사용자에게 필요한 즉시 수행절차는
없다. HR 원문 140–153쪽을 합법적으로 구할 수 있다면 추가 대조에 유용하지만 필수 선결조건으로
남겨 두지는 않는다.

## 참고문헌

- James Maynard, “Dense Clusters of Primes in Subsets,” *Compositio Mathematica* 152 (2016),
  DOI 10.1112/S0010437X16007296, arXiv:1405.2593.
- D. A. Goldston, S. W. Graham, J. Pintz, C. Y. Yıldırım, “Small Gaps Between Products of
  Two Primes,” *Proceedings of the London Mathematical Society* 98 (2009),
  DOI 10.1112/plms/pdn046, arXiv:math/0609615.
- 같은 저자, corrigendum, DOI 10.1112/plms/pds053.
- H. Halberstam and H.-E. Richert, *Sieve Methods*, London Mathematical Society Monographs 4,
  Academic Press (1974); Dover reprint (2011), ISBN 9780486479392.
- Vivian Kuperberg, “Sums of singular series with large sets and the tail of the distribution
  of primes,” *Quarterly Journal of Mathematics* 74 (2023), 1457–1479,
  DOI 10.1093/qmath/haad030, arXiv:2210.09775.
- A. Castillo, C. Hall, R. J. Lemke Oliver, P. Pollack, L. Thompson,
  “Bounded gaps between primes in number fields and function fields,”
  *Proceedings of the American Mathematical Society* 143 (2015), 2841–2856,
  DOI 10.1090/S0002-9939-2015-12554-3, arXiv:1403.5808.
