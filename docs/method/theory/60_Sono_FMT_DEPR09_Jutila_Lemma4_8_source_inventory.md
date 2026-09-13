# Sono/FMT DEP-R09 Jutila Lemma 4--8 정량 source inventory

- 작성일: 2026-09-13 KST
- 단계: `DEP-R09 / JUTILA LEMMAS 4--8 SOURCE INVENTORY`
- 선행 정본: [Theory 59](59_Sono_FMT_DEPR09_branch_S_quantitative_transfer_audit.md)
- 기계 원장: [Jutila Lemma 4--8 v1](data/Sono_FMT_DEPR09_Jutila_Lemma4_8_v1.json)
- 판정: `LEMMA4_ACTUAL_UPPER_CALL_EXPLICIT / FULL_DENSITY_PACKAGE_OPEN`
- 비목적: actual prime sweep, numerical \(X_{\rm cert}\) 계산기, 숨은 상수의 임의 선택

> **후속 상태(2026-09-13):** 이 문서의 `JL5 HARD_BLOCKER` 판정은 당시 snapshot이다.
> [Theory 61](61_Sono_FMT_DEPR09_Jutila_Lemma5_finite_harmonic_lower_bound.md)이
> peer-reviewed explicit source로 `JL5`를 \(q\)-의존 cutoff까지 닫았다.
> 이어 [Theory 62](62_Sono_FMT_DEPR09_Jutila_Lemma6_Mellin_integral_explicit.md)가
> `JL6-MELLIN`을 actual form에서 parameterized explicit로 닫았다. 이어
> [Theory 63](63_Sono_FMT_DEPR09_Jutila_Lemma6_truncation_tail_actual.md)이 actual
> `JL6-TAIL`을 닫았고, [Theory 64](64_Sono_FMT_DEPR09_Jutila_Lemma6_actual_common_budget.md)가
> 네 loss와 공통 cutoff를 합쳐 `JL6-ACTUAL`도 parameterized explicit로 닫았다.
> printed general JL6, `JL8`과 root certificate는 계속 OPEN이다.

> **후속 상태(2026-09-13, JL8):** [Theory 65](65_Sono_FMT_DEPR09_Jutila_Lemma8_actual_local_zero_count.md)가
> McCurley 1984의 식 (5), (13)과 Lemmas 1--4를 직접 합성해 actual near-one square
> `0<r<=1/21`에서 `N_square<3+r log(q(1+|t0|))`를 얻었다. 따라서
> `JL8-ACTUAL-NEAR-ONE`은 explicit source replacement로 닫혔다. printed unrestricted
> JL8, Jutila 식 (3.6) 종단 density, PAP-11·DEP-R09·fixed coefficient·`X_cert`는 OPEN이다.

> **중요 후속 교정(2026-09-13, JL7/식 (3.6)):** 이 문서가 식 (60.1)의
> `tau=8/5`, `37.769894`를 식 (3.6)의 actual 호출로 분류한 것은 잘못이었다. 그
> 고정값은 printed p.54의 Theorem 1-prime branch에만 해당한다. printed p.52의 식
> (3.6)은 `tau_theta=(1+16 theta)/(1+14 theta)`를 사용한다. 현재 교정 정본인
> [Theory 66](66_Sono_FMT_DEPR09_Jutila_JL7_terminal_parameter_repair.md)이
> `K_BV(theta)<13/theta`와 결합 상계 `34/theta^2`로 실제 호출을 다시 닫는다.

## 1. 결론

Jutila 1977의 Lemma 4--8을 원문과 인용 source 단위로 분해한 결과, Lemma 4의
**Theorem 1-prime branch에 필요한 한쪽 상계**는 Ramaré--Zuniga Alterman의 명시적
Corollary 1.3으로 교체할 수 있다. Jutila Theorem 1-prime의 실제 매개변수
\(\tau=8/5\)에서 새 상수는

\[
 K_{\rm BV}
 =3.09\frac{1.084(\tau+1)+1.301(1+\tau^2)-0.116}{\tau-1}
 =\frac{18884947}{500000}=37.769894.
\tag{60.1}
\]

