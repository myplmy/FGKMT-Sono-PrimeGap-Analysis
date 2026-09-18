# Theory 84 — DEP-R09 sparse divisor-conductor source 감사

> **2026-09-18 successor note.** 이 문서의
> <code>REQUESTED_VAUGHAN_FULL_TEXT_MISSING</code>은 당시 supplied-file snapshot이다.
> 이후 <code>article/vaughan2001.pdf</code>로 정확한 원문이 추가되어 page-level 감사가
> 완료됐다. 현재 판정은
> [Theory 85](85_Sono_FMT_DEPR09_Vaughan2001_variance_source_audit.md)와
> [review 94](../../review/94_20260918_DEPR09_Vaughan2001_variance_source_타당성검토.md)를
> 따른다.

- 상태:
  <code>GENERIC_SPARSE_LARGE_SIEVE_CERTIFICATE_REJECTED /
  PRIME_SPECIFIC_OR_WEIGHTED_CORRELATION_OPEN /
  REQUESTED_VAUGHAN_FULL_TEXT_MISSING</code>
- 선행 정본: Theory 82--83, review 90·92
- 목표: character를 primitive conductor별로 정확히 분해하고, divisor conductor가
  희소하다는 사실과 sparse-modulus large sieve source가 Theory 82의 strict gate를
  닫을 수 있는지 판정한다.
- 비목적: actual \(V(Y,q)\)의 하한, 모든 conductor-sensitive 정리의 불가능성,
  GRH 채택, PAP-11, DEP-R09, fixed \(2\times10^{-17}\), numerical
  \(X_{\rm cert}\)를 이번 단계에서 인증하는 것.

## 1. 결론

현재 normalization은

\[
 q=P(x)/B_0,\qquad Y=q^d,\qquad 21\le d\le186
 \tag{84.1}
\]

이고 Theory 82의 충분조건은

\[
 V(Y,q)<V_{\rm gate}:=
 \tau^2p_*\frac{Q_{\mathcal S}M_{\min}^2Y^2}
 {\varphi(q)N^2}.
 \tag{84.2}
\]

모든 character modulo \(q\)를 conductor \(r\mid q\)별 primitive core로 나누는 것은
exact하다. 그러나 이는 **conductor level 수의 희소성**이지 character 총수의 감소가
아니다. nonprincipal 총수는 여전히 \(\varphi(q)-1\)이다.

Baier의 sparse-modulus large sieve를 포함한 coefficient-agnostic sampled-frequency
부등식은 길이 \(Y\) 항을 보존한다. 그 항만 사용해도 Theory 83에서

\[
 Y\sum_{n\le Y}\Lambda(n)^2>V_{\rm gate}
 \tag{84.3}
\]

가 이미 성립한다. 따라서 conductor divisor가 희소하다는 사실로 classical RHS의
modulus-density 항만 줄이는 경로는 strict gate를 인증하지 못한다.

이 판정은 실제 \(V(Y,q)\)가 크다는 뜻이 아니다. 남은 최소 입력은 다음 중 하나다.

1. \(\Lambda\)와 fixed primorial을 함께 쓰는 unconditional prime-specific 상계.
2. full \(V\) 대신 actual final law의 \(C_\chi(\omega)Z_\chi(Y)\)만 제어하는
   same-law weighted-correlation 정리.
3. 명시적 가정 아래의 conditional branch를 새 연구범위로 채택하는 별도 결정.

## 2. conductor별 exact partition

\(\varphi^*(r)\)를 conductor가 정확히 \(r\)인 primitive character의 수라 하자.
character induction의 유일성과 Möbius inversion은

\[
 \varphi^*(r)=\sum_{e\mid r}\mu(r/e)\varphi(e)
 \tag{84.4}
\]

및

\[
 \boxed{\sum_{r\mid q}\varphi^*(r)=\varphi(q)}
 \tag{84.5}
\]

를 준다. conductor \(1\)의 principal core가 하나이므로

\[
 \sum_{\substack{r\mid q\\r>1}}\varphi^*(r)=\varphi(q)-1.
 \tag{84.6}
\]

