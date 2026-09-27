# DEP-R09 fixed-Q' pre-absolute-value bilinear 감사 작업원장

- 시작: 2026-09-27 23:19 KST
- 기준 commit: <code>0294205175bc861ee3bee4b6d7e00a8016c4d324</code>
- 선행 정본: Theory 77, 92--93, review 102,
  <code>handoff/202609271236_HANDOFF.md</code>
- 목표: Theory 93 식 (93.11)/(93.25)의 deterministic fixed-\(Q'\) mean을
  centered kernel, prime-prime bilinear form, B0와 prime-power correction으로 exact하게
  분해하고 R10 upper-bound sieve가 제공하는 것과 제공하지 않는 것을 고정한다.
- 승인·금지: source audit·다운로드·문서·Python·Lean·local commit 허용. actual
  prime/dataset 실험, package 설치, threshold calculator, 장시간 계산, GRH/
  Hardy--Littlewood branch, push/PR 금지.

## 영향도

| 축 | 판정 | 통제 |
|---|---|---|
| fixed analytic mean | 직접 영향 | \(D_Q\) equality만 재색인; law·coefficient 변경 없음 |
| prime/prime-power normalization | 결정적 | \(\Lambda=\Lambda_{\mathbb P}+\Lambda_{\ge2}\), B0와 \((n,fh)=1\) 보존 |
| R10 source | 영향 있음 | one-sided pair upper를 centered two-sided theorem으로 승격 금지 |
| outer/inner probability | 영향 없음 | Theory 91--93 outputs를 premise로만 사용 |
| end-bounded \(G(x)\), dataset | 영향 없음 | 보조 analytic proof만 감사, dataset 미접근 |
| numerical threshold | 간접 영향 | elementary corrections만 parameterized; bilinear gate 전 calculator 금지 |
| Lean | 제한적 | kernel bookkeeping·correction transfer·upper-only countermodel scalar만 형식화 |
| 문서 파급 | 영향 있음 | Theory 94·review 103·METHODS·indexes·handoff 동기화 예정 |

## 접근 비교

| 접근 | 정확성·재현성 | 비용·위험 | 선택 |
|---|---|---|---|
| centered kernel + prime/prime-power exact split | 양화사·sign 보존 | 새 bilinear theorem은 남음 | **우선 채택** |
| R10/Selberg upper 즉시 대입 | source 재사용 | lower/main cancellation 없음 | component boundary만 감사 |
| full character energy | 기존 source 많음 | Theory 83 length-term 장벽 재도입 | 기각 |
| Λ/log로 small-prime indicator 확장 | standard bilinear form | h/B0-supported small prime-power correction 추가 | 필요할 때 후속 |

## 단계 현황

1. **DONE — clean HEAD·Theory 93·R10 DAG·Sono Section 4 복구**
2. **DONE — explicit prime-pair/Selberg source 표적 검색**
3. **DONE — centered kernel·prime/prime-power·B0 exact identities**
4. **DONE — prime-power correction explicit absorption**
5. **DONE — R10 one-sided upper의 logical insufficiency와 applicability 판정**
6. **DONE — Theory 94·review 103·Python·Lean·verification**
7. **IN PROGRESS — local commit·다음 gate 연결**

## source-first 초기 판정

- Exact bilinear reindexing 자체는 finite orthogonality와 \(\Lambda\) support의 직접
  lemma이며 별도 deep source가 필요하지 않다.
- Sono Section 4/Theorem 4.1은 Halberstam--Richert의 Selberg upper-bound sieve를
  사용해 두 linear forms가 모두 prime인 수의 **one-sided upper**를 준다. current
  centered absolute discrepancy에는 lower/main cancellation이 별도로 필요하다.
- Generic Selberg/twin-prime sources도 upper만 제공한다. 이를 signed centered bound로
  채택하지 않는다.

### 2026-09-27 23:45 KST — Theory 94 완료

- Fixed mean을 mean-zero kernel von Mangoldt sum으로 exact하게 전개했다.
- Prime/prime-power split, B0 atom과 unique \(p=q+\ell f\) reindex를 고정했다.
- B0 relative cost \(\log X/U\), prime-power cost
  \((U^{1/21}+1)\log U/\sqrt U\)를 parameterized explicit으로 분리했다.
- Sono Section 4/Theorem 4.1을 원문 대조해 per-shift determinant/error와 one-sided
  output의 범위를 고정했다. Upper-only countermodel은 relative centered error 1을
  exact하게 달성한다.
- Python targeted 12 tests, canonical DEP-R09 360 tests PASS.
- pinned Lean direct compile과 full build 8,765 jobs PASS.
- canonical verification PASS: theory 95, formulas 1,861, declarations 349,
  forbidden proof escape 0.
- actual prime/dataset 실험, 설치, threshold calculator, 장시간 계산, conditional
  branch, push/PR은 수행하지 않았다.

## 완료 판정

- Theory 94 batch는 local commit으로 보존한 뒤 character/conductor dualization을 새
  ledger에서 이어간다.
- 이 batch 자체는 numerical \(X_{\rm cert}\) range를 만들지 않았다.
