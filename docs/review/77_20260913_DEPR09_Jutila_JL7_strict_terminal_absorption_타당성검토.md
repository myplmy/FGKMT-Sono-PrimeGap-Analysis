# DEP-R09 Jutila JL7 strict 종단 흡수 타당성검토

- 검토일: 2026-09-13 KST
- 대상: [Theory 70](../method/theory/70_Sono_FMT_DEPR09_Jutila_JL7_strict_terminal_absorption.md)
- 원문: Jutila, *On Linnik's constant*, printed pp.51--53
- 판정: **한 fixed modulus의 actual nonprincipal near-one branch에 한해 타당함**
- 비판정: Jutila Theorem 1 전체, averaged 식 (3.7), PAP-11, DEP-R09,
  fixed \(2\times10^{-17}\), numerical \(X_{\rm cert}\)

## 1. 쉬운 결론

이번 단계는 지금까지 따로 계산한 비용들을 마지막 한 부등식에 넣어, 오차항을 왼쪽
주항에서 실제로 뺄 수 있는지 확인한 작업이다. 주항을 \(A\), 원하는 선형항을 \(BJY\),
다시 \(J^2\)에 붙는 위험한 오차를 \(EJ^2\)라 쓰면

\[
 AJ^2\le BJY+EJ^2
\]

이다. \(E\le A/2\)가 되도록 시작점을 명시하면 왼쪽에 최소 \(A/2\)가 남고,
\(J\)의 수치 상계를 안전하게 얻는다. Theory 70은 그 시작점을 기호식으로 만들었다.

다만 여기서 얻은 시작점은 \(X_{\rm cert}\)가 아니다. 고정된 modulus 하나와
\(\alpha\)가 1에 가까운 비주지표 영점 구역에만 해당한다. 여러 modulus를 합치는
averaged 단계와 그것을 소수 개수 하한으로 바꾸는 Gallagher--Maier 단계가 아직 남는다.

## 2. 원문 대조 방식은 적절한가

Jutila PDF의 native text layer는 사실상 비어 있어 OCR을 페이지 위치 탐색에만 사용했고,
printed pp.51--53 렌더링을 직접 대조했다. 확인 대상은 parity별 well-spaced system,
Lemma 7, 식 (3.6), shifted contour, principal residue와 마지막 흡수 문단이다.

이 방식은 적절하다. OCR 문자열만으로 계수나 지수를 판정하지 않았으며, source 식의
복소해석 부분을 Lean에서 증명한 것처럼 가장하지 않았다. 이번 새 증명은 앞 단계에서
source 고정한 값을 유한 대수로 합성하는 부분에 한정된다.

## 3. \(A,B,E\) 합성 검토

Theory 70의 핵심 정규화는

\[
 A=\underline c_g^2A_{\rm int},\qquad
 B=52C_{\rm pre},
\]

\[
 E=C_{\rm pre}A_{\rm int}\overline C_{\rm CL3}
   \left(\frac q{\varphi(q)}\right)^2L^{-2}e^{-\gamma L}.
\]

이다. 다음 이유로 차원이 맞는다.

1. weighted square-sum의 \(34/\theta^2\)와 denominator loss 5는
   \(C_{\rm pre}=170/\theta^2\)로 정확히 한 번 곱해진다.
2. contour 적분면적 \(A_{\rm int}\)는 contour \(J^2\) 항에 한 번 남는다.
3. residue 상수 52는 이미 residue 이중적분과 바깥 \(L^{-2}\) 정규화를 포함하므로
   \(A_{\rm int}\)를 다시 곱하지 않는다.
4. \(q/\varphi(q)\le6L\)을 제곱해 36을 얻으므로 \(L^{-2}\)가 정확히 상쇄된다.
5. even/odd factor 2는 한 system의 흡수식이 끝난 뒤 local count를 복원할 때만 들어간다.

## 4. 가장 위험한 중복 계상 점검

| 항 | 올바른 위치 | 잘못 넣었을 때 문제 | 이번 문서 |
|---|---|---|---|
| weight quotient 5 | \(C_{\rm pre}\) 한 번 | residue와 contour에 따로 다시 곱하면 중복 | 한 번만 반영 |
| Lemma 3 상수 3 | \(\overline C_{\rm CL3}\) | residue 52에 다시 곱하면 상수 3 중복 | 재곱하지 않음 |
| \(A_{\rm int}\) | detector와 contour 각 항에 한 번 | residue에도 넣으면 차원 오류 | residue에는 없음 |
| parity factor 2 | 최종 \(N_{\rm nonprin}\) | one-system \(A,B,E\)에 넣고 최종에 또 넣으면 중복 | 마지막에만 반영 |
| local row factor | \(3+r\log(2D)\) | selected \(J\)와 실제 zero count를 혼동 | 별도 복원 |

따라서 현재 합성에서 식별되는 계수 중복이나 누락은 없다.

## 5. strict cutoff 검토

\[
 \underline c_g=\frac35(1-\theta)\theta,\qquad
 \gamma=\frac{29\theta}{252}
\]

이고