현재 \(q\)는 squarefree primorial-type modulus다. 이때

\[
 \varphi^*(r)=\prod_{p\mid r}(p-2).
 \tag{84.7}
\]

특히 \(2\mid r\)이면 우변은 0이다. \(q\)가 짝수이고 squarefree이며
\(\omega(q)=k\)이면 양의 primitive count를 갖는 conductor level은

\[
 \#\{r\mid q:\varphi^*(r)>0\}=2^{k-1}.
 \tag{84.8}
\]

Python exact check는 다음을 얻었다.

| \(q\) | positive conductor levels | \(\sum_{r\mid q}\varphi^*(r)\) |
|---:|---:|---:|
| 3 | 2 | 2 |
| 30 | 4 | 8 |
| 210 | 8 | 48 |
| 2,310 | 16 | 480 |
| 30,030 | 32 | 5,760 |
| 510,510 | 64 | 92,160 |

따라서 “divisor가 \(2^k\)개뿐”이라는 사실을 “character energy 항도 \(2^k\)개뿐”으로
바꾸면 안 된다. 각 level에는 \(\varphi^*(r)\)개의 primitive character가 있다.

## 3. sparse-modulus source와 적용범위

Baier, *On the Large Sieve with Sparse Sets of Moduli*, Theorem 2 식 (6)은
source의 distribution hypotheses와 notation 아래 대략 다음 구조를 갖는다.

\[
 \sum_{q\in\mathcal S(Q)}\ \sum_{(a,q)=1}
 \left|\sum_{n=M+1}^{M+N}a_ne(an/q)\right|^2
 \le
 c_2\{N+QXN^\varepsilon(\sqrt N+S)\}Z,
 \tag{84.9}
\]

여기서 \(S=|\mathcal S(Q)|\), \(Z=\sum|a_n|^2\)이고 \(X\)는 local distribution
parameter다. source가 강조하는 sparse 개선은 really sparse set과
\(Q\gg N^{1/2+\varepsilon}\) 쪽의 modulus-density 항에 있다. 현재는

\[
 Q\le q=Y^{1/d}\le Y^{1/21}\ll\sqrt Y.
 \tag{84.10}
\]

이고 conductor divisors는 한 dyadic block의 arbitrary sparse moduli와도 동일하지
않다. 따라서 식 (84.9)를 actual theorem으로 바로 대입하지 않는다. 더 근본적으로,
식 (84.9)의 첫 \(N\) 항은 sparse cardinality와 무관하게 남는다.

## 4. coefficient-agnostic length-term 장벽

sampled frequency family가 하나의 \(\alpha_0\)를 포함한다고 하자. 길이 \(N\)에서

\[
 a_n=e(-n\alpha_0)
 \quad\Longrightarrow\quad
 \left|\sum_{n=1}^{N}a_ne(n\alpha_0)\right|^2=N^2,
 \qquad
 \sum_{n=1}^{N}|a_n|^2=N.
 \tag{84.11}
\]

따라서 모든 coefficient에 대해 성립하는 sampled-frequency upper bound의 전체
coefficient는 적어도 \(N\)이어야 한다. sparse theorem이 modulus-density contribution을
\(D(q)\ge0\)로 줄인 가장 유리한 no-loss certificate를

\[
 B_{\rm sparse}(Y,q):={Y+D(q)\}S_2(Y),
 \qquad S_2(Y):=\sum_{n\le Y}\Lambda(n)^2
 \tag{84.12}
\]

라 쓰면

\[
 B_{\rm sparse}(Y,q)\ge YS_2(Y).
 \tag{84.13}
\]

Theory 83 식 (83.17)--(83.24)는 모든 \(q\ge3,d\ge21\)에서

\[
 \frac{S_2(Y)}Y>
 \frac{\log Y-\log2}{4}>
 5\log q>
 e^{-4}\frac q{\varphi(q)}
 \ge\frac{V_{\rm gate}}{Y^2}.
 \tag{84.14}
\]

식 (84.13)--(84.14)를 합치면 식 (84.3)이 나온다. 즉 generic sparse theorem의
나머지 항을 전부 0으로 놓아도 그 **수치 upper certificate**가 target보다 크다.
이 upper certificate만으로 \(V<V_{\rm gate}\)를 논리적으로 도출할 수 없다.

