# DEP-R09 sharp-density fixed-f specialization 작업원장

- 시작: 2026-09-28 03:50 KST
- 기준 commit: <code>49c53a4</code>
- 선행 정본: Theory 61--73, 98--99, review 108, handoff 202609280344
- 목표: Theory 71의 sharp near-one averaged density와 Theory 73 tightened coefficient를
  fixed \(f\), full-interval endpoint에 재특수화하고 PAP 전용 후단 비용을 제거한
  optimistic density-core certificate가 current range를 통과하는지 판정한다.
- 승인·금지: source audit·문서·Python·Lean·local commit 허용. actual prime/zero 계산,
  package 설치, threshold calculator, 장시간 계산, conditional branch, push/PR 금지.

## 영향도·접근 비교

| 접근 | 장점 | 한계 | 선택 |
|---|---|---|---|
| Theory 72 PAP certificate 그대로 | 이미 완전한 split | principal·Maier·count 비용 과대포함 | 기각 |
| Theory 71 density core만 fixed-f 특수화 | endpoint에 필요한 부분만 보존 | averaged \(Q^2\), 큰 detector coefficient | **채택** |
| Theory 73 tightened coefficient | 기존 source 안 최선의 finite-safe 수치 | w=1/21 endpoint 전용 | **채택** |
| 새 detector/weight 설계 | coefficient 구조 변경 가능 | construction redesign 승인 필요 | 후속 별도 |

Dataset/end-bounded 의미론에는 영향이 없고 analytic source·Lean 원장·handoff에만 영향이
있다. 큰 upper certificate를 actual error lower로 읽지 않는다.

## 단계 현황

1. **DONE — Theory 61--73 source·coefficient chain 복구**
2. **DONE — Q=f, T=f^5, D=f^7 fixed-family specialization**
3. **DONE — theta=1/21에서 kappa=22, lambda=1-22/d_f 복원**
4. **DONE — PAP 후단 비용 제거한 optimistic density-core floor 도출**
5. **DONE — Theory 100·review 109·machine ledger·Python·Lean 작성**
6. **DONE — canonical verification**
7. **IN PROGRESS — handoff·local commit**

## 핵심 진단

Theory 73 tightened coefficient

\[
C_{J,\mathrm{tight}}=11503697604450072/425315>2.7\times10^{10}
\]

만 보존하고 all outer factors를 버린다. \(d_f>22\)에서 가장 유리한 current endpoint
\(d_f<416\)과 explicit \(c_M=1/9.645908801\)을 써도

\[
C_{J,\mathrm{tight}}
\exp\{-c_M(d_f-22)/5\}
>
C_{J,\mathrm{tight}}e^{-9}
>
C_{J,\mathrm{tight}}/3^9
>10^6.
\]

\(21\le d_f\le22\)에서는 \(\lambda=1-22/d_f\le0\)라 near density decay 자체가
없다. 이는 current Theory 61--73 **certificate package**의 불충분성이지 actual error
하한이나 모든 sharp-density proof의 불가능성 정리가 아니다.

## 완료 결과 — 2026-09-28 04:04 KST

- Theory 71 primitive near-one family를 \(Q=f,T=f^5,D=f^7\)로 특수화했다.
- \(\omega=1/21\)의 \(\kappa=22\), \(\lambda=1-22/d_f\)를 복원했다.
- PAP outer costs를 모두 제거한 Theory 73 tightened core floor \(>10^6\)을 증명했다.
- 모든 dimensionless factor를 1로 둔 \(\omega^{-6}\)-only floor \(>4000\)을 증명했다.
- Current certificate architecture만 <code>INSUFFICIENT</code>로 판정하고 actual error,
  fixed-modulus reproof와 pre-sup cancellation은 OPEN으로 보존했다.

검증:

~~~text
new targeted Python                          8 tests PASS
canonical DEP-R09 regression               422 tests PASS
verification inventory                     PASS
theory / display / Lean declarations       101 / 1,978 / 381
forbidden proof escape                      0
Lean direct compile                         exit 0
Lean full build                             8,765 jobs PASS
inventory numeric-order regression             2 tests PASS
full Python regression                      1,092 tests, existing 1 failure
~~~

첫 ledger validation은 Theory 100 식 (100.4)의 <code>\frac</code>가 U+000C로 저장된
text-integrity 문제를 fail-closed로 검출했다. 해당 한 줄을 교정하고 generator부터 다시
실행해 최종 PASS했다.

Theory 번호가 100에 도달하면서 기존 inventory generator의 두 자리 regex와 lexical sort가
Theory 100을 Theory 10 뒤에 삽입하는 문제도 발견했다. Regex를 2자리 이상으로 확장하고
numeric sort key를 추가해 기존 00--99 order를 보존했으며 전용 2-test regression을 추가했다.

Full regression의 유일한 failure는 기존 PowerShell 5.1
<code>test_windows_powershell_51_preserves_quote_sensitive_argv</code>의
<code>$LASTEXITCODE</code> undefined다. 이번 diff는 해당 runner/test를 변경하지 않았다.

Actual prime/zero 계산, package 설치, threshold calculator, 장시간 계산,
conditional branch, push/PR은 수행하지 않았다.
