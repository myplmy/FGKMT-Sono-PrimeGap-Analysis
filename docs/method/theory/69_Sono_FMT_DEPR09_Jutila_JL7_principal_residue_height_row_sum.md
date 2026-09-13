# Sono/FMT DEP-R09 Jutila JL7 주잔여항·높이 행합 명시화

- 작성일: 2026-09-13 KST
- 단계: DEP-R09 / JL7-RES
- 선행 정본: [Theory 68](68_Sono_FMT_DEPR09_Jutila_JL7_Lemma3_absolute_sum.md)
- 기계 원장: [JL7 residue v1](data/Sono_FMT_DEPR09_Jutila_JL7_residue_v1.json)
- 판정: **JL7-RES = ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT**
- 비목적: terminal absorption·variable-modulus averaged replay·PAP 닫기,
  fixed \(2\times10^{-17}\) 인증, \(X_{\rm cert}\) 계산기 제작, actual prime 계산

## 1. 결론

Jutila printed p.53의 주잔여항을 원문 식 그대로 유지하고, Lemma 3의 대각식과
같은 character의 선택 영점 높이 간격을 유한 상계로 합성했다. actual 범위

\[
 0<\theta\le\frac1{21},\qquad
 D=qT,\qquad L=\log D\ge\theta^{-2}
\tag{69.1}
\]

에서 한 even 또는 odd selected system의 주잔여항 절댓값은

\[
 \boxed{
 |\mathcal R|
 <52J\left(\frac{\varphi(q)}q\right)^2
       x^{2-2\alpha}L^2.}
\tag{69.2}
\]

상수 52는 최적값이 아니라 다음 terminal inequality에 그대로 넣을 수 있는
계산기 안전 상수다. 새 cutoff는 없고 Theory 66의 조건만 쓴다.

> **쉬운 설명:** 원 논문은 “같은 문자에 속한 영점들이 너무 가까이 몰리지 않는다”는
> 사실로 잔여항을 제어했지만 숫자는 숨겼다. 이번에는 각 영점에서 다른 영점들의 영향을
> 거리 제곱의 역수로 더해도 한 행당 일정한 양을 넘지 않는다는 것을 이용해, 숨은
> “대략”을 52라는 안전한 숫자로 바꿨다. 다만 이것은 전체 증명의 한 부품일 뿐이다.

## 2. source-first 조사와 원문 경계

| source | 확인 위치 | 역할 | 판정 |
|---|---|---|---|
| Jutila, *On Linnik's constant* | printed p.49 Lemma 3, p.51 strip selection, pp.52--53 식 (3.6)과 residue 문단 | actual residue, 대각 조건, Δ-well-spacing | 원출처 |
| NIST DLMF | 5.5.1, 5.9.1 | Gamma recurrence와 Euler 적분 | 표준 exact identity |

Jutila scan은 native text layer가 사실상 비어 있어 OCR을 locator로만 사용하고, 위 네
printed page의 렌더링 원페이지와 수식을 직접 대조했다. 관련 density·large-values 문헌도
표적 검색했으나 이 p.53 local residue를 수치 multiplier까지 바로 대입할 수 있는 정리는
식별하지 못했다. 이는 전 세계 문헌에 없다는 novelty 주장이 아니다. 따라서 Jutila의 exact
식과 표준 Gamma identity에서 직접 유한 상계를 만든다.

## 3. 원문 residue와 정확한 대각화

Theory 66의 actual 매개변수를 다시 쓰면

\[
 R=D^\theta,\qquad
 z_1=D^{1/2+7\theta},\qquad
 x=D^{1+12\theta}L^2.
\tag{69.3}
\]

선택 영점을 \(s_j=\rho_j-\alpha\)라 두면

\[
 0\le\Re s_j\le\theta,\qquad |\Im s_j|\le T.
\tag{69.4}
\]

Jutila p.53 residue에는

