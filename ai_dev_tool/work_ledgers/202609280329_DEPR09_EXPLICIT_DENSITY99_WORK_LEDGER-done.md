# DEP-R09 explicit density-99 route 작업원장

- 시작: 2026-09-28 03:29 KST
- 기준 commit: <code>dd85de6f113b38538426286de6445b236daa1fa4</code>
- 선행 정본: Theory 58, 90, 98, review 107, handoff 202609280324
- 목표: fully explicit Thorner--Zaman density exponent 99를 fixed \(f\) endpoint
  theorem에 대입하고, current \(99<d_f<416\) overlap에서 direct black-box certificate가
  실제로 small relative error를 줄 수 있는지 exact하게 판정한다.
- 승인·금지: source audit·문서·Python·Lean·local commit 허용. actual prime/zero 계산,
  package 설치, threshold calculator, 장시간 계산, conditional branch, push/PR 금지.

## 영향도·접근 비교

| 접근 | 장점 | 한계 | 선택 |
|---|---|---|---|
| sharp \(12/5\) density | current range에 큰 epsilon 여유 | multiplier·cutoff 미수치 | 다음 fallback |
| explicit near-one exponent 99 | multiplier·범위 전부 인쇄 | theta=98/99, epsilon 매우 작음 | **이번 감사** |
| explicit all-sigma exponent 127 | sigma restriction 없음 | exponent가 더 나빠 epsilon 더 작음 | 비교 후 기각 |
| actual computation | source error와 무관 | 승인 금지·정리 증명 대체 불가 | 금지 |

수학·provenance에만 영향이 있고 dataset/end-bounded 정의에는 영향이 없다. Source theorem을
current fixed modulus family로 확대하지 않고, fixed family가 modulus-height box의 subset인
방향만 사용한다.

## 단계 현황

1. **DONE — explicit density Theorem 1.2·Corollary 6.1 원문 복구**
2. **DONE — fixed \(f,T\) family를 \(Q=\max(f,T)\) box에 포함**
3. **DONE — exponent 99 range \(d_f>99\), epsilon ceiling 도출**
4. **DONE — t=e endpoint가 만드는 optimistic certificate floor 도출**
5. **DONE — Theory 99·review 108·machine ledger·Python·Lean 작성**
6. **DONE — canonical verification**
7. **IN PROGRESS — handoff·local commit**

## 핵심 진단

Explicit density exponent \(c_7=99\)이면 \(\theta=98/99\)이고 full-interval range는

\[
0<\varepsilon\le\frac1{99}-\frac1{d_f}.
\]

Current \(d_f<416\)에서 \(\varepsilon<317/41184\)다. Explicit McCurley zero-free
constant \(c_M=1/9.645908801\)를 써도

\[
\varepsilon^2c_Md_f<3/1000.
\]

Theorem 2.3의 sup에는 \(t=e\)가 들어가므로 multiplier-one으로 낙관해도 첫 relative
factor \(d_f\sup U^{-\varepsilon^2\delta(t)}/\sqrt t\)는 \(d_f>99\)에서 49보다 크다.
이는 explicit-99 **direct certificate**의 불충분성이지 실제 endpoint error의 하한이나
모든 explicit proof의 불가능성 정리가 아니다.

## 완료 결과 — 2026-09-28 03:43 KST

- Explicit Theorem 1.2의 fixed-family subset transfer와 sigma range를 고정했다.
- Current \(99<d_f<416\) overlap과 epsilon ceiling \(317/41184\)을 도출했다.
- McCurley constant를 exact rational로 고정하고 decay exponent \(<3/1000\)을 검증했다.
- Theorem 2.3 sup의 \(t=e\) endpoint에서 optimistic floor
  \(98703/2000>49\)를 증명했다.
- Explicit-99 direct black-box route만 <code>REJECTED</code>로 판정하고 sharp \(12/5\)
  route와 actual error는 OPEN으로 보존했다.

검증:

~~~text
new targeted Python                          9 tests PASS
canonical DEP-R09 regression               414 tests PASS
verification inventory                     PASS
theory / display / Lean declarations       100 / 1,964 / 376
forbidden proof escape                      0
Lean direct compile                         exit 0
Lean full build                             8,765 jobs PASS
full Python regression                      1,082 tests, existing 1 failure
~~~

Full regression의 유일한 failure는 기존 PowerShell 5.1
<code>test_windows_powershell_51_preserves_quote_sensitive_argv</code>의
<code>$LASTEXITCODE</code> undefined다. 이번 diff는 해당 runner/test를 변경하지 않았다.

Actual prime/zero 계산, package 설치, threshold calculator, 장시간 계산,
conditional branch, push/PR은 수행하지 않았다.
