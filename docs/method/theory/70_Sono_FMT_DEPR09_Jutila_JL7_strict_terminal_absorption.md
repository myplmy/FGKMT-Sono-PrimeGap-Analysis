# Sono/FMT DEP-R09 Jutila JL7 strict 종단 흡수

- 작성일: 2026-09-13 KST
- 단계: **DEP-R09 / JL7-ABSORB**
- 선행 정본: [Theory 69](69_Sono_FMT_DEPR09_Jutila_JL7_principal_residue_height_row_sum.md)
- 기계 원장: [JL7 absorption v1](data/Sono_FMT_DEPR09_Jutila_JL7_absorption_v1.json)
- 판정: **JL7-ABSORB = ACTUAL NONPRINCIPAL NEAR-ONE PARAMETERIZED EXPLICIT**
- 비목적: Jutila Theorem 1의 전 \(\alpha\) 범위 또는 식 (3.7)의 averaged theorem 완성,
  PAP-11·DEP-R09·fixed \(2\times10^{-17}\) 인증, numerical \(X_{\rm cert}\) 계산기 제작,
  actual prime 계산

## 1. 결론

Theory 64--69의 detector, weighted square sum, denominator, contour, Lemma 3와 residue
상수를 한 식에 넣으면 Jutila printed p.53의 마지막 \(J^2\) 항을 엄밀히 흡수할 수 있다.
actual 범위는

\[
 0<\theta\le\frac1{21},\qquad
 D=qT,\quad q\ge3,\quad T\ge1,\quad L=\log D,
 \qquad 0<\delta:=1-\alpha\le\theta .
\tag{70.1}
\]

Theory 64의 네 detector loss budget을 양수로 배분해 합이
\(\eta_{\rm out}\le\theta\)가 되게 하고, 아래 식 (70.17)의 공통 cutoff를 만족시키면 한
even 또는 odd selected system의 크기 \(J\)에

\[
 \boxed{
 J\le C_J(\theta)x^{2\delta},\qquad
 C_J(\theta)=
 \frac{884000}{9(1-\theta)^2\theta^6},
 \qquad x=D^{1+12\theta}L^2 .}
\tag{70.2}
\]

Theory 65의 짝·홀 및 local zero-count 복원을 마지막에 적용하면

\[
 \boxed{
 N_{\rm nonprin}(\alpha,T,q)
 \le2C_J(\theta)x^{2\delta}
       \{3+r\log(2D)\},
 \qquad r=\max\{\delta,L^{-1}\}.}
\tag{70.3}
\]

따라서 actual **비주지표 near-one pointwise branch**의 종단 density는
parameterized explicit이다. 그러나 principal character, \(4/5\le\alpha<1-\theta\)인
away-from-one branch, 고전적 \(D^{(2+\varepsilon)(1-\alpha)}\) 형태로의 전체 재매개화와
가변 modulus averaged 식 (3.7)은 이 결론에 포함되지 않는다.

> **쉬운 설명:** 지금까지 숫자로 만든 여러 비용을 한 계산서에 처음으로 모두 넣었다.
> 주 신호가 오차보다 최소 두 배 크도록 시작점을 잡을 수 있었고, 그 뒤에는 양쪽에서 같은
> 항을 안전하게 빼도 된다. 다만 이것은 한 고정 modulus의 1에 가까운 영점 구역에 대한
> 계산서다. Sono가 필요로 하는 여러 modulus의 합과 소수 개수 부등식까지 끝난 것은 아니다.

## 2. source-first 대조와 적용 범위

| source·정본 | 확인 위치 | 이번 역할 | 판독·판정 |
|---|---|---|---|
| Jutila, *On Linnik's constant* | printed p.46 (1.7), pp.51--53 Lemmas 7--8, (3.1)--(3.6) | 한 selected system, contour·residue와 마지막 흡수 구조 | native text 18 bytes라 OCR은 locator만 사용하고 렌더링 원페이지 대조 |
| Theory 64 | (64.3), (64.20) | detector lower와 \(L_0\) | actual JL6 parameterized explicit |
| Theory 65 | (65.21) | local count와 짝·홀 factor 2 | actual near-one explicit source replacement |
| Theory 66 | (66.9), (66.11)--(66.17), (66.19) | weighted·denominator·area·decay·strict algebra | finite/parameterized explicit |
| Theories 67--68 | (67.17), (68.12) | contour와 Lemma 3 | actual-input parameterized explicit |
| Theory 69 | (69.2) | 한 system residue 52 | actual-input parameterized explicit |