\[
 \sum_{r,r'\le R}'\frac1{rr'}
 \sum_d\frac{h(d;r,r')}d
 \sum_{\bar\chi_j\chi_k=\chi_0}
 \bar\eta_j\eta_k\,\mathcal I(\bar s_j+s_k)
\tag{69.5}
\]

가 들어간다. 여기서 prime은 squarefree와 \((rr',q)=1\) 조건이고
\(|\eta_j|=1\)이다. Theory 68이 보존한 Lemma 3 exact identity

\[
 \sum_d\frac{h(d;r,r')}d
   =\delta_{r,r'}\varphi(r)
\tag{69.6}
\]

때문에 \(r=r'\)만 남는다. 또한
\(\bar\chi_j\chi_k=\chi_0\)는 같은 modulus \(q\)에서
\(\chi_j=\chi_k\)와 동치다. 따라서 outer arithmetic sum은 정확히

\[
 S_q(R)=
 \sum_{\substack{r\le R\;r\ {\rm squarefree}\\(r,q)=1}}
 \frac{\varphi(r)}{r^2}
\tag{69.7}
\]

가 된다. 절댓값 Lemma 3 상수 3을 이 residue에 다시 곱하면 안 된다.

## 4. Gamma pole을 제거한 ladder kernel

다음 endpoint를 둔다.

\[
\begin{aligned}
 a&=(1-\theta)\log z_1,& b&=\log z_1,\\
 c&=\log x,& d&=(1+\theta)\log x,\\
 A&=b-a,&B&=d-c.
\end{aligned}
\tag{69.8}
\]

\(z=\bar s_j+s_k\)라 하면 \(0\le\Re z\le2\theta\)다. Gamma recurrence로

\[
 (e^{-\xi z}-e^{-\eta z})\Gamma(-z)
 =-\Gamma(1-z)\int_\xi^\eta e^{-uz}\,du.
\tag{69.9}
\]

이 식은 \(z=0\)에서도 우변의 analytic continuation으로 정의된다. 즉 원래 보이는
\(\Gamma(0)\) pole은 exponential difference와 정확히 상쇄된다. 다음 kernel을 쓰자.

\[
 K(z)=\int_a^b\int_c^d\int_\xi^\eta e^{-uz}\,du\,d\eta\,d\xi.
\tag{69.10}
\]

\(z\ne0\)이면 유한적분을 직접 계산하여

\[
 K(z)=
 \frac{B(e^{-az}-e^{-bz})-A(e^{-cz}-e^{-dz})}{z^2}.
\tag{69.11}
\]

## 5. 실제 interval의 유리수 상계

\(L\ge\theta^{-2}\ge441\)에서는 \(2\log L\le L\)이다. 따라서

\[
 A\le\frac56\theta L,\qquad
 B\le\frac{18}{7}\theta L,\qquad
 d-a<3L.
\tag{69.12}
\]

\(z=0\)의 triple-integral mass는

\[
 K(0)=\int_a^b\int_c^d(\eta-\xi)\,d\eta\,d\xi
 <7\theta^2L^3.
\tag{69.13}
\]

반면 \(z=u+iv\), \(v\ne0\)에서는 \(u\ge0\)이므로 식 (69.11)의 네 exponential
절댓값이 1 이하이고,

\[
 |K(z)|
 \le\frac{2(A+B)}{|z|^2}
 <\frac{7\theta L}{v^2}.
\tag{69.14}
\]

## 6. Gamma의 완전한 수치 상계

\(0\le\Re z\le2/21\)이므로 \(w=1-z\)에

\[
 \frac{19}{21}\le\Re w\le1.
\]

Euler 적분을 1에서 나누면

\[
\begin{aligned}
 |\Gamma(w)|
 &\le\Gamma(\Re w)\\
 &\le\int_0^1 t^{-2/21}\,dt+\int_1^\infty e^{-t}\,dt\\
 &<\frac{21}{19}+1=\frac{40}{19}<3.
\end{aligned}
\tag{69.15}
\]

복소 Gamma에 hidden constant를 남기지 않는다.

## 7. 같은 character의 높이 행합

Jutila p.51은 높이 폭

\[
 \Delta=L^{-1}
\tag{69.16}
\]

인 strip마다 각 \(L(s,\chi)\)의 영점을 최대 하나 선택하고 even strip과 odd strip을
분리한다. 한 parity system 안에서 같은 character의 서로 다른 선택 높이는 적어도
\(\Delta\)만큼 떨어진다. 고정한 \(j\)의 위·아래 \(m\)번째 높이는 각각 최소
\(m\Delta\) 떨어지므로

\[
 \sum_{\substack{k\ne j\\\chi_k=\chi_j}}
 \frac1{(t_k-t_j)^2}
 \le2L^2\sum_{m\ge1}\frac1{m^2}
 <\frac{10}{3}L^2.
\tag{69.17}
\]

식 (69.13)--(69.17)을 곱하면 \(k=j\) 대각은

\[
 3\cdot7\theta^2L^3=21\theta^2L^3,
\]

off-diagonal 한 행은

\[
 3\cdot7\theta L\cdot\frac{10}{3}L^2
 =70\theta L^3.
\]

\(\theta\le1\)이므로 한 행 전체, 이어서 \(J\)개 행 전체는

\[
 \boxed{
 \sum_{j,k:\chi_j=\chi_k}
 |\Gamma(1-\bar s_j-s_k)K(\bar s_j+s_k)|
 <91J\theta L^3.}
\tag{69.18}
\]

이 \(J\)는 한 parity system의 cardinality다. even·odd 두 system으로 돌아가는 factor 2는
JL7-ABSORB에서 다른 terminal 항과 함께 보존한다.

## 8. 대각 \(r\)-합의 Rankin 상계

\(\lambda=1/L\)라 두면 \(r\le R\)에서 \(1\le(R/r)^\lambda\)이고
\(R^\lambda=e^\theta<2\)이다. 따라서

\[
 S_q(R)
 \le e^\theta
 \prod_{p\nmid q}
 \left(1+\frac{p-1}{p^{2+\lambda}}\right)
 \le e^\theta\zeta(1+\lambda)
 \prod_{p\mid q}(1-p^{-1-\lambda}).
\tag{69.19}
\]

각 \(p\mid q\)에

\[
 \frac{1-p^{-1-\lambda}}{1-p^{-1}}
 =1+\frac{1-p^{-\lambda}}{p-1}
 \le\exp\!\left(\frac{\lambda\log p}{p-1}\right).
\tag{69.20}
\]

\(\sum_{p\mid q}\log p/(p-1)\le\log q\le L\)이므로 식 (69.20)의 곱은 \(e\)
이하다. 또한 적분판정으로
\(\zeta(1+\lambda)\le1+L\le2L\)이다. \(e^\theta<2\), \(e<3\)을
유리수 안전 상계로 쓰면

\[
 \boxed{S_q(R)<12\frac{\varphi(q)}qL.}
\tag{69.21}
\]

\(e^\theta<2\)는 \(0\le\theta<1\)에서 exponential series를 geometric series로
항별 비교한 \(e^\theta\le(1-\theta)^{-1}\le21/20<2\)로도 확인된다.

## 9. 최종 residue multiplier

Jutila p.53의 바깥 prefactor는

\[
 L^{-2}\frac{\varphi(q)}q x^{2-2\alpha}.
\]

여기에 식 (69.18)과 (69.21)을 넣으면 coefficient는

\[
 12\cdot91\theta=1092\theta\le\frac{1092}{21}=52.
\tag{69.22}
\]

따라서 식 (69.2)가 나온다. 이것은 Jutila가 쓴
\(\ll_\theta J(\varphi(q)/q)^2x^{2-2\alpha}L^2\)의 actual 범위용 수치 복원이다.

## 10. 구현·Lean 증거 경계

- [finite checker](../../../source/dep_r09_jutila_jl7_residue.py)는 interval geometry,
  pole-cancelled closed form, Fubini로 분리한 두 독립 1차원 quadrature, well-spaced finite row,
  exact \(S_q(K)\), excluded-prime product와 endpoint coefficient를 검사한다.
- [fail-closed tests](../../../tests/test_dep_r09_jutila_jl7_residue.py)는 closed form과
  독립 적분을 70 dps에서 대조하고 downstream flag를 false로 강제한다.
- Lean 단일 파일은 \(5/6,18/7,7,40/19,10/3,91,12,52\)의 부등식 방향과 최종
  coefficient 합성을 kernel에서 확인한다.
- 복소 Gamma 적분 전체, Dirichlet character 선택구조, 무한 Euler-product/Rankin 전개는
  project-local axiom으로 채우지 않는다. 각각 source theorem 또는
  PARTIAL_FORMALIZATION으로 남긴다.
- `sorry`, `admit`, project-local `axiom`은 사용하지 않는다.

따라서 Lean PASS는 Jutila density theorem 전체의 독립 형식증명이 아니다. 이번에 닫힌 것은
actual p.53 residue multiplier와 그 유한 대수뿐이다.

## 11. 상태와 다음 gate

| ID | 판정 | 남은 일 |
|---|---|---|
| JL7-CONT | ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT | Theory 67 상수 보존 |
| JL7-LEMMA3 | ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT | Theory 68의 절댓값 3과 residue 대각 identity 구분 |
| JL7-RES | **ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT** | 이번 상수 52와 parity factor를 terminal 합성에 보존 |
| JL7-ABSORB | HARD_BLOCKER | weighted lower bound와 모든 upper multiplier의 strict \(A-E>0\) 공통 cutoff |
| JL7-AVERAGED | HARD_BLOCKER | 식 (3.7) variable-modulus primitive-character replay |

terminal density, PAP-11, DEP-R09, fixed \(2\times10^{-17}\), numerical
\(X_{\rm cert}\)와 threshold calculator는 계속 OPEN/NOT READY다. 다음 우선순위는
JL7-ABSORB다.

## 12. 참고문헌

- M. Jutila, *On Linnik's constant*, Math. Scand. 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- NIST Digital Library of Mathematical Functions,
  [§5.5 Functional Relations](https://dlmf.nist.gov/5.5),
  [§5.9 Integral Representations](https://dlmf.nist.gov/5.9).
