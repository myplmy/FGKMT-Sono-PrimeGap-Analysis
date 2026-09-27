# DEP-R09 conductor-weighted character dual 감사 작업원장

- 시작: 2026-09-27 23:39 KST
- 기준 commit: <code>dc1565b</code>
- 선행 정본: Theory 84, 94, review 103
- 목표: centered binary-prime form을 nonprincipal character와 primitive conductor별로
  exact dualize하고, prime-supported large-sieve source를 두 coefficient 축에 적용했을
  때 current strict gate를 인증할 수 있는지 판정한다.
- 승인·금지: source audit·다운로드·문서·Python·Lean·local commit 허용. actual
  prime/dataset 실험, 설치, threshold calculator, 장시간 계산, conditional branch,
  push/PR 금지.

## 영향도

| 축 | 판정 | 통제 |
|---|---|---|
| character normalization | 직접 영향 | primes \(>X\)라 induction correction 없이 primitive core 일치 |
| conductor partition | 직접 영향 | Theory 84 count identity 재사용, character-count 감소로 오인 금지 |
| analytic source | 영향 있음 | Schlage--Puchta prime-supported large sieve 원문 적용범위 대조 |
| proof target | 유지 | full L2가 아니라 signed product sum을 최종 target으로 보존 |
| dataset/end-bounded | 영향 없음 | analytic proof only |
| calculator | NOT READY | separate-L2 certificate가 실패하면 weighted correlation OPEN 유지 |

## 접근 비교

| 접근 | 장점 | 한계 | 선택 |
|---|---|---|---|
| exact character + conductor dualization | sign·primitive structure 보존 | analytic product bound 필요 | **채택** |
| separate prime-supported L2 + Cauchy | known source 사용 | \(\varphi(f)N\) coefficient energy 재지불 | certificate 비교 |
| pointwise character bounds | simple | character 수와 implicit constants 폭증 | 비권장 |
| modulus-average dispersion | potential sign saving | prescribed divisor family와 불일치 | source screen 후속 |

## 단계 현황

1. **DONE — Theory 84/94·clean HEAD 복구**
2. **DONE — Schlage--Puchta prime-supported large-sieve PDF 다운로드·hash 고정**
3. **DONE — exact character/conductor dual identities**
4. **DONE — separate-L2 normalized certificate barrier**
5. **DONE — low/high conductor source range 판정**
6. **DONE — Theory 95·review 104·Python·Lean·verification**
7. **IN PROGRESS — local commit·다음 weighted-correlation source 감사 연결**

## source provenance

- J.-C. Schlage-Puchta, *Primes in short arithmetic progressions*,
  arXiv:1105.1623v1, 5 pages.
- local SHA-256:
  <code>51af128d287a021305412213b3828439dddd70a6bed8266134fac6d95b6705ac</code>.
- Theorem 2는 prime-supported coefficients에 \(N>Q^{2+\varepsilon}\)에서
  conductor/modulus average L2를 주지만 implied constant는 \(\varepsilon\)-dependent다.
- Theorem 3·Corollary 5는 single modulus/character bounds를 주며 cubefree case의 range를
  개선하지만 current small-prime coefficient length \(Y\ll f^c\)의 full character
  family를 numerical하게 제어하지 않는다.

### 2026-09-27 23:55 KST — Theory 95 완료

- Centered prime core를 character 및 primitive conductor별 weighted product로 exact
  dualize했다.
- Primitive coefficient energy를 residue occupancy와 divisor Möbius inversion으로
  고정했고 total \(N(\varphi(f)-N)\)을 확인했다.
- Schlage--Puchta Theorem 2는 large-prime axis range를 덮지만 small-prime full-modulus
  axis는 덮지 않음을 확인했다.
- Separate L2+Cauchy는 optimistic source multiplier one에서도 normalized square
  \((\varphi(f)-N)/N>1\)을 남긴다.
- Python targeted 11 tests, canonical DEP-R09 371 tests PASS.
- Lean direct compile과 full build 8,765 jobs PASS.
- canonical verification PASS: theory 96, formulas 1,883, declarations 354,
  forbidden proof escape 0.
- actual prime/dataset 계산, package 설치, threshold calculator, conditional branch,
  push/PR은 수행하지 않았다.

## 완료 판정

- Theory 95 batch는 local commit으로 보존하고, direct joint weighted-product source
  audit을 새 ledger에서 계속한다.
