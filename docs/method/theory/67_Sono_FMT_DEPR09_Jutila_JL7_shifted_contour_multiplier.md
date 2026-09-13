# Sono/FMT DEP-R09 Jutila JL7 shifted-contour multiplier 명시화

- 작성일: 2026-09-13 KST
- 단계: `DEP-R09 / JL7-CONT`
- 선행 정본: [Theory 66](66_Sono_FMT_DEPR09_Jutila_JL7_terminal_parameter_repair.md)
- 기계 원장: [JL7 contour v1](data/Sono_FMT_DEPR09_Jutila_JL7_contour_v1.json)
- 판정: `JL7-CONT ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT / JL7-LEMMA3·RES·ABSORB·AVERAGED OPEN`
- 비목적: Jutila terminal density 전체 또는 averaged density를 닫기, fixed
  (2\times10^{-17}) 인증, (X_{\rm cert}) 계산기 제작, actual prime 계산

## 1. 결론

Jutila printed p.53의

\[
 I_d(s,\chi)\ll_\theta D^{1/2}(M/d)^{-1+\theta}
\]

에서 숨은 multiplier를 actual 식 (3.6) 범위에 대해 수치화했다. 모든 product character,
즉 비주지표와 주지표를 함께 포함해

\[
 \boxed{
 |I_d(s,\chi)|
 \le C_{\rm CONT}(\theta)\sqrt{qT}(M/d)^{-1+\theta}}
\tag{67.15}
\]

로 둘 수 있고,

\[
 C_{\rm CONT}(\theta)
 =\frac{96\sqrt2}{\pi}\zeta(1+\theta)
   \left(\frac2\theta+1\right).
\]

완전히 초등적인 계산기 입력으로는 더 큰 안전 상계

\[
 \boxed{
 \overline C_{\rm CONT}(\theta)
 =48\left(1+\frac1\theta\right)
    \left(\frac2\theta+1\right)}
\tag{67.17}
\]

를 쓸 수 있다.

> **쉬운 설명:** 원 논문은 이 오차를 “
> \(\theta\)에 따라 달라지는 어떤 상수 이하”라고만 적었다. 이번 단계는 그 빈칸에 실제로
> 넣을 수 있는 안전한 숫자 공식을 만들었다. 다만 바로 다음 합과 residue 계산에도 별도의
> 빈칸이 있으므로, 전체 정리가 끝난 것은 아니다.

## 2. 원문과 선행 source를 고정한 방식

| source | 확인 위치 | 판독 | 이번 역할 |
|---|---|---|---|
| Jutila, *On Linnik's constant* | printed pp.48, 52--53 | native text 18 bytes라 OCR은 locator로만 사용하고 원페이지 직접 대조 | actual (I_d), 변수 범위와 원래 정성 상계 |
| Bennett et al., *Counting zeros of Dirichlet L-functions* | printed p.1469, Lemma 5.6 (5.3) | native text 우선·원페이지 대조 | 비주지표 primitive (L)-함수의 exact Rademacher bound |
| Hasanalizade--Shen--Wong, *Counting zeros of Dedekind zeta functions* | printed p.286, Proposition 3.8 | 저자 공개 peer-reviewed PDF의 native text 우선·원페이지 대조 | 주지표에서 필요한 Riemann zeta exact Rademacher bound |
| NIST DLMF | §§5.5, 5.9 | 공식 웹 수식 | Gamma recurrence·Euler integral 교차검증 |

Rademacher 1959 원 논문은 두 peer-reviewed 논문이 각각 Theorem 3과 Theorem 4를 exact
statement로 재기록한 원출처다. 실제 계산은 접근하지 못한 원 논문의 기억이 아니라, 이번에
직접 확인한 두 재기록 statement에 고정한다.

## 3. Jutila actual 범위와 적분

식 (3.6)에서

\[
 0<\theta\le\frac1{21},\quad q\ge3,\quad T\ge1,\quad D=qT,
\]