\[
 \mathcal P=
 \frac{72C_{\rm pre}\overline C_{\rm CL3}}{\underline c_g^2},
\qquad
 L_{\rm abs}=\frac{\log\mathcal P}{\gamma}
\]

로 두면 \(L\ge L_{\rm abs}\)에서 \(E\le A/2<A\)가 성립한다.
여기서 72는 \(q/\varphi(q)\) 상계의 36과 half-margin의 2를 곱한 값이다.
strict 부등식이 필요한 지점에서 단순히 \(E\le A\)를 쓰지 않고 \(A/2\) 여유를
보존했으므로 fail-closed 조건으로 적합하다.

\(L\ge e^8\)은 \(4\log L/L\le29/252\)를 보장하는 독립적인 유한 gate이고,
Theory 64의 \(L_0\)까지 포함해

\[
 L_{\rm common}=\max\{L_0,e^8,L_{\rm abs}\}
\]

로 잡는 것도 논리적으로 타당하다. 다만 이 값들은 \(L=\log(qT)\) 기준이며,
\(\log X\)나 최종 theorem threshold와 동일시해서는 안 된다.

## 6. 수치 진단에서 얻는 정보

\(\theta=1/21\)에서

\[
 C_{\rm pre}=74970,\quad
 \overline C_{\rm CL3}=136224,\quad
 \underline c_g=4/147,\quad
 \mathcal P=993089345703840
\]

이고 \(L_{\rm abs}\approx6301.47\)이다. 동일한 loss 배분에서 선행 JL6 공통 cutoff는
약 8827.24로 더 크다. 그러므로 이 진단점에서는 새 종단 흡수가 병목을 더 악화시키지
않고 JL6 detector 단계가 계속 지배한다.

반면

\[
 C_J(\theta)=\frac{884000}{9(1-\theta)^2\theta^6}
\]

은 \(\theta\)가 작아질수록 대략 \(\theta^{-6}\)으로 급증한다. 따라서 이후 averaged
합성에서 \(\theta\)를 작게 잡는 것은 decay margin을 세밀하게 만드는 대신 최종 multiplier를
매우 크게 만드는 비용이 있다. 이 trade-off는 최종 calculator 이전에 최적화해야 한다.

고정밀 decimal은 진단값이지 outward-rounded interval certificate는 아니다. 엄밀한
판정은 exact rational coefficient와 기호적 cutoff implication에 의존한다.

## 7. Python·Lean 증거 경계

- Python checker는 exact rational endpoint, half-margin 양쪽과 잘못된 premise 거부를
  검사한다.
- Lean은 \(C_{\rm pre}\), rational detector lower, finite log gate, exponential cutoff,
  half-margin 대수, \(C_J\), parity/local-count 합성을 검증한다.
- Jutila Lemma 7의 complex integral과 predecessor source theorem은
  source premise 또는 미형식화 상태다.
- sorry, admit, project-local axiom은 사용하지 않는다.

따라서 Lean PASS는 이번 유한 합성의 오류를 막는 증거이지 Jutila의 외부 복소해석 정리를
독립 재증명했다는 뜻이 아니다.

## 8. 아직 닫히지 않은 부분

| 항목 | 상태 | 이유 |
|---|---|---|
| JL7-ABSORB, actual selected system | 닫힘 | strict half-margin과 \(C_J\) 명시 |
| actual nonprincipal near-one fixed-\(q\) density | 닫힘 | parity/local-count 복원 포함 |
| printed Jutila Theorem 1 전체 | OPEN | principal 및 away-from-one branch 미합성 |
| JL7-AVERAGED | HARD_BLOCKER | 식 (3.7)의 가변 modulus·primitive character 합 미감사 |
| Gallagher--Maier PAP bridge | HARD_BLOCKER | density에서 pointwise prime count까지 수치 전달 미완성 |
| PAP-11 / DEP-R09 | OPEN | root dependency 미완성 |
| fixed \(2\times10^{-17}\) / \(X_{\rm cert}\) | 미인증 / OPEN | calculator 착수 조건 미충족 |

## 9. 최종 판정과 다음 순서

Theory 70은 명시한 좁은 범위에서는 타당하다. 특히 residue 52, contour area, Lemma 3의
3과 parity 2를 중복하지 않은 점이 핵심이다. 다음 우선순위는 Jutila 식 (3.7)의
JL7-AVERAGED source-first replay다. conductor, primitive-character multiplicity,
principal character 처리와 modulus 합에서 새 \(Q\)-factor가 생기는지를 먼저 고정해야 한다.

그 다음에야 Gallagher--Maier pointwise PAP bridge를 합성할 수 있다. 두 단계가 닫히기
전에는 fixed \(2\times10^{-17}\) 인증이나 numerical \(X_{\rm cert}\) 계산기를 만들면 안 된다.

## 10. 참고문헌

- M. Jutila, *On Linnik's constant*, *Mathematica Scandinavica* 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- J. B. Rosser and L. Schoenfeld,
  *Approximate formulas for some functions of prime numbers*,
  *Illinois Journal of Mathematics* 6 (1962), 64--94,
  DOI [10.1215/ijm/1255631807](https://doi.org/10.1215/ijm/1255631807).
