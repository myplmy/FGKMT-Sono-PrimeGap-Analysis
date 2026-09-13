# Sono/FMT DEP-R09 Jutila Lemma 6 actual 공통 오차예산

- 작성일: 2026-09-13 KST
- 단계: **DEP-R09 / JL6c ACTUAL COMMON DETECTOR BUDGET**
- 선행 정본: [Theory 63](63_Sono_FMT_DEPR09_Jutila_Lemma6_truncation_tail_actual.md)
- 기계 원장: [Jutila Lemma 6 common budget v1](data/Sono_FMT_DEPR09_Jutila_Lemma6_common_budget_v1.json)
- 판정: **JL6-ACTUAL ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT / PRINTED GENERAL JL6 AND JL8 OPEN**
- 비목적: 인쇄된 Lemma 6의 임의 매개변수 전체를 닫기, JL8 승격, actual prime sweep,
  fixed \(2\times10^{-17}\) 또는 \(X_{\rm cert}\) 계산기 제작

## 1. 결론

Jutila 1977 식 (2.11)의 actual application에서는 이제 Lemma 5 주항 오차, 지수 감쇠,
Mellin 적분, 절단 tail을 하나의 명시적 예산으로 합칠 수 있다. Jutila의 작은 양의
매개변수를 \(\theta\)라 쓰고

\[
 0<\theta\le\frac1{21},\qquad
 D=qT,\quad R=D^\theta,\quad
 z_2=D^{1/2+8\theta},\quad X=D^{1+12\theta}
\tag{64.1}
\]

라 하자. 네 양의 loss를

\[
 \eta_5+\eta_X+\eta_M+\eta_T
 \le\eta_{\rm out}\le\theta
\tag{64.2}
\]

로 배분한다. 이 문서의 계산 가능한 \(L_0=L_0(\theta,\eta_5,\eta_X,\eta_M,\eta_T)\)에
대해

\[
 \log D\ge L_0
 \Longrightarrow
 |g(\rho,\chi)|
 \ge(1-\eta_{\rm out})
 \frac6{\pi^2}\frac{\varphi(q)}q\log R
 \ge(1-\theta)
 \frac6{\pi^2}\frac{\varphi(q)}q\log R .
\tag{64.3}
\]

따라서 Jutila가 p.52에서 실제로 쓰는 매개변수와
\(\alpha\ge1-\theta\)에 한정한 **actual JL6**는
**ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT**이다. 이것은 인쇄된 일반 Lemma 6의
임의 \(R,X,\alpha\) 전체를 증명한 것이 아니다. 특히 일반 tail의 uniform cancellation은
여전히 열려 있다. JL8, PAP-11, DEP-R09, fixed Sono 계수와 numerical
\(X_{\rm cert}\)도 OPEN이다.

> 쉬운 설명: 앞 단계에서 오차 세 종류를 각각 숫자로 바꿨지만, 원 식 앞에는
> \(e^{-1/X}\)라는 작은 감쇠도 있었다. 이번에는 그 감쇠까지 네 번째 비용으로 포함해
> 총비용이 원 논문이 허용한 \(\theta\)를 넘지 않도록 했다. 이로써 실제 후속 증명에서
> 쓰는 JL6 한 부품은 닫혔다. 그러나 그 다음 부품인 JL8과 전체 PAP 조립은 아직 남아 있다.

## 2. source와 읽기 방식

| source | 확인 위치 | 읽기 방식 | 역할 |
|---|---|---|---|
| Jutila, *On Linnik's constant* | 인쇄 pp. 50--52, (2.8)--(2.11), (3.2) | native text 18 bytes로 사실상 비어 OCR locator 뒤 렌더링 원페이지 대조 | 정확한 부호, 네 번째 감쇠, actual 매개변수 |
| Zuniga Alterman, *Explicit averages of square-free supported functions* | 인쇄 pp. 10--12, Cor. 3.4(b), (3.16) | native text 우선, 원페이지 대조 | JL5 절대오차 \((1277/500)\mathcal B_qR^{-1/3}\) |
| Rosser--Schoenfeld, *Approximate formulas for some functions of prime numbers* | 인쇄 p.72, Theorem 15, (3.41)--(3.42) | text locator와 scan 원페이지 대조 | \(q/\varphi(q)\)의 예외안전 명시 상계 |

