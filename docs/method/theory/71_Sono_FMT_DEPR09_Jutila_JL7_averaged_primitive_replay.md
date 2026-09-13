# Sono/FMT DEP-R09 Jutila JL7 averaged primitive replay

- 작성일: 2026-09-14 KST
- 단계: **DEP-R09 / JL7-AVERAGED-NP-NEAR-ONE**
- 선행 정본: [Theory 70](70_Sono_FMT_DEPR09_Jutila_JL7_strict_terminal_absorption.md)
- 기계 원장: [JL7 averaged v1](data/Sono_FMT_DEPR09_Jutila_JL7_averaged_v1.json)
- 판정: **primitive nonprincipal near-one averaged branch =**
  **ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT**
- 계속 OPEN: Jutila printed Theorem 1의 전 \(\alpha\) 범위, principal zeta branch,
  Gallagher--Maier pointwise PAP transfer, `PAP-11`, `DEP-R09`, fixed
  \(2\times10^{-17}\), numerical \(X_{\rm cert}\)

## 1. 결론

Jutila 1977 printed pp.53--54의 식 (3.7)은 서로 다른 modulus의 primitive character를
한 번에 다루지만, 논문은 \(|\eta_j|=q_j/\varphi(q_j)\)를 고른 뒤 “arguing as before”라고
쓰고 수치 계산을 생략한다. 이번 감사에서는 선행 Theory 61--70의 실제 부품을 공통 family
scale

\[
 D:=Q^2T,\qquad L:=\log D
\tag{71.1}
\]

에서 다시 합성했다. 그 결과 primitive nonprincipal character \(\chi_j\)의 conductor가
\(q_j\le Q\), \(0<1-\alpha\le\theta\le1/21\)인 branch에 대해 계산 가능한 공통
cutoff 뒤

\[
 N^*_{\rm np}(\alpha,T,Q)
 \le 2C_J(\theta)x^{2(1-\alpha)}
 \{3+r\log(2D)\},
 \qquad
 C_J(\theta)=
 \frac{884000}{9(1-\theta)^2\theta^6}
\tag{71.2}
\]

를 얻는다. 여기서

\[
 x=D^{1+12\theta}L^2,\qquad
 r=\max\{1-\alpha,L^{-1}\}.
\tag{71.3}
\]

이 식은 식 (3.7)의 실제 near-one averaged 부품을 수치화한 것이다. 그러나 Jutila가
인쇄한 모든 \(4/5\le\alpha\le1\)의 \((2+\varepsilon)(1-\alpha)\) 꼴 정리나,
그 정리를 prime count로 옮기는 Gallagher--Maier 증명은 아직 아니다.

> **쉬운 설명:** 앞 단계는 한 도로에서만 차량 수를 세었다. 이번에는 여러 도로를 동시에
> 세는 공식에서 도로마다 다른 보정값이 정확히 지워지는지 확인했다. 보정값은 실제로
> 지워졌고, 도로 수 \(Q\)를 잘못 한 번 더 곱할 필요도 없었다. 다만 이 결과를 “모든
> 산술진행에 충분히 많은 소수가 있다”는 최종 명제로 바꾸는 다리는 아직 남아 있다.

## 2. source-first 조사와 PDF 판독

| source | 확인 위치 | 이번 역할 | 판독·판정 |
|---|---|---|---|
| Jutila, *On Linnik's constant* | printed p.46 (1.7)--(1.8), pp.50--54 Lemmas 6--8, (3.1)--(3.7) | 식 (3.7), phase 크기, primitive principal-pair 조건 | native text 18 bytes라 OCR은 locator만 사용하고 렌더 원페이지 대조 |
| Jutila, *Zero-density estimates for L-functions* | complete printed pp.55--62; 특히 Theorem (1.2)--(1.4), Corollary (1.5)--(1.8), Lemma 3(ii) | variable primitive-conductor mean-value 구조 교차검증 | 5개 landscape PDF page에 두 인쇄면씩 수록; native text 5 bytes라 OCR은 locator만 쓰고 전체 인쇄면 대조; \(\ll_{\varepsilon,k}\)라 수치 drop-in 아님 |
| Theories 61--70 | 각 finite component | detector, local count, weighted sum, contour, pseudocharacter sum, residue, strict absorption | source premise와 kernel-checked finite algebra를 구분하여 재사용 |

