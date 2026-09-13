# Sono/FMT DEP-R09 Jutila Lemma 6 Mellin 적분 명시화

- 작성일: 2026-09-13 KST
- 단계: `DEP-R09 / JL6a MELLIN INTEGRAL`
- 선행 정본: [Theory 61](61_Sono_FMT_DEPR09_Jutila_Lemma5_finite_harmonic_lower_bound.md)
- 기계 원장: [Jutila Lemma 6 Mellin v1](data/Sono_FMT_DEPR09_Jutila_Lemma6_Mellin_v1.json)
- 판정: `JL6-MELLIN ACTUAL_FORM_PARAMETERIZED_EXPLICIT / JL6-TAIL AND JL6 OPEN`
- 비목적: 절단 tail을 Mellin 적분과 합치기, actual prime sweep, threshold calculator,
  fixed (2\times10^{-17}) 또는 (X_{\rm cert}) 승격

> **후속 상태(2026-09-13):** [Theory 63](63_Sono_FMT_DEPR09_Jutila_Lemma6_truncation_tail_actual.md)이
> actual 선택 `R=D^epsilon`, `X=D^(1+12epsilon)`에서 truncation tail을
> `ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT`으로 닫았다. 인쇄된 일반 Lemma 6의
> uniform tail은 계속 OPEN이다. [Theory 64](64_Sono_FMT_DEPR09_Jutila_Lemma6_actual_common_budget.md)는
> damping까지 포함한 common budget을 합쳐 `JL6-ACTUAL`을 parameterized explicit로
> 닫았지만, printed general JL6·JL8·root certificate는 계속 OPEN이다.

## 1. 결론

Jutila 1977 Lemma 6 proof에서 첫 번째 숨은 오차인 Mellin 적분은 Jutila의 원래
power condition (2.8)을 강화하지 않고 계산 가능한 상수로 바꿀 수 있다. 적분선을 원문의
\(\Re w=-\beta\) 대신 조금 오른쪽인

\[
 \Re w=-\beta+\delta,\qquad 0<\delta\le\frac14
\]

에 두고, peer-reviewed Bennett--Martin--O'Bryant--Rechnitzer 2021이 정확히 전사한
Rademacher의 Dirichlet \(L\)-함수 convexity bound를 사용한다. 그 결과

\[
 \boxed{
 |I_{\delta_\varepsilon}|
 \le K_M(\delta_\varepsilon)A^{-\varepsilon/2}}
\tag{62.13}
\]

를 얻는다. 여기서

\[
 A=(qT)^{1/2}Rz_2,\qquad
 \delta_\varepsilon=\frac{\varepsilon}{4(1+\varepsilon)},
\]

\[
 K_M(\delta)=
 \frac{12\sqrt6}{\pi^{3/2}}
 \zeta(1+\delta)\left(\frac2\delta+1\right).
\]

그러나 원문은 이 적분을 작게 만든 뒤에도 무한급수를
\(x=X\log^2(qT)\)에서 자른 나머지를 별도로 \(\ll_\varepsilon1\)이라 쓴다.
식 (62.13)은 그 tail을 포함하지 않는다. 따라서 `JL6-MELLIN`만 진전하고 `JL6` 전체,
`JL8`, `PAP-11`, DEP-R09, fixed Sono 계수와 \(X_{\rm cert}\)는 계속 OPEN이다.

> 쉬운 설명: 긴 계산을 두 조각으로 나눴을 때 첫 조각의 최대 오차를 숫자가 있는 식으로
> 바꿨다. 두 번째 조각인 “어디서 계산을 잘랐을 때 버린 꼬리”는 아직 숫자로 제한하지
> 못했다. 첫 조각이 해결됐다고 전체 계산이 끝난 것은 아니다.

## 2. 원문 고정과 PDF 읽기 방식

| source | 확인 위치 | 읽기 방식 | 역할 |
|---|---|---|---|
| Jutila, *On Linnik's constant* | 인쇄 pp. 48--52, (2.1), (2.5)--(2.11), Lemma 6 | native text 18 bytes로 사실상 비어 OCR 후 원페이지 대조 | 원래 적분·weight·조건·두 오차의 분리 |
| Bennett et al., *Counting zeros of Dirichlet L-functions* | 인쇄 p. 1469, Lemma 5.6, (5.3) | native text 우선, 렌더링 원페이지 대조 | Rademacher convexity bound의 exact peer-reviewed 전사 |
| Fiori, *A note on the Phragmén--Lindelöf theorem* | pp. 1, 6 | native text 우선, 렌더링 원페이지 대조 | 최근 complex-log 오류 경고의 적용범위 확인 |
| NIST DLMF | §§2.5, 5.5, 5.9, 5.11 | 공식 웹 수식 | Mellin inversion·Gamma recurrence/integral/수직 감쇠 교차검증 |