Jutila p.53은 모든 multiplier를 \(\ll_\theta\)에 숨긴 뒤 “which implies (1.7)”이라고
끝낸다. 이번 단계는 새 외부 analytic theorem을 가정하지 않고, 앞 여섯 감사에서 이미
source 고정한 actual component들을 차원에 맞게 합성한다. 별도 lemma를 찾아 대체할
필요가 없는 유한 대수 단계이므로 source-first 원칙과 직접 증명 원칙이 충돌하지 않는다.

## 3. preterminal multiplier는 한 번만 곱한다

Theory 66의 weighted square-sum과 Lemma 7 denominator quotient가 만드는 공통 계수는

\[
 C_{\rm pre}(\theta)
 :=5\frac{34}{\theta^2}
 =\frac{170}{\theta^2}.
\tag{70.4}
\]

Theory 68의 contour와 Lemma 3 합성에는

\[
 \overline C_{\rm CL3}(\theta)
 :=144\left(1+\frac1\theta\right)
       \left(\frac2\theta+1\right)
\tag{70.5}
\]

를 쓴다. Theory 69의 residue multiplier는 52다. 이 52에는 p.53 residue의 이중적분,
\(L^{-2}\) 바깥 정규화, 대각 \(r\)-합과 height row가 이미 포함되어 있다. 따라서
\(\overline C_{\rm CL3}\)의 Lemma 3 상수 3이나 아래 \(A_{\rm int}\)를 residue에 다시
곱하면 중복 계상이다.

## 4. 왼쪽 detector와 rational lower

Theory 64의 actual detector coefficient와 Theory 66의 normalized integration area는

\[
 c_g(\theta)=(1-\theta)\frac6{\pi^2}\theta,\qquad
 A_{\rm int}(\theta,L)=
 \theta^2\left(\frac12+7\theta\right)
 \left(1+12\theta+\frac{2\log L}{L}\right)
 \ge\frac{\theta^2}{2}.
\tag{70.6}
\]

\(\pi^2<10\)이므로 완전한 유리수 lower를

\[
 \underline c_g(\theta):=\frac35(1-\theta)\theta<c_g(\theta)
\tag{70.7}
\]

로 둔다. 그러면 Lemma 7의 왼쪽을

\[
 \underline c_g(\theta)^2 A_{\rm int}(\theta,L)
 \left(\frac{\varphi(q)}q\right)^2J^2L^2
\tag{70.8}
\]

로 아래에서 잡을 수 있다.

## 5. contour 적분면적과 residue의 차원

contour bound의 \(M^{-1+\theta}\)를 \(\xi\)-구간 왼쪽 끝에서 상계한 뒤 남는 이중적분
면적은 정확히 \(A_{\rm int}L^2\)이다. 식 (3.6)의 바깥 \(L^{-2}\)와 상쇄되므로 contour
항에는 \(A_{\rm int}\)가 **한 번** 남는다. Theory 66의 finite log gate 뒤
\(\gamma(\theta)=29\theta/252\)라 쓰면, 앞 단계의 모든 안전 상계를 넣은 한-system 식은

\[
\begin{aligned}
 &\underline c_g^2A_{\rm int}
   \left(\frac{\varphi(q)}q\right)^2J^2L^2 \\
 &\quad\le C_{\rm pre}\Bigg[
 52\left(\frac{\varphi(q)}q\right)^2Jx^{2\delta}L^2
 +A_{\rm int}\overline C_{\rm CL3}J^2e^{-\gamma L}
 \Bigg].
\end{aligned}
\tag{70.9}
\]

여기서 첫 줄의 \(A_{\rm int}\)는 detector를 같은 \(\xi,\eta\) 영역에서 적분한 결과이고,
둘째 줄의 \(A_{\rm int}\)는 contour를 그 영역에서 상계한 결과다. 서로 다른 두 항에 한
번씩 나타났다가 흡수비에서 상쇄된다. residue 52에는 새 \(A_{\rm int}\)가 없다.

## 6. \(A,B,E\) 정규화

식 (70.9)를 \((\varphi(q)/q)^2L^2\)로 나누고 \(Y=x^{2\delta}\)라 두면