두 Jutila 원문 및 후속 관련 문헌을 표적 검색했지만 식 (3.7)의 생략된 계산을 numerical
multiplier와 finite cutoff까지 그대로 재현한 선행정리는 식별하지 못했다. 이는 전 세계
문헌에 그런 결과가 없다는 주장이 아니다. 두 번째 논문은 primitive conductor \(\le Q\)인
가변 character의 mean-value 구조를 확인해 주지만 \((QT)^\varepsilon\)와 implied
constant를 남기므로 이번 계산기의 직접 입력으로 채택하지 않았다.

## 3. 식 (3.7)의 정확한 역할

Jutila의 일반화된 Halasz inequality를 표기만 압축하면

\[
 \left|\sum_{j=1}^J\eta_j
   \sum_n a_nC(n,\chi_j)\chi_j(n)n^{-s_j}\right|^2
 \le
 \sum_n|a_n|^2b_n^{-1}
 \sum_{j,k}\bar\eta_j\eta_k\,
 \mathcal B_{jk}(\bar s_j+s_k)
\tag{71.4}
\]

이다. 여기서

\[
 C(m,\chi_j)=
 \sum_{\substack{r\le R\\(r,q_j)=1}}'
 \frac{\psi_r(m)}r
\tag{71.5}
\]

는 \(\chi_j\)의 conductor modulus \(q_j\)에 따라 달라진다. 식 (71.4)는 고정
modulus 식을 나중에 더한 것이 아니라, 처음부터 \(C(\cdot,\chi_j)\)가 서로 달라도 되는
한 개의 부등식이다. 따라서 modulus 평균에서 raw \(Q\) factor를 임의로 붙이면 안 된다.

## 4. 공통 scale에서 detector를 다시 증명해야 하는 이유

각 \(j\)에 대해

\[
 A_j:=(q_jT)^{1/2}Rz_2,\qquad
 R=D^\theta,\quad z_2=D^{1/2+8\theta}
\tag{71.6}
\]

라 두자. \(1\le q_jT\le D\)이므로 서로 다른 두 방향의 envelope가 성립한다.

\[
 \boxed{
 D^{1/2+9\theta}\le A_j\le D^{1+9\theta}.}
\tag{71.7}
\]

- 오른쪽 **상계**는 power condition을 확인할 때 쓴다.
- 왼쪽 **하계**는 음의 거듭제곱 \(A_j^{-\theta/2}\)을 위에서 제한할 때 쓴다.

두 방향을 바꾸면 오차가 작다는 결론이 거꾸로 되므로 가장 중요한 fail-closed 조건이다.
\(X=D^{1+12\theta}\), \(\alpha\ge1-\theta\)에서 선행 지수 대수는

\[
 (1-\theta)(1+12\theta)
 -(1+\theta)(1+9\theta)
 =\theta(1-21\theta)\ge0.
\tag{71.8}
\]

따라서 \(X^\alpha\ge A_j^{1+\theta}\)가 모든 \(j\)에 공통으로 성립한다. 반면
Mellin 오차는 식 (71.7)의 왼쪽을 써서

\[
 |I_j|
 \le K_M(\delta_\theta)A_j^{-\theta/2}
 \le K_M(\delta_\theta)
 D^{-\theta(1/2+9\theta)/2},
 \qquad
 \delta_\theta=\frac{\theta}{4(1+\theta)}
\tag{71.9}
\]

로 통일한다.

### 4.1 averaged detector 공통 cutoff

네 loss \(\eta_5,\eta_X,\eta_M,\eta_T>0\)가
\(\eta_5+\eta_X+\eta_M+\eta_T\le\eta_{\rm out}\le\theta\)라 하자.
Theory 64의 공통 cutoff에서 Mellin 항만 식 (71.9)에 맞게 바꾸면