Jutila가 직접 인용한 Prachar 1957 p. 380 Satz 3.2의 공개 원문은 식별하지 못했다.
OpenLibrary/Internet Archive의 제한 대출을 우회하지 않았다. 대신 표준 Mellin inversion을
NIST DLMF와 대조하고, 이 actual integrand의 contour 이동을 아래에서 직접 검사했다.

Rademacher 1959 원 논문의 DOI와 출판 metadata는 확인했으나 공개 full text는 독립적으로
읽지 못했다. 따라서 실제 사용 statement는 Bennett et al. Lemma 5.6 식 (5.3)에 고정한다.

## 3. Jutila의 원래 식과 분리해야 할 두 오차

\(\rho=\beta+it\)를 비주지표 \(\chi\pmod q\)의 영점이라 하자. Jutila 식 (2.11)은
Mellin 이동 뒤 다음 형태다.

\[
\begin{aligned}
 &e^{-1/X}\sum_{r\le R}'\frac1r
 +\sum_{n>z_1}a(n)\chi(n)e^{-n/X}n^{-\rho}
   \sum_{r\le R}'\frac{\psi_r(n)}r \\
 &=\frac1{2\pi}\int_{-\infty}^{\infty}
 L(i(t+u),\chi)\Gamma(-\beta+iu)X^{-\beta+iu}
 \sum_{r\le R}'\frac1r M(i(t+u),\chi,\psi_r)\,du.
\end{aligned}
\tag{62.1}
\]

원문은 오른쪽을 \(\ll_\varepsilon1\)로 제한한 뒤, 다음 페이지에서 양쪽 무한급수를
\(x=X\log^2(qT)\)에서 자른 나머지도 다시 \(\ll_\varepsilon1\)이라 쓴다. 이 두 문장은
서로 다른 증명 의무다.

## 4. contour를 오른쪽으로 옮기는 이유

원문의 \(\Re w=-\beta\)에서는 \(L\)이 \(\Re s=0\)에 놓인다. 이를 그대로 명시화하면
functional equation 주변 상수가 더 복잡해진다. 대신

\[
 \Re w=-\beta+\delta
\tag{62.2}
\]

로 이동하면 \(L(\rho+w,\chi)=L(\delta+i(t+u),\chi)\)가 된다.

- \(-1<-\beta+\delta<0\)이므로 Gamma의 pole 중 \(w=0\)만 지난다.
- 그 residue에는 \(L(\rho,\chi)=0\)가 곱해져 0이다.
- \(w=-1\)은 지나지 않는다.
- \(M\)은 유한 Dirichlet polynomial이다.
- 수평변의 \(L\)-함수 polynomial growth는 Gamma의 지수감쇠에 눌리므로 사라진다.

따라서 같은 왼쪽 급수는

\[
 I_\delta=\frac1{2\pi}\int_{-\infty}^{\infty}
 L(\delta+i(t+u),\chi)\Gamma(-\beta+\delta+iu)
 X^{-\beta+\delta+iu}
 \sum_{r\le R}'\frac1rM(\delta+i(t+u),\chi,\psi_r)\,du
\]

로 쓸 수 있다. 이 complex-analytic 이동은 문헌과 직접 proof의 영역이며 Lean local axiom으로
넣지 않는다.

## 5. actual Barban--Vehov weight의 \(M\) 상계

Jutila에서

\[
 f(n)=\psi(n)=\mu(n)\varphi(n),\qquad \xi_d=\lambda_d,
\]

이고 (2.5)--(2.6)에서 \(|\lambda_d|\le1\), \(d\le z_2\) support다. 식 (2.1)에서
\(g=(r,d)\)라 하면

- \(p\mid g\)인 local factor의 절대값은 \(p-1\),
- \(p\mid r/g\)인 factor는
  \(|1-p\chi(p)p^{-s}|\le1+p^{1-\delta}\le p+1\)

이다. 두 경우 모두 \(p^2/(p-1)\) 이하이므로

\[
 |M(\delta+iv,\chi,\psi_r)|
 \le z_2\frac{r^2}{\varphi(r)}.
\tag{62.3}
\]

또한

\[
 \frac n{\varphi(n)}=\sum_{d\mid n}\frac{\mu^2(d)}{\varphi(d)}
\]

이므로

\[
\begin{aligned}
 \sum_{n\le R}\frac n{\varphi(n)}
 &\le R\prod_p\left(1+\frac1{p(p-1)}\right) \\
 &<R\exp\left(\sum_{m=2}^{\infty}\frac1{m(m-1)}\right)
 =eR<3R.
\end{aligned}
\tag{62.4}
\]