이는 Graham/Jutila Lemma 4의 전체 점근식과 오차항을 복원한 것이 아니며, 식 (3.6)에
그대로 적용되는 값도 아니다. 식 (3.6)의 올바른 theta-dependent 특수화는 Theory 66을 따른다.

반면 다음 세 병목은 남는다.

1. Lemma 5의 \(1+o(1)\)을 \(q,R\)에 균일한 수치 lower bound로 바꾸는 일
2. Lemma 6의 Mellin 적분과 절단 tail에 붙은 \(\ll_\varepsilon 1\)을 합성하는 일
3. Lemma 8의 local zero-count \(\ll\) 상수를 숫자로 만드는 일

따라서 `RS02-A`는 일부 진전했지만 계속 `HARD_BLOCKER`이고, `PAP-11`, `DEP-R09`, fixed
\(2\times10^{-17}\), \(X_{\rm cert}\)는 모두 OPEN이다.

> 쉬운 설명: 여러 부품 중 “체의 제곱합” 부품에는 이제 숫자가 적힌 새 부품을 쓸 수 있다.
> 하지만 그 앞의 신호 증폭 부품과, 영점들을 묶어 세는 부품에는 아직 숫자가 없는 오차가
> 남아 있다. 부품 하나를 고쳤다고 전체 기계의 안전검사가 끝난 것은 아니다.

## 2. 원문과 읽기 방식

| source | 확인한 위치 | 읽기 방식 | 이번 역할 |
|---|---|---|---|
| Jutila, *On Linnik's constant* | 인쇄 pp. 49--54, 식 (2.4)--(3.6) | native text가 18 bytes뿐이어서 300dpi OCR 후 원페이지 대조 | Lemma 4--8와 실제 proof DAG |
| Huxley, *Large values III* | pp. 435, 438--439, 442--443 | native text가 사실상 비어 OCR 후 원페이지 대조 | exponent 2 계열 선행 source와 숨은 상수 확인 |
| Huxley--Jutila, *Large values IV* | pp. 297--299 | OCR 후 원페이지 대조 | Jutila가 \(4/5\) 바깥 구간에 호출한 density source |
| Ramaré--Zuniga Alterman, arXiv `2405.12662` | pp. 1, 5--6, Cor. 1.2--1.3 | native text 우선, 원페이지 대조 | Lemma 4 actual upper-call 대체 |
| Berkane 2014 | pp. 35--36 | native text 우선, 원페이지 대조 | \(\tau=2\) explicit 선행경로 비교 |
| Zuniga Alterman 2022 | pp. 1--3 | native text 우선, 원페이지 대조 | one-parameter·\(X\ge U^2\) explicit 경로 비교 |

Huxley 1975 III 공식 PDF는 IMPAN의 실제 CC-BY endpoint에서 확보해
`article/Huxley 1975 Large values of Dirichlet polynomials III.pdf`에 보존했다.
파일 SHA-256은
`cc8b7282c1963687d357829416d5e471e130810e5324709a96319bb7a2a3428f`다.

## 3. Jutila Lemma 4와 Theorem 1-prime actual replacement

Jutila의 Barban--Vehov weight를 \(a(n)=\sum_{d\mid n}\lambda_d\)라 쓰면 Lemma 4는

\[
 \sum_{n\le x}a(n)^2
 =\frac{x}{\log(z_2/z_1)}
  +O\!\left(\frac{x}{\log^2(z_2/z_1)}\right)
 \qquad (x\ge z_2)
\tag{60.2}
\]

와 \(z_1<x<z_2\)인 두 번째 점근식을 제시한다. 인용 당시 `to appear`였던 Graham 논문은
J. Number Theory 10 (1978), 83--94, DOI `10.1016/0022-314X(78)90010-0`로 출판됐다.
식 (60.2)의 \(O\)-상수는 Jutila 문장만으로는 numerical하지 않다.

