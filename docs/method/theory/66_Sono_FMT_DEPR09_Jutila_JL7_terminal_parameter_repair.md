# Sono/FMT DEP-R09 Jutila JL7·식 (3.6) 종단 매개변수 교정

- 작성일: 2026-09-13 KST
- 단계: `DEP-R09 / JL7 AND EQUATION (3.6) TERMINAL PARAMETER REPAIR`
- 선행 정본: [Theory 65](65_Sono_FMT_DEPR09_Jutila_Lemma8_actual_local_zero_count.md)
- 교정 대상: [Theory 60](60_Sono_FMT_DEPR09_Jutila_Lemma4_8_source_inventory.md)
- 기계 원장: [JL7 terminal v1](data/Sono_FMT_DEPR09_Jutila_JL7_terminal_v1.json)
- 판정: `EQUATION_3_6_PARAMETER_REPAIRED / WEIGHTED CALL EXPLICIT / TERMINAL MULTIPLIERS OPEN`
- 비목적: general JL8 재증명, averaged density 완성, PAP-11·DEP-R09·fixed
  \(2\times10^{-17}\)·\(X_{\rm cert}\) 인증, actual prime 계산

## 1. 결론과 중대한 선행 문서 교정

Jutila 원문을 식 (3.6)과 Theorem \(1'\)의 두 proof branch로 다시 대조하자, Theory 60의
적용범위 표기에 오류가 있었다. 기존 exact 값

\[
 \tau=\frac85,\qquad K_{\rm BV}=\frac{18884947}{500000}=37.769894
\tag{66.1}
\]

는 인쇄 p.54의 **Theorem \(1'\)** 선택
\((a_1,a_2,c)=(5/2,4,11/2)\)에 맞는 값이다. 인쇄 p.52의 Theorem 1 식 (3.6)은

\[
 R=D^\theta,\qquad
 z_1=D^{1/2+7\theta},\qquad
 z_2=D^{1/2+8\theta},\qquad
 X=D^{1+12\theta},\qquad
 x=X(\log D)^2
\tag{66.2}
\]

를 사용하므로 \(\tau\)가 \(\theta\)에 따라 달라진다. 따라서 식 (3.6)에
`37.769894`를 고정 대입하면 안 된다.

올바른 대입으로 식 (3.6)의 weighted square-sum 호출은 다시 명시화할 수 있었다. 그러나
그 뒤 contour integral, Lemma 3 합, residue·well-spacing의 \(\ll_\theta\) multiplier가
원문에 숫자로 주어지지 않는다. 이 때문에 이번 단계는 **매개변수 오류를 고치고 이미 보이는
유한 손실을 숫자로 만든 단계**이며, 종단 density theorem 자체는 아직 OPEN이다.

> 쉬운 설명: 같은 논문의 서로 다른 두 계산에 서로 다른 톱니바퀴 크기가 쓰였는데, 앞선
> 문서가 뒤쪽 계산의 톱니바퀴 `37.769894`를 앞쪽 계산에도 붙였다. 이번에는 앞쪽 계산에
> 맞는 크기를 다시 계산했다. 이 부품은 고쳤지만, 그 다음 두 부품에는 아직 제조사가 적어
> 놓지 않은 허용오차가 남아 있어 전체 기계를 합격시킨 것은 아니다.

## 2. source와 원문 대조 방식

| source | 확인 위치 | 읽기 방식 | 판정상 역할 |
|---|---|---|---|
| Jutila 1977, *On Linnik's constant* | printed pp.51--54, Lemma 7, (3.2)--(3.7), Theorems 1·\(1'\) | native text 18 bytes로 사실상 비어 300 dpi OCR을 locator로 쓴 뒤 렌더링 원페이지와 대조 | 두 매개변수 branch와 숨은 종단 multiplier 식별 |
| Ramaré--Zuniga Alterman, *An \(L^2\)-bound for the Barban--Vehov weights* | Corollary 1.3 | native text 우선, 렌더링 식 대조 | 모든 \(\tau>1\)에 대한 explicit weighted upper bound |
| Ramaré 2016, *An explicit density estimate for Dirichlet \(L\)-series* | Theorem 1.1 | native text 우선, 정리 원페이지 대조 | 명시적 대체자료 가능성의 source-first 비교 |

Jutila scan에서 OCR은 수식 판독의 최종 근거로 쓰지 않았다. 특히 \(z_1,z_2,X,x\)의
지수와 Theorem \(1'\)의 별도 매개변수는 렌더링 원페이지에서 다시 확인했다.

## 3. 식 (3.6)의 올바른 Barban--Vehov 특수화

식 (66.2)에서

\[
 \tau_\theta=\frac{\log z_2}{\log z_1}
 =\frac{1+16\theta}{1+14\theta},\qquad
 \tau_\theta-1=\frac{2\theta}{1+14\theta}.
\tag{66.3}
\]

Ramaré--Zuniga Corollary 1.3의 계수에 이를 exact rational로 대입하면

\[
\begin{aligned}
 K_{\rm BV}(\theta)
 &=\frac{309}{200}\,
 \frac{\frac{2327}{500}+\frac{34421}{250}\theta+\frac{255149}{250}\theta^2}
      {\theta(1+14\theta)}.
\end{aligned}
\tag{66.4}
\]

모든 \(0<\theta\le1/21\)에서

\[
 K_{\rm BV}(\theta)<\frac{13}{\theta}.
\tag{66.5}
\]

식 (66.5)의 양의 분모를 제거한 차이를 \(Q(\theta)\)라 하면

\[
 Q(\theta)=13(1+14\theta)-\frac{309}{200}\left(\frac{2327}{500}
 +\frac{34421}{250}\theta+\frac{255149}{250}\theta^2\right),\qquad
 Q(1/21)=\frac{11334739}{14700000}>0.
\tag{66.6}
\]

\(Q'(\theta)<0\)인 구간이므로 이 끝점 값이 하한이다. 이 유리 대수와 부등식은 Lean에서
독립 검증한다.

또한 \(L=\log D\)라 두면

\[
 \frac{\log x}{\log(z_2/z_1)}
 =\frac1\theta+12+\frac{2\log L}{\theta L}.
\tag{66.7}
\]

\(L\ge4\)이면 \(2\log L\le L\)이고, \(\theta\le1/21\)이므로

\[
 \frac{\log x}{\log(z_2/z_1)}\le\frac{18}{7\theta}.
\tag{66.8}
\]

따라서 Corollary 1.3이 주는 actual one-sided 호출은

\[
 \sum_{n\le x}\frac{a(n)^2}{n^{2\alpha-1}}
 <\frac{34}{\theta^2}\,x^{2-2\alpha}
\tag{66.9}
\]

로 쓸 수 있다. 이는 식 (3.6)의 `JL4-T1-DENSITY-ACTUAL`을
`ACTUAL_APPLICATION_PARAMETERIZED_EXPLICIT_SOURCE_REPLACEMENT`로 닫는다. 외부
Corollary 1.3 자체의 analytic proof는 Lean에 local axiom으로 넣지 않는다.

예를 들어 계수는 다음과 같이 변한다.

| \(\theta\) | \(\tau_\theta\) | \(K_{\rm BV}(\theta)\) |
|---:|---:|---:|
| \(1/1000\) | \(508/507\) | \(7302.493689\ldots\) |
| \(1/100\) | \(58/57\) | \(831.169287\ldots\) |
| \(1/21\) | \(37/35\) | \(263.284509\ldots\) |

고정 `37.769894`와의 차이는 작은 보정이 아니라 적용 branch 자체의 차이다.

## 4. Lemma 7의 \(b_n^{-1}\)에서 생기는 손실

Jutila 식 (3.3)의 weight를 식 (3.6)에 넣으면 다음 quotient가 나타난다.

\[
 W(n;M,N,x)=
 \frac{e^{-2n/x}}{e^{-n/N}-e^{-n/M}}.
\tag{66.10}
\]

actual integration range에서 \(z_1<n\le x\), \(N\ge x\), \(M\le z_1\)이고
\(x/z_1\ge4\)라 하자. \(n=\sqrt{xz_1}\)에서 나누면

- \(n\le\sqrt{xz_1}\)일 때 분모는
  \(e^{-1/2}-e^{-1}>1/5\),
- \(n\ge\sqrt{xz_1}\)일 때 분모는
  \(e^{-1}-e^{-2}>1/5\)

보다 크다. 여기에는
\(e^{-1/2}>3/5\), \(9/25<e^{-1}<2/5\)만 쓰면 충분하다. 분자는 1 이하이므로

\[
 0<W(n;M,N,x)<5.
\tag{66.11}
\]

즉 `JL7-WEIGHT-DENOMINATOR`의 숨은 손실은 project finite component로 5에 닫힌다.
단, 이 5는 뒤의 contour·residue multiplier를 대신하지 않는다.

## 5. integration 면적과 detector 정규화

식 (3.4)--(3.5)의 두 적분 길이를 곱하고 \(L^2\)로 나눈 exact factor는

\[
 A_{\rm int}(\theta,L)=\theta^2\left(\frac12+7\theta\right)
 \left(1+12\theta+\frac{2\log L}{L}\right)
 \ge\frac{\theta^2}{2}\qquad(L\ge1).
\tag{66.12}
\]

Theory 64가 actual JL6에 대해 준 detector coefficient는

\[
 c_g(\theta)=(1-\theta)\frac6{\pi^2}\theta.
\tag{66.13}
\]

따라서 Lemma 7을 적분한 왼쪽의 정규화 계수는

\[
 A_{\rm left}(\theta,L)=c_g(\theta)^2A_{\rm int}(\theta,L)>0.
\tag{66.14}
\]

이다. 이 면적을 단순히 \(\ll_\theta\) 속에 숨기면 종단 흡수 cutoff를 계산할 수 없으므로,
향후 모든 식에서는 \(A_{\rm left}\)를 명시적으로 보존한다.

## 6. off-diagonal exponent와 finite \(\log L/L\) gate

Jutila p.53의 contour contribution에서 \(\delta=1-\alpha\le\theta\)를 적용하면, 로그
보정을 제외한 \(D\)-지수의 최악값은

\[
 E_0(\theta)
 =2\theta(1+12\theta)+\frac12
  -\left(\frac12+7\theta\right)(1-\theta)^2+2\theta
 =-2\theta+\frac{75}{2}\theta^2-7\theta^3.
\tag{66.15}
\]

\(0<\theta\le1/21\)에서

\[
 E_0(\theta)\le-\frac{29}{126}\theta.
\tag{66.16}
\]

\(x^{2\delta}\)의 \((\log D)^{4\delta}=L^{4\delta}\)를 \(D\)-거듭제곱으로 바꾸는
유한 보정까지 포함하려면

\[
 \frac{4\log L}{L}\le\frac{29}{252}
 \quad\Longrightarrow\quad
 E_{\rm total}(\theta,L)\le-\frac{29}{252}\theta.
\tag{66.17}
\]

를 충분조건으로 쓸 수 있다. 이로써 off-diagonal 항의 **감쇠 방향과 명시적 지수 여유**는
닫혔다. 그러나 그 앞에 곱해진 원문의 \(\ll_\theta\) multiplier가 아직 숫자가 아니므로
해당 항 전체의 흡수 cutoff는 계산할 수 없다.

## 7. 종단 inequality에서 실제 남은 상수

원문 p.53은 최종적으로 정성식

\[
 \left(\frac{\varphi(q)}q\right)^2J^2L^2
 \ll_\theta
 \left(\frac{\varphi(q)}q\right)^2Jx^{2-2\alpha}L^2+J^2
\tag{66.18}
\]

을 얻고 “which implies (1.7)”이라고 끝낸다. numerical proof에서는 이를 단순히 나눌 수
없다. 정확한 interface는 양의 \(A,B,E\)에 대해

\[
 AJ^2\le BJY+EJ^2,\qquad E<A
 \quad\Longrightarrow\quad
 (A-E)J\le BY,\qquad J\le\frac{BY}{A-E}
\tag{66.19}
\]

로 써야 한다. 식 (66.19)의 유한 대수는 Lean에서 검증한다. 여기서
\(A=A_{\rm left}(\theta,L)\)는 이번 단계에서 explicit이고, weighted diagonal의 보이는
부분은 식 (66.9)와 (66.11)로 explicit이다. 그러나 \(B,E\)를 완성하려면 다음 source
multiplier가 필요하다.

| ID | 남은 항 | 원문 상태 | 닫힘에 필요한 것 |
|---|---|---|---|
| `JL7-CONT` | shifted contour \(I_d(s,\chi)\) | \(I_d\ll_\theta D^{1/2}(M/d)^{-1+\theta}\) | actual 범위에서 uniform numerical multiplier·cutoff |
| `JL7-LEMMA3` | \(r,r',d\) absolute sum | “by Lemma 3” | Lemma 3 multiplier와 endpoint 전수 합성 |
| `JL7-RES` | principal residue·well-spacing | \(\ll_\theta\) 뒤 한 문단 | 같은 character의 여러 높이까지 포함한 numerical row-sum |
| `JL7-ABSORB` | 마지막 \(J^2\) 흡수 | “implies (1.7)” | \(q/\varphi(q)\), \(L\), 위 multiplier를 식 (66.19)에 대입 |
| `JL7-AVERAGED` | 식 (3.7)에서 (1.8) | “easy ... arguing as before” | variable modulus·primitive/principal case를 전부 재실행 |

## 8. explicit density 선행연구가 바로 대체하지 못하는 이유

source-first 원칙에 따라 Ramaré 2016 Theorem 1.1도 조사했다. 이 정리는
\(T\ge2000\), \(T\ge Q\ge10\), \(\sigma\ge0.52\)에서 명시적인 averaged density 상계를
주지만, 우변에

\[
 32Q^2\log^2(Q^2T)
\tag{66.20}
\]

이라는 additive 항이 남는다. \(1-\sigma=\lambda/\log D\)이고 \(Q\)가 커지는 현재 near-one
regime에서는 이 항을 bounded multiplier의 \(D^{c(1-\sigma)}\)로 일률 흡수할 수 없다.
따라서 좋은 비교 source이지만 Jutila의 near-one log-free density에 대한 drop-in replacement는
아니다. 이를 사용하려면 PAP transfer 자체를 새로 설계해야 한다.

## 9. 기계검증과 증거 경계

- [Python evaluator](../../../source/dep_r09_jutila_jl7_terminal_interface.py)는 exact
  rational 특수화, log ratio, weight quotient, 면적, exponent gate를 검사한다.
- [fail-closed tests](../../../tests/test_dep_r09_jutila_jl7_terminal_interface.py)는 두
  branch의 scope 분리, source hash, exact 값과 root false flag를 검사한다.
- Lean 단일 파일은 식 (66.3)--(66.8), (66.12), (66.15)--(66.17), (66.19)의 유한 대수와
  식 (66.11)에 쓰인 elementary exponential slack을 검증한다.
- Ramaré--Zuniga Corollary 1.3, Jutila의 character series·contour·residue 계산,
  Ramaré density theorem을 project-local axiom으로 선언하지 않는다.
- `sorry`, `admit`, project-local `axiom`을 사용하지 않는다.

따라서 이번 Lean PASS는 외부 analytic source theorem을 독립 형식증명했다는 뜻이 아니다.

## 10. 상태와 다음 권장 순서

```text
JL4-T1PRIME-ACTUAL fixed 37.769894       = EXPLICIT, page-54 branch only
JL4-T1-DENSITY-ACTUAL theta coefficient  = PARAMETERIZED EXPLICIT
JL7 finite Cauchy--Schwarz statement      = EXACT SOURCE STATEMENT
JL7 weight denominator loss               = PROJECT FINITE COMPONENT EXPLICIT (5)
JL7 integration/detector normalization    = PARAMETERIZED EXPLICIT
JL7 off-diagonal exponent direction       = PARAMETERIZED EXPLICIT
JL7 contour/Lemma3/residue multipliers     = HARD BLOCKER
Jutila terminal density / averaged form   = OPEN / OPEN
PAP-11 / DEP-R09 / fixed 2e-17 / X_cert   = OPEN / OPEN / NOT CERTIFIED / OPEN
threshold calculator                      = NOT READY
```

다음 우선순위는 `JL7-CONT`다. 먼저 Jutila가 contour 이동에 사용한 gamma·\(L\)-function
상계의 선행 source에 numerical multiplier가 있는지 조사한다. 없으면 actual
\(0<\theta\le1/21\) 범위만 직접 정량화한다. 그 뒤 `JL7-LEMMA3`, `JL7-RES`,
`JL7-ABSORB`, 마지막으로 averaged 식 (3.7) 순서가 가장 짧다.

이번 단계에는 장시간 CPU 계산, 새 Python package, actual prime 데이터가 필요하지 않다.

## 11. 참고문헌

- M. Jutila, *On Linnik's constant*, Math. Scand. 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- O. Ramaré and S. Zuniga Alterman, *An \(L^2\)-bound for the Barban--Vehov weights*,
  DOI [10.7169/facm/241018-19-5](https://doi.org/10.7169/facm/241018-19-5),
  arXiv [2405.12662](https://arxiv.org/abs/2405.12662).
- O. Ramaré, *An explicit density estimate for Dirichlet \(L\)-series*,
  [author PDF](https://ramare-olivier.github.io/Maths/DensityEstimate-34.pdf).