\[
 AJ^2\le BJY+EJ^2,\qquad
 A=\underline c_g^2A_{\rm int},\quad
 B=52C_{\rm pre},
\tag{70.10}
\]

\[
 E=C_{\rm pre}A_{\rm int}\overline C_{\rm CL3}
 \left(\frac q{\varphi(q)}\right)^2L^{-2}e^{-\gamma L}.
\tag{70.11}
\]

Theory 64의 \(q/\varphi(q)\le6L\)을 넣으면

\[
 E\le36C_{\rm pre}A_{\rm int}\overline C_{\rm CL3}e^{-\gamma L}.
\tag{70.12}
\]

## 7. strict half-margin cutoff와 공통 cutoff

다음을 정의한다.

\[
 \mathcal P(\theta):=
 \frac{72C_{\rm pre}(\theta)\overline C_{\rm CL3}(\theta)}
      {\underline c_g(\theta)^2},\qquad
 L_{\rm abs}(\theta):=\frac{\log\mathcal P(\theta)}{\gamma(\theta)}.
\tag{70.13}
\]

\(L\ge L_{\rm abs}\)이면 \(e^{-\gamma L}\le1/\mathcal P\)이므로 식 (70.12)는

\[
 E\le\frac12\underline c_g^2A_{\rm int}=\frac A2<A.
\tag{70.14}
\]

strict \(E<A\)가 자동으로 보존된다. transcendental log 계산을 쓰지 않는 교차검산용
보수적 충분조건은

\[
 L\ge L_{\rm abs}^{\rm rat}(\theta)
 :=\frac{\mathcal P(\theta)}{\gamma(\theta)}
 \quad\Longrightarrow\quad L\ge L_{\rm abs}(\theta),
\tag{70.15}
\]

이다. \(\log u\le u\)를 쓴 것이므로 매우 크며 실제 계산기 권장값은 아니다.

Theory 66의 \(4\log L/L\le29/252\)에도 완전히 계산 가능한 충분조건을 준다.
\(\log L/L\)는 \(L\ge e\)에서 감소하고 \(e^8\ge8^6/6!=16384/45\)이므로

\[
 L\ge e^8
 \quad\Longrightarrow\quad
 \frac{4\log L}{L}\le\frac{32}{e^8}
 \le\frac{45}{512}<\frac{29}{252}.
\tag{70.16}
\]

따라서 Theory 64의 \(L_0(\theta,\eta_5,\eta_X,\eta_M,\eta_T)\)와 합친 공통
충분 cutoff는

\[
 \boxed{
 L_{\rm common}:=
 \max\{L_0,\ e^8,\ L_{\rm abs}(\theta)\}.}
\tag{70.17}
\]

이 식은 numerical \(X_{\rm cert}\)가 아니다. Jutila actual fixed-modulus near-one
component 하나의 \(L=\log D\) cutoff다.

## 8. 선택 system과 전체 nonprincipal count

식 (70.14)와 Theory 66의 fail-closed algebra에서

\[
 J\le\frac{2B}{A}Y
 \le\frac{104C_{\rm pre}}
          {\underline c_g^2(\theta^2/2)}x^{2\delta}
 =\frac{884000}{9(1-\theta)^2\theta^6}x^{2\delta},
\tag{70.18}
\]

이므로 식 (70.2)가 나온다. 이 \(C_J\)에는 한 parity system만 들어 있다. Jutila
p.51의 even/odd 두 system과 Theory 65 local square를 복원해야 식 (70.3)이 된다.
factor 2를 식 (70.10)의 \(A,B,E\)에 먼저 넣고 다시 식 (70.3)에 넣으면 중복이다.

## 9. 수치 진단과 의미

네 JL6 loss를 각각 \(\theta/4\)로 배분한 120-dps 진단은 다음과 같다.

| \(\theta\) | \(L_{\rm abs}\) | 선행 \(L_0\) | 공통 cutoff 지배항 | \(C_J\) |
|---:|---:|---:|---|---:|
| \(1/21\) | 6301.465743... | 8827.240704... | JL6 common | 9,287,613,243,090 |
| \(1/100\) | 38028.656061... | 91726.754431... | JL6 common | \(1.0021653\times10^{17}\) |
| \(1/1000\) | 500064.527589... | 2900654.663772... | JL6 common | \(9.8418962\times10^{22}\) |