\[
 s=u+iv,\qquad 0\le u\le2\theta,\qquad |v|\le2T,
\]

이고 (0<M\le N)이다. Jutila가 residue를 분리한 뒤 남긴 contour term은

\[
 I_d(s,\chi)=\frac1{2\pi i}
 \int_{\Re w=-1+\theta}
 L(1+s+w,\chi)
 \left\{(N/d)^w-(M/d)^w\right\}\Gamma(w)\,dw.
\tag{67.1}
\]

여기서

\[
 w=-1+\theta+iy,\qquad
 z=1+s+w=\theta+u+i(v+y),\qquad
 0<\Re z\le3\theta\le\frac17.
\tag{67.2}
\]

이다. 이 범위는 다음 두 branch에서 같은 \(\sqrt{qT}\) 높이 scale을 얻는 핵심이다.

## 4. 공통 Euler-factor와 높이 상계

(chi\pmod q)가 conductor (f)인 (chi^*)에서 유도되면

\[
 L(z,\chi)=L(z,\chi^*)
 \prod_{\substack{p\mid q\\p\nmid f}}(1-\chi^*(p)p^{-z}).
\]

(p\ge5)에는 (1+p^{-\Re z}\le2\le\sqrt p)를 쓰고, 빠질 수 있는 2와 3의
최대 비용을 함께 보존하면

\[
 \prod_{\substack{p\mid q\\p\nmid f}}(1+p^{-\Re z})
 \le\frac4{\sqrt6}\sqrt{\frac qf}.
\tag{67.3}
\]

이 식은 비주지표 (f>1)뿐 아니라 주지표를 (f=1)로 읽을 때도 유효하다. 또한

\[
 |1+z|
 \le 1+3\theta+2T+|y|
 \le\frac{22}{7}T(1+|y|).
\tag{67.4}
\]

마지막 부등식은 (T\ge1), (3\theta\le1/7)만 사용한다.

## 5. 비주지표 branch

(f>1)인 primitive (chi^*)에 Bennett et al. Lemma 5.6 (5.3)을
(eta=\theta)로 적용한다. (sigma=\Re z=\theta+u)이므로

\[
 |L(z,\chi^*)|
 \le\zeta(1+\theta)
 \left(\frac f{2\pi}|1+z|\right)^{(1-u)/2}.
\tag{67.5}
\]

(0\le(1-u)/2\le1/2)이고 모든 (B>0)에 (B^a\le1+\sqrt B)를 쓸 수 있다.
primitive nonprincipal conductor는 (f\ge3)이므로 식 (67.3)--(67.5)를 합치면

\[
 |L(z,\chi)|
 \le C_{\rm NP}\zeta(1+\theta)
       \sqrt{qT}\sqrt{1+|y|},
\tag{67.6}
\]

\[
 C_{\rm NP}
 =\frac4{\sqrt{18}}+\frac4{\sqrt6}\sqrt{\frac{11}{7\pi}}
 <\frac94.
\tag{67.7}
\]

이다. (9/4)는 최적화한 값이 아니라 exact source를 안전하게 합성한 유리 상계다.

## 6. 주지표 branch와 중요한 비율 보존

주지표 (chi_0\pmod q)이면

\[
 L(z,\chi_0)=\zeta(z)\prod_{p\mid q}(1-p^{-z}).
\tag{67.8}
\]

Hasanalizade--Shen--Wong Proposition 3.8을 (K=\mathbb Q),
(eta=\theta)로 특수화하면

\[
 |\zeta(z)|
 \le3\left|\frac{1+z}{1-z}\right|
 \left(\frac{|1+z|}{2\pi}\right)^{(1-u)/2}
 \zeta(1+\theta).
\tag{67.9}
\]

여기서 분자와 분모를 따로 상계하면 불필요한 높이 손실이 생긴다.
(sigma=\Re z\le1/7)에 대해 비율의 제곱을 그대로 비교하면

