# DEP-R09 pre-sup joint-angle source audit 작업원장

- 시작: 2026-09-29 17:02 KST
- 기준 commit: <code>cced2c2</code>
- 선행 정본: Theory 75--77, 89, 95--96, 100, review 109, handoff 202609280408
- 목표: explicit formula의 character별 절댓값·density sup 이전 target을 exact하게 고정하고,
  recent weighted-sieve·dispersion·prime-character sources가 small-prime coefficient와
  prime-error packet의 joint angle을 실제로 제어하는지 검토한다.
- 승인·금지: academic download·source audit·문서·Python·Lean·local commit 허용.
  actual prime/zero/dataset 계산, package 설치, threshold calculator, 장시간 계산,
  construction redesign, conditional branch, push/PR 금지.

## 영향도

| 축 | 판정 | 통제 |
|---|---|---|
| analytic norm | 결정적 | separate magnitudes와 joint angle을 구분 |
| character orientation | 결정적 | \(C_\chi=\sum_{q\in Q'}\bar\chi(q)\) orientation 보존 |
| source provenance | 직접 영향 | 2026-09 신규 Ramaré 두 편 포함 official PDF·TeX hash 고정 |
| data/end-bounded | 영향 없음 | source/proof audit only |
| threshold | 간접 영향 | joint theorem 전에는 calculator 금지 |

## 접근 비교

| 접근 | 장점 | 한계 | 선택 |
|---|---|---|---|
| support-only weighted sieve | fully explicit finite inequalities | phase를 \(|u_n|\)로 제거 | source screen |
| character/residue second moment | 표준적·넓은 source | separate-L2 Cauchy sharp | source screen |
| simultaneous-AP dispersion | signed mean-value 구조 | modulus average·well-factorable·implicit constants | source screen |
| direct pre-sup joint angle | target과 정확히 일치 | drop-in source 미식별 | **project target** |

## 단계 현황

1. **DONE — Theory 75--77·95--100 exact target 복구**
2. **DONE — Ramaré 2609.25885/25879 official PDF·source audit**
3. **DONE — Motohashi 1201.3134 official PDF·source audit**
4. **DONE — Zheng 2512.22798 official PDF·source audit**
5. **DONE — Szabó 2208.05762 bounded-order character source audit**
6. **DONE — Theory 101·review 110·machine ledger·Python·Lean 작성**
7. **DONE — canonical verification**
8. **IN PROGRESS — handoff·local commit**

## 핵심 target

Explicit-formula packet을 \(\mathfrak Z_\chi(X,U;T)\)라 하면

\[
\mathcal Z_{f,T}=\sum_{\chi\ne\chi_0}C_\chi(Q')\mathfrak Z_\chi(X,U;T)
\]

의 numerical direct upper가 필요하다. Phase-blind envelopes
\(|\mathfrak Z_\chi|\le M_\chi\)만 알면 triangle upper
\(\sum|C_\chi|M_\chi\)는 arbitrary packet phases에 대해 exact sharp하다.

Separate \(L^2\) source와 optimistic prime-error energy \(\le U^2\)를 쓸 때 normalized
angle \(\Gamma\)가 충족해야 할 squared budget은

\[
\Gamma^2<\delta_{\rm bin}^2\frac{N}{\varphi(f)-N}.
\]

즉 새로운 source는 norms가 아니라 actual vectors의 joint angle/covariance를 제어해야 한다.

## 완료 결과 — 2026-09-29 17:20 KST

- Signed zero-packet target과 explicit correction interface를 고정했다.
- Phase-blind triangle alignment와 same-magnitude cancellation witness를 exact하게 증명했다.
- Conditional optimistic energy 아래 required squared-angle budget을 도출했다.
- Ramaré 2026 두 preprint, Motohashi, Zheng, Szabó 공식 원문을 hash 고정·감사했다.
- Checked source에는 prescribed \(f\) numerical joint-angle theorem이 없음을 object·range·
  quantifier별로 기록했다. 전 문헌 부재는 주장하지 않는다.

검증:

~~~text
new targeted Python                          9 tests PASS
canonical DEP-R09 regression               431 tests PASS
verification inventory                     PASS
theory / display / Lean declarations       102 / 1,998 / 385
forbidden proof escape                      0
Lean direct compile                         exit 0
Lean full build                             8,765 jobs PASS
full Python regression                      1,101 tests, existing 1 failure
~~~

첫 Lean direct compile은 final field identity에서 <code>field_simp</code>가 goal을 이미
닫은 뒤 남은 <code>ring</code> 때문에 <code>No goals to be solved</code>로 실패했다.
불필요 tactic만 제거하고 같은 statement를 재검증해 PASS했다.

Full regression의 유일한 failure는 기존 PowerShell 5.1
<code>test_windows_powershell_51_preserves_quote_sensitive_argv</code>의
<code>$LASTEXITCODE</code> undefined다. 이번 diff는 해당 runner/test를 변경하지 않았다.

Actual prime/zero/dataset 계산, package 설치, threshold calculator, 장시간 계산,
construction redesign, conditional branch, push/PR은 수행하지 않았다.
