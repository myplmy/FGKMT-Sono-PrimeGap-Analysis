# DEP-R09 reweighted local character-transform 감사 작업원장

- 시작: 2026-09-27 06:43 KST
- 루트: <code>Z:\FGKMT-Sono-PrimeGap-Analysis</code>
- WSL 작업경로: <code>/mnt/z/fgkmt-sono-primegap-analysis</code>
- 기준 commit: <code>55594f308272a2a053dda38063ae1256b9094649</code>
- 선행 정본: Theory 47, 53--54, 77, 80--88, review 97, handoff 202609221428
- 목표: FGKMT formula (5.9)의 reweighted coordinate law에 대한 exact local
  Dirichlet-character transform을 고정하고, existing source theorem의 적용범위와
  randomized-coordinate transform이 보지 못하는 blind-character family를 감사한다.
- 사용자 승인: source audit, 필요한 학술자료 다운로드, 관련 문서·코드·Lean 검증,
  로컬 staging·commit.
- 금지 범위: actual maximal-gap·prime·dataset 실험, 패키지 설치, threshold calculator,
  장시간 계산, GRH branch 채택, push, PR, 외부 게시.
- 중단 조건:
  1. numerical \(X_{\rm cert}\) bounded range가 생기면 사용자에게 보고하고 일시 중단.
  2. 기존에 확인되지 않은 학술적 가치가 큰 발견이면 과잉 novelty 없이 보고 후 중단.
  3. 장시간 연산이 필요하면 정확한 사용자 실행 절차를 작성하고 중단.
  4. 추가 Python library가 필요하면 설치하지 않고 사용자에게 요청.
  5. <code>sorry</code>, <code>admit</code>, project-local <code>axiom</code> 금지.

## 입력과 provenance

| 입력 | 현재 증거 | 상태 |
|---|---|---|
| FGKMT/FMT proof law | 기존 hash-pinned 원문, formulas (5.7)--(5.11) | reweighted coordinate transform source |
| Theory 47 | Maynard multidimensional weight, growing k, \(R\asymp X^{1/9}\) | preliminary law normalization |
| Theory 53 | full-residue lift, fixed coordinates 0 | local residue map |
| Theory 80 | global \(C_\chi(\omega)Z_\chi\) observable | downstream target |
| Theory 88 | randomized modulus와 fixed modulus 분리 | blind family 정의 |
| Granville--Koukoulopoulos--Maynard | arXiv:1606.06781v4, 85 pages, SHA-256 <code>67feecce65ced4250aa046d6e0c36300744eb84358d21d53409a512d1649e34d</code> | character-twisted divisor-sum 비교 source |

## 영향도 분석

| 축 | 판정 | 통제 |
|---|---|---|
| final probability law | 영향 있음 | stage-history conditional transform만 사용; global independence 금지 |
| character factorization | 영향 있음 | randomized modulus \(h\), fixed modulus \(f=\mathfrak q/h\) CRT 분해 |
| same-law moment | 영향 있음 | local transform saving과 blind family를 별도 ledger로 분리 |
| prime-error theorem | 계속 OPEN | coefficient energy와 \(Z_\chi\) correlation을 혼동하지 않음 |
| empirical/data 축 | 영향 없음 | dataset·runner 미접근 |
| numerical \(X_{\rm cert}\) | 영향 없음 예상 | calculator·actual evaluation 금지 |
| 문헌 provenance | 영향 있음 | theorem object, growing-k uniformity, modulus/range를 개별 대조 |
| Lean | 제한적 | transform triangle, blind energy, Cauchy terminal만 finite scalar 형식화 |

## 접근법 비교

| 접근 | 정확성·재현성 | 비용·위험 | 선택 |
|---|---|---|---|
| exact local transform + blind family split | actual law와 CRT factorization을 보존 | blind prime-error correlation은 새 입력 | **채택** |
| atom cap에서 Fourier decay 추론 | 간단 | 작은 atom이어도 character level-set 분포는 transform 1; 거짓 | 기각 |
| GKM character-twisted sieve theorem 직접 대입 | 선행연구 우선 원칙 | 단일 divisor sum·fixed k·다른 range라 양화사 불일치 | source 비교만 |
| Maynard weight를 직접 전개해 Burgess 적용 | 가능성 있음 | growing-k coefficient L1·hypergraph reweighting 손실 미복원 | 후속 후보 |
| full \(V\) large sieve | 기존 검증 | Theory 83·88 장벽 | 기각 |

## 단계 현황

1. **DONE — WSL·Git·handoff·skills·source hash 확인**
2. **DONE — 관련 선행문헌 검색·GKM PDF 다운로드**
3. **DONE — exact local transform·atom-cap counterexample 정식화**
4. **DONE — blind-character energy·source applicability·next gate**
5. **DONE — Theory 89·review 98·machine ledger·Python·Lean**
6. **DONE — canonical 회귀·전수 verification·local commit**

## 착수 기록

### 2026-09-27 06:43 KST — source-first 착수

- clean worktree와 latest handoff·Theory 88을 확인했다.
- web primary-source screen에서 가장 가까운 자료인 Granville--Koukoulopoulos--Maynard,
  *Sieve weights and their smoothings* arXiv v4를 식별해 <code>tmp/</code>에 내려받았다.
- 원문 Theorem 1.5는 real character로 twisted한 **단일 truncated Möbius divisor
  sum의 \(2k\)-moment**를 다룬다. actual multidimensional Maynard \(w(p,n)\),
  growing \(k\), full-residue edge와 hypergraph formula (5.9)는 대상이 아니다.
- exceptional branch는 \(e^{(\log q)^C}\le R\le e^{1/(1-\beta)}\)를 요구한다.
  actual local modulus \(p\asymp X\), sieve scale \(R\asymp X^{1/9}\)와 맞지 않고
  constants도 fixed k에 의존한다. 따라서 drop-in으로 채택하지 않는다.
- atom cap alone에서 local Fourier saving을 추론할 수 없는 exact counterexample로,
  quadratic character의 한 level set에 균등분포를 두면 max atom은 작아도 transform
  modulus가 1이 됨을 확인했다.
- randomized coordinates에서 principal인 global characters는 local nonprincipal
  transform saving을 전혀 받지 않는 blind family를 이룬다. 이 family의 coefficient
  energy를 fixed modulus character orthogonality로 감사한다.

### 2026-09-27 07:02 KST — Theory 89 구현·검증·local commit

- exact local transform, quadratic level-set counterexample와 blind family
  coefficient energy identity를 Theory 89·review 98에 고정했다.
- GKM Theorem 1.5 원문은 대상·range·growing dimension이 불일치해 drop-in으로
  채택하지 않았다.
- canonical Python 회귀시험 138개, Lean direct compile·full build와 verification
  refresh가 PASS했다. inventory는 theory 90개, display 식 1,733개, declaration
  324개, 금지 proof escape 0건이다.
- local commit <code>14511e000bbf0ea01e1c7a5dcc5788734093ad15</code>을 만들었다.
- 다음 gate인 blind fixed-modulus reduction을 같은 세션에서 계속한다.

## 완료 판정

- Theory 89 batch는 local commit <code>14511e000bbf0ea01e1c7a5dcc5788734093ad15</code>에
  포함됐다.
- source PDF는 ignored <code>tmp/</code>에만 보존되고 commit 대상이 아니다.
- successor Theory 90--92가 blind family를 native fixed modulus, weighted moment,
  sparse real discrepancy 순으로 더 좁혔다.
- actual prime/dataset 실험, package 설치, threshold calculator, long computation,
  GRH branch, push/PR은 수행하지 않았다.