\(\theta=1/21\)에서 exact 값은

\[
 C_{\rm pre}=74970,\quad
 \overline C_{\rm CL3}=136224,\quad
 \underline c_g=\frac4{147},\quad
 \gamma=\frac{29}{5292},\quad
 \mathcal P=993089345703840.
\tag{70.19}
\]

공통 cutoff에서 계산한 \(E/A\) 상계는 약 \(4.8734\times10^{-7}\)로 \(1/2\)보다
훨씬 작다. 즉 현재 세 진단점에서는 새 absorption보다 선행 JL6 detector cutoff가 더
큰 병목이다. 이 decimal은 directed interval certificate가 아니라 진단이며, 엄밀한 결론은
식 (70.13)--(70.17)의 기호적 implication이다.

## 10. 정확히 무엇이 닫혔고 무엇이 남았는가

| ID | 판정 | 의미·다음 의무 |
|---|---|---|
| JL7-ABSORB | **ACTUAL_NONPRINCIPAL_NEAR_ONE_PARAMETERIZED_EXPLICIT** | 한 fixed modulus의 selected system과 식 (70.3) |
| Jutila printed Theorem 1 전체 | OPEN | principal·away-from-one·전체 \(\varepsilon\) 재매개화 |
| JL7-AVERAGED | HARD_BLOCKER | 식 (3.7)의 variable modulus·primitive character replay |
| Gallagher--Maier PAP bridge | HARD_BLOCKER | density에서 one-sided prime count까지의 수치 합성 |
| PAP-11 / DEP-R09 | HARD_BLOCKER / OPEN | root 상태 변화 없음 |
| fixed \(2\times10^{-17}\) / \(X_{\rm cert}\) | NOT CERTIFIED / OPEN | threshold calculator 제작 금지 유지 |

machine field terminal_density_closed=true는 오직
terminal_density_scope=ACTUAL_NONPRINCIPAL_NEAR_ONE_ONLY와 함께 읽어야 한다. printed
Theorem 1 전체나 averaged theorem을 뜻하지 않는다.

## 11. Python·Lean 증거 경계

- [finite evaluator](../../../source/dep_r09_jutila_jl7_absorption.py)는 모든 rational
  coefficient, logarithmic/rational cutoff와 common-cutoff diagnostic을 계산한다.
- [fail-closed tests](../../../tests/test_dep_r09_jutila_jl7_absorption.py)는 predecessor
  상태, source hash, endpoint exact 값, half-margin 양쪽과 잘못된 premise를 검사한다.
- Lean 단일 파일은 \(C_{\rm pre}\), rational detector lower, \(e^8\) log gate,
  exponential cutoff transfer, half-margin terminal algebra, \(C_J\)와 parity composition을
  검증한다.
- Jutila Lemma 7의 complex/character 전체, predecessor analytic sources와 무한합은
  project-local axiom으로 채우지 않는다. 해당 식은 source theorem 또는 conditional/partial
  상태로 남긴다.
- sorry, admit, project-local axiom은 사용하지 않는다.

따라서 Lean PASS는 외부 analytic theorem을 새로 증명했다는 뜻이 아니라, 고정된 source
premise를 받았을 때 이번 dependency-critical 종단 대수에 오류가 없다는 증거다.

## 12. 다음 권장 gate

다음 순서는 JL7-AVERAGED다. 먼저 Jutila p.53--54의 식 (3.7)이 \(q\le Q\)의 primitive
character를 어떤 conductor와 multiplicity로 세는지 source 재전사하고, fixed-modulus
식 (70.9)의 각 상수가 modulus 합에서도 그대로인지 또는 \(Q\)-factor가 추가되는지
확인해야 한다. 이 단계가 닫혀도 Gallagher--Maier PAP bridge와 \(X_{\rm cert}\)는 자동으로
닫히지 않는다.

## 13. 참고문헌

- M. Jutila, *On Linnik's constant*, *Mathematica Scandinavica* 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- J. B. Rosser and L. Schoenfeld,
  *Approximate formulas for some functions of prime numbers*,
  *Illinois Journal of Mathematics* 6 (1962), 64--94,
  DOI [10.1215/ijm/1255631807](https://doi.org/10.1215/ijm/1255631807).