\[
 \left|\frac{1+z}{1-z}\right|^2
 =\frac{(1+\sigma)^2+(\Im z)^2}
        {(1-\sigma)^2+(\Im z)^2}
 \le\left(\frac{1+\sigma}{1-\sigma}\right)^2
 \le\frac{16}{9}.
\tag{67.10}
\]

따라서 식 (67.3)--(67.4), (67.8)--(67.10)으로

\[
 |L(z,\chi_0)|
 \le C_{\rm P}\zeta(1+\theta)
       \sqrt{qT}\sqrt{1+|y|},
\]

\[
 C_{\rm P}=\frac{16}{\sqrt6}
 \left(1+\sqrt{\frac{11}{7\pi}}\right)<12.
\tag{67.11}
\]

를 얻는다. 이것이 주지표 때문에 (D^{1/2}) scale을 잃지 않는 핵심 보정이다.

## 7. 두 branch의 uniform (L)-상계

식 (67.7)과 (67.11)을 하나의 보수값으로 묶으면 모든 actual product character에

\[
 \boxed{
 |L(\theta+u+i(v+y),\chi)|
 \le12\zeta(1+\theta)\sqrt{qT}\sqrt{1+|y|}}
\tag{67.12}
\]

를 쓸 수 있다. 이 상계는 (chi_j,chi_k)가 서로 달라 product character가 imprimitive인
경우와, 서로 같아 주지표가 되는 경우를 모두 포함한다.

## 8. power difference와 Gamma 적분

\(\operatorname{Re} w=-1+\theta<0\), \(N\ge M\)이므로

\[
 \left|(N/d)^w-(M/d)^w\right|
 \le (N/d)^{-1+\theta}+(M/d)^{-1+\theta}
 \le2(M/d)^{-1+\theta}.
\tag{67.13}
\]

Gamma recurrence를 두 번 적용하고 Euler integral로
(|\Gamma(1+\theta+iy)|\le\Gamma(1+\theta)<2)를 쓰면

\[
 |\Gamma(-1+\theta+iy)|\le
 \begin{cases}
  8/\theta,& |y|\le1,\\
  2/y^2,& |y|\ge1.
 \end{cases}
\]

따라서

\[
 \int_{-\infty}^{\infty}
 \sqrt{1+|y|}\,|\Gamma(-1+\theta+iy)|\,dy
 \le8\sqrt2\left(\frac2\theta+1\right).
\tag{67.14}
\]

식 (67.12)--(67.14)와 (1/(2\pi))를 곱하면 식 (67.15)가 나온다.

## 9. 계산기용 초등 majorant

적분판정으로 모든 \(\theta>0\)에

\[
 \zeta(1+\theta)
 =\sum_{n\ge1}n^{-1-\theta}
 \le1+\int_1^\infty t^{-1-\theta}\,dt
 =1+\frac1\theta.
\tag{67.16}
\]

또 \(\sqrt2/\pi<1/2\)이므로 식 (67.15)는 식 (67.17)의 상계로 완전히 유리화된다.
가장 큰 허용값 \(\theta=1/21\)에서

\[
 C_{\rm CONT}(1/21)
 \approx40102.3459386232,\qquad
 \overline C_{\rm CONT}(1/21)=45408.
\tag{67.18}
\]

이 수치는 contour 한 항의 multiplier일 뿐, 최종 density coefficient나
(X_{\rm cert})가 아니다. \(\theta\to0^+\)에서 대략 \(\theta^{-2}\)로 커지는 것도
원 proof가 \(\ll_\theta\)였던 사실과 일치한다.

## 10. 증거 경계와 남은 의무