Ramaré--Zuniga Alterman Corollary 1.3은 \(X\ge z_1\ge100\),
\(z_2=z_1^\tau\), \(\tau>1\), \(1/2\le\alpha\le1\)에서

\[
 \sum_{n\le X}\frac{a(n)^2}{n^{2\alpha-1}}
 \le K_{\rm BV}(\tau)X^{2-2\alpha}
       \frac{\log X}{\log(z_2/z_1)}
\tag{60.3}
\]

를 준다. 제곱합 항은 음이 아니므로 해당 parameter branch의 부분구간도 같은 우변으로
상계된다. 즉 **full asymptotic은 열려 있지만 Theorem 1-prime의 one-sided call은
닫힌다.** 식 (3.6)의 별도 one-sided call은 Theory 66에서 올바른
\(\tau_\theta\)로 닫는다.

### 3.1 Theorem 1-prime 매개변수 대입

Jutila의 선택은

\[
 a_1=\frac52,\quad a_2=4,\quad c=\frac{11}{2},\quad
 z_i=D^{a_i},\quad X=D^c,\quad x_D=X\log^2D.
\tag{60.4}
\]

따라서

\[
 \tau=\frac{a_2}{a_1}=\frac85,\qquad
 \frac{\log x_D}{\log(z_2/z_1)}
 =\frac{11}{3}+\frac43\frac{\log_2D}{\log D}.
\tag{60.5}
\]

여기서 \(\log_2D=\log\log D\)는 반복 자연로그다. 또한
\(\alpha=1-\lambda/\log D\)이면

\[
 x_D^{2-2\alpha}
 =\exp\!\left(11\lambda+
      4\lambda\frac{\log_2D}{\log D}\right).
\tag{60.6}
\]

식 (60.3)--(60.6)은 actual call에 완전히 명시적인 upper bound를 준다. 그러나 finite
\(D\)에서는 \(\log^2D\) 때문에 \(e^{11\lambda}\) 외에 작은 양의 보정이 남는다. 원하는
\(\delta>0\)에 대해

\[
 4\frac{\log_2D}{\log D}\le\delta
\tag{60.7}
\]

인 수치 cutoff를 잡으면 이 보정은 \(e^{\delta\lambda}\) 이하가 된다. 따라서 이 교체는
Jutila의 인쇄된 `10 exp(11 lambda)`를 그대로 인증하지 않고, finite 재증명에서 쓸 수 있는
수치 입력을 제공한다.

> 쉬운 설명: 새 정리는 원래 식과 같은 속도로 거의 내려가지만, 유한한 \(D\)에서는 아주
> 작은 추가 보정이 붙는다. 그 보정을 무시하지 않고 별도 cutoff로 계산해야 한다.

## 4. Lemma 5--8 의무

### 4.1 Lemma 5: squarefree·coprime 조화합

Jutila Lemma 5는 \(\log R\ge\sqrt{\log q}\), \(R\to\infty\)에서

\[
 \sum_{\substack{r\le R\\ r\text{ squarefree}\\(r,q)=1}}\frac1r
 =\frac6{\pi^2}\prod_{p\mid q}\left(1+\frac1p\right)^{-1}
  \log R\{1+o(1)\}.
\tag{60.8}
\]

생성함수는 정확하지만 `o(1)`의 rate와 최초 적용점이 없다. Lemma 6은 이 합의 lower bound를
사용하므로 다음 형태가 필요하다.

```text
R >= R0(q, eta), log R >= sqrt(log q)
  -> sum >= (1-eta)*(6/pi^2)*product*log R.
```

이는 직접 정량화 가능성이 높은 다음 우선순위다. 다만 \(q\)가 커질 때 product와 remainder를
동시에 균일하게 다뤄야 하므로 단순히 고정 \(q\) Mertens 상수를 가져오면 안 된다.

### 4.2 Lemma 6: zero detector lower bound

Lemma 6의 목표는

\[
 |g(\rho,\chi)|\ge
 (1-\varepsilon)\frac{\varphi(q)}q\frac6{\pi^2}\log R,
\tag{60.9}
\]