\[
\begin{aligned}
 L_{0,*}=\max\Bigg\{&
 e,\ \theta^{-2},\
 \left(\frac{18}{\theta(\log2)^{1/3}}\right)^{3/2},\\
 &\frac6\theta\log\frac{(1277/500)\pi^2}{\theta\eta_5},\
 \frac{\log(1/\eta_X)}{1+12\theta},\\
 &\frac{2}{\theta(1/2+9\theta)}
   \log\frac{\pi^2K_M(\delta_\theta)}{\theta\eta_M},\\
 &2(1+13\theta),\
 \sqrt{2\log\frac{4\pi^2}{\theta\eta_T}}
 \Bigg\}.
\end{aligned}
\tag{71.10}
\]

\(L\ge L_{0,*}\)이면 모든 \(q_j\le Q\)에서

\[
 |g_j|\ge
 (1-\theta)\frac6{\pi^2}
 \frac{\varphi(q_j)}{q_j}\log R.
\tag{71.11}
\]

여기서는 printed Lemma 6의 정성 조건
\(\log R\ll\log(q_jT)\)를 숫자 없이 재사용하지 않았다. JL5, damping, Mellin, tail
네 component를 공통 \(D\)에서 직접 다시 합성했다. 특히 작은 \(q_j\)도 식 (71.7)의
Mellin 하계가 덮는다.

## 5. phase가 detector의 totient factor를 정확히 지운다

식 (71.4)는 임의 복소수 \(\eta_j\)에 성립한다. 각 detector가 양의 lower를 가지므로
phase를 맞추고

\[
 |\eta_j|=\frac{q_j}{\varphi(q_j)},\qquad
 \eta_jg_j=\frac{q_j}{\varphi(q_j)}|g_j|
\tag{71.12}
\]

로 고른다. 그러면

\[
 \left|\sum_j\eta_jg_j\right|
 =\sum_j\frac{q_j}{\varphi(q_j)}|g_j|
 \ge(1-\theta)\frac6{\pi^2}J\log R.
\tag{71.13}
\]

즉 modulus마다 달랐던 \(\varphi(q_j)/q_j\)가 왼쪽에서 정확히 사라진다.

## 6. primitive principal pair와 residue 상쇄

\(\chi_j,\chi_k\)가 각각 자신의 conductor에 대한 primitive character이면

\[
 \bar\chi_j\chi_k\ \hbox{가 principal}
 \quad\Longleftrightarrow\quad
 \chi_j=\chi_k.
\tag{71.14}
\]

같은 primitive character는 같은 conductor를 가지므로 이때 \(q_j=q_k=q\)다. 단,
같은 character에서 높이가 다른 영점을 여러 개 고를 수 있으므로 식 (71.14)를
\(j=k\)라고 바꾸면 안 된다. Theory 69의 same-character height row가 바로 이 여러
영점을 센다.

principal \(L\)-residue의 \(\varphi(q)/q\), pseudocharacter diagonal sum의
\(\varphi(q)/q\), 두 phase weight를 곱하면

\[
 \left(\frac q{\varphi(q)}\right)^2
 \frac{\varphi(q)}q\frac{\varphi(q)}q=1.
\tag{71.15}
\]

따라서 Theory 69의 residue coefficient 52는

\[
 |\mathcal R_*|<52Jx^{2(1-\alpha)}L^2
\tag{71.16}
\]

로 그대로 남고, modulus 수 \(Q\)나 \(Q^2\)가 추가되지 않는다.

## 7. off-diagonal에서 생기는 정확한 새 손실

서로 다른 primitive character pair의 product character modulus는

\[
 m_{jk}=\operatorname{lcm}(q_j,q_k)
 \le q_jq_k\le Q^2,\qquad m_{jk}T\le D.
\tag{71.17}
\]

