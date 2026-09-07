# Sono/FMT H1b-1b-2b 교정된 \(\kappa=1\) Wirsing multiplier 정식화

- 작성일: 2026-09-08
- 상위 obligation: `H1B1-L83-GGPY3`, `H1B-L83`, `SIV-07`
- 기계 계약:
  `data/Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier_v1.json`
- 구현:
  `source/h1b1b2b_corrected_wirsing.py`
- 판정:

~~~text
Ford corrected structural theorem                 SOURCE REVIEWED
kappa=1 finite multiplier as a function of a,A2   PROJECT PARAMETERIZED EXPLICIT
valid summation range                              every real x >= 2
actual Maynard a,A2,L                              OPEN
corrected Lemma 8.4 r-fold composition             OPEN
H1B1-PACKAGE / SIV-07 / X_cert                    HARD_BLOCKER / HARD_BLOCKER / OPEN
~~~

## 1. 쉬운 요약

앞 단계는 GGPY와 Maynard에 인쇄된 오류항에서 \(c_\gamma\)가 정당화되지 않는다는
Castillo 등의 지적을 받아들여, 먼저 절대오차 상수 \(C_{3,\mathrm{abs}}\)를 찾고 나중에
\(c_\gamma\) 하한으로 나누는 경로를 택했다.

이번에 찾은 Kevin Ford의 2023 sieve 강의노트 Theorem 4.4는 문제의 정확한 원인과
보정법을 함께 제시한다. 빠졌던 항은

\[
c_\gamma(L+1)^\kappa
\]

이다. 일반 \(\kappa\)에서는 이 항이 첫 오류항과 다를 수 있지만, 현재 Maynard 적용은
\(\kappa=1\)이므로 두 항이 모두 \(c_\gamma(L+1)\) 크기다. 따라서 올바르게 보정한
Wirsing 증명을 사용하면 \(c_\gamma\)를 처음부터 포함한 상대오차를 얻을 수 있다.

Ford의 노트도 \(O_{\kappa,A_1,A_2}\) 안의 숫자는 주지 않는다. 그래서 노트의 증명
구조는 선행증명으로 채택하되, 현재 필요한 \(\kappa=1\)의 유한 부등식만 보수적으로
다시 전개했다. 얻은 상수는 매우 크고 최적화되지 않았지만, 숫자 없는 \(O\)를 임의로
1로 놓지 않았다는 점과 모든 \(x\ge2\)에서 유효하다는 점이 중요하다.

비유하면 과거 경로는 “할인율 \(c_\gamma\)가 빠졌으니 원가를 먼저 구한 뒤 별도로
할인율을 증명하자”였다. 새 경로는 “영수증에서 빠진 별도 항을 되살리면 할인율이 포함된
올바른 총액을 직접 계산할 수 있다”는 것이다. 과거 \(c_\gamma\) 하한 결과는 틀린 것이
아니며, 새 상수의 독립 교차검사와 다른 오류항에 계속 쓸 수 있다.

## 2. 선행연구 우선 전략의 적용성 감사

| 출처 | 제공하는 것 | 그대로 채택할 수 없는 부분 | 이번 사용 |
|---|---|---|---|
| Halberstam--Richert, Lemmas 5.3--5.4 | 원래 Wirsing/renewal 계보 | 인쇄 proof 접근 제한, 역수 전개에 smallness 누락 | 계보만 유지 |
| GGPY, Lemmas 3--4 | Maynard가 인용한 합 공식과 부분적분 | \(c_\gamma\)-상대 오류가 원 가정만으로 정당화되지 않음 | 표기와 목표식 대조 |
| Castillo et al., Lemma 2.5와 Remark | 안전한 절대오차와 기존 오류의 지적 | 수치 multiplier 없음 | 오류 판정 유지 |
| Kuperberg, Lemma 4.3 | HR recurrence의 현대적 재현 | 특수 함수, 비명시적 \(B_L,B_k,O\)-상수 | 구조 교차검사 |
| Ford, Theorem 4.4 | 누락된 \(c_\gamma(L+1)^\kappa\)를 포함한 교정 정리와 전체 proof | 저자 강의노트이고 multiplier가 비명시적 | 주 proof 구조로 사용 후 \(\kappa=1\) 상수 직접 전개 |
| Dusart, Theorems 6.10--6.12 | prime reciprocal sum, weighted prime sum, Mertens product의 explicit 범위 | 작은 구간은 별도 처리가 필요 | 작은 구간은 초등 상계, 큰 구간은 Dusart로 결합 |

