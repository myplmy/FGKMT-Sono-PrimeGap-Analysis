# Sono/FMT DEP-R09 Jutila Lemma 5 유한 조화합 하한

- 작성일: 2026-09-13 KST
- 단계: `DEP-R09 / JL5a UNIFORM FINITE HARMONIC LOWER BOUND`
- 선행 정본: [Theory 60](60_Sono_FMT_DEPR09_Jutila_Lemma4_8_source_inventory.md)
- 기계 원장: [Jutila Lemma 5 finite v1](data/Sono_FMT_DEPR09_Jutila_Lemma5_finite_v1.json)
- 판정: `JL5 EXPLICIT / JL6 AND ROOT CERTIFICATE OPEN`
- 비목적: actual prime sweep, threshold calculator, JL6의 숨은 두 오차를 임의 상수로 대체

> **후속 상태(2026-09-13):** [Theory 62](62_Sono_FMT_DEPR09_Jutila_Lemma6_Mellin_integral_explicit.md)가
> 두 오차 중 Mellin 항을 `ACTUAL_FORM_PARAMETERIZED_EXPLICIT`으로 닫았다.
> 별도 truncation tail, JL6 전체, JL8과 root certificate는 계속 OPEN이다.

## 1. 결론

Jutila 1977 Lemma 5의 `1+o(1)`은 더 이상 numerical blocker가 아니다. Zuniga
Alterman의 동료심사 논문 Corollary 3.4(b), 식 (3.16)이 **같은 합**에 모든 양의 실수
\(R\)와 모든 양의 정수 \(q\)에 적용되는 명시적 절대오차를 준다. 이 정리를 사용하면
원하는 \(0<\eta\le1\)마다 완전히 계산 가능한 \(q\)-의존 충분 cutoff
\(R_0(q,\eta)\)를 얻는다.

그러나 Jutila Lemma 6에는 Lemma 5 이외에도 Mellin 적분 오차와 무한급수 절단 tail이라는
두 개의 \(\ll_\varepsilon1\)이 남는다. 따라서 이번 닫힘은 정확히 `JL5` 하나이며
`JL6`, `JL8`, `PAP-11`, DEP-R09, fixed \(2\times10^{-17}\), \(X_{\rm cert}\)는
계속 OPEN이다.

> 쉬운 설명: 원래 증명에는 “\(R\)이 충분히 크면 이 합은 대략 이만큼”이라는 말만 있었다.
> 새 논문은 그 대략값에서 얼마나 벗어날 수 있는지를 숫자 2.554로 알려 준다. 이제 \(R\)을
> 얼마 이상 잡으면 원하는 비율만큼 안전한지 계산할 수 있다. 하지만 다음 Lemma에는 별도의
> 오차 두 개가 더 있어서 전체 증명은 아직 끝나지 않았다.

## 2. 원문·읽기 방식·source 적합성

| source | 확인 위치 | 읽기 방식 | 역할 |
|---|---|---|---|
| Jutila, *On Linnik's constant* | 인쇄 pp. 49--51, Lemmas 5--6 | native text 18 bytes로 사실상 비어 300 dpi OCR 후 원페이지 대조 | 원래 목표와 downstream 호출 |
| Zuniga Alterman, *Explicit averages of square-free supported functions* | 인쇄 pp. 10--12, Cor. 3.4(b), 식 (3.16); pp. 19--21 비교 | native text 우선 추출 후 원페이지 대조 | JL5의 직접 명시적 대체정리 |
| Ford, *Sieve Methods Lecture Notes* | 인쇄 pp. 47--50, Thm. 4.4 | native text 우선 후 원페이지 대조 | corrected Wirsing 구조의 독립 fallback |

Zuniga Alterman 파일은
`article/Zuniga Alterman 2022 Explicit averages of square-free supported functions.pdf`에
보존했다. SHA-256은
`848a3a10b32f7639b584598bda98b4d9a092d4eacf87f68e9b1364e9f6880495`이고
307,611 bytes, 25 pages다. native text가 정상 추출되므로 OCR을 사용하지 않았다.

논문의 함수·endpoint·서로소 조건은 Jutila의 합과 일치한다.

- 합은 \(\mu^2(r)/r\)이므로 정확히 squarefree support다.
- 조건은 \((r,q)=1\)이다.
- endpoint는 \(r\le R\)로 일치한다.
- \(q\)는 임의의 양의 정수이고, \(q\)-의존성이 유한 Euler product로 드러난다.
- \(O^*\)는 표시한 양으로 절대값이 제한된다는 논문의 convention이다.