이다. 그러나 proof에는 다음 별도 수치 의무가 있다.

- Mellin integral의 \(\ll_\varepsilon1\)
- 무한 series를 \(x=X\log^2(qT)\)에서 자르는 tail의 \(\ll_\varepsilon1\)
- Lemma 5 lower bound가 두 절대오차를 흡수하기 위한 \(D_0(\varepsilon)\)

따라서 Lemma 5만 닫아도 Lemma 6 전체가 자동으로 닫히지 않는다.

### 4.3 Lemma 7: modified Halasz inequality

Lemma 7은

\[
 \left(\sum_{j=1}^J|f(s_j,\chi_j)|\right)^2
 \le \sum_{n=1}^N|a_n|^2b_n^{-1}
 \sum_{j,k=1}^J\overline{\eta_j}\eta_k
 B(\overline{s_j}+s_k,\overline{\chi_j}\chi_k)
\tag{60.10}
\]

라는 상수 1의 weighted Cauchy--Schwarz 형태다. Montgomery, *Topics in Multiplicative
Number Theory*, Lemma 1.6을 인용한다. 이 문장 자체에는 숨은 Vinogradov multiplier가 없고
finite-sum version은 직접 재증명 가능하다. 다만 analytic \(B\)-series의 절대수렴 가정까지
Lean으로 전개하는 일은 현재 최초 numerical blocker가 아니므로 뒤로 둔다.

### 4.4 Lemma 8: local zero count

Jutila Lemma 8은 local square 안의 영점 수를

\[
 \#\{\rho:\alpha\le\Re\rho\le1,
      |\Im\rho-T|\le(1-\alpha)/2\}
 \ll (1-\alpha)\log(q(T+1))+1
\tag{60.11}
\]

로 제한하고 Prachar p.331의 Linnik density lemma를 인용한다. implied constant가 숫자가
아니므로 이 단계도 hard blocker다. Bennett--Martin--O'Bryant--Rechnitzer의 explicit
\(N(T,\chi)\)는 전 높이 영점수에는 숫자를 주지만, 그대로 차분하면 식 (60.11)의
\((1-\alpha)\) 국소화가 보존되지 않는다. 따라서 useful fallback이지만 drop-in replacement는
아니다.

## 5. Huxley 계열 source의 역할

Huxley III의 Theorem 3과 Huxley--Jutila IV의 도입부는 \(\alpha>4/5\)에서 exponent 2형
density 경로를 제공한다. 대표적으로 fixed-modulus 형태는

\[
 \sum_{\chi\bmod q}N(\alpha,T,\chi)
 \ll_\varepsilon(qT)^{2-2\alpha+\varepsilon}.
\tag{60.12}
\]

그러나 원문은 `D sufficiently large`, `constant depending on ... and epsilon`, 그리고
여러 번 서로 같을 필요가 없는 \(o(1)\) exponent를 사용한다. 공식 PDF 확보로 source leaf는
닫혔지만 numerical multiplier·common cutoff는 닫히지 않았다.

## 6. 상태표

| ID | 명제·호출 | 이번 판정 | 다음 닫힘 조건 |
|---|---|---|---|
| `JL4-FULL` | Graham/Jutila Lemma 4 전체 점근식 | `SOURCE_THEOREM_UNFORMALIZED` | 원문 explicit \(O\) 또는 독립 재증명 |
| `JL4-T1PRIME-ACTUAL` | p.54 Theorem 1-prime weighted upper call | `ACTUAL_APPLICATION_EXPLICIT_SOURCE_REPLACEMENT` | 고정 `37.769894`; 식 (3.6)에 사용 금지 |
| `JL4-T1-DENSITY-ACTUAL` | p.52 식 (3.6)의 theta-dependent weighted upper call | `CORRECTED_BY_SUCCESSOR_THEORY66` | Theory 66의 \(K_{\rm BV}(\theta)\), `34/theta^2` 사용 |
| `JL5` | squarefree·coprime harmonic lower bound | `HARD_BLOCKER` | uniform eta·R0 숫자 |
| `JL6` | detector lower bound | `HARD_BLOCKER` | JL5 + Mellin/tail absolute constants |
| `JL7` | modified Halasz inequality | `EXACT_SOURCE_STATEMENT` | 필요 시 finite direct proof·Lean |
| `JL8` | local zero count | `HARD_BLOCKER` | local explicit constant 또는 budgeted weaker replacement |
| `HJ-LOW` | Huxley 계열 away-from-one density | `SOURCE_AVAILABLE_CONSTANTS_HIDDEN` | epsilon multiplier·cutoff 복원 |