이는 actual \(V\ge YS_2(Y)\)라는 하한이 아니다. 실제 prime coefficient의 cancellation을
쓰는 정리는 coefficient-agnostic extremizer의 적용대상이 아니므로 계속 OPEN이다.

## 5. 사용자 추가 원문 1 — Montgomery--Vaughan 2001

로컬 파일
<code>article/Montgomery-Vaughan 2001.pdf</code>는 16쪽이며 SHA-256은
<code>e4d6a5fae3a41b9b50fe34355b0ea098e852bd84384bba7e1e83dbb083af0c9b</code>다.
서지는 다음과 같다.

> H. L. Montgomery and R. C. Vaughan, “Mean Values of Multiplicative
> Functions,” *Periodica Mathematica Hungarica* 43 (2001), 199--214.

따라서 이 파일은 요청 대상이던 R. C. Vaughan,
“On a Variance Associated with the Distribution of Primes in Arithmetic
Progressions,” *PLMS* 82 (2001), 533--553이 아니다.

로컬 원문의 printed p.202 Theorem 5는

\[
 T(x,n):=\sum_{\substack{m\mid n\\m\le x}}\mu(m)
 \ll x(\log x)^{-1+1/\pi}
 \quad(x\ge2,n\ge1)
 \tag{84.15}
\]

를 uniform하게 준다. 증명은 printed pp.212--214에서 Theorem 1과 Lemma 3을
호출한다. 상수는 implicit이고, 이것은 **signed** Möbius cancellation이다.

절댓값 또는 absolute square 뒤에 식 (84.15)를 그대로 옮길 수 없다. 최소 witness는

\[
 1+(-1)=0,
 \qquad |1|+|-1|=2.
 \tag{84.16}
\]

이다. 따라서 이 source는 pre-absolute-value divisor cancellation의 아이디어에는
관련되지만, 현재 \(\Lambda\)-twisted character energy의 fully numerical drop-in은 아니다.

## 6. 사용자 추가 원문 2 — Friedlander--Goldston 1996

<code>article/friedlander1996.pdf</code>는 24쪽 scan+OCR PDF이며 SHA-256은
<code>4981fe4eb38f8788a74082d031063e4dd9e98c63411fbb31d761e346b8a01bd9</code>다.
title·저자·journal·printed pp.313--336은 요청 논문과 일치한다.

printed p.314의 variance는

\[
 G(x,q):=\sum_{a\bmod q}^{*}E(x;q,a)^2.
 \tag{84.17}
\]

같은 페이지 식 (1.5)는 GRH 아래

\[
 G(x,q)\ll x(\log x)^4
 \tag{84.18}
\]

인 fixed-\(q\) upper를 인용한다. 이 사실은 정확히 기록해야 한다. 다만 implicit
constant와 finite cutoff가 없고 GRH 조건부이므로 현재 프로젝트의 unconditional
fully numerical certificate가 아니다.

printed p.315 Theorem 1은 큰 \(Q\)에서 \(Q/2<q\le Q\)를 평균하는 결과이며,
GRH branch도 \(Q\ge x^{3/4}\) 범위다. printed pp.315--316 Theorem 2는
unconditional \(x(\log x)^{-A}\le q\le x\), GRH
\(x^{3/4+\varepsilon}\le q\le x\) 쪽의 **lower bound**다. 현재

\[
 q=Y^{1/d}\le Y^{1/21}<Y^{3/4}
 \tag{84.19}
\]

와 겹치지 않고, lower bound는 필요한 upper certificate 방향도 아니다.

printed p.333의 divisor approximation \(\lambda_R\)도 감사했으나, 결론부까지
확인한 source theorem은 prescribed primorial \(q=Y^{1/d}\)의 unconditional numerical
upper를 주지 않는다.

## 7. Theory 83 source 기술의 정밀화