Jutila 원페이지에서 식 (2.11)의 왼쪽은 양의 주항과 무한 \(n\)-합이고, 식 (2.9)의
\(g\)는 그 무한합을 \(x\)에서 자른 유한 부분이다. 따라서 아래 부호는 추정이 아니라
source identity에서 나온다.

## 3. 정확한 detector identity와 네 loss

\[
 M+g+E_{\rm tail}=I,\qquad
 M=e^{-1/X}S_q(R),
\qquad
 S_q(R)=\sum_{\substack{r\le R\\(r,q)=1}}\frac{\mu^2(r)}r .
\tag{64.4}
\]

\(M>0\)이므로 triangle inequality는

\[
 |g|\ge M-|I|-|E_{\rm tail}|
\tag{64.5}
\]

방향이다. Theory 61의 source 식과

\[
 C_\varphi:=\frac6{\pi^2}\frac{\varphi(q)}q
\tag{64.6}
\]

를 사용해 JL5 source error를
\(\eta_5C_\varphi\log R\) 이하로 만들면

\[
 S_q(R)\ge(1-\eta_5)C_\varphi\log R.
\tag{64.7}
\]

또한 \(e^{-u}\ge1-u\)와 \(u=1/X\)에서

\[
 X^{-1}\le\eta_X
 \Longrightarrow
 e^{-1/X}S_q(R)
 \ge(1-\eta_X)(1-\eta_5)C_\varphi\log R
 \ge(1-\eta_X-\eta_5)C_\varphi\log R.
\tag{64.8}
\]

여기에

\[
 |I|\le\eta_M C_\varphi\log R,\qquad
 |E_{\rm tail}|\le\eta_T C_\varphi\log R
\tag{64.9}
\]

를 넣으면 식 (64.2)--(64.3)이 나온다. 감쇠 \(\eta_X\)를 빼고 세 항만 더하면
원문의 최종 계수를 엄밀히 보존할 수 없으므로 허용하지 않는다.

## 4. actual power condition

actual 선택에서

\[
 A=(qT)^{1/2}Rz_2=D^{1+9\theta}.
\tag{64.10}
\]

Jutila p.51에서 현재 proof branch는 \(\alpha\ge1-\theta\)다. \(D>1\)이므로 식 (2.8)의
\(X^\alpha\ge A^{1+\theta}\)에는 다음 exponent margin이면 충분하다.

\[
\begin{aligned}
 &(1-\theta)(1+12\theta)
 -(1+\theta)(1+9\theta)\\
 &\qquad=\theta(1-21\theta)\ge0.
\end{aligned}
\tag{64.11}
\]

따라서 \(0<\theta\le1/21\)이면 원래 power condition을 강화하지 않는다.
또 \(\log R=\theta\log D\)이고

\[
 \log D\ge\theta^{-2}
 \Longrightarrow
 \sqrt{\log q}\le\sqrt{\log D}\le\theta\log D=\log R.
\tag{64.12}
\]

\(\theta\le1\)이므로 \(\log R\le\log D\)도 자동이다.

## 5. 공통 정규화 \(1/C_\varphi\)

\(L=\log D\ge e\)라 하자. \(3\le q\le15\)에서는 exact 계산으로
\(\max q/\varphi(q)=3\)이다. \(q\ge16\)에서는 Rosser--Schoenfeld Theorem 15의
유일한 예외까지 포함한 식 (3.41)--(3.42)에
\(e^\gamma<3\), \(2.50637<3\), \(\log\log q>1\)을 쓰면

\[
 \frac q{\varphi(q)}
 <3\log\log q+\frac3{\log\log q}
 \le6\log q\le6L.
\tag{64.13}
\]

따라서 모든 actual \(q\ge3\)에 대해

