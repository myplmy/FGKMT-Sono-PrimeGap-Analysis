# Sono/FMT H1b-COV2: post-covering 구간·예외·smooth remainder의 유한 합성

- 작성: 2026-09-10 KST.
- 증거 수준: SOURCE APPLICABILITY AUDIT + PROJECT FINITE ANALYTIC PROOF + bounded exact algebra checks.
- 독립 동료심사·Lean 형식 인증 아님.
- 결론: 고정된 \(A,\varepsilon,\eta\)와 아래 유한 gate 아래에서 actual post-covering
  `DEP-R08`은 **parameterized explicit**이다. `DEP-R09`–`DEP-R12`, broad
  `SIV-07/08/09`, 같은 \(2\times10^{-17}\)의 최종 오차 예산과 \(X_{\rm cert}\)는 OPEN이다.
- 계약: [COV2 successor JSON](data/Sono_FMT_H1bCOV2_post_covering_v1.json).

## 1. 먼저 선행 정리와 실제 source를 확인한 결과

| source | 원문 위치 | 채택한 내용·한계 |
|---|---|---|
| Sono, *An explicit lower bound for gaps between some consecutive primes* | printed pp.525–526, 538–542; Proposition 3.1, Proposition 6.1과 그 증명 | 고정 구간의 survivor asymptotic, \(\varepsilon\)-partition, \(m\)과 \(A'\), \(T=S_*\cup R\) 구조. 모든 \(o(1)\)의 수치 rate는 직접 보충해야 한다. |
| Ford–Maynard–Tao, *Chains of large gaps between primes* | PDF pp.8–11; §4–5 | smooth remainder의 \(u\log u\) 감쇠와 hypergraph fixed-subset 구조. smooth estimate에는 implied constant가 남는다. |
| Rosser–Schoenfeld (1962) | printed pp.65, 70–71; (2.7), Theorem 5 (3.18), Theorem 9 (3.32) | \(B<1\), prime harmonic upper bound, and \(\vartheta(t)<1.01624t<(21/20)t\). 아래 special-case Rankin 증명에 사용한다. |
| [theory 51](51_Sono_FMT_H1bCOR3_finite_local_count_partition.md) | §§3–6 | covering 전에 정한 유한 interval family의 상대오차 \(1/(100b^2)\)와 실패율. |
| [theory 53](53_Sono_FMT_H1bCOV1_full_residue_hypergraph_interface.md), [theory 54](54_Sono_FMT_H1bCOV1a_explicit_covering_constant.md) | §§3–8 | full residue cap·예외점·고정 subset 1·2점 moment, 충분한 \(C_0=100\). |

Sono와 FMT PDF는 native text를 먼저 읽고 위 핵심 page 전체를 렌더링해 분수선·floor·끝점을
대조했다. Rosser–Schoenfeld PDF는 scan-with-text-layer이므로 text는 locator로만 쓰고 원본
page에서 채택 식을 대조했다. 새 OCR이나 원본 수정은 없다.

명시적 smooth-number 선행 결과도 먼저 조사했다. 확인한 Waterloo 명시 bound는 이
parameter에서 필요한 \(u\log u\) 크기의 감쇠를 주지 못했고, 확인한 sharp lecture-note 형태는
여전히 implied constant를 가진다. 따라서 “선행연구가 없다”거나 novelty를 주장하지 않고,
FMT가 사용한 Rankin 구조를 Rosser–Schoenfeld 명시식과 결합해 **이 actual parameter만**
직접 유한화한다.

## 2. 표기·양화와 선행 입력

이 문서의 \(X\)는 최종 maximal-gap 변수와 아직 연결되지 않은 **보조 sieve 변수**다.

\[
 a=\log X,\qquad b=\log a,\qquad q=\log b,\qquad
 c=\frac1{153600\log5},\qquad
 Y=cXa\frac q b.
 \tag{55.1}
\]

기존 child 조건 \(X\ge2\exp(10^{1000})\), \(b>2000\)와 theories 51·53·54의 모든
actual 가정을 유지한다. 최종 coefficient 예산에서 나중에 정할 상수들을 여기서는
\[
 A\ge1,\qquad0<\varepsilon\le1,\qquad0<\eta\le\frac14
 \tag{55.2}
\]
로 **무작위 residue와 covering을 고르기 전에 고정**한다. 이번 단계가 그 실제 값이나 최적값을
선정했다는 뜻은 아니다.

`S_*`는 \(Q'\cap\mathscr S(\mathbf A)\cap\mathscr S(\mathbf n)\)의 실제 surviving-prime
집합, \(T\)는 모든 \(p\le X\) residue를 확장한 뒤의 sifted integer 집합이다. FMT §4에 따라
\[
 S_*\subseteq T\subseteq S_*\cup R,
 \tag{55.3}
\]
여기서 \(R\)은 \(Y\) 이하의 \(z\)-smooth 수에 \(B_0\)의 거듭제곱을 곱한 예외다.

## 3. COV2a-1: 끝점에 안전한 동일 길이 격자

\[
 J=\left\lceil\frac2\varepsilon\right\rceil,\qquad h=\frac1J,\qquad
 I_j=((j-1)h,jh]\quad(1\le j\le J).
 \tag{55.4}
\]

ceil 정의만으로
\[
 \frac{\varepsilon}{2+\varepsilon}\le h\le\frac\varepsilon2,\qquad h\ge\frac\varepsilon3.
 \tag{55.5}
\]
격자는 서로소이고 \((0,1]\)을 정확히 덮는다. 임의의 \(0\le\alpha<\beta\le1\)에서
\((\alpha,\beta]\)와 만나는 **전체 cell**의 합집합을 \(U_{\alpha,\beta}\)라 하면, 양 끝에서
각각 한 cell 폭보다 더 늘어날 수 없으므로
\[
 |U_{\alpha,\beta}|\le(\beta-\alpha)+2h
 \le(\beta-\alpha)+\varepsilon
 \le2(\beta-\alpha)+\varepsilon.
 \tag{55.6}
\]

이 보정은 Sono printed p.538의 literal cell-count 문구를 수치 정본으로 삼지 않는다.
예를 들어 폭이 한 cell보다 훨씬 작은 구간도 cell 경계를 가로지르면 두 cell과 만날 수 있다.
(55.6)은 그 off-by-one 위험 없이 원문의 최종 \(2|\beta-\alpha|+\varepsilon\)을 보존한다.

스케일된 cell은 \(((j-1)hY,jhY]\)다. 정수 \(n\)에 대해
\(\alpha Y<n\le\beta Y\)는 정확히
\(\lfloor\alpha Y\rfloor+1\le n\le\lfloor\beta Y\rfloor\)이므로 별도 반올림 손실이 없다.
theory 51의 폭 조건에는
\[
 a\ge J^4
 \tag{55.7}
\]
만 추가하면 된다. \(J\)개 cell과 whole interval을 합친 family 크기는 \(K=J+1\)이다.
무한히 많은 \((\alpha,\beta)\)를 확률 union하는 것이 아니라, \(K\)개 고정 subset에 한 번
성공한 뒤 (55.6)을 결정론적으로 적용한다.

## 4. COV2a-2: \(m\), \(A'\)와 Vinogradov 조건의 유한 교체

\[
 R_A=\frac{80cb}{A},\qquad
 m=\lfloor\log_5R_A\rfloor,\qquad
 A'=5^{-m}80cb.
 \tag{55.8}
\]
다음 gate를 둔다.
\[
 R_A\ge5.
 \tag{55.9}
\]
그러면 \(m\ge1\), \(5^m\le R_A<5^{m+1}\)이므로 정확히
\[
 A\le A'<5A.
 \tag{55.10}
\]
또 \(80c/A<1\)이므로 \(R_A<b\), 따라서
\[
 m<\log_5b=\frac{\log_3X}{\log5}.
 \tag{55.11}
\]
이는 Sono p.541의 \(1\ll80c/A\le1\)을 숫자 없는 Vinogradov lower constant로 사용하지
않는다. 실제로 필요한 “\(m\)이 양의 정수이고 허용범위 안”이라는 사실을 (55.9)로 교체한 것이다.
여기서 \(1\ll\varepsilon_0\)도 \(\varepsilon_0>1\)이라는 뜻이 아니라 \(X\)와 독립인 양의
고정량이라는 asymptotic 표기이므로, 부등호의 일상적 의미로 읽지 않는다.

## 5. COV2a-3: 실제 cell 폭을 사용한 예외 복원

theory 51의 한 cell pre-cover count를 \(M_{0,j}\), 이상적 주항을
\[
 \mu_j=80ch\frac{Xb}{a},\qquad r_0=\frac1{100b^2}
 \tag{55.12}
\]
라 하면 outer good event에서 \(|M_{0,j}/\mu_j-1|\le r_0\)다. theory 53의 전체
예외 집합은 \(\#E\le\lfloor2X/(ab)\rfloor\), covering 생존비는
\(\rho=5^{-m}\)이고 \(\rho80cb=A'\ge A\)다. 따라서 각 cell에 대해
\[
 e_j:=\frac{#(E\cap I_jY)}{\rho M_{0,j}}
 \le\frac2{(1-r_0)Ahb}
 <\frac7{A\varepsilon b}.
 \tag{55.13}
\]
마지막에는 (55.5), \(1-r_0>99/100\)을 썼다. 이전의 subset-independent
\(8000/\sqrt b\)보다 훨씬 강한 **actual-width 복원식**이다.

covering moment의 허용오차를
\[
 t=\eta/8
 \tag{55.14}
\]
로 고정하고 다음 두 gate를 둔다.
\[
 r_0\le\eta/8,\qquad e_*:=\frac2{(1-r_0)Ahb}\le\eta/8.
 \tag{55.15}
\]
두 번째 식은 예외 제거 뒤 cell이 비어 있지 않음도 보장한다. 실제 survivor count를 \(Z_j\)라
하면 theory 53의 복원식과 pre-cover 정규화의 곱으로
\[
 \left|\frac{Z_j}{\rho\mu_j}-1\right|
 \le r_0+(1+r_0)(t+e_*)
 \le\frac{49}{128}\eta<\eta.
 \tag{55.16}
\]
whole interval도 같은 식에서 \(h\)를 1로 바꾸면 더 작으므로 같은 \(\eta\) bound를 쓴다.
예외를 지웠다가 공짜로 되돌린 것이 아니다.

## 6. COV2b-1: outer와 inner 성공사건의 순차 합성

먼저 random residue vector \(\mathbf A\)를 고른다. theories 51–53에서 \(K=J+1\) family를
포함한 outer failure bound는
\[
 F_{\rm out}=
 \frac{4800c}{b^5}+\frac{800c}{b^{10}}
 +\frac{112kb^4}{a^{11}}+\frac{3Kb^6}{a^{17}}.
 \tag{55.17}
\]
\(F_{\rm out}<1\)이면 한 good \(\mathbf A\)가 존재한다. 이를 먼저 고정한다.

그 고정값에서 cell과 whole interval subset들을 결정한 뒤 covering law를 적용한다. theory 53의
\[
 \epsilon_h=X^{-1/(20\cdot10^{m+1})},\qquad
 \xi=3^m/b,
 \tag{55.18}
\]
\[
 \alpha_h=(1+\epsilon_h)e^\xi-1,\qquad
 \beta_h=(1+\epsilon_h)e^{2\xi}-1
 \tag{55.19}
\]
를 쓴다. (55.15) 때문에 retained cell size \(M_j\ge M_{0,j}/2\), 따라서 모든 \(K\)개
subset의 centered-square 상대 bound는
\[
 v_*:=\beta_h+2\alpha_h+
 \frac{2(1+\alpha_h)a}{(1-r_0)AhX}
 \tag{55.20}
\]
이하이다. Markov와 finite union으로 inner failure는
\[
 F_{\rm in}:=\frac{Kv_*}{t^2}.
 \tag{55.21}
\]
\(F_{\rm in}<1\)이면 이 **이미 고정한** \(\mathbf A\)에 대해 한 covering outcome이 존재한다.

outer와 inner 확률공간의 독립성이나 \(F_{\rm out}+F_{\rm in}<1\)을 요구하지 않는다.
첫 단계에서 good \(\mathbf A\) 하나를 고른 뒤 그 조건부 공간에서 두 번째 성공값을 고르는
순차 존재증명이다. smooth remainder는 결정론적 count여서 제3의 확률사건이 아니다.

모든 gate는 유한식이다. 원한다면 각 항을 \(1/8\) 이하로 두는 더 보수적 충분조건으로 한 숫자
cutoff를 만들 수 있지만, 최종 \(A,\varepsilon,\eta\)를 R11에서 결정하기 전 그 숫자를
\(X_{\rm cert}\)처럼 고정하지 않는다.

## 7. COV2b-2: smooth remainder의 special-case 명시화

FMT의 정의를 그대로 써
\[
 z=X^{q/(4b)},\quad L=\log z=\frac{aq}{4b},\quad
 u=\frac{\log Y}{L}.
 \tag{55.22}
\]
다음 충분조건을 둔다.
\[
 b\ge e^{200},\qquad caq/b>1,\qquad
 w:=\log u+\log\log u,\qquad0<\delta:=w/L\le1/20.
 \tag{55.23}
\]
첫 두 식에서 \(Y>X\), \(u>4b/q\), \(w>100\)이다. 이 조건들은 fixed elementary expression의
방향성 있는 검사 대상이며 hidden \(O\)나 소수 전수계산이 아니다.

\(\Psi(Y,z)\)를 \(Y\) 이하의 \(z\)-smooth 양의 정수 개수라 하고
\(\alpha=1-\delta\)로 둔다. Rankin의 부등식은
\[
 \Psi(Y,z)\le Y^\alpha\prod_{p\le z}(1-p^{-\alpha})^{-1}
 =Y e^{-uw}\prod_{p\le z}(1-p^{-\alpha})^{-1}.
 \tag{55.24}
\]

### 7.1 Euler product의 명시 상계

Rosser–Schoenfeld (2.7)에서
\[
 B=\gamma+\sum_p\{\log(1-1/p)+1/p\}<\gamma<1
\]
이고, Theorem 5 (3.18)은 \(z\ge286\)에서
\[
 \sum_{p\le z}\frac1p
 <\log L+B+\frac1{2L^2}
 <\log L+\frac32.
 \tag{55.25}
\]
를 준다. 여기 \(L=\log z\ge20w\ge2000\)이므로 적용범위와 마지막 상계가 모두
명시적으로 충족된다.

이제
\[
 S_\delta:=\sum_{p\le z}\frac{p^\delta-1}{p},\qquad
 h(t):=\frac{t^\delta-1}{t\log t}
      =\int_0^\delta t^{v-1}\,dv.
 \tag{55.26}
\]
라 하자. \(0<\delta\le1/20\)이면 \(h\)는 \(t\ge1\)에서 양수이고 감소한다.
Rosser–Schoenfeld Theorem 9 (3.32)의
\(\vartheta(t)<1.01624t<(21/20)t\)와 Stieltjes 부분적분을 쓰면
\[
\begin{aligned}
 S_\delta
 &=\int_{1^-}^{z}h(t)\,d\vartheta(t)\\
 &\le\frac{21}{20}
 \left\{h(1)+\int_1^z h(t)\,dt\right\}\\
 &=\frac{21}{20}\{\delta+\operatorname{Ein}(w)\},
\end{aligned}
 \tag{55.27}
\]
여기서
\[
 \operatorname{Ein}(w):=\int_0^w\frac{e^v-1}{v}\,dv,
 \qquad \delta L=w.
\]
\(h(1)=\delta\)는 연속 연장값이다. 이 계산은 작은 소수 구간을 따로 잘라 생기는
경계항을 숨기지 않는다.

\(w\ge100\)에서 적분을 \([0,w/2]\)와 \([w/2,w]\)로 나눈다. 첫 구간에서는
\((e^v-1)/v\le e^v\), 둘째 구간에서는 \(t=w-v\)와
\((1-t/w)^{-1}\le1+2t/w\)를 써
\[
\begin{aligned}
 \int_0^{w/2}\frac{e^v-1}{v}\,dv
 &\le e^{w/2}
 \le\frac1{100}\frac{e^w}{w},\\
 \int_{w/2}^{w}\frac{e^v-1}{v}\,dv
 &\le\frac{e^w}{w}
 \int_0^\infty e^{-t}\left(1+\frac{2t}{w}\right)dt
 \le\frac{51}{50}\frac{e^w}{w}.
\end{aligned}
 \tag{55.28}
\]
첫 줄의 두 번째 부등식은 \(we^{-w/2}\)가 \(w\ge100\)에서 감소하고
\(100e^{-50}<100/2^{50}<1/100\)인 데서 따른다. 따라서
\[
 \operatorname{Ein}(w)\le\frac{103}{100}\frac{e^w}{w}.
\]
또 \(\delta\le1/20<e^w/(20w)\), \(e^w=u\log u\), \(w>\log u\)이므로
\[
 S_\delta
 <\frac{21}{20}\frac{27}{25}\frac{e^w}{w}
 =\frac{567}{500}\frac{e^w}{w}
 <\frac{189}{160}u.
 \tag{55.29}
\]

Euler product의 \(j\ge2\) 항은 \(\alpha=1-\delta\ge3/4\)에서
\[
 \sum_p\sum_{j\ge2}\frac{p^{-j\alpha}}j
 \le\frac12\frac1{1-2^{-3/4}}\sum_{n\ge2}n^{-3/2}<3.
 \tag{55.30}
\]
여기에는 \(2^{-3/4}<3/5\)와 적분검사
\(\sum_{n\ge2}n^{-3/2}<2^{-3/2}+\int_2^\infty t^{-3/2}dt<2\)를 썼다.
(55.25), (55.29), (55.30)을 합치면
\[
 \log\prod_{p\le z}(1-p^{-\alpha})^{-1}
 <\log L+7+\frac{189}{160}u.
 \tag{55.31}
\]

### 7.2 \(u\log u\)가 \(a^{-3}\)을 만드는 이유

\(q\ge200\)에서 \(\log q\le q/20\)이고
\(\log(19/20)>-1/19\)이다. \(u>4b/q\)이므로
\[
 \log u>q+\log4-\log q,\qquad
 \log\log u>\log q-1/19.
 \tag{55.32}
\]
\(\log4>4/3\)과 정확한 유리수 차
\[
 \frac43-\frac1{19}-\frac{189}{160}=\frac{907}{9120}>0
 \tag{55.33}
\]
에서
\[
 u\left(w-\frac{189}{160}\right)>4b.
 \tag{55.34}
\]
또 \(\log L=b+\log q-\log4-q<b\). (55.24), (55.31), (55.34)을 합치면
\[
 \boxed{\Psi(Y,z)<e^7\frac{Y}{a^3}.}
 \tag{55.35}
\]

\(B_0=1\)이면 power factor는 하나다. \(B_0\)가 prime이면 \(B_0\ge2\),
\(\log Y<2a\), \(\log2>2/3\)이므로 가능한 거듭제곱 수는 \(4a\) 미만이다. 따라서
\[
 \#R<4e^7\frac{Y}{a^2}
 =4e^7c\frac q b\frac Xa
 <\boxed{\frac q{17b}\frac Xa}.
 \tag{55.36}
\]
마지막에는 \(e<3\), \(\log5>1\)과 \(4\cdot3^7\cdot17<153600\)을 썼다.
이 식은 FMT의 \(o(X/\log X)\)를 actual 변수에 필요한 한쪽 명시 상계로 교체한다.

## 8. 유한 COV2 출력 정리

(55.7), (55.9), (55.15), (55.17)의 \(F_{\rm out}<1\), (55.21)의
\(F_{\rm in}<1\), smooth gates (55.23)과
\[
 \frac q{17b}\le A\eta\varepsilon
 \tag{55.37}
\]
가 모두 성립한다고 하자. 그러면 한 residue 선택에 대해
\[
 A(1-\eta)\frac Xa\le\#T\le5A(1+2\eta)\frac Xa,
 \tag{55.38}
\]
그리고 모든 실수 \(0\le\alpha<\beta\le1\)에 동시에
\[
 \boxed{
 \#\bigl(T\cap(\alpha Y,\beta Y]\bigr)
 \le5A(1+2\eta)\bigl(2(\beta-\alpha)+\varepsilon\bigr)\frac Xa.}
 \tag{55.39}
\]
가 성립한다.

증명: (55.16)과 \(\rho\mu_j=A'hX/a\)가 cell과 whole interval의 \(S_*\) count를
\(\eta\) 상대오차로 묶는다. (55.6)으로 임의 구간을 성공한 cell들의 합으로 덮고
\(A'<5A\)를 쓴다. (55.3), (55.36), (55.37)로 \(R\)을 한 번 더한다.
하계는 \(S_*\subseteq T\), \(A'\ge A\)에서 바로 나온다. random outcome을 본 뒤 새로운
subset을 골라 moment 정리를 재사용하지 않는다.

(55.38)–(55.39)는 Proposition 3.1의 actual 구조를 hidden \(o(1)\) 없이 재현하는
**parameterized finite successor**다. 다만 Sono가 최종 coefficient에서 쓰는 실제
\(A,\varepsilon,\eta\)와 다른 PAP/UB/transfer 오차를 아직 하나의 공통 budget으로 고르지
않았으므로, numerical \(x_{\rm cover}\)나 \(X_{\rm cert}\)라고 부르지 않는다.

## 9. 닫힌 것과 남은 것

| 항목 | 판정 | 이유 |
|---|---|---|
| equal-grid·endpoint·integer rounding | `PROJECT_EXPLICIT` | (55.4)–(55.7) |
| \(m,A'\) floor와 허용범위 | `PROJECT_EXPLICIT` | (55.8)–(55.11) |
| actual-width exception restoration | `PROJECT_EXPLICIT` | (55.12)–(55.16) |
| outer/inner simultaneous choice | `PROJECT_EXPLICIT` | (55.17)–(55.21); 순차 존재, independence 불필요 |
| smooth \(R\) | `PROJECT_EXPLICIT` | (55.22)–(55.36); special-case Rankin–RS proof |
| `DEP-R08` actual child | `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT` | fixed \(A,\varepsilon,\eta\)의 finite gate와 출력 (55.38)–(55.39) |
| 최종 \(A,\varepsilon,\eta\), 같은 Sono 계수 총예산 | `OPEN` | `DEP-R11`에서 PAP/UB와 함께 선택해야 함 |
| numerical PAP·two-prime UB | `OPEN` | `DEP-R09`, `DEP-R10` |
| auxiliary \(X\)→모든 최종 \(X\) | `OPEN` | `DEP-R12` |
| broad SIV-07/08/09, COV-12, \(X_{\rm cert}\) | `HARD_BLOCKER/OPEN` | actual child 하나를 전체 root theorem으로 확대하지 않음 |

T1에서는 순수한 finite partition `COV-02`, smooth remainder `COV-03`, floor relation
`COV-09`를 `EXPLICIT`으로 올릴 수 있다. actual finite-family 확률과 sequential choice가
생겼으므로 `COV-08`, `COV-11`은 `PARTIAL`로 완화한다. 하지만 SIV 입력과 최종 parameter
budget을 포함한 `COV-12`는 `HARD_BLOCKER`를 유지한다.

## 10. bounded 검증과 다음 단계

`source/h1bcov2_post_covering.py`와 `tests/test_h1bcov2_post_covering.py`는 다음을 exact
`Fraction`으로 검산한다.

1. 여러 endpoint와 crossing interval의 equal-grid cover.
2. floating log 없이 \(m=\lfloor\log_5R_A\rfloor\)를 계산하는 작은 oracle.
3. exception restoration·pre/post normalization 곱.
4. outer와 inner failure의 순차 판정 및 잘못된 자동 합산 부재.
5. smooth proof의 유리수 anchor와 source hash·범위 미승격.

이는 실제 거대 \(X\), prime list, smooth number list 또는 threshold를 계산하지 않는다.
toy PASS는 이 해석적 증명의 독립 형식 인증이 아니다.

다음 root는 `DEP-R09`: Sono의 numerical PAP에서 \(C_{\rm PAP}=1-e^{-2}\),
\(D_{\rm PAP}=160\), exceptional modulus와 actual interval을 source equation별로 다시 고정하고
finite cutoff·오차를 합성하는 일이다. 그 뒤 `DEP-R10`, `DEP-R11`, `DEP-R12` 순서다.
