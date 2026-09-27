# DEP-R09 prescribed-modulus endpoint \(L^\infty\) transfer 작업원장

- 시작: 2026-09-28 02:16 KST
- 기준 commit: <code>f4b1115e4cc2a9469bc3cc958b8828d835db1d68</code>
- 선행 정본: Theory 47, 58--59, 90, 96, review 105, handoff 202609280026
- 목표: Vaughan general-sequence I/II·Harper·Thorner--Zaman을 Theory 96 식
  (96.9)에 직접 매핑하고, mixed covariance theorem보다 약한 single-endpoint centered
  \(L^\infty\) 충분조건과 그 exact multiplier를 복원한다.
- 승인·금지: 학술 source 다운로드·문서·Python·Lean·local commit 허용. actual
  prime/dataset 계산, package 설치, threshold calculator, 장시간 계산, conditional
  branch, push/PR 금지.

## 영향도

| 축 | 판정 | 통제 |
|---|---|---|
| analytic root | 직접 영향 | mixed covariance와 pointwise endpoint sufficient route를 구분 |
| exceptional zero | 결정적 | centered residue error 자체를 interface로 두어 main-term 정규화를 숨기지 않음 |
| small-scale normalization | 직접 영향 | Rosser--Schoenfeld prime count와 project \(Y/X\) 조건만 사용 |
| source quantifier | 결정적 | cumulative/dyadic modulus average를 prescribed \(f\) theorem으로 승격하지 않음 |
| data/end-bounded | 영향 없음 | analytic proof only |
| threshold | 간접 영향 | numerical endpoint PNT package 전에는 calculator 금지 |

## 접근 비교

| 접근 | 장점 | 한계 | 선택 |
|---|---|---|---|
| Vaughan I/II variance | general sequence framework | Criterion-U 선행가정·large-Q 누적 평균 | source boundary |
| Harper general BDH | finite complex sequence | \(Q>\sqrt{2x}\) dyadic average; fixed \(f\) 미포함 | source boundary |
| mixed covariance direct theorem | 가장 날카로운 cancellation | 확인된 numerical source 없음 | OPEN 유지 |
| short-side \(L^1\) × large-endpoint \(L^\infty\) | fixed \(f\), exact, source 의무 축소 | numerical pointwise PNT error 필요 | **채택** |
| Thorner--Zaman pointwise PNT | 구조상 endpoint input 공급 가능 | multiplier·decay·cutoff 미수치 | 최종 analytic root |

## 단계 현황

1. **DONE — clean HEAD·Theory 96·handoff 복구**
2. **DONE — Vaughan I/II 공식 저자 PDF download·hash·native text 감사**
3. **DONE — Harper Theorems 1--2 range·hypotheses 재대조**
4. **DONE — endpoint \(L^\infty\) sufficient transfer 직접 증명**
5. **DONE — Rosser--Schoenfeld/project scale에서 \(21/10\) normalization 도출**
6. **DONE — Theory 97·review 106·machine ledger·Python·Lean 작성**
7. **DONE — canonical verification**
8. **IN PROGRESS — handoff·local commit**

## source-first 판정

- Vaughan 1998 I는 식 (1.6)의 uniform Criterion-U를 먼저 가정하고
  \(x^{2/3}\le Q\le x\)에서 \(q\le Q\) 누적 variance를 준다.
- Vaughan 1998 II는 uniform 식 (1.4), mean-square 식 (1.5)를 먼저 가정하고
  \(Q>\sqrt{x}\log(2x)\)에서 \(q\le Q\) 누적 variance를 준다.
- Harper 2024 Theorems 1--2는 \(\sqrt{2x}<Q\le x\)와
  \(Q/2<q\le Q\)를 요구한다. Current \(f=U^{1/d_f}\), \(d_f\ge21\)은
  그 dyadic block에 들어가지 않는다.
- Thorner--Zaman은 pointwise route의 구조를 주지만 current fixed exponent에서 숨은
  multiplier는 \(U\) 증가로 사라지지 않는다.

## 진행 중 핵심 식

Centered endpoint error를

\[
 \epsilon_\infty(U,f):=
 \frac{\varphi(f)}U\max_a^*|E_f(U;a)|
\]

로 두면, short side의 exact \(L^1\) bound와 project prime-count normalization에서

\[
 \delta_{\rm bin}
 \le \frac{21}{5}
 \{\epsilon_\infty(U,f)+\epsilon_0(X,U,f)\}
 \left(2+\frac ba\right)
\]

을 얻는 방향이다. \(\epsilon_0\)는 lower endpoint \(X<f\)의 elementary one-atom
correction이다. Source theorem 없이 \(\epsilon_\infty\)를 작다고 선언하지 않는다.

## 완료 결과 — 2026-09-28 02:38 KST

- Vaughan 1998 I·II 공식 저자 PDF를 각각 12쪽·18쪽으로 확인하고 SHA-256을 고정했다.
- Vaughan I 식 (1.6), Theorem 1의 \(x^{2/3}\le Q\le x\), Vaughan II 식
  (1.4)--(1.5), Theorems 1--2의 \(Q>\sqrt{x}\log(2x)\)를 current contract에 대조했다.
- Harper Theorems 1--2의 \(\sqrt{2x}<Q\le x\), \(Q/2<q\le Q\) dyadic range가
  current \(f\le U^{1/21}\)을 포함하지 않음을 고정했다.
- Centered finite mass \(L^1\), lower endpoint correction, small-scale
  \(21/10\), endpoint-to-cross \(21/5\), Abel project transfer를 Theory 97로 증명했다.
- 남은 root는 fully numerical centered fixed-\(f\) endpoint error
  \(\epsilon_\infty(U,f)\)다. PAP-11·DEP-R09·\(X_{\rm cert}\)는 OPEN이다.

검증:

~~~text
new targeted Python                         12 tests PASS
canonical DEP-R09 regression               393 tests PASS
verification inventory                     PASS
theory / display / Lean declarations       98 / 1,927 / 365
forbidden proof escape                      0
Lean direct compile                         exit 0
Lean full build                             8,765 jobs PASS
full Python regression                      1,061 tests, existing 1 failure
~~~

Full regression의 유일한 failure는 변경 전부터 있던 PowerShell 5.1
<code>test_windows_powershell_51_preserves_quote_sensitive_argv</code>의
<code>$LASTEXITCODE</code> undefined다. 이번 diff는 해당 runner/test를 변경하지 않았다.

Actual prime/dataset 계산, package 설치, threshold calculator, 장시간 계산,
conditional branch, push/PR은 수행하지 않았다.