## 3. peer-reviewed explicit source theorem

\[
 S_q(R):=
 \sum_{\substack{r\le R\\(r,q)=1}}\frac{\mu^2(r)}r
 =
 c_q\{\log R+b_q\}+\mathcal E_q(R),
 \qquad
 |\mathcal E_q(R)|
 \le \frac{(1277/500)\mathcal B_q}{R^{1/3}}.
\tag{61.1}
\]

여기서

\[
 c_q=
 \frac6{\pi^2}\frac q{\kappa(q)}
 =
 \frac6{\pi^2}\prod_{p\mid q}\left(1+\frac1p\right)^{-1},
 \qquad
 \mathcal B_q=
 \prod_{p\mid q}
 \left(1+\frac{p^{2/3}-1}{p^{4/3}+1}\right).
\tag{61.2}
\]

또한 source의 상수항은

\[
 b_q=
 \gamma+\sum_p\frac{2\log p}{p^2-1}
       +\sum_{p\mid q}\frac{\log p}{p+1}>0.
\tag{61.3}
\]

따라서 양의 \(b_q\)를 버리고 오차의 나쁜 부호만 취해도

\[
 S_q(R)\ge
 c_q\log R-\frac{(1277/500)\mathcal B_q}{R^{1/3}}.
\tag{61.4}
\]

가 된다. 이 단계는 점근 기호를 새로 추정한 것이 아니라 출판된 명시적 정리의 안전한
한쪽 방향 사용이다.

## 4. 유한 cutoff 도출

\(0<\eta\le1\)에 대해

\[
 A(q,\eta):=
 \frac{(1277/500)\mathcal B_q}{\eta c_q}.
 \qquad
 R^{1/3}\log R\ge A(q,\eta)
 \Longrightarrow
 \frac{(1277/500)\mathcal B_q}{R^{1/3}}
 \le\eta c_q\log R.
\tag{61.5}
\]

정확한 최소해를 풀 필요 없이 다음 닫힌식을 충분조건으로 쓴다.

\[
 R_0(q,\eta):=
 \max\left\{
   \exp\!\sqrt{\log q},\
   e,\
   A(q,\eta)^3
 \right\}.
\tag{61.6}
\]

\(R\ge e\)이면 \(\log R\ge1\)이고, \(R\ge A^3\)이면
\(R^{1/3}\ge A\)다. 그러므로 \(R\ge R_0\)에서 식 (61.5)의 예산이 성립한다.
첫 항은 Jutila가 원래 요구한 \(\log R\ge\sqrt{\log q}\)도 보존한다. 결론은

\[
 R\ge R_0(q,\eta)
 \Longrightarrow
 S_q(R)\ge(1-\eta)c_q\log R.
\tag{61.7}
\]

이다. \(R_0\)은 **간단하고 검증하기 쉬운 충분 cutoff**이지 최적 cutoff가 아니다.
필요해질 때 \(R^{1/3}\log R=A\)를 Lambert \(W\)로 풀면 줄일 수 있지만, 현재 root
blocker는 그 최적화가 아니다.

## 5. Jutila Lemma 6 계수로의 안전한 bridge

각 소수 \(p\)에 대해

\[
 \frac{p-1}{p}\le\frac p{p+1},
 \qquad
 c_q\ge
 \frac6{\pi^2}\prod_{p\mid q}\left(1-\frac1p\right)
 =
 \frac6{\pi^2}\frac{\varphi(q)}q.
\tag{61.8}
\]

따라서 JL6에서 실제로 필요한 더 약한 주항도 얻는다.

\[
 R\ge R_0(q,\eta)
 \Longrightarrow
 S_q(R)\ge
 (1-\eta)\frac{\varphi(q)}q\frac6{\pi^2}\log R.
\tag{61.9}
\]

단, 여기의 \(\eta\)를 Jutila 식 (2.10)의 최종 \(\varepsilon\)과 곧바로 같다고 두면 안
된다. JL6의 다른 두 오차가 차지할 예산을 먼저 복원한 뒤 \(\varepsilon\)을 여러 부분으로
나눠야 한다.

## 6. 수치 예시