따라서 prime과 \(q\)-서로소 조건을 버린 더 큰 합으로

\[
 \sum_{r\le R}'\frac1r|M(\delta+iv,\chi,\psi_r)|<3Rz_2.
\]

원문에 숨은 \(\ll Rz_2\)의 이 부분에는 이제 절대 multiplier 3을 쓸 수 있다.

## 6. imprimitive character를 빠뜨리지 않은 \(L\)-상계

\(\chi\pmod q\)가 conductor \(f>1\)인 primitive \(\chi^*\)에서 유도되면

\[
 L(s,\chi)=L(s,\chi^*)
 \prod_{\substack{p\mid q\\p\nmid f}}(1-\chi^*(p)p^{-s}).
\]

\(\Re s=\delta\)에서 \(p\ge5\)이면 \(1+p^{-\delta}\le2\le\sqrt p\)다.
빠진 소수 2와 3이 모두 있을 때의 가장 나쁜 추가비용만 남기면

\[
 \sqrt f\prod_{\substack{p\mid q\\p\nmid f}}(1+p^{-\delta})
 \le\frac4{\sqrt6}\sqrt q.
\tag{62.5}
\]

Bennett et al. 식 (5.3)에 \(\eta=\sigma=\delta\)를 넣으면 primitive 지표에 대해

\[
 |L(\delta+iv,\chi^*)|
 \le\zeta(1+\delta)
 \left(\frac f{2\pi}|1+\delta+iv|\right)^{1/2}.
\tag{62.6}
\]

\(|t|\le T\), \(T\ge1\)이면

\[
 |1+\delta+i(t+u)|
 \le\frac94T(1+|u|).
\]

식 (62.5)--(62.6)을 합치면

\[
 |L(\delta+i(t+u),\chi)|
 \le \sqrt{\frac3\pi}\zeta(1+\delta)(qT)^{1/2}(1+|u|)^{1/2}.
\tag{62.7}
\]

Fiori 2026이 지적한 최근 오류는 \(|\log(Q+s)|\)를 다루는 방식이다. 식 (62.6)은
\(|s+1|\)의 실수 거듭제곱이므로 그 특정 complex-log 오류를 사용하지 않는다. 그렇다고
Fiori 논문이 이번 전체 contour proof를 대신 증명한다는 뜻도 아니다.

## 7. Gamma 적분의 초등 상계

\[
 a=-\beta+\delta,\qquad -1+\delta<a\le-\frac14,
 \qquad 1<a+2\le\frac74.
\]

Gamma recurrence를 두 번 쓰면

\[
 |\Gamma(a+iu)|=
 \frac{|\Gamma(a+2+iu)|}{|a+iu|\,|a+1+iu|}.
\]

Gamma 적분에서 \(|\Gamma(a+2+iu)|\le\Gamma(a+2)<2\)다. 마지막 2는
적분을 \([0,1]\)과 \([1,\infty)\)로 나누어 각각 1과 \(2/e\)보다 작게 잡은 보수값이다.
따라서

\[
 |\Gamma(a+iu)|\le
 \begin{cases}
  8/\delta,&|u|\le1,\\
  2/u^2,&|u|\ge1.
 \end{cases}
\tag{62.8}
\]

이고 \(u\ge1\)에서 \((1+u)^{1/2}\le\sqrt2u^{1/2}\)를 써서

\[
 \int_{-\infty}^{\infty}(1+|u|)^{1/2}|\Gamma(a+iu)|\,du
 \le8\sqrt2\left(\frac2\delta+1\right).
\tag{62.9}
\]

## 8. 상수 합성과 Jutila (2.8) transfer

식 (62.3)--(62.9)를 \(1/(2\pi)\)와 합치면

\[
 |I_\delta|\le K_M(\delta)A X^{-\beta+\delta},
\tag{62.10}
\]

\[
 K_M(\delta)=
 \frac{12\sqrt6}{\pi^{3/2}}\zeta(1+\delta)
 \left(\frac2\delta+1\right).
\]

다음 선택은 모든 \(\varepsilon>0\)에서 \(0<\delta_\varepsilon<1/4\)다.

\[
 \delta_\varepsilon=\frac{\varepsilon}{4(1+\varepsilon)}.
\tag{62.11}
\]

Jutila (2.8)의 power condition

\[
 X^\alpha\ge A^{1+\varepsilon}
\]

과 \(\beta\ge\alpha\ge1/2\), \(A>1\)을 쓰면 exponent는

\[
\begin{aligned}
 1-\frac{(1+\varepsilon)(\beta-\delta_\varepsilon)}\alpha
 &\le-\varepsilon+\frac{(1+\varepsilon)\delta_\varepsilon}\alpha\\
 &\le-\varepsilon+2(1+\varepsilon)\delta_\varepsilon
 =-\frac\varepsilon2.
\end{aligned}
\tag{62.12}
\]