## 7. Lean·기계검증 경계

- 식 (60.1)의 Theorem 1-prime \(\tau=8/5\) 대입과 exact rational 값은 Lean theorem
  `jutila_bv_actual_coefficient_value`로 검증한다.
- 식 (60.5)의 유리 대수는 `jutila_bv_actual_log_ratio_identity`로 검증한다.
- 외부 Corollary 1.3, Jutila Lemmas 4--8, Huxley density를 project-local axiom으로 선언하지
  않는다. 이들은 계속 `SOURCE_THEOREM_UNFORMALIZED` 또는 source premise 상태다.
- JSON·unittest는 source hash, exact rational, actual parameter map과 fail-closed root flags를
  검사한다.
- `sorry`, `admit`, project-local `axiom`은 사용하지 않는다.

## 8. 다음 권장 순서

1. `JL5a`: 식 (60.8)의 uniform finite lower bound를 source-first로 조사하고, 없으면 초등
   convolution·partial summation으로 직접 정량화한다.
2. `JL6a`: Mellin integral과 truncation tail을 분리해 각각 absolute constant를 붙인다.
3. `JL8a`: Prachar/Linnik local lemma의 원 source와 현대 explicit local zero-count를 비교한다.
4. 위 세 항이 숫자가 된 뒤 식 (3.6)의 theta-dependent branch와 Theorem 1-prime branch를
   섞지 않고 각각 종단 multiplier를 합성한다.
5. 그 뒤에만 Branch S의 \(K e^{-160c}\) gate와 \(0.1361687\ldots\) 예산을 비교한다.

현재 단계는 문헌·증명 감사이므로 장시간 CPU, 추가 Python package, 새 prime 계산이 필요 없다.

## 9. 참고문헌

- M. Jutila, *On Linnik's constant*, DOI
  [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- M. N. Huxley, *Large values of Dirichlet polynomials, III*, DOI
  [10.4064/aa-26-4-435-444](https://doi.org/10.4064/aa-26-4-435-444).
- M. N. Huxley and M. Jutila, *Large values of Dirichlet polynomials, IV*, DOI
  [10.4064/aa-32-3-297-312](https://doi.org/10.4064/aa-32-3-297-312).
- S. W. Graham, *An asymptotic estimate related to Selberg's sieve*, DOI
  [10.1016/0022-314X(78)90010-0](https://doi.org/10.1016/0022-314X(78)90010-0).
- O. Ramaré and S. Zuniga Alterman, *An \(L^2\)-bound for the Barban--Vehov weights*,
  [arXiv:2405.12662](https://arxiv.org/abs/2405.12662), DOI
  [10.7169/facm/241018-19-5](https://doi.org/10.7169/facm/241018-19-5).
- D. Berkane, *An explicit estimate for the Barban and Vehov weights*,
  [journal PDF](https://nntdm.net/papers/nntdm-20/NNTDM-20-2-35-43.pdf).
- S. Zuniga Alterman, *On a logarithmic sum related to the Selberg sieve*,
  [arXiv:2005.04280](https://arxiv.org/abs/2005.04280), DOI
  [10.4064/aa200712-22-6](https://doi.org/10.4064/aa200712-22-6).
- M. A. Bennett, G. Martin, K. O'Bryant and A. Rechnitzer,
  *Counting Zeros of Dirichlet L-Functions*,
  [arXiv:2005.02989](https://arxiv.org/abs/2005.02989).