| ID | 이번 판정 | 다음에 필요한 것 |
|---|---|---|
| `JL7-CONT` | `ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT` | 식 (67.15) 또는 더 단순한 (67.17)을 downstream에 보존 |
| `JL7-LEMMA3` | `HARD_BLOCKER` | (sum_{r,r'}(rr')^{-1}\sum_d|h(d;r,r')|)의 multiplier·support endpoint |
| `JL7-RES` | `HARD_BLOCKER` | principal residue·diagonal 조건·같은 character의 height row sum |
| `JL7-ABSORB` | `HARD_BLOCKER` | 모든 상수를 Theory 66 식 (66.19)에 넣은 공통 strict cutoff |
| `JL7-AVERAGED` | `HARD_BLOCKER` | 식 (3.7)의 variable-modulus replay |

이 component 자체에는 (q\ge3,T\ge1) 외의 새 수치 (D)-cutoff가 필요 없다. 그러나
Jutila Lemma 3·residue·detector와 PAP의 기존 cutoff는 그대로 남는다. 따라서
terminal density, `PAP-11`, DEP-R09, fixed (2\times10^{-17}), numerical
(X_{\rm cert})와 threshold calculator는 계속 OPEN/NOT READY다.

## 11. 코드·Lean 검증 경계

- [Python evaluator](../../../source/dep_r09_jutila_jl7_contour.py)는 두 branch coefficient,
  높이·power difference, Gamma·contour multiplier와 초등 majorant를 100-dps로 검산한다.
- [fail-closed tests](../../../tests/test_dep_r09_jutila_jl7_contour.py)는 source hash,
  exact scope, rational envelopes와 모든 downstream false flag를 검사한다.
- Lean 단일 파일에는 식 (67.4), (67.10)의 제곱형, coefficient 유리 상계,
  식 (67.13)의 추상 합성과 식 (67.15)--(67.17)의 유한 대수만 넣는다.
- Rademacher convexity theorem, complex contour 이동, Gamma complex integral과
  Riemann-zeta 급수 자체를 project-local `axiom`으로 선언하지 않는다.
- `sorry`, `admit`, project-local `axiom`을 사용하지 않는다.

따라서 Lean PASS는 두 외부 analytic theorem을 Lean 안에서 새로 증명했다는 뜻이 아니다.
source statement를 premise로 받은 finite composition과 범위 오류 방지를 kernel에서 검사한다.

## 12. 다음 우선순위

다음은 `JL7-LEMMA3`다. Jutila Lemma 3의 actual (f(n)=\mu(n)\varphi(n)) local factor를
직접 전개해 (h(d;r,r')) support와 절대합을 exact Euler product로 복원한 뒤, (r,r'\le R)
endpoint까지 숫자로 합성해야 한다. 이 단계에도 맞는 explicit 선행 source가 있는지 먼저
찾고, 없을 때만 원문의 짧은 proof를 actual input에 맞춰 직접 유한화한다.

## 13. 참고문헌

- M. Jutila, *On Linnik's constant*, Math. Scand. 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- M. A. Bennett, G. Martin, K. O'Bryant, A. Rechnitzer,
  *Counting zeros of Dirichlet L-functions*, Math. Comp. 90 (2021), 1455--1482,
  DOI [10.1090/mcom/3599](https://doi.org/10.1090/mcom/3599),
  arXiv [2005.02989](https://arxiv.org/abs/2005.02989).
- E. Hasanalizade, Q. Shen, P.-J. Wong,
  *Counting zeros of Dedekind zeta functions*, Math. Comp. 91 (2022), 277--293,
  DOI [10.1090/mcom/3665](https://doi.org/10.1090/mcom/3665),
  arXiv [2102.04663](https://arxiv.org/abs/2102.04663).
- H. Rademacher, *On the Phragmén--Lindelöf theorem and some applications*,
  Math. Z. 72 (1959/1960), 192--204,
  DOI [10.1007/BF01162949](https://doi.org/10.1007/BF01162949).
- NIST Digital Library of Mathematical Functions,
  [Gamma recurrence](https://dlmf.nist.gov/5.5) and
  [Gamma integral](https://dlmf.nist.gov/5.9).