\[
 \frac1{C_\varphi}
 =\frac{\pi^2}{6}\frac q{\varphi(q)}
 \le\pi^2L.
\tag{64.14}
\]

이 한 식으로 Mellin과 tail의 절대오차를 같은 상대오차 단위로 바꾼다.

## 6. \(\mathcal B_q\)의 elementary uniform envelope

Zuniga Alterman의

\[
 \mathcal B_q=
 \prod_{p\mid q}
 \left(1+\frac{p^{2/3}-1}{p^{4/3}+1}\right)
\tag{64.15}
\]

에서 각 local factor는 \(1+p^{-2/3}\le e^{p^{-2/3}}\) 이하이다. 서로 다른 소인수를
\(p_1<\cdots<p_\omega\)라 쓰면 \(p_i\ge i\), \(\omega\log2\le\log q\le L\)이고

\[
 \sum_{i=1}^{\omega}i^{-2/3}
 \le1+\int_1^\omega t^{-2/3}\,dt
 =3\omega^{1/3}-2
 \le3\omega^{1/3}.
\tag{64.16}
\]

따라서

\[
 \mathcal B_q
 \le\exp\!\left(3\left(\frac L{\log2}\right)^{1/3}\right).
\tag{64.17}
\]

특히

\[
 L\ge L_B(\theta):=
 \left(\frac{18}{\theta(\log2)^{1/3}}\right)^{3/2}
 \Longrightarrow
 \log\mathcal B_q\le\frac{\theta L}{6}.
\tag{64.18}
\]

이는 간단함을 우선한 매우 보수적 상계다. 현재 JL6을 닫는 데 충분하지만 최종 cutoff를
줄이는 후속 최적화 후보로 남긴다.

## 7. 네 component cutoff

Theory 61, 식 (64.14), \(R=D^\theta\)와 식 (64.18)에서 JL5 source error의 상대비는

\[
 \frac{(1277/500)\mathcal B_qR^{-1/3}}
 {C_\varphi\log R}
 \le\frac{1277\pi^2}{500\theta}
 e^{-\theta L/6}.
\tag{64.19}
\]

Theory 62의 \(K_M\)과 Theory 63의 tail을 같은 방식으로 정규화하면 다음 여덟 수의
최댓값을 충분 cutoff로 취할 수 있다.

\[
\boxed{
\begin{aligned}
 L_0=\max\Bigg\{&
 e,\ \theta^{-2},\
 \left(\frac{18}{\theta(\log2)^{1/3}}\right)^{3/2},\\
 &\frac6\theta\log\frac{(1277/500)\pi^2}{\theta\eta_5},\
 \frac{\log(1/\eta_X)}{1+12\theta},\\
 &\frac{2}{\theta(1+9\theta)}
   \log\frac{\pi^2K_M(\delta_\theta)}{\theta\eta_M},\\
 &2(1+13\theta),\
 \sqrt{2\log\frac{4\pi^2}{\theta\eta_T}}
 \Bigg\},
\end{aligned}}
\tag{64.20}
\]

\[
 \delta_\theta=\frac{\theta}{4(1+\theta)},\qquad
 K_M(\delta)=\frac{12\sqrt6}{\pi^{3/2}}
 \zeta(1+\delta)\left(\frac2\delta+1\right).
\tag{64.21}
\]

각 항의 역할은 순서대로 base range, 원래 \(\log R\) 조건,
\(\mathcal B_q\) 흡수, JL5, 감쇠, Mellin, tail의 선형부, tail의 상대오차부다.
식 (64.20)은 최소 cutoff가 아니라 검증하기 쉬운 충분 cutoff다.

## 8. 수치 진단

\(\theta=1/100\), \(\eta_{\rm out}=\theta\), 네 budget을 각각 \(\theta/4\)로 두면
120-dps 진단은

\[
 \delta_\theta=0.00247524752475\ldots,\qquad
 K_M=1\,727\,755.159185\ldots,
\tag{64.22}
\]

