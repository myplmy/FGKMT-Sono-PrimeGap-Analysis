# DEP-R09 Thorner--Zaman full-interval centered transfer 작업원장

- 시작: 2026-09-28 03:08 KST
- 기준 commit: <code>0fff3475679a47a8468192c4846145c64e694d7a</code>
- 선행 정본: Theory 57, 59, 90, 97, review 106, handoff 202609280241
- 목표: actual \(B_0\) zero-free exclusion을 Thorner--Zaman full-interval PNT와
  결합해 exceptional secondary main term을 structural하게 제거하고, Theory 97의
  centered endpoint norm에 필요한 exact remaining multiplier interface를 고정한다.
- 승인·금지: source 다운로드·문서·Python·Lean·local commit 허용. actual
  prime/dataset 계산, package 설치, threshold calculator, 장시간 계산, conditional
  branch, push/PR 금지.

## 영향도

| 축 | 판정 | 통제 |
|---|---|---|
| exceptional zero | 결정적 | actual \(B_0=B_{P(X)}\), primitive conductor \(r\mid f\)를 명시 |
| source normalization | 결정적 | Sono Prop. 5.3의 \(t=0\) direct bound만 사용; 잘못된 \(3c_{\rm ZFR}\) transfer 금지 |
| endpoint norm | 직접 영향 | pointwise common-main error에서 centered error로 factor 2 exact transfer |
| modulus range | 직접 영향 | \(U=f^{d_f}\), \(d_f\ge21>12\)로 full-interval source range 검사 |
| data/end-bounded | 영향 없음 | analytic proof only |
| threshold | 간접 영향 | source \(K,c,U_0\) 숫자 전에는 calculator 금지 |

## 접근 비교

| 접근 | 정확성·장점 | 비용·한계 | 선택 |
|---|---|---|---|
| Theorem 2.3 short-interval proof 재전개 | 전체 DAG 관찰 가능 | \(h=U\)는 proof가 별도 처리; 불필요 loss 다수 | 비교 기준 |
| Corollary 1.4 full interval 직접 사용 | prime theta를 직접 제어, \(U\ge f^{12}\) | \(K,c,U_0\) 미인쇄 | **채택** |
| exceptional secondary term 직접 center | source main을 보존 | character pattern은 center 후에도 남음 | B0 없을 때 경계 |
| actual B0 + relative zero-free Remark 1.3 | \(\lambda=1,\theta=7/12\)로 structural 제거 | effective constants 여전히 미수치 | **채택** |

## 단계 현황

1. **DONE — clean HEAD·Theory 97·handoff 복구**
2. **DONE — arXiv v2 official source TeX download·hash 고정**
3. **DONE — Theorem 2.3/Corollary 1.4 proof-DAG 식 단위 복원**
4. **DONE — actual B0에서 relative zero-free constant \(47/2520\) 도출**
5. **DONE — common-main pointwise error에서 centered norm factor 2 도출**
6. **DONE — Theory 98·review 107·machine ledger·Python·Lean 작성**
7. **DONE — canonical verification**
8. **IN PROGRESS — handoff·local commit**

## source-first 핵심 판정

- Thorner--Zaman source TeX는 proof of Theorem 2.3에서 \(h\le x-1\)만 다루고,
  \(h=x\)는 이미 Corollary 1.4로 별도 인쇄한다.
- Current \(d_f\ge21\)은 Corollary 1.4의 \(U\ge f^{12}\) range를 덮는다.
- Sono Proposition 5.3의 direct \(t=0\) bound \(c_{\rm ZFR}=1/24\),
  \(\log f>47X/100\), \(\log P(X)<21X/20\)에서
  \(c_2=(1/24)(47/105)=47/2520\)다.
- 따라서 Thorner--Zaman Remark 1.3의 \(\lambda=1,\theta=7/12\) branch를
  structural하게 적용할 수 있다. 다만 implied multiplier와 decay/cutoff는 인쇄되지 않았다.

## 진행 중 exact interface

Source pointwise relative error를 \(R_{\rm TZ}(U,f)\)라 하면

\[
 \max_a^*\left|
 \vartheta(U;f,a)-\frac{U}{\varphi(f)}
 \right|
 \le R_{\rm TZ}(U,f)\frac{U}{\varphi(f)}
\]

에서 finite centering만으로

\[
 \epsilon_\infty(U,f)\le2R_{\rm TZ}(U,f)
\]

가 따른다. 남은 source shape는

\[
 R_{\rm TZ}=K_{\rm TZ}
 \left\{e^{-c_{\rm TZ}d_f}
 +e^{-c_{\rm TZ}(\log U)^{3/5}/(\log\log U)^{1/5}}\right\}
\]

이며 \(K_{\rm TZ},c_{\rm TZ}\), common cutoff가 numerical OPEN이다.

## 완료 결과 — 2026-09-28 03:23 KST

- Official arXiv v2 source archive와 TeX를 hash 고정하고 Theorem 2.3 proof와
  Corollary 1.4의 full-interval 분리를 확인했다.
- Actual \(B_0\) conductor exclusion과 project log scale에서
  \(c_2=47/2520\)을 도출했다.
- Thorner--Zaman Remark 1.3의 \(\lambda=1,\theta=7/12\) branch와
  current \(d_f\ge21>12\) range를 연결했다.
- Exceptional character secondary main은 centering만으로 사라지지 않는다는 finite
  counterfixture를 보존했다.
- Common-main pointwise error에서 centered endpoint norm으로 factor 2 transfer를
  exact하게 고정했다.

검증:

~~~text
new targeted Python                         12 tests PASS
canonical DEP-R09 regression               405 tests PASS
verification inventory                     PASS
theory / display / Lean declarations       99 / 1,948 / 371
forbidden proof escape                      0
Lean direct compile                         exit 0
Lean full build                             8,765 jobs PASS
full Python regression                      1,073 tests, existing 1 failure
~~~

Full regression의 유일한 failure는 변경 전부터 있던 PowerShell 5.1
<code>test_windows_powershell_51_preserves_quote_sensitive_argv</code>의
<code>$LASTEXITCODE</code> undefined다. 이번 diff는 해당 runner/test를 변경하지 않았다.

Actual prime/dataset 계산, package 설치, threshold calculator, 장시간 계산,
conditional branch, push/PR은 수행하지 않았다.
