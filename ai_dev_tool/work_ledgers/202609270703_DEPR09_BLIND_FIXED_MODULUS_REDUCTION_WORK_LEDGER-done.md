# DEP-R09 blind fixed-modulus reduction 작업원장

- 시작: 2026-09-27 07:03 KST
- 기준 commit: <code>14511e000bbf0ea01e1c7a5dcc5788734093ad15</code>
- 선행 정본: Theory 76, 83--85, 89, review 98
- 목표: blind lifted character energy를 fixed-coordinate modulus \(f\)의 native
  character energy와 explicit imprimitive prime-power correction으로 환원하고,
  existing variance·PNT source의 actual range를 재판정한다.
- 승인·금지 범위: local transform ledger와 동일. actual 계산·설치·threshold·GRH·
  push/PR 금지, source audit·Lean·local commit 허용.

## 영향도

| 축 | 판정 | 통제 |
|---|---|---|
| character normalization | 영향 있음 | lifted modulo \(\mathfrak q=fh\)와 native modulo \(f\) endpoint 동일화 |
| imprimitive correction | 영향 있음 | \(p\mid h\) prime powers를 누락 없이 합산 |
| source range | 결정적 | \(d_f=\log Y/\log f\)의 actual 21--416 범위 |
| GRH | 범위 밖 | conditional source를 unconditional 정본에 채택하지 않음 |
| numerical correction | parameterized explicit 목표 | \(X_{\rm cert}\)로 승격 금지 |
| empirical 축 | 영향 없음 | actual prime data 미사용 |

## 접근 비교

| 접근 | 장점 | 한계 | 선택 |
|---|---|---|---|
| native-\(f\) energy + explicit lift correction | normalization exact, 기존 variance source 재사용 가능 | native analytic upper OPEN | **채택** |
| pointwise Bennett PNT | direct | source cutoff가 actual \(d_f\)와 불일치 예상 | range audit |
| Vaughan modulus average | exact bridge 있음 | prescribed \(f\), small power modulus와 불일치 | source audit |
| Friedlander--Goldston fixed \(f\) | object 일치 | GRH·implicit | unconditional 미채택 |
| direct weighted correlation | 가장 약한 target | 새 theorem 필요 | 후속 |

## 단계 현황

1. **DONE — predecessor·source normalization 확인**
2. **DONE — imprimitive prime-power correction exact reduction**
3. **DONE — correction absorption gate**
4. **DONE — \(d_f\) range와 source theorem 재감사**
5. **DONE — Theory 90·review 99·Python·Lean·verification**
6. **DONE — local commit·successor 연결**

### 2026-09-27 07:18 KST — Theory 90 완료

- blind lifted error를 native modulo-\(f\) error와 explicit randomized-prime
  prime-power correction으로 환원했다.
- correction quarter-budget과 \(21\le d_f<416\)을 고정하고 checked sources의
  range 불일치를 기록했다.
- canonical Python 48 tests, Lean direct compile·full build, verification
  inventory 91 theories/1,763 formulas/329 declarations가 PASS했다.
- local commit <code>8aee8ba</code>를 생성했고 direct weighted correlation을 계속한다.

## 완료 판정

- full commit은 <code>8aee8bac382d5727b0b235af514e57717661db41</code>이다.
- Theory 91--92 successor는 native energy 전체를 직접 닫는 대신 blind weighted
  observable의 특수 구조를 사용한다. Theory 90의 correction identity와 source-range
  판정은 그대로 유효하다.
- actual prime/dataset 실험, package 설치, threshold calculator, long computation,
  GRH branch, push/PR은 수행하지 않았다.
