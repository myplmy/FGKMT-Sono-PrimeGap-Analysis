# DEP-R09 outer-law sparse centered-mean 감사 작업원장

- 시작: 2026-09-27 12:21 KST
- 기준 commit: <code>d9fd30b6655bbc676837642e3aa125481d203a41</code>
- 선행 정본: Theory 49--53, 81, 91--92, review 101,
  <code>handoff/202609270808_HANDOFF.md</code>
- 목표: Theory 92 식 (92.25)의 construction-dependent selected mean을 actual outer
  residue law에서 fixed \(Q'\) mean과 explicit fluctuation·adaptive-deletion 비용으로
  환원하고, 남는 analytic object의 선행정리 적용성을 판정한다.
- 승인·금지: source audit·관련 다운로드·문서·Python·Lean·local commit 허용.
  actual prime/dataset 실험, package 설치, threshold calculator, 장시간 계산, GRH,
  push/PR 금지.

## 영향도

| 축 | 판정 | 근거·통제 |
|---|---|---|
| outer probability law | 직접 영향 | Theory 49 independent uniform \(A_s\)와 exact one/two-point survival만 사용 |
| selected vertex set | 직접 영향 | \(V_0=Q'\cap\mathscr S(\mathbf A)\), adaptive \(E(\mathbf A)\), \(V=V_0\setminus E\) 보존 |
| blind analytic weight | 직접 영향 | Theory 92의 deterministic real \(B_h(q)\), \(|B_h(q)|<11U/5\) 사용 |
| quantifier | 결정적 | weights는 outer draw 전에 fixed, \(E\)만 outcome-dependent; postselection을 fixed-set theorem으로 바꾸지 않음 |
| end-bounded \(G(x)\) | 영향 없음 | 보조 sieve proof만 감사 |
| dataset provenance | 영향 없음 | dataset 미접근 |
| numerical threshold | 간접 영향 | elementary outer costs만 parameterized; fixed mean이 닫히기 전 calculator 금지 |
| Lean | 제한적 | weighted covariance·deletion·strict gate의 scalar terminal만 형식화 |
| 문서/검증 | 영향 있음 | Theory 93·review 102·원장·handoff·inventory 동기화 예정 |

## 접근 비교

| 접근 | 정확성·재현성 | 비용·위험 | 선택 |
|---|---|---|---|
| outer weighted second moment + L∞ deletion | actual law 보존, finite exact | fixed \(Q'\) mean은 남음 | **우선 채택** |
| fixed \(Q'\) dispersion/weighted-BDH source | analytic core에 직접 밀착 | prescribed primorial·numerical cutoff 불일치 가능 | source screen 병행 |
| full residue Parseval/large sieve | 기존 theorem 재사용 | Theory 83 length-term 장벽을 되살림 | 비교 기준만 |
| weighted matching construction redesign | mean을 construction에서 제어할 가능성 | proof architecture 변경 | 별도 승인 전 보류 |

## 단계 현황

1. **DONE — clean HEAD·handoff·Theory 49--53·92 양화사 복구**
2. **DONE — primary-source 표적 검색 착수**
3. **DONE — outer weighted expectation·variance exact reduction**
4. **DONE — adaptive deletion·count-good event와 uniform selected-mean gate 합성**
5. **DONE — fixed \(Q'\) prime-residue mean source applicability 판정**
6. **DONE — Theory 93·review 102·Python·Lean·verification**
7. **DONE — 새 handoff 작성·local commit 준비·중단조건 판정**

## source-first 초기 판정

- FGKMT/FMT의 existing source는 unweighted fixed-subset survival moment를 제공한다.
  deterministic signed weights에 필요한 finite covariance algebra는 직접 전개해야 한다.
- Maynard의 large-moduli I/III는 residue class에 uniform한 강한 mean-value theorem이지만
  modulus average와 large-modulus factorization을 사용한다. current single prescribed
  \(f=U^{1/d_f}\), \(21\le d_f<416\)의 fully numerical selected-residue mean에 바로
  대입되는 source로 아직 판정하지 않는다.
- fixed \(Q'\) mean은 \(q\in Q'\)와 \(q+\ell f\) prime mass의 shifted prime-pair형
  signed discrepancy다. one-sided sieve upper나 full-residue variance와 구별한다.

### 2026-09-27 12:35 KST — Theory 93 완료

- Outer weighted expectation은 exact하게 \(\sigma D_Q\)이며 fixed mean을 제거하지
  않음을 확인했다.
- Relative pair error \(2a^{-17}\)와 \(|B_q|<11U/5\)를 합쳐 normalized weighted
  variance와 Chebyshev failure mass를 parameterized explicit으로 만들었다.
- Outcome-dependent exceptional set은 independence를 가정하지 않고
  \((11/5)U|E|\) worst-case 비용으로 처리했다.
- Construction-dependent \(D_V\)를 deterministic fixed \(D_Q\), fluctuation \(t\),
  deletion \(O(b^{-2})\)로 환원했다.
- Maynard I/III, Stadlmann, Klurman--Mangerel--Teräväinen, Leung 원문을 다운로드·hash
  고정해 theorem object·average·assumption을 대조했다. current relative fixed-primorial
  mean에 대한 unconditional fully numerical drop-in은 식별되지 않았다.
- Python targeted 11 tests와 canonical DEP-R09 348 tests PASS.
- pinned Lean direct compile exit 0, full build 8,765 jobs exit 0.
- canonical verification PASS: theory 94, formulas 1,839, declarations 344,
  forbidden proof escape 0.
- full Python 1,016 tests는 기존 PowerShell 5.1
  <code>test_windows_powershell_51_preserves_quote_sensitive_argv</code> 한 건만 같은
  <code>$LASTEXITCODE</code> undefined로 FAIL했다. 이번 diff에 관련 파일은 없다.
- actual prime/dataset 실험, package 설치, threshold calculator, long computation,
  GRH branch, push/PR은 수행하지 않았다.

## 중단 판정

- 권장 1순위 outer-law 감사는 완료했다.
- numerical \(X_{\rm cert}\) range는 아직 없다.
- 다음 fixed-\(Q'\) pre-absolute-value dispersion은 별도 deep analytic gate이므로 최신
  handoff와 local commit을 만든 뒤 사용자에게 보고하고 일시 중단한다.
- 완료 handoff는 <code>handoff/202609271236_HANDOFF.md</code>다.