일반 Selberg--Delange 정리나 fundamental lemma도 검색했지만, 현재의 양의 sieve density,
두 쪽 prime-sum 가정, 같은 norm과 같은 finite uniformity를 동시에 제공하지 않았다.
따라서 제목이나 결론이 비슷하다는 이유로 섞지 않았다. 이번 검색은 표적 탐색의 결과이며
“전 세계에 더 좋은 정리가 없다”는 novelty 주장은 아니다.

Ford 노트는 peer-reviewed 논문이 아니다. 따라서 권위만으로 채택하지 않고 아래 proof를
독립적으로 다시 전개했다. Lean은 이 분석적 수론 proof 전체를 새로 형식화하는 비용에 비해
현재 gate에서 얻는 이득이 작아 사용하지 않았다.

## 3. 표기와 정확한 정리

Maynard/Ford의 표기를 따라

\[
\rho_p=\frac{\gamma(p)}p,
\qquad 0<a\le1,
\qquad 0\le\rho_p\le1-a
\tag{22.1}
\]

라 하자. GGPY가 쓰는 parameter와는

\[
A_1^{\rm GGPY}=\frac1a
\tag{22.2}
\]

의 관계다. 같은 이름 `A1`을 그대로 복사하면 안 된다. 모든 \(2\le w\le y\)에서

\[
-L\le
\sum_{w\le p\le y}\rho_p\log p-\log(y/w)
\le A,
\qquad A>0, L>0
\tag{22.3}
\]

를 가정한다. squarefree support에서

\[
h(p)=\frac{\rho_p}{1-\rho_p},
\qquad
c_\gamma=\prod_p(1-\rho_p)^{-1}(1-1/p)
\tag{22.4}
\]

로 둔다. 다음 보조량을 정의한다.

\[
Q(a,A)=
\frac A a\left(1+\frac{100A}{69}\right)
+\frac{2(1-a)^2}{a},
\tag{22.5}
\]

\[
D(a,A)=4+A+Q(a,A),
\tag{22.6}
\]

\[
C_\Sigma(a,A)=40960D(a,A)e^{256+A}.
\tag{22.7}
\]

### Project theorem H1b-1b-2b

모든 실수 \(x\ge2\)에 대해

\[
\boxed{
\left|
\sum_{n\le x}\mu^2(n)h(n)-c_\gamma\log x
\right|
\le C_\Sigma(a,A)c_\gamma(L+1).
}
\tag{22.8}
\]

또한 매끄러운 \(G:[0,1]\to\mathbb R\)와