아래 값은 100-dps evaluator가 단순 cutoff 식 (61.6)을 계산한 진단 예이며, 실제 PAP
매개변수를 선택했거나 directed interval arithmetic로 최종 정수 cutoff를 인증했다는
뜻이 아니다. 엄밀한 것은 식 (61.6)의 기호적 충분조건이다.

| \(q\) | \(\eta\) | \(c_q\) | \(\mathcal B_q\) | 100-dps 진단 \(\lceil R_0\rceil\) |
|---:|---:|---:|---:|---:|
| 1 | 0.1 | 0.607927101854... | 1 | 74,150 |
| 30 | 0.1 | 0.253302959106... | 1.686248040456... | 4,914,805 |
| 2310 | 0.01 | 0.203170081783... | 2.307464955045... | 24,405,558,697 |

> 쉬운 설명: 더 작은 오차 비율 \(\eta\)를 요구하거나 \(q\)에 소인수가 많아지면 안전한
> 시작점은 커진다. 그래도 이제 그 증가량은 숨은 “충분히 큼”이 아니라 계산 가능한 식이다.

## 7. corrected Wirsing fallback과의 비교

Theory 22의 corrected \(\kappa=1\) Wirsing 정리는
\(h(p)=1/p\) for \(p\nmid q\), \(h(p)=0\) for \(p\mid q\)로 특수화할 수 있다.
안전한 \(a=2/3\), \(A_2=130\)을 넣으면 project multiplier의
\(\log_{10}\)은 약 176.819다. 구조적으로 독립적인 fallback이지만 JL5만을 위해 쓰기에는
지나치게 거칠다. Corollary 3.4(b)의 직접 오차를 primary로 채택하고 이 경로는
cross-check로만 남긴다.

## 8. 코드·Lean·증거 경계

\[
 2.554=\frac{1277}{500}.
\tag{61.10}
\]

- high-precision evaluator: `source/dep_r09_jutila_jl5_finite.py`. 이는 최종
  directed interval certificate가 아니다.
- fail-closed test: `tests/test_dep_r09_jutila_jl5_finite.py`
- machine ledger:
  `docs/method/theory/data/Sono_FMT_DEPR09_Jutila_Lemma5_finite_v1.json`
- Lean은 \(2.554=1277/500\), 절대오차 budget의 lower transfer, 각 소수인수와
  임의의 유한 소수집합에 대한 \(\varphi/q\) 방향 bridge를 검증한다.
- 출판된 Corollary 3.4(b)를 project-local axiom으로 선언하지 않는다.
- \(A^3\) cutoff의 real cube-root·로그 연결은 문서·Python 검산 범위이며
  `PARTIAL_FORMALIZATION` 상태를 유지한다.
- `sorry`, `admit`, project-local `axiom`을 사용하지 않는다.

## 9. 상태와 다음 proof gate

| ID | 판정 | 의미 |
|---|---|---|
| `JL5` | `EXPLICIT_PEER_REVIEWED_SOURCE_REPLACEMENT_WITH_Q_DEPENDENT_CUTOFF` | 숨은 `o(1)` 제거 |
| `JL6` | `HARD_BLOCKER` | Mellin integral·truncation tail의 absolute constants 필요 |
| `JL8` | `HARD_BLOCKER` | local zero-count multiplier 필요 |
| `PAP-11` / DEP-R09 | `OPEN` | full density composition 미완 |
| fixed \(2\times10^{-17}\) / \(X_{\rm cert}\) | `OPEN` | calculator 제작 금지 유지 |

이 문서 작성 당시 다음 우선순위였던 `JL6a`의 Mellin 항은 Theory 62에서 진전했다.
현재 다음 우선순위는 `JL6b` truncation tail의 source-first 명시화와 이후 JL5·Mellin·tail
공통 error-budget 합성이다.

## 10. 참고문헌

- M. Jutila, *On Linnik's constant*, Math. Scand. 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- S. Zuniga Alterman, *Explicit averages of square-free supported functions:
  to the edge of the convolution method*, Colloq. Math. 168 (2022), 1--23,
  DOI [10.4064/cm8337-11-2020](https://doi.org/10.4064/cm8337-11-2020),
  arXiv [2003.05887](https://arxiv.org/abs/2003.05887).
- K. Ford, *Sieve Methods Lecture Notes* (2023), Theorem 4.4; corrected
  fallback 정본은 [Theory 22](22_Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier.md).