이것이 식 (62.13)을 준다. Jutila의 별도 조건
\(\log R\ll\log(qT)\)는 이 고립된 Mellin 상계에는 쓰지 않았지만, JL6 전체와 actual
parameter 합성에서는 여전히 원 조건으로 보존한다.

## 9. 수치 진단의 의미

`source/dep_r09_jutila_jl6_mellin.py`는 \(q,T,R,z_2,X,\alpha,\beta,\varepsilon\)을 받아
다음 두 값을 계산한다.

1. 식 (62.10)의 직접 bound
2. (2.8)이 충족될 때 식 (62.13)의 더 단순한 transferred bound

이는 100-dps `mpmath` 진단이며 directed interval certificate가 아니다. 또한 원 power
condition이 거짓이면 boolean을 `false`로 남긴다. 어떤 경우에도 tail이 닫혔다거나
JL6 전체가 닫혔다고 반환하지 않는다.

## 10. Lean 형식검증 경계

단일 파일 `lean/FGKMTSono/TheoryVerification.lean`에는 다음 유한 대수만 넣는다.

- \(\delta_\varepsilon\)의 양수성과 \(1/4\) 미만
- local prime factor의 유리부등식
- \(|1+\delta+i(t+u)|\)에 쓰는 실수 triangle budget
- 식 (62.12)의 exponent budget
- 상수의 유한 대수 합성

Mellin inversion, contour 이동, Rademacher convexity theorem, Gamma complex integral을
project-local `axiom`으로 넣지 않는다. 이 부분은
`SOURCE_THEOREM_UNFORMALIZED` 또는 `PARTIAL_FORMALIZATION`으로 남긴다. `sorry`,
`admit`, project-local `axiom`은 사용하지 않는다.

## 11. 상태와 다음 proof gate

| ID | 판정 | 의미 |
|---|---|---|
| `JL5` | `EXPLICIT_PEER_REVIEWED_SOURCE_REPLACEMENT_WITH_Q_DEPENDENT_CUTOFF` | Theory 61 유지 |
| `JL6-MELLIN` | `ACTUAL_FORM_PARAMETERIZED_EXPLICIT` | actual integrand·weight에서 절대상수 복원 |
| `JL6-TAIL` | `HARD_BLOCKER` | \(x=X\log^2(qT)\) 이후 tail의 절대상수 필요 |
| `JL6` | `HARD_BLOCKER` | JL5·Mellin·tail 공통 error budget과 finite cutoff 필요 |
| `JL8` | `HARD_BLOCKER` | local zero-count multiplier 필요 |
| `PAP-11` / DEP-R09 | `OPEN` | full density composition 미완 |
| fixed \(2\times10^{-17}\) / \(X_{\rm cert}\) | `OPEN` | calculator 제작 금지 유지 |

다음 우선순위는 `JL6b`다. 먼저 tail 자체를 기존 explicit incomplete-Gamma 또는
exponential Dirichlet-series 선행정리로 직접 닫을 수 있는지 조사하고, 정확히 맞는 source가
없을 때만 \(n>x\)의 두 series를 actual \(a(n),\psi_r(n)\)에 맞춰 직접 상계한다.

## 12. 참고문헌

- M. Jutila, *On Linnik's constant*, Math. Scand. 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- M. A. Bennett, G. Martin, K. O'Bryant, A. Rechnitzer,
  *Counting zeros of Dirichlet L-functions*, Math. Comp. 90 (2021), 1455--1482,
  DOI [10.1090/mcom/3599](https://doi.org/10.1090/mcom/3599),
  arXiv [2005.02989](https://arxiv.org/abs/2005.02989).
- H. Rademacher, *On the Phragmén--Lindelöf theorem and some applications*,
  Math. Z. 72 (1959), 192--204,
  DOI [10.1007/BF01162949](https://doi.org/10.1007/BF01162949).
- A. Fiori, *A note on the Phragmén--Lindelöf theorem*, J. Math. Anal. Appl.
  559 (2026), 130404, DOI
  [10.1016/j.jmaa.2026.130404](https://doi.org/10.1016/j.jmaa.2026.130404),
  arXiv [2502.13282](https://arxiv.org/abs/2502.13282).
- NIST Digital Library of Mathematical Functions,
  [Mellin transforms](https://dlmf.nist.gov/2.5),
  [Gamma recurrence](https://dlmf.nist.gov/5.5),
  [Gamma integral](https://dlmf.nist.gov/5.9),
  [vertical-line asymptotic](https://dlmf.nist.gov/5.11#E9).