\[
G_{\max}=\sup_{0\le t\le1}(|G(t)|+|G'(t)|)
\]

에 대해 모든 실수 \(z\ge2\)에서

\[
\boxed{
\begin{aligned}
\sum_{d<z}\mu^2(d)h(d)G\!\left(\frac{\log d}{\log z}\right)
={}&c_\gamma\log z\int_0^1G(t)\,dt+E_G,\\
|E_G|\le{}&C_{8.3}(a,A)c_\gamma(L+1)G_{\max},
\end{aligned}}
\tag{22.9}
\]

여기서

\[
\boxed{C_{8.3}(a,A)=2\{C_\Sigma(a,A)+2\}.}
\tag{22.10}
\]

상수는 안전성을 우선한 것이며 최적값이라는 주장은 하지 않는다.

## 4. 세 가지 전역 초등 입력

아래의 느슨한 상계만 사용한다.

\[
\left|\sum_{p\le x}\frac{\log p}{p}-\log x\right|\le64
\qquad(x\ge2),
\tag{22.11}
\]

\[
\left|\sum_{p\le x}\frac1p-\log\log x\right|\le16
\qquad(x\ge2),
\tag{22.12}
\]

\[
\prod_{p\le x}(1-1/p)^{-1}\le8192\log x
\qquad(x\ge2).
\tag{22.13}
\]

Dusart Theorems 6.10--6.12는 각각 충분히 큰 구간에서 이보다 훨씬 강한 값을 준다.
그 아래의 유한 구간은 다음 초등 상계로 덮는다.

- \(n\ge3\)에서 \(\log n/n\)은 감소하므로, Dusart의 시작점 2974 아래에서는
  정수 전체에 대한 적분비교로 prime sum을 위에서 덮는다.
- \(\sum_{n=2}^N1/n\le\log N\)과 함수
  \(\log x-\log\log x\)의 끝점 비교를 사용해 10372 아래를 덮는다.
- prime product는 모든 정수 factor를 더한
  \(\prod_{n=2}^{\lfloor x\rfloor}n/(n-1)=\lfloor x\rfloor\)로 상계한다.
- \(\log2>69/100\), \(\log6<2\), \(0<\gamma<1\)을 사용한다.

따라서 64, 16, 8192는 소수표 fitting이 아니라 출판된 큰 구간 부등식과 초등 유한구간
상계의 합성이다.

## 5. Ford recurrence의 명시화

\[
H(x)=\sum_{n\le x}\mu^2(n)h(n),
\qquad B=L+1
\]

로 둔다. Ford 식 (4.8)의 exact squarefree 재배열은

\[
\sum_{n\le x}h(n)\log n
=\sum_{m\le x}h(m)\left{
\sum_{p\le x/m}\rho_p\log p+
\sum_{\sqrt{x/m}<p\le x/m\atop p\nmid m}
\rho_ph(p)\log p
\right}.
\tag{22.14}
\]

식 (22.3)에 \(w=y=p\)를 넣으면
\(\rho_p\log p\le A\), 따라서

\[
h(p)\le\frac{A}{a\log p}.
\tag{22.15}
\]

\(y=x/m\ge4\)이면 (22.3)을 \([\sqrt y,y]\)에 적용하고,
\(y<4\)이면 가능한 소수 2, 3을 직접 상계한다. 그 결과 두 번째 합은

\[
\frac A a\left(1+\frac A{\log2}\right)
+\frac{(1-a)^2}{a}\log6
\le Q(a,A).
\tag{22.16}
\]

첫 번째 합의 \(\log y\) 대비 오차는 \(L+A+\log2\) 이하이다.
부분합과 (22.14)를 결합하고 \([1,2]\) 적분을 흡수하면

\[
H(x)\log x=2\int_2^x\frac{H(u)}u\,du+\Delta(x),
\qquad
|\Delta(x)|\le D(a,A)B H(x).
\tag{22.17}
\]

## 6. 빠진 tail을 보존하는 핵심 단계

\[
c_\gamma(x)=\prod_{p\le x}(1-\rho_p)^{-1}(1-1/p)
\]

라 하자. 각 소수에서

\[
\log(1-\rho_p)-\log(1-1/p)
\le\frac1p-\rho_p+\frac2{p^2}.
\tag{22.18}
\]

먼저 \(E(t)=\sum_{p\le t}\log p/p-\log t\)라 두면 (22.11)에서
\(|E(t)|\le64\)이다. \(p>x\)인 구간에는 (22.3)의 왼쪽 끝점을
\(x\)의 오른쪽에서 접근시켜 endpoint를 맞춘다. 그러면 모든 \(y>x\)에서

\[
\left|\sum_{x<p\le y}(1/p-\rho_p)\log p\right|
\le 128+A+L\le(130+A)B.
\tag{22.19a}
\]

Abel 부분합으로

\[
\sum_{p>x}(1/p-\rho_p)
\le\frac{(130+A)B}{\log x}.
\tag{22.19}
\]

\(x\ge e^B\)에서는 제곱항까지 합쳐

\[
\log\frac{c_\gamma(x)}{c_\gamma}
\le132+A.
\tag{22.20}
\]

\(2\le x<e^B\)에서는 \([x,e^B]\)의 \(-\rho_p\)를 버리고 (22.12)를 사용한다.
이때 reciprocal-prime 구간 오차 32, 제곱항 2, 큰 구간 상계 \(132+A\)를
합치면 지수 166보다 작다. 계산을 단순하고 fail-closed하게 유지하기 위해 이를
256으로 올려 두 경우를 한 식으로 묶는다.

\[
c_\gamma(x)\le e^{256+A}c_\gamma
\max\left(1,\frac B{\log x}\right).
\tag{22.21}
\]

바로 이 작은 \(x\) 경우가 기존 proof에서 누락됐던
\(c_\gamma(L+1)^\kappa\) 항을 만든다. 이를 버리거나
\((1+O(L/\log x))^{-1}=1+O(L/\log x))를 smallness 확인 없이 쓰지 않는다.

(22.13)과 Euler product 양성성으로

\[
H(x)\le8192e^{256+A}c_\gamma(\log x+B).
\tag{22.22}
\]

따라서 (22.17)의 \(\Delta\)도 완전히 명시적으로 상계된다.

## 7. 적분방정식과 주항 식별

(22.17)을 Ford 식 (4.14)와 같이 풀면

\[
H(x)=2\log x\int_2^x
\frac{\Delta(t)}{t(\log t)^3}\,dt+\frac{\Delta(x)}{\log x}.
\tag{22.23}
\]

적분은 절대수렴한다. \(x\ge e^B\)에서는 tail 적분과 마지막 항의 합이

\[
5D(a,A)\,8192e^{256+A}c_\gamma B
=C_\Sigma(a,A)c_\gamma B
\tag{22.24}
\]

이하이다. \(x<e^B\)에서는 (22.22)를 직접 쓰며, \(D\ge4\)이므로 같은 상수가
그 구간도 덮는다.

남은 주항계수는 Ford proof처럼 Dirichlet series

\[
\zeta(s+1)^{-1}\sum_nh(n)n^{-s}
\]

의 \(s\to0^+\) Euler-product 극한으로 식별하면 정확히 \(c_\gamma\)다.
수렴은 (22.3)을 지수 구간별로 부분합하고
\(\rho_p^2\)를 \(O_{a,A}(j^{-2})\)로 묶어 확인할 수 있다. 이 단계는 주항의 exact
identity이며 새 수치 \(O\)-상수를 도입하지 않는다. 이로써 (22.8)이 따른다.

## 8. strict endpoint와 smooth partial summation

\(u>2\)에서 \(x\uparrow u\)의 좌극한을 취하면
\(\sum_{d<u}\mu^2(d)h(d)\)에도 (22.8)이 그대로 적용된다. \(1<u\le2\)의 항 1은
(22.8)을 \(x=2\)에 적용해

\[
1\le c_\gamma\{C_\Sigma B+\log2\}
\]

로 흡수한다. 따라서 strict cumulative error의 전 구간 상계는

\[
(C_\Sigma+2)c_\gamma B
\tag{22.25}
\]

이다. Stieltjes 부분적분에서 경계항 한 번과 미분 적분항 한 번이 생기므로 factor 2를
곱하면 (22.9)--(22.10)을 얻는다.

## 9. 무엇이 닫혔고 무엇이 남았는가

| obligation | 이전 | 현재 | 주의 |
|---|---|---|---|
| `H1B1-L83-GGPY3` | `RATE_MISSING` | `PROJECT_PARAMETERIZED_EXPLICIT_CORRECTED_KAPPA1` | 절대 \(C_3\) 대신 교정된 상대 경로 |
| `H1B1-L83-GGPY4` | 절대 factor 2만 parameterized | 교정된 \(C_{8.3}(a,A)\), \(z\ge2\) | actual 입력은 미대입 |
| `H1B-L83` | `RATE_MISSING` | `PARAMETERIZED_EXPLICIT_INPUTS_OPEN` | 공통 실제 \(a,A,L\) 필요 |
| legacy \(C_{3,\mathrm{abs}}\) route | primary | optional secondary | 틀린 경로가 아니라 더 긴 경로 |
| `H1B-L84` | `RATE_MISSING` | 변화 없음 | \(r\)-회 합성 필요 |
| `H1B1-PACKAGE` | `HARD_BLOCKER` | 변화 없음 | 다른 Section 8 입력도 남음 |
| `SIV-07`, \(X_{\rm cert}\) | blocker/open | 변화 없음 | threshold 계산 불가 |

이번 정리는 “Sono/FGKMT 부등식이 어느 \(X\)부터 성립한다”를 증명한 것이 아니다.
그 계산에 필요한 파이프 한 구간에서 숫자 없는 오류율을 명시식으로 바꾼 것이다.

## 10. 검증 범위와 한계

기계 계약과 회귀시험은 다음을 확인한다.

- Maynard/Ford와 GGPY의 서로 다른 \(A_1\) parameter 변환
- (22.5)--(22.7)의 exact rational 부분과 multiplier 평가
- 입력 domain 거부와 상수 단조 안전성
- Ford/Dusart 원문 SHA-256
- Lemma 8.3 child만 승격하고 Lemma 8.4, package, `SIV-07`,
  \(X_{\rm cert}\)는 승격하지 않는 fail-closed 상태

수치시험은 (22.8)의 분석적 증명을 대신하지 않는다. 상수가 매우 크므로 다음 단계에서
실제 \(a,A,L\)을 넣은 뒤 크기 병목을 평가하고, 필요할 때만 각 보조상계를 더 날카롭게
만든다. 지금 미리 최적화하면 실제 병목이 아닌 항에 시간을 쓸 위험이 있다.

## 11. 다음 gate

1. Maynard Section 8의 모든 실제 호출에서 하나의 공통 수치 \(a,A,L\)을 인증한다.
2. 그 값을 (22.10)에 넣어 실제 one-step multiplier의 크기를 진단한다.
3. smooth norm과 \(r\)-회 binomial error를 다시 합성한다.
4. 독립 root인 H1c/PAP와 나머지 H1b obligation이 닫힐 때까지 threshold calculator는
   만들지 않는다.

사용자 수행절차는 없다. Lean이나 추가 Python 패키지도 필요하지 않았다.

## 참고문헌

- Kevin Ford, *Sieve Methods Lecture Notes, Spring 2023*, Theorem 4.4,
  <https://ford126.web.illinois.edu/sieve2023.pdf>.
- Pierre Dusart, *Estimates of Some Functions Over Primes without R.H.*,
  arXiv:1002.0442, Theorems 6.10--6.12,
  <https://arxiv.org/abs/1002.0442>.
- D. A. Goldston, S. W. Graham, J. Pintz, C. Y. Yıldırım,
  *Small Gaps Between Products of Two Primes*, DOI 10.1112/plms/pdn046,
  arXiv:math/0609615.
- A. Castillo, C. Hall, R. J. Lemke Oliver, P. Pollack, L. Thompson,
  *Bounded Gaps Between Primes in Number Fields and Function Fields*,
  DOI 10.1090/S0002-9939-2015-12554-3, arXiv:1403.5808.
- Vivian Kuperberg, *Sums of Singular Series with Large Sets and the Tail of the
  Distribution of Primes*, DOI 10.1093/qmath/haad030, arXiv:2210.09775.