\[
 L_0=91\,726.754431106\ldots
\tag{64.23}
\]

이다. 이 예에서는 \(L_B(\theta)\)가 최대 항이다. 즉 현재 숫자를 크게 만드는 주원인은
Mellin이나 tail이 아니라 모든 \(q\le D\)를 한 번에 덮는 \(\mathcal B_q\)의 거친
elementary envelope다.

이 수치는 high-precision 진단이지 바깥쪽으로 반올림한 directed certificate가 아니다.
엄밀한 내용은 식 (64.20)의 기호적 implication이다. 또한 \(D\ge e^{L_0}\)는 JL6 한 단계의
충분조건일 뿐, Sono 정리 전체의 \(X_{\rm cert}\)가 아니다.

## 9. Python·Lean 증거 경계

- evaluator: [dep_r09_jutila_jl6_common_budget.py](../../../source/dep_r09_jutila_jl6_common_budget.py)
- fail-closed tests:
  [test_dep_r09_jutila_jl6_common_budget.py](../../../tests/test_dep_r09_jutila_jl6_common_budget.py)
- machine ledger:
  [Sono_FMT_DEPR09_Jutila_Lemma6_common_budget_v1.json](data/Sono_FMT_DEPR09_Jutila_Lemma6_common_budget_v1.json)
- Lean 단일 파일은 식 (64.11)의 exponent margin, 두 multiplicative loss의 합,
  네 budget의 최종 transfer와 식 (64.18)의 유한 실수대수를 검증한다.
- Zuniga Alterman·Rosser--Schoenfeld의 analytic theorem, character/Mellin identity와
  무한급수 proof를 project-local axiom으로 넣지 않는다.
- 금지된 proof escape인 sorry, admit, project-local axiom을 사용하지 않는다.

따라서 Lean 통과는 source analytic theorem의 독립 형식증명이 아니라, 그 theorem을
정확한 premise로 썼을 때 dependency-critical 유한 대수가 맞다는 증거다.

## 10. 상태표와 다음 gate

| ID | 현재 판정 | 의미 |
|---|---|---|
| JL5 | EXPLICIT peer-reviewed source replacement | Theory 61 유지 |
| JL6-MELLIN | ACTUAL_FORM_PARAMETERIZED_EXPLICIT | Theory 62 유지 |
| JL6-TAIL-ACTUAL | ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT | Theory 63 유지 |
| JL6-COMMON-BUDGET | ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT | 네 loss와 공통 \(L_0\) |
| JL6-ACTUAL | ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT | p.52 parameter branch |
| JL6-PRINTED-GENERAL | OPEN | 임의 \(X\)의 uniform tail/cancellation 미증명 |
| JL8 | HARD_BLOCKER | local zero-count multiplier·finite range 필요 |
| PAP-11 / DEP-R09 | OPEN | density 종단 합성 미완 |
| fixed \(2\times10^{-17}\) / \(X_{\rm cert}\) | OPEN | calculator 제작 금지 유지 |

다음 권장 우선순위는 JL8 source-first 감사다. 먼저 Jutila가 인용한 Linnik/Prachar 형태와
현대 peer-reviewed explicit local zero-count theorem이 정확히 같은 square와
\((1-\alpha)\log(q(T+1))+1\) 구조를 수치 multiplier·범위까지 주는지 조사한다.

## 11. 참고문헌

- M. Jutila, *On Linnik's constant*, Math. Scand. 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- S. Zuniga Alterman, *Explicit averages of square-free supported functions:
  to the edge of the convolution method*, Colloq. Math. 168 (2022), 1--23,
  DOI [10.4064/cm8337-11-2020](https://doi.org/10.4064/cm8337-11-2020),
  arXiv [2003.05887](https://arxiv.org/abs/2003.05887).
- J. B. Rosser and L. Schoenfeld,
  *Approximate formulas for some functions of prime numbers*,
  Illinois J. Math. 6 (1962), 64--94,
  DOI [10.1215/ijm/1255631807](https://doi.org/10.1215/ijm/1255631807).
