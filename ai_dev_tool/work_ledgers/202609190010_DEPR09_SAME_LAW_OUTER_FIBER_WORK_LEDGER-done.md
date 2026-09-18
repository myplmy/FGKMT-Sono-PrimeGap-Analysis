# DEP-R09 same-law outer-fiber minimax 감사 작업원장

- 시작: 2026-09-19 00:10 KST
- 루트: <code>Z:\FGKMT-Sono-PrimeGap-Analysis</code>
- WSL 작업경로: <code>/mnt/z/fgkmt-sono-primegap-analysis</code>
- 기준 commit: <code>3eed30037f9e6851eb662ba2c2e31a92dbd3cc34</code>
- 선행 정본: Theory 79--85, review 87--94, handoff 202609182247
- 목표: 실제 FMT final law에서 outer 좌표의 정확한 균등성을 보존해 raw
  weighted-correlation moment를 outer-fiber maximum energy로 축약하고, 이 정보만으로는
  그 envelope를 보편적으로 더 낮출 수 없음을 exact finite minimax witness로 감사한다.
- 사용자 승인: source audit과 관련 문서·코드·Lean 검증, 로컬 commit.
- 금지 범위: actual maximal-gap·prime·dataset 실험, 패키지 설치, threshold calculator,
  장시간 계산, GRH branch 채택, push, PR, 외부 게시.
- 중단 조건:
  1. 새 bounded <code>X_cert</code> 범위가 생기면 즉시 사용자에게 보고한다.
  2. FMT outer-coordinate 보존이나 final-law 양화사가 원문과 불일치하면 reduction을 승격하지 않는다.
  3. 추가 패키지나 actual 계산이 필요하면 실행하지 않고 사용자에게 요청한다.
  4. <code>sorry</code>, <code>admit</code>, project-local <code>axiom</code>을 도입하지 않는다.

## 입력과 provenance

| 입력 | 현재 증거 | 상태 |
|---|---|---|
| FMT 원문 | <code>tmp/FMT_Chains_of_large_gaps_between_primes.pdf</code>, SHA-256 <code>396e54a9699ad80e749b1607c0b5c26982329625615d8769de1e23328f651828</code> | printed pp. 9, 11--14와 extracted text 대조 대상 |
| Theory 79--82 | 실제 joint law, sieve-good event, atom cap, full-energy reduction | source normalization 정본 |
| Theory 83--85 | generic energy certificate와 variance source의 current-range 장벽 | 새 fiber target과 비교 대상 |

## 영향도 분석

| 축 | 판정 | 통제 |
|---|---|---|
| same-law raw moment | 영향 있음 | full residue energy 앞에 outer-fiber maximum envelope를 삽입 |
| FMT source law | 영향 있음 | outer uniformity와 final coordinate 보존만 사용; inner independence를 가정하지 않음 |
| analytic prime input | 계속 OPEN | fiber maximum을 실제로 낮추는 prime-specific theorem을 발명하지 않음 |
| numerical certificate | 영향 없음 | fixed coefficient·<code>X_cert</code>를 승격하지 않음 |
| empirical/data 축 | 영향 없음 | dataset·runner·result를 읽거나 실행하지 않음 |
| Lean | 제한적 | finite scalar composition과 strict gate만 형식화 |

## 접근법 비교

| 접근 | 장점 | 한계 | 선택 |
|---|---|---|---|
| outer-fiber maximum envelope | actual adaptive inner law를 그대로 허용하며 Theory 82 full-energy보다 약한 exact target | fiber maximum analytic upper가 새로 필요 | **채택** |
| final nibble conditional variance | 성공하면 더 강한 same-law 평균 상계 가능 | source가 increment·variance·Lipschitz 입력을 현재 제공하지 않음 | 후속 OPEN |
| pointwise PAP 또는 GRH | inner adaptation을 우회 가능 | 기존 PAP 장벽 또는 별도 방법론 승인 필요 | 이번 범위 제외 |

## 단계 현황

1. **DONE — WSL·Git·handoff·skills·source locator 확인**
2. **DONE — FMT 양화사와 outer-fiber exact reduction 감사**
3. **DONE — machine ledger·Python exact witness·tests 구현**
4. **DONE — Theory 86·review 95·정본 동기화**
5. **DONE — Lean·전수 verification·회귀시험**
6. **DONE — 완료 handoff·로컬 commit**

## 착수 기록

### 2026-09-19 00:10 KST — 우선순위 1 착수