Theory 83의 핵심 결론인 “unconditional fully numerical current-range drop-in이
식별되지 않았다”는 유지된다. 다만 Friedlander--Goldston에 fixed-\(q\) upper가 전혀
없는 것으로 읽으면 부정확하다. 정확한 상태는 다음과 같다.

- GRH 아래 식 (84.18)의 implicit upper는 있다.
- 해당 upper는 unconditional·fully numerical이 아니다.
- large-\(Q\) 평균 정리와 lower theorem은 현재 prescribed small-\(q\) upper를 공급하지 않는다.

## 8. 코드·Lean 검증 범위

<code>source/dep_r09_sparse_divisor_conductor_audit.py</code>와 단위시험은 다음을
exact하게 확인한다.

1. sample 6개 modulus에서 식 (84.4)--(84.8).
2. positive conductor level 수와 character 총수의 분리.
3. \(d=21,186\)에서 식 (84.14)의 conservative margin.
4. 식 (84.11)과 (84.16)의 finite witness.
5. 두 PDF의 SHA-256·byte size 및 fail-closed status ledger.

Lean은 다음 finite implication만 검사한다.

\[
 0\le D,\ 0\le S_2
 \quad\Longrightarrow\quad
 YS_2\le(Y+D)S_2,
 \tag{84.20}
\]

\[
 G<YS_2\le(Y+D)S_2
 \quad\Longrightarrow\quad
 G<(Y+D)S_2.
 \tag{84.21}
\]

Conductor induction, Baier, Montgomery--Vaughan, Friedlander--Goldston, Dusart와
Rosser--Schoenfeld의 analytic theorem은 project-local axiom으로 넣지 않는다.

## 9. 현재 판정

| 항목 | 판정 |
|---|---|
| conductor partition | <code>EXACT</code> |
| sparse conductor level 수 | <code>EXACT, BUT NOT CHARACTER-COUNT REDUCTION</code> |
| generic sparse large-sieve certificate | <code>REJECTED FOR THEORY-82 GATE</code> |
| Friedlander--Goldston 1996 원문 | <code>VERIFIED; NO UNCONDITIONAL NUMERICAL DROP-IN</code> |
| 로컬 Montgomery--Vaughan 2001 PDF | <code>VERIFIED DIFFERENT PAPER</code> |
| 요청 Vaughan 2001 variance 전문 | <code>NOT PRESENT</code> |
| prime-specific fixed-primorial upper | <code>OPEN</code> |
| actual same-law weighted correlation | <code>OPEN</code> |
| PAP-11·DEP-R09 | <code>OPEN</code> |
| fixed \(2\times10^{-17}\), numerical \(X_{\rm cert}\) | <code>OPEN</code> |
| 새 bounded \(X_{\rm cert}\) 범위 | <code>NONE</code> |
| threshold calculator·actual prime 계산 | <code>NOT READY / NOT RUN</code> |

## 10. 다음 gate

다음 source audit은 generic sparse cardinality가 아니라 **prime-specific** 또는
**actual-weight-specific** cancellation을 정면으로 요구한다. 요청 Vaughan 2001 전문이
확보되면 title이 일치하는 원문으로 page·theorem·range를 다시 고정한다. GRH branch를
연구범위에 추가하려면 unconditional 목표와 분리한 사용자 결정이 먼저 필요하다.

## 11. 참고문헌

- S. Baier, “On the Large Sieve with Sparse Sets of Moduli,”
  [arXiv:math/0512228v1](https://arxiv.org/abs/math/0512228).
- H. L. Montgomery and R. C. Vaughan, “Mean Values of Multiplicative
  Functions,” *Period. Math. Hungar.* 43 (2001), 199--214.
- J. B. Friedlander and D. A. Goldston, “Variance of Distribution of Primes
  in Residue Classes,” *Q. J. Math.* 47 (1996), 313--336,
  [DOI 10.1093/qmath/47.3.313](https://doi.org/10.1093/qmath/47.3.313).
- R. C. Vaughan, “On a Variance Associated with the Distribution of Primes
  in Arithmetic Progressions,” *Proc. LMS* 82 (2001), 533--553,
  [DOI 10.1112/plms/82.3.533](https://doi.org/10.1112/plms/82.3.533).