따라서 Theory 67의 product-character contour 상계에서 \((m_{jk}T)^{1/2}\)를
\(D^{1/2}\)로 올릴 수 있다. 서로 다른 coprimality restrictions는 Theory 68의
absolute \(r,r',d\) 합에서 일부 항을 제거할 뿐이므로 coefficient 3을 키우지 않는다.

Theory 64의 \(q/\varphi(q)\le6L\)을 각 phase에 한 번씩 쓰면

\[
 \frac1{L^2}
 \frac{q_j}{\varphi(q_j)}
 \frac{q_k}{\varphi(q_k)}\le36.
\tag{71.18}
\]

즉 phase 때문에 \(36L^2\)가 생기지만 식 (3.7)의 detector 쪽 \(L^2\) 정규화와
상쇄된다. 고정-modulus Theory 70에서 왼쪽의 totient 제곱을 나눈 뒤 생겼던 36과
같은 숫자이므로 strict absorption coefficient는 변하지 않는다.

## 8. averaged terminal inequality

다시

\[
 C_{\rm pre}=\frac{170}{\theta^2},\quad
 \overline C_{\rm CL3}=
 144\left(1+\frac1\theta\right)\left(\frac2\theta+1\right),\quad
 \underline c_g=\frac35(1-\theta)\theta,\quad
 \gamma=\frac{29\theta}{252}
\tag{71.19}
\]

로 둔다. \(A_{\rm int}\)는 Theory 70과 같은 적분면적이다. 식 (71.13),
(71.16), (71.18)과 contour decay를 합치면 한 parity system에

\[
 \underline c_g^2A_{\rm int}J^2L^2
 \le C_{\rm pre}\left[
 52Jx^{2(1-\alpha)}L^2
 +36A_{\rm int}\overline C_{\rm CL3}
 J^2L^2e^{-\gamma L}\right].
\tag{71.20}
\]

\(L^2\)로 나누면 Theory 70과 정확히 같은

\[
 AJ^2\le BJY+EJ^2,\quad
 A=\underline c_g^2A_{\rm int},\quad
 B=52C_{\rm pre},\quad
 E=36C_{\rm pre}A_{\rm int}\overline C_{\rm CL3}e^{-\gamma L},
 \quad Y=x^{2(1-\alpha)}
\tag{71.21}
\]

이 된다. 따라서

\[
 L_{\rm avg}:=max\left\{
 L_{0,*},\ e^8,\
 \frac1\gamma\log
 \frac{72C_{\rm pre}\overline C_{\rm CL3}}
      {\underline c_g^2}
 \right\}
\tag{71.22}
\]

이면 \(E\le A/2<A\)이고

\[
 \boxed{
 J\le
 \frac{884000}{9(1-\theta)^2\theta^6}
 x^{2(1-\alpha)}.}
\tag{71.23}
\]

식 (71.20)의 `+36` 표기가 오해를 일으킬 수 있으므로 machine ledger와 Python에서는
`36*A_int*...`로 저장했다.

## 9. 전체 primitive nonprincipal zero count로 복원

높이 strip을 공통 \(\Delta=L^{-1}\)로 나눈다. \(L\ge\theta^{-2}\)이면
\(r=\max\{1-\alpha,L^{-1}\}\le\theta\). 또한 각 \(q_j\le Q\)에

\[
 \log\{q_j(1+T)\}\le\log(2QT)\le\log(2D).
\tag{71.24}
\]

Theory 65의 local-square bound를 각 nonempty character-strip cell에 적용하고 짝·홀 두
system을 복원하면 식 (71.2)가 나온다. conductor 1의 primitive principal character,
즉 zeta branch는 이 \(N^*_{\rm np}\)에 포함하지 않는다.

## 10. endpoint 진단

네 detector loss를 각각 \(\theta/4\)로 둔 120-dps 진단은 다음과 같다.

| \(\theta\) | averaged Mellin cutoff | \(L_{0,*}\) | 지배항 |
|---:|---:|---:|---|
| \(1/21\) | 953.850175... | 8827.240704... | \(\mathcal B_q\) absorption |
| \(1/100\) | 9236.755265... | 91726.754431... | \(\mathcal B_q\) absorption |
| \(1/1000\) | 143176.702275... | 2900654.663772... | \(\mathcal B_q\) absorption |

\(\theta=1/21\)에서는 새 averaged Mellin decay exponent가 정확히 \(13/588\)이고,
공통 cutoff는 여전히 선행 \(\mathcal B_q\) envelope가 지배한다. 따라서 가변 modulus로
옮긴 것이 현재 진단점의 cutoff를 더 키우지는 않았다. decimal은 directed interval
certificate가 아니라 진단이며, 엄밀한 결론은 식 (71.7)--(71.10), (71.20)--(71.23)의
기호적 implication이다.

## 11. 무엇이 닫혔고 무엇이 남았는가

| ID | 판정 | 의미·남은 의무 |
|---|---|---|
| `JL7-AVERAGED-NP-NEAR-ONE` | **ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT** | primitive nonprincipal, \(0<1-\alpha\le\theta\), 공통 \(D=Q^2T\) |
| Jutila printed Theorem 1 (1.8) 전체 | OPEN | principal zeta, away-from-one branch, exact \((2+\varepsilon)\) 재매개화 |
| `JL7-AVERAGED-TO-PAP` | HARD_BLOCKER | density를 Gallagher--Maier pointwise prime lower bound 안에서 재생 |
| `PAP-11 / DEP-R09` | HARD_BLOCKER / OPEN | root 상태는 아직 바뀌지 않음 |
| fixed \(2\times10^{-17}\) / \(X_{\rm cert}\) | NOT CERTIFIED / OPEN | threshold calculator 제작 금지 유지 |

이번 결과는 중요한 analytic 부품 하나를 닫았지만, averaged density 자체는 modulus 평균
명제이고 PAP는 각 \(q,a\)에 대한 pointwise lower bound다. 두 논리형은 같지 않으므로
식 (71.2)를 곧바로 PAP라고 부르지 않는다.

## 12. Python·Lean 증거 경계

- [finite evaluator](../../../source/dep_r09_jutila_jl7_averaged.py)는 common detector
  cutoff, phase·residue exact cancellation, off-diagonal 36과 endpoint 진단을 계산한다.
- [fail-closed tests](../../../tests/test_dep_r09_jutila_jl7_averaged.py)는 두 source hash,
  Mellin envelope 방향, exact cancellation, 잘못된 totient 전제와 root false flag를 검사한다.
- Lean 단일 파일은 detector phase 상쇄, principal residue 상쇄, phase pair 36,
  \(A_j\) 상·하 envelope의 유한 대수와 기존 terminal coefficient 보존만 검증한다.
- generalized Halasz inequality, primitive conductor uniqueness, complex contour와 source
  analytic estimate 전체는 project-local axiom으로 만들지 않는다.
- `sorry`, `admit`, project-local `axiom`은 사용하지 않는다.

Lean PASS는 외부 analytic source 전체의 독립 형식증명이 아니라, source premise가 맞을 때
이번 dependency-critical finite normalization이 틀리지 않았다는 증거다.

## 13. 다음 권장 gate

다음은 `JL7-AVERAGED-TO-PAP`다. 먼저 Gallagher--Maier proof에서 실제로 쓰는 zero family와
적분 kernel을 원문 페이지별로 다시 고정하고, 식 (71.2)의 near-one 범위만으로 충분한지
확인한다. 충분하면 away-from-one Jutila 정리를 불필요하게 수치 재증명하지 않고,
exceptional character, principal term, prime powers, \(\psi\to\pi\), endpoint와 공통 cutoff를
각각 분리한다. 이 source map이 끝나기 전에는 threshold calculator를 만들지 않는다.

## 14. 참고문헌

- M. Jutila, *On Linnik's constant*, Math. Scand. 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- M. Jutila, *Zero-density estimates for L-functions*, Acta Arith. 32 (1977),
  55--62, DOI
  [10.4064/aa-32-1-55-62](https://doi.org/10.4064/aa-32-1-55-62).
