# DEP-R09 cross-scale covariance·Abel interface 작업원장

- 시작: 2026-09-28 00:09 KST
- 기준 commit: <code>81353e5f0198e5b5a9e91bac33a32fa9b34f29f5</code>
- 선행 정본: Theory 85, 95, review 104, handoff 202609280001
- 목표: unweighted small-prime character coefficient를 endpoint-safe theta Abel
  integral로 바꾸고, fixed mean의 weighted product를 two-scale residue covariance로
  exact 환원해 variance/PNT source의 실제 적용 interface를 고정한다.
- 승인·금지: source audit·문서·Python·Lean·local commit 허용. actual data/prime 계산,
  package 설치, threshold calculator, 장시간 계산, conditional branch, push/PR 금지.

## 영향도

| 축 | 판정 | 통제 |
|---|---|---|
| endpoint normalization | 결정적 | \((X,Y]\) half-open prime interval과 Abel plus integral 보존 |
| character conjugation | 결정적 | \(C_\chi=\sum\bar\chi(q)\), cross term orientation 고정 |
| prime powers | 영향 있음 | small variable is prime indicator; theta 사용으로 별도 correction 없음 |
| source bridge | 직접 영향 | fixed-q variance upper와 mixed covariance를 구분 |
| data/end-bounded | 영향 없음 | analytic proof only |
| threshold | 간접 영향 | covariance source 전에는 calculator 금지 |

## 접근 비교

| 접근 | 장점 | 한계 | 선택 |
|---|---|---|---|
| Abel + exact cross-covariance | endpoint/sign 보존 | mixed moment theorem 필요 | **채택** |
| separate variance Cauchy | known sources 많음 | Theory 95 phi/N loss | 비교 기준 |
| polarization of variances | mixed term을 variance로 표현 | combined-sequence fixed-q theorem 필요 | source interface |
| pointwise PNT per residue | 충분히 강함 | 기존 DEP-R09 hidden constants | fallback |

## 단계 현황

1. **DONE — clean HEAD·Theory 95·Vaughan variance source 복구**
2. **DONE — cross-covariance 선행자료 표적 검색**
3. **DONE — endpoint-safe Abel·mixed character identity**
4. **DONE — residue-space cross-covariance·polarization**
5. **DONE — Vaughan/Harper/Thorner--Zaman applicability 판정**
6. **DONE — Theory 96·review 105·Python·Lean·verification**
7. **IN PROGRESS — local commit·다음 covariance proof gate 연결**

## source-first 초기 판정

- Vaughan 2001은 one-scale residue variance와 character energy의 exact bridge를 주지만
  current mixed scale covariance theorem을 statement로 제공하지 않는다.
- Harper 2024 general-sequence BDH는 modulus average \(Q>\sqrt x\) 쪽의 variance
  asymptotic이며 prescribed \(f=U^{1/d_f}\) 한 개의 fully numerical covariance가 아니다.
- Thorner--Zaman pointwise PNT는 mixed covariance를 충분히 닫을 수 있지만 기존 audit의
  unnamed multiplier·finite cutoff blocker가 그대로 남는다.

### 2026-09-28 00:22 KST — Theory 96 완료

- Small-prime coefficient를 half-open endpoint와 plus integral을 보존한 Abel identity로
  exact하게 변환했다.
- Character mixed product와 residue two-scale covariance, real polarization identity를
  exact하게 고정했다.
- Uniform cross input의 whole-core transfer multiplier를
  \(2+\log(\log Y/\log X)\le2+b/a\)로 explicit화했다.
- Vaughan 2001, Harper 2024, Thorner--Zaman source의 exact non-drop-in 범위를 기록했다.
- Python targeted 10 tests와 canonical DEP-R09 381 tests PASS.
- Lean direct compile과 full build 8,765 jobs PASS.
- canonical verification PASS: theory 97, formulas 1,902, declarations 360,
  forbidden proof escape 0.
- actual prime/dataset 계산, package 설치, threshold calculator, conditional branch,
  push/PR은 수행하지 않았다.
- full Python 1,049 tests는 기존 PowerShell 5.1
  <code>test_windows_powershell_51_preserves_quote_sensitive_argv</code> 한 건만 같은
  <code>$LASTEXITCODE</code> undefined로 FAIL했다. 이번 diff에 관련 파일은 없다.

## 완료 판정

- Theory 96 batch는 local commit으로 보존하고, 식 (96.9)의 direct prescribed-modulus
  covariance proof/source audit을 다음 batch에서 계속한다.
- 최신 session handoff에서 검증 증거와 다음 source/proof 순서를 고정한다.
