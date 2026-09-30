# 2026-10-01 DEP-R09 common-height centered replay 타당성 검토

## 1. 최종 판정

[Theory 102](../method/theory/102_Sono_FMT_DEPR09_common_height_centered_replay.md)은
공통 height의 low-zero regularizer를 상쇄하고 principal pole·zero packet을
residue-centered projection으로 제거한다. Exact remainder coefficient는
\(2N(\varphi(f)-N)\)이며 \(T=f^{3/2}\)에서 correction decay는 parameterized하게 닫힌다.

Corrected analytic endpoint identity·numerical \(K_{\rm EF}\)·weighted signed zero upper는
별도 source leaves다. 결과는 <code>FINITE_REPLAY_AND_PARAMETERIZED_CORRECTION_PASS</code>이지
numerical PNT·\(X_{\rm cert}\)·range-narrowing certificate가 아니다.

## 2. Source-first 점검

기존 official Thorner--Zaman PDF·native TeX의 hash와 printed p.9 rendered image를
확인했다. 식 (4.2) 바로 위의 \(\psi\) display를 사용한다. Davenport Chapters 17--20은
그 원문이 인용한 source이며 book 자체를 이번에 직접 확인했다고 주장하지 않는다.

| 항목 | 확인·처리 |
|---|---|
| prime-power 합동조건 | literal \(p\equiv a\) 대신 canonical \(p^k\equiv a\); finite witness |
| low-zero regularizer | preceding display처럼 character마다 한 번, 두 endpoint 공통 convention |
| (4.2) nested regularizer | zero sum 안의 추가 low-zero sum을 literal 전사하지 않음 |
| endpoint | closed \(n\le x\); half-weight 보정은 remainder에 보존 |
| numerical EF constant | effective implied constant만 인쇄; \(K_{\rm EF}>0\) premise·OPEN |
| imprimitive Euler zeros | \(\Re s=0\) terms와 primitive nontrivial zeros 구분 |
| possible real zero | relative separation은 부재 증명이 아님; all-zero packet 또는 explicit term |

Finite mask·sum identities는 standard linear algebra다. Lean/Mathlib의 finite sum,
complex coercion과 norm triangle을 재사용했으며 새 analytic source theorem을
증명하거나 local axiom으로 추가하지 않았다.

## 3. Orientation·normalization

\(\sum H=0\)이고 nonprincipal channel은
\(\phi^{-1}\sum H(a)\overline{\chi(a)}=C_\chi(Q')\)다. 따라서 zero packet의 음수 부호와
prime-power subtraction을 유지하면 core는
\(-\sum C_\chi\Delta F_\chi+R_{\rm EF}-R_{\rm pp}\)다.

Principal character는 constant 1이므로 pole와 zero packet 전체가 사라진다.
\(f\mid P(X)/B_0\) 때문에 \(P^+(f)\le X\): \((X,U]\)의 primes는 모두 unit이다.
Possible \(\beta_1\)를 제외하면
\(-C_{\chi_1}(U^{\beta_1}-X^{\beta_1})/\beta_1\)를 반드시 따로 유지한다.
Actual character orthogonality·prime/zero identification 전체가 Lean proof는 아니다.

## 4. Remainder와 낮은 height

Selected \(N\)개에서 \(H=\phi-N\), complement \(\phi-N\)개에서 \(H=-N\)이므로
\(\sum|H|=2N(\phi-N)\)다. Uniform complex endpoint errors 아래 interval upper를
Lean으로 증명했다. Abstract error class에서 sharp하지만 actual error lower가 아니다.

\(U=f^d,T=f^s\)에서 가장 큰 correction power는 \(f^{1-s}\)다.
\(s=3/2\), \(21\le d<416\)의 uniform coefficient는
\(4[416^2+(3+3/2)416+1]=699716\)이다.
Prime powers는 source의 implicit \(\sqrt x\) constant를 1로 바꾸지 않고 elementary
\(\sqrt U\log U\) mass와 \(\|H\|_\infty\le\phi\)로 별도 상계했다.
Real log/exp absorption과 symbolic cutoff는 문서 증명이며 Lean 전체 형식화는 아니다.

## 5. Historical 판정 교정

Theory 100의 \(>10^6\), \(>4000\) arithmetic은 \(T=f^5\)에서 유효하다. Height를 바꾸면
detector exponent·zero-free denominator·correction powers가 함께 변하므로 모든 height를
배제하는 floor는 아니다. Theory 100과 canonical 요약에 이 scope를 명시했다.

Theory 101의 angle budget은 conditional energy upper \(A_Z\le U^2\)로 target을
보증하는 충분조건이다. Actual \(A_Z\)가 더 작으면 그 angle bound 없이도 target이
성립할 수 있다. “target의 필요조건”이라는 표현만 교정했으며 기존 Lean statement와
rational test는 유지했다.

## 6. 검증 수준

- New finite tests 9건 PASS: all small abstract masks·sharp uniform-error coefficient,
  modulo-5 complex projection·principal invariance·regularizer mismatch rejection·source hashes.
- Lean 직접 compile PASS: finite zero sum·complex constant channel·exact \(L^1\)·interval
  remainder·regularizer cancellation·finite weighted replay·rational coefficient.
- Formula (102.7)은 generic replay만 Lean이 검사하므로
  <code>PARTIAL_FORMALIZATION</code>이다. Whole analytic source theorem으로 승격하지 않는다.
- Numerical \(K_{\rm EF}\), signed gate, lower-height density composition, PAP-11·DEP-R09·
  fixed \(2e-17\)·\(X_{\rm cert}\)는 OPEN이다.

최종 regression·build·inventory 결과는 신규 작업원장·handoff에 기록한다.
기존 PowerShell 5.1 failure는 이번 수정 대상이 아니다.

## 7. 다음 gate와 연구적 가치

우선 \(T=f^{3/2}\)에서 finite density prerequisites와 actual zero-free denominator를
재합성하고 corrected endpoint의 uniform numerical \(K_{\rm EF}\)를 복원한다.
부족하면 actual weighted signed-zero theorem을 source-first로 찾거나 증명한다.
Numerical source 및 DEP-R09--R12 composition 전 calculator는 NOT READY다.

이번 결과는 standard explicit-formula cancellation과 finite normalization의 정확한 적용이다.
Lower-height route 재개는 프로젝트 진전이지만 미검증 선행연구를 넘어선 새 학술정리나
numerical threshold의 발견이라고 보고할 근거는 없다. 큰 학술 발견이나 장시간 계산이
필요해지면 사용자에게 보고하고 해당 단계에서 중단한다.