- WSL2 Ubuntu, bash, repository root와 clean worktree를 확인했다.
- FMT printed p.12는 각 outer <code>A_s mod s</code>가 독립 균등이고 preliminary
  변수와 독립임을 명시한다. printed pp.9, 11의 final extension·conditional covering은
  outer 좌표를 보존하고 inner output만 완성한다.
- 선행 Theory 82의 atom cap을 fiber별로 합치면 full residue energy를 쓰기 전에 더 작은
  outer-fiber maximum energy가 나타난다. 임의의 adaptive inner law에서는 각 fiber의
  maximizer를 결정론적으로 고를 수 있으므로 이 envelope는 outer law만으로 sharp할
  가능성이 있다. 이 명제를 finite exact witness로 검증한 뒤 승격한다.

### 2026-09-19 00:18 KST — exact reduction·구현

- actual conditional shift support \({\cal M}(\boldsymbol a)\)와
  \({\cal H}_{\rm FMT}(R)=\sum_{\boldsymbol a}\max_{m\in{\cal M}(\boldsymbol a)}
  |R(m)|^2\)를 정의했다.
- event conditional subprobability만 사용해
  \(\rho_S\le{\cal H}_{\rm FMT}(R)/Q_{\cal S}\)를 얻었다. outer·inner 또는 event·shift
  독립성은 사용하지 않았다.
- 서로 다른 outer support가 disjoint하므로 \({\cal H}_{\rm FMT}\)는 Theory 82 full
  residue energy 이하이다. 새 direct gate는
  \({\cal H}_{\rm FMT}<\tau^2p_*Q_{\cal S}M_{\min}^2Y^2\)다.
- 각 fiber maximizer에 질량 1을 주는 abstract conditional law가 envelope를 exact하게
  달성한다. 이는 actual FMT law가 worst case라는 주장이 아니라 outer marginal과
  support만 사용하는 보편 논증의 한계다.
- Theory 86, review 95, machine ledger, exact helper와 11개 새 단위시험을 추가했다.

### 2026-09-19 00:25 KST — 회귀·Lean·전수 원장 검증

- canonical Python 3.11.16으로 same-law Theory 80--82·86 회귀시험 44개가 PASS했다.
- fresh Lean direct compile은 Theory 85의 기존 곱 순서
  <code>vaughanVariance * phi</code> 대 <code>phi * vaughanVariance</code> 차이를
  검출했다. 수학 내용은 바꾸지 않고 <code>mul_comm</code>을 명시한 뒤 direct compile이
  exit 0이었다.
- pinned Lean 4.34.0-rc2 full build는
  <code>Build completed successfully (8765 jobs)</code>, exit 0이었다.
- verification refresh/validation은 theory 87개, display 식 1,630개, declaration
  307개, <code>KERNEL_PASS=98</code>, <code>CONDITIONAL_KERNEL_PASS=83</code>,
  <code>NOT_YET_FORMALIZED=1067</code>, 금지 proof escape 0건, text-integrity issue
  0건으로 PASS했다.
- actual prime/dataset 실험, 패키지 설치, threshold calculator, 장시간 계산, GRH
  branch, push/PR은 실행하지 않았다. 새 bounded <code>X_cert</code> 범위도 없다.

## 완료 점검

- [x] WSL runtime·Git·source hash 재확인
- [x] FMT outer/final 양화사 원문 대조
- [x] support-restricted same-law reduction과 strict gate 고정
- [x] outer-only minimax sharpness의 범위와 비주장 고정
- [x] Python exact witness·회귀시험 PASS
- [x] Lean direct compile·full build PASS
- [x] formula/declaration 원장 refresh·validation PASS
- [x] actual 실험·설치·threshold·장시간 계산 미실행 확인
- [x] 새 bounded <code>X_cert</code> 없음 확인
- [x] 완료 handoff·명시 경로 local commit

### 2026-09-19 00:29 KST — local commit·완료 handoff

- 검토한 Theory 86 관련 17개 경로만 명시적으로 stage해 local commit
  <code>a282fe1ca31747c396b5e1635821e4ab3b53b13f</code>을 생성했다.
- WSL Git global/local config는 변경하지 않고 기존 저장소 author identity를 commit
  명령에만 적용했다.
- 완료 핸드오프 <code>handoff/202609190029_HANDOFF.md</code>를 새 파일로 작성했다.
- push·PR·issue·외부 게시는 수행하지 않았다.
